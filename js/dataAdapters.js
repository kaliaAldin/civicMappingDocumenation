// js/dataAdapters.js

export function adaptDataset(items, datasetConfig) {
  if (!Array.isArray(items)) return [];

  return items
    .map(item => {
      if (!item[datasetConfig.latlngField]) return null;

      const [lat, lng] = item[datasetConfig.latlngField]
        .split(",")
        .map(Number);

      if (isNaN(lat) || isNaN(lng)) return null;

      return {
        ...item,
        latlng: [lat, lng]
      };
    })
    .filter(Boolean);
}
