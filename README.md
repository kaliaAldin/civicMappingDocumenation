# CIVIC MAPPING INFRASTRUCTURE

# COUNTER-MILITARISATION MAPPING FRAMEWORK



An open, reusable civic mapping system for documenting civilian-led

initiatives, humanitarian infrastructures, and grassroots resilience

in contexts of conflict.



## OVERVIEW



This repository contains an open, reusable civic mapping infrastructure

originally developed for the Counter-Militarisation Mapping project

focused on Sudan.



The system enables communities, activists, researchers, and artists

to build interactive maps based on collaboratively maintained data,

without relying on proprietary platforms or constant technical

intervention.



The infrastructure separates data, server logic, and visualization

into clear layers. Users are expected to modify configuration files

and data sources only — not core logic.



## ORIGIN PROJECT: COUNTER-MILITARISATION MAPPING



The Counter-Militarisation Mapping project is a critical exploration

of dominant narratives surrounding the Sudan conflict.



Instead of presenting the war as a binary military confrontation,

the project reframes the conflict through a civilian and humanitarian

lens. It foregrounds the work of non-combatant actors, particularly

grassroots initiatives and emergency response rooms operating under

conditions of extreme violence and infrastructural collapse.



Through mapping and visual methodologies, the project documents how

civilian networks organize care, logistics, and survival. The map

specifically traces the work of Emergency Response Rooms in Khartoum

and surrounding regions.



The database is updated daily by activists on the ground and is

designed as an open-source resource. It serves researchers, artists,

and organizers by offering a living archive of civilian agency

in conflict zones.



This repository extracts the technical infrastructure of that project

and makes it reusable for other contexts.



### WHAT THIS SYSTEM IS (AND IS NOT)



THIS SYSTEM IS:



An open civic mapping framework



A Google Sheets -> API -> Map pipeline



Designed for fragile, distributed, contested data



Intended for long-term community maintenance



#### THIS SYSTEM IS NOT:



A no-code website builder



A commercial dashboard



A military or surveillance tool



A closed or proprietary platform



CORE TECHNOLOGIES



DATA



Google Sheets (collaborative dataset editing)



API ACCESS



Google Sheets API (read-only access via service account)



SERVER



Flask (Python): minimal API server that reads the sheet and returns JSON



FRONTEND



JavaScript (ES Modules): configuration-driven visualization



MAP



Leaflet.js: open-source mapping library (supports OSM or Mapbox tiles)



WEB



HTML + CSS: minimal structure and shared visual language



SYSTEM ARCHITECTURE (IMPORTANT)



The system is intentionally split into three layers:

##### 

##### (1) DATA LAYER



Google Sheet



Edited by activists/collaborators



Single source of truth

##### 

##### (2) SERVER LAYER



Flask application



Reads the sheet



Outputs structured JSON



Does NOT know how data is visualized

##### 

##### (3) MAP LAYER



JavaScript frontend



Reads JSON from the server



Visualizes data based on configuration



Does NOT know where the data comes from



You should NEVER mix these responsibilities.



FOLDER STRUCTURE (SIMPLIFIED)



**/serverside**



**server.py**



**project\_config.json**



**/js**



**app.js**



**project.config.js**



**map.config.js**



**mapEngine.js**



**dataAdapters.js**



**/style**



**style.css**



**index.html**

**make-your-map.html**

**README.txt**



##### STEP-BY-STEP: HOW TO CREATE YOUR OWN MAP



###### STEP 1 — PREPARE YOUR GOOGLE SHEET



Each row represents ONE place



Each column represents ONE attribute



One column MUST contain GPS coordinates



Coordinates format: latitude,longitude

Example: 15.56,32.53



You can have multiple sheets (tabs) inside one document for different datasets.



###### STEP 2 — CLONE THIS REPOSITORY



Clone or download the repository



You are allowed — and encouraged — to copy it



This system is designed to be reused

###### 

###### STEP 3 — SET UP GOOGLE API ACCESS



Create a Google Cloud project



Enable Google Sheets API



Create a Service Account



Download the credentials JSON file



Share your Google Sheet with the service account email (Viewer access)



Set environment variable:

GOOGLE\_APPLICATION\_CREDENTIALS=/path/to/credentials.json



###### STEP 4 — CONFIGURE THE SERVER (NO CODE CHANGES)

Edit only:

serverside/project\_config.json



This file defines:



Google Sheet ID



Which sheet tabs to read



Which column index corresponds to which field



If your sheet structure changes, update this file.



###### STEP 5 — RUN THE SERVER



Start the Flask server



It exposes a single endpoint: /data



Visiting /data should return JSON



###### STEP 6 — CONFIGURE THE MAP

Edit only:

js/project.config.js



This file defines:



Map center and zoom



Which datasets exist



Which field contains coordinates



How points/circles are rendered



Popup content



##### IMPORTANT:

Dataset names in project.config.js MUST match dataset names returned by the server.



STEP 7 — STYLE (OPTIONAL BUT RECOMMENDED)

The default style.css provides a visual language inspired by the original project:



Dark background



High contrast



Monospace typography



Overlay-based UI



You may keep it, modify it, or rebrand it.

You do not need to write CSS from scratch.



WHAT HAPPENS AFTER SETUP



Edit Google Sheet -> the map updates automatically



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



##### WHO THIS IS FOR



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



##### LICENSE AND ETHOS



This project is open source.



Reuse is encouraged.

Attribution is appreciated.

Extraction without care is discouraged.



============================================================

END

