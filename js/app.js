// js/app.js

import { PROJECT } from "./project.config.js";
import { adaptDataset } from "./dataAdapters.js";
import { createMap, renderPoints, renderCircles } from "./mapEngine.js";
import { MAP_CONFIG } from "./map.config.js"; // tile layer etc.

const map = createMap(
  "map",
  PROJECT.meta.defaultCenter,
  PROJECT.meta.defaultZoom,
  MAP_CONFIG.tileLayer
);

fetch(PROJECT.api.baseUrl + PROJECT.api.dataEndpoint)
  .then(res => res.json())
  .then(data => {
    const datasets = data.datasets;

    for (const [datasetName, items] of Object.entries(datasets)) {
      const config = PROJECT.datasets[datasetName];
      if (!config) continue; // dataset not visualized

      const adapted = adaptDataset(items, config);

      if (config.geometry === "point") {
        renderPoints(map, adapted, config);
      }

      if (config.geometry === "circle") {
        renderCircles(map, adapted, config);
      }
    }
  })
  .catch(err => {
    console.error("Failed to load map data:", err);
  });
