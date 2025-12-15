// js/project.config.js

export const PROJECT = {
  meta: {
    title: "My Civic Map",
    defaultCenter: [15.56, 32.53],
    defaultZoom: 12
  },

  api: {
    baseUrl: "https://sudancivicmap.com",
    dataEndpoint: "/data"
  },

  /**
   * IMPORTANT:
   * backendKey = key as returned by the server
   * datasetKey = internal name used by the map
   */
  datasetMapping: {
    hospitals: "Hospitals",
    emergency_rooms: "BaseERR"
  },

  datasets: {
    hospitals: {
      geometry: "point",
      latlngField: "GPS_Location",

      popup: d => `
        <strong>${d.name}</strong><br/>
        Status: ${d.Status}<br/>
        District: ${d.District}
      `
    },

    emergency_rooms: {
      geometry: "circle",
      latlngField: "geolocation",

      circle: {
        radius: d =>
          Math.min((Number(d.ServedPopulation) || 500) * 2, 3000),
        color: "wheat"
      },

      popup: d => `
        <strong>${d.baseerr}</strong><br/>
        Population: ${d.ServedPopulation}
      `
    }
  }
};
