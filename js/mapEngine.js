// js/mapEngine.js

export function createMap(containerId, center, zoom, tileLayer) {
  const map = L.map(containerId).setView(center, zoom);
  L.tileLayer(tileLayer.url, tileLayer.options).addTo(map);
  return map;
}

export function renderPoints(map, data, config) {
  data.forEach(d => {
    const marker = L.marker(d.latlng);
    if (config.popup) marker.bindPopup(config.popup(d));
    marker.addTo(map);
  });
}

export function renderCircles(map, data, config) {
  data.forEach(d => {
    const circle = L.circle(d.latlng, {
      radius: config.circle.radius(d),
      color: config.circle.color,
      fillOpacity: 0.5
    });
    if (config.popup) circle.bindPopup(config.popup(d));
    circle.addTo(map);
  });
}
