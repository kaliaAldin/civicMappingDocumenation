// js/app.js

import { PROJECT } from "./project.config.js";
import { adaptDataset } from "./dataAdapters.js";
import { createMap, renderPoints, renderCircles } from "./mapEngine.js";
import { MAP_CONFIG } from "./map.config.js";

/* ===============================
   DOM
================================ */

const titleEl = document.getElementById("project-title");
const metaEl = document.getElementById("meta");
const datasetListEl = document.getElementById("dataset-list");

/* ===============================
   Map init
================================ */

const map = createMap(
  "map",
  PROJECT.meta.defaultCenter,
  PROJECT.meta.defaultZoom,
  MAP_CONFIG.tileLayer
);

if (titleEl) {
  titleEl.textContent = PROJECT.meta.title;
}

function showError(msg) {
  if (metaEl) {
    metaEl.innerHTML = `<p style="color:#ffb4a2"><strong>Error:</strong> ${msg}</p>`;
  }
}

function showStatus(msg) {
  if (metaEl) {
    metaEl.innerHTML = `<p>${msg}</p>`;
  }
}

function addDatasetInfo(name, count) {
  if (!datasetListEl) return;

  const el = document.createElement("div");
  el.className = "dataset-item";
  el.innerHTML = `<strong>${name}</strong><br/>Entries: ${count}`;
  datasetListEl.appendChild(el);
}

/* ===============================
   Fetch + render
================================ */

showStatus("Loading data…");

fetch(PROJECT.api.baseUrl + PROJECT.api.dataEndpoint)
  .then(res => {
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    return res.json();
  })
  .then(rawData => {
    datasetListEl.innerHTML = "";

    let renderedAny = false;

    for (const [datasetKey, backendKey] of Object.entries(PROJECT.datasetMapping)) {
      const config = PROJECT.datasets[datasetKey];
      const rawItems = rawData[backendKey];

      if (!config) {
        console.warn(`No config for dataset "${datasetKey}"`);
        continue;
      }

      if (!Array.isArray(rawItems)) {
        console.warn(`Backend key "${backendKey}" not found`);
        continue;
      }

      const adapted = adaptDataset(rawItems, config);

      if (config.geometry === "point") {
        renderPoints(map, adapted, config);
      }

      if (config.geometry === "circle") {
        renderCircles(map, adapted, config);
      }

      addDatasetInfo(datasetKey, adapted.length);
      renderedAny = true;
    }

    if (!renderedAny) {
      showError("No datasets could be rendered. Check datasetMapping.");
    } else {
      showStatus("Data loaded");
    }
  })
  .catch(err => {
    console.error(err);
    showError("Failed to load data from server.");
  });
