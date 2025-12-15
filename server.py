import os
import glob
import json
import re
import shutil
from datetime import datetime, timezone as dt_timezone

import requests
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_caching import Cache
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from apscheduler.schedulers.background import BackgroundScheduler

# ============================================================
# Universal, config-driven server:
# - Reads a project_config.json that defines datasets and columns
# - Exposes:
#     GET /data
#     GET /history?date=YYYY-MM-DD
#     GET /history/manifest
#     (optional) GET /config
# - Optionally proxies Mapbox styles (if you need it)
# ============================================================

# ---- Paths & constants ----
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.getenv("PROJECT_CONFIG_PATH", os.path.join(BASE_DIR, "project_config.json"))

SCHEDULER_TIMEZONE = os.getenv("SCHEDULER_TIMEZONE", "UTC")
HISTORY_DIR = os.path.join(BASE_DIR, os.getenv("HISTORY_DIR", "history"))
MANIFEST_PATH = os.path.join(HISTORY_DIR, "manifest.json")
CACHE_DIR = os.path.join(BASE_DIR, os.getenv("CACHE_DIR", "cache-directory"))
SAMPLE_JSON = os.path.join(BASE_DIR, os.getenv("SAMPLE_JSON", "sample.json"))

SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

MAPBOX_ACCESS_TOKEN = os.getenv("MAPBOX_ACCESS_TOKEN")

# Ensure history directory exists
os.makedirs(HISTORY_DIR, exist_ok=True)

# ---- Flask setup ----
app = Flask(__name__)
CORS(app)
cache = Cache(app, config={"CACHE_TYPE": "FileSystemCache", "CACHE_DIR": CACHE_DIR})

# ---- Helpers ----
def load_project_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            f"Missing config: {CONFIG_PATH}. "
            f"Set PROJECT_CONFIG_PATH or create project_config.json."
        )
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)

    if "sheet_id" not in cfg:
        raise ValueError("project_config.json must include 'sheet_id'")
    if "datasets" not in cfg or not isinstance(cfg["datasets"], dict) or not cfg["datasets"]:
        raise ValueError("project_config.json must include non-empty 'datasets' object")

    # minimal validation
    for ds_name, ds in cfg["datasets"].items():
        if "range" not in ds:
            raise ValueError(f"Dataset '{ds_name}' missing 'range'")
        if "fields" not in ds or not isinstance(ds["fields"], dict) or not ds["fields"]:
            raise ValueError(f"Dataset '{ds_name}' missing non-empty 'fields' mapping")

    return cfg


def get_sheets_service():
    cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if not cred_path:
        raise RuntimeError("GOOGLE_APPLICATION_CREDENTIALS env var is not set")
    if not os.path.exists(cred_path):
        raise RuntimeError(f"GOOGLE_APPLICATION_CREDENTIALS file not found: {cred_path}")

    creds = Credentials.from_service_account_file(cred_path, scopes=SCOPES)
    return build("sheets", "v4", credentials=creds).spreadsheets()


def row_to_object(row: list, field_map: dict) -> dict:
    """
    field_map example: {"name": 0, "gps": 5}
    Column indexes are 0-based.
    """
    obj = {}
    for out_key, idx in field_map.items():
        if isinstance(idx, int) and 0 <= idx < len(row):
            obj[out_key] = row[idx]
        else:
            obj[out_key] = None
    return obj


def extract_all_datasets() -> dict:
    """
    Returns an object like:
      {
        "meta": {...optional...},
        "datasets": { "hospitals": [...], "emergency_rooms": [...] }
      }
    """
    cfg = load_project_config()
    sheet_id = cfg["sheet_id"]
    datasets_cfg = cfg["datasets"]

    sheet = get_sheets_service()

    out = {
        "meta": {
            "project_name": cfg.get("project_name", ""),
            "sheet_id": sheet_id,
            "generated_at_utc": datetime.now(dt_timezone.utc).isoformat(),
        },
        "datasets": {},
    }

    try:
        for ds_name, ds in datasets_cfg.items():
            result = sheet.values().get(spreadsheetId=sheet_id, range=ds["range"]).execute()
            rows = result.get("values", [])

            items = []
            for row in rows:
                items.append(row_to_object(row, ds["fields"]))

            out["datasets"][ds_name] = items

    except HttpError as err:
        # raise to be handled by caller
        raise RuntimeError(f"Google Sheets API error: {err}") from err

    return out


def write_live_snapshot(data: dict):
    with open(SAMPLE_JSON, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


def update_manifest():
    files = glob.glob(os.path.join(HISTORY_DIR, "*.json"))
    dates = [
        os.path.splitext(os.path.basename(p))[0]
        for p in files
        if re.match(r"^\d{4}-\d{2}-\d{2}\.json$", os.path.basename(p))
    ]
    dates.sort()
    with open(MANIFEST_PATH, "w", encoding="utf-8") as mf:
        json.dump(dates, mf, ensure_ascii=False)


def archive_daily_snapshot():
    data = extract_all_datasets()
    write_live_snapshot(data)

    now = datetime.now(dt_timezone.utc)
    date_str = now.strftime("%Y-%m-%d")
    dest = os.path.join(HISTORY_DIR, f"{date_str}.json")

    shutil.copyfile(SAMPLE_JSON, dest)
    update_manifest()
    print(f"[archive] Archived snapshot for {date_str}")


# ---- Scheduler ----
scheduler = BackgroundScheduler(timezone=SCHEDULER_TIMEZONE)
scheduler.add_job(archive_daily_snapshot, "cron", hour=0, minute=5)
scheduler.start()

# ---- Initial population ----
try:
    archive_daily_snapshot()
except Exception as e:
    # Server can still start; /data will show error until fixed
    print(f"[startup] Initial snapshot failed: {e}")


# ============================================================
# Routes
# ============================================================

@app.route("/data")
def live_data():
    """
    Returns the latest snapshot (meta + datasets).
    """
    try:
        if not os.path.exists(SAMPLE_JSON):
            # attempt to generate once if missing
            data = extract_all_datasets()
            write_live_snapshot(data)

        with open(SAMPLE_JSON, "r", encoding="utf-8") as f:
            return jsonify(json.load(f))
    except Exception as e:
        return jsonify({"error": "live data unavailable", "details": str(e)}), 500


@app.route("/history")
def history_data():
    """
    GET /history?date=YYYY-MM-DD
    Returns the snapshot for a date.
    """
    date = request.args.get("date", "").strip()
    if not re.match(r"^\d{4}-\d{2}-\d{2}$", date):
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    path = os.path.join(HISTORY_DIR, f"{date}.json")
    if not os.path.exists(path):
        return jsonify({"error": "No data for that date"}), 404

    with open(path, "r", encoding="utf-8") as f:
        return jsonify(json.load(f))


@app.route("/history/manifest")
def history_manifest():
    """
    Returns list of available dates.
    """
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, "r", encoding="utf-8") as mf:
            return jsonify(json.load(mf))
    return jsonify([])


@app.route("/config")
def public_config():
    """
    Optional: returns safe parts of config (no secrets).
    Useful for frontend to show project name or dataset labels.
    """
    try:
        cfg = load_project_config()
        safe = {
            "project_name": cfg.get("project_name", ""),
            "datasets": list(cfg.get("datasets", {}).keys()),
        }
        return jsonify(safe)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/mapbox-tiles/styles/v1/<path:path>")
@cache.cached(timeout=3600, query_string=True)
def mapbox_tiles_proxy(path):
    """
    Optional proxy for Mapbox styles to avoid exposing token in frontend.
    If MAPBOX_ACCESS_TOKEN is not set, return a clear error.
    """
    if not MAPBOX_ACCESS_TOKEN:
        return jsonify({"error": "MAPBOX_ACCESS_TOKEN not set"}), 500

    url = f"https://api.mapbox.com/styles/v1/{path}?access_token={MAPBOX_ACCESS_TOKEN}"
    resp = requests.get(url)
    if resp.ok:
        return (resp.content, resp.status_code, resp.headers.items())
    return jsonify({"error": "tile fetch failed", "status": resp.status_code}), resp.status_code


# WSGI-ready (no __main__ guard needed)
