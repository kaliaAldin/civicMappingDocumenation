OVERVIEW

This repository contains an open, reusable civic mapping infrastructure
originally developed for the Counter-Militarisation Mapping project
focused on Sudan.

The system enables communities, activists, researchers, and artists
to build interactive maps based on collaboratively maintained data,
without relying on proprietary platforms or continuous technical
intervention.

The infrastructure separates data, server logic, and visualization
into clear layers. Users are expected to modify configuration files
and data sources only — not core logic.

ORIGIN PROJECT: COUNTER-MILITARISATION MAPPING

The Counter-Militarisation Mapping project is a critical exploration
of dominant narratives surrounding the Sudan conflict.

Instead of presenting the war as a binary military confrontation,
the project reframes the conflict through a civilian and humanitarian
lens. It foregrounds the work of non-combatant actors, particularly
grassroots initiatives and emergency response rooms operating under
conditions of extreme violence and infrastructural collapse.

Through mapping and visual methodologies, the project documents
how civilian networks organize care, logistics, and survival.
The map specifically traces the work of Emergency Response Rooms
in Khartoum and surrounding regions.

The database is updated daily by activists on the ground and is
designed as an open-source resource. It serves researchers, artists,
and organizers by offering a living archive of civilian agency
in conflict zones.

This repository extracts the technical infrastructure of that project
and makes it reusable for other contexts.

WHAT THIS SYSTEM IS (AND IS NOT)

This system IS:

An open civic mapping framework

A Google Sheets → API → Map pipeline

Designed for fragile, distributed, contested data

Intended for long-term community maintenance

This system IS NOT:

A no-code website builder

A commercial dashboard

A military or surveillance tool

A closed or proprietary platform

CORE TECHNOLOGIES

Google Sheets

Acts as the primary data source

Used by non-technical collaborators

Supports real-time updates

Google Sheets API

Read-only access via service account

No public write access required

Flask (Python)

Minimal API server

Reads Google Sheets

Normalizes data

Exposes a single JSON endpoint

JavaScript (ES Modules)

Fully configuration-driven

No hardcoded dataset meanings

Decoupled rendering logic

Leaflet.js

Open-source mapping library

No vendor lock-in

Works with OpenStreetMap or Mapbox

HTML + CSS

Minimal structure

Shared visual language

Easily customizable

SYSTEM ARCHITECTURE (IMPORTANT)

The system is intentionally split into three layers:

DATA LAYER

Google Sheet

Edited by activists or collaborators

Single source of truth

SERVER LAYER

Flask application

Reads the sheet

Outputs structured JSON

Does not know how data is visualized

MAP LAYER

JavaScript frontend

Reads JSON from the server

Visualizes data based on configuration

Does not know where data comes from

You should NEVER mix these responsibilities.

FOLDER STRUCTURE (SIMPLIFIED)

/serverside

server.py

project_config.json

/js

app.js

project.config.js

map.config.js

mapEngine.js

dataAdapters.js

/style

style.css

index.html
make-your-map.html
README.txt

STEP-BY-STEP: HOW TO CREATE YOUR OWN MAP

STEP 1 — PREPARE YOUR GOOGLE SHEET

Your Google Sheet is where all data lives.

Rules:

Each row represents ONE place

Each column represents ONE attribute

One column MUST contain GPS coordinates

Coordinates format must be:
latitude,longitude

Example:
15.56,32.53

You can have multiple sheets (tabs) inside one document
for different datasets.

STEP 2 — CLONE THIS REPOSITORY

Clone or download the repository.

You are allowed — and encouraged — to copy it.

This system is designed to be reused.

STEP 3 — SET UP GOOGLE API ACCESS

Create a Google Cloud project

Enable Google Sheets API

Create a Service Account

Download the credentials JSON file

Share your Google Sheet with the service account email
(Viewer access only)

Set the environment variable:

GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json

STEP 4 — CONFIGURE THE SERVER (NO CODE CHANGES)

Open:

serverside/project_config.json

In this file you define:

Google Sheet ID

Which sheet tabs to read

Which column index corresponds to which field

You DO NOT edit Python logic.
You ONLY edit this configuration file.

If your sheet structure changes, update this file.

STEP 5 — RUN THE SERVER

Run the Flask server.

Once running, it exposes a single endpoint:

/data

Visiting this URL should return JSON.

This JSON is the only thing the frontend cares about.

STEP 6 — CONFIGURE THE MAP

Open:

js/project.config.js

This file defines:

Map center and zoom

Which datasets exist

Which field contains coordinates

How points or circles are rendered

Popup content

Dataset names here MUST MATCH the dataset names
returned by the server.

You do NOT edit app.js, mapEngine.js, or dataAdapters.js.

STEP 7 — STYLE (OPTIONAL BUT RECOMMENDED)

The default style.css provides a visual language
inspired by the original Sudan project:

Dark background

High contrast

Monospace typography

Overlay-based UI

You may:

Keep it as is

Modify colors

Replace fonts

Add branding

But you do not need to write CSS from scratch.

WHAT HAPPENS AFTER SETUP

Edit Google Sheet → map updates automatically

No redeployment required

No JavaScript knowledge required for editors

Data remains community-owned

DESIGN PHILOSOPHY

This infrastructure assumes:

Data is political

Maps are narratives

Infrastructure should empower, not extract

Communities must control representation

The system avoids:

Hardcoded meanings

Military metaphors

Data hierarchy baked into code

WHO THIS IS FOR

Activists

Researchers

Artists

Journalists

Community organizers

Educators

Archivists

Especially those working in:

Conflict zones

Post-colonial contexts

Humanitarian documentation

Counter-narrative practices

LICENSE AND ETHOS

This project is open source.

Reuse is encouraged.
Attribution is appreciated.
Extraction without care is discouraged.