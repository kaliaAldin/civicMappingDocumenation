// js/project.config.js

export const PROJECT = {
  meta: {
    title: "My Civic Map",
    defaultCenter: [15.56, 32.53],
    defaultZoom: 12
  },

  api: {
    baseUrl: "https://your-domain.com",
    dataEndpoint: "/data"
  },

  datasets: {
    hospitals: {
      geometry: "point",
      latlngField: "gps",

      popup: (d) => `
        <strong>${d.name}</strong><br/>
        Status: ${d.status ?? "unknown"}
      `
    },

    emergency_rooms: {
      geometry: "circle",
      latlngField: "gps",

      circle: {
        radius: d => Math.min((d.population ?? 500) * 2, 3000),
        color: "wheat"
      },

      popup: (d) => `
        <strong>${d.name}</strong><br/>
        Population: ${d.population}
      `
    }
  }
};
