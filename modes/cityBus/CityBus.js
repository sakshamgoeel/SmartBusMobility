const stations = [
  "Clement Town",
  "Raipur",
  "I.S.B.T",
  "Laal Pul",
  "Clock Tower",
  "Dilaram Chowk",
  "Paltan Bazaar",
  "Rajpur Road",
  "Jakhan",
  "Prem Nagar",
  "Majra",
  "Balliwala",
  "Kishanpur",
  "Vikasnagar",
  "Sahaspur"
];

const fromSelect = document.getElementById("fromStation");
const toSelect = document.getElementById("toStation");
const resultDiv = document.getElementById("result");
const searchBtn = document.getElementById("searchBtn");

let map;
let routeControl = null;
let animatedMarker = null;

// Populate dropdowns
function populateStations() {
  fromSelect.innerHTML = "";
  toSelect.innerHTML = "";

  stations.forEach((station) => {
    const option1 = document.createElement("option");
    option1.value = station;
    option1.textContent = station;
    fromSelect.appendChild(option1);

    const option2 = document.createElement("option");
    option2.value = station;
    option2.textContent = station;
    toSelect.appendChild(option2);
  });
}

// Map & route display
function initMap(coordinates, path) {
  const placeholder = document.querySelector("#map .placeholder");
  if (placeholder) placeholder.remove();

  if (!map) {
    map = L.map("map").setView(coordinates[0], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      maxZoom: 19,
    }).addTo(map);
  } else {
    map.setView(coordinates[0], 13);
    if (routeControl) map.removeControl(routeControl);
    if (animatedMarker) map.removeLayer(animatedMarker);
  }

  routeControl = L.Routing.control({
    waypoints: coordinates.map(coord => L.latLng(coord[0], coord[1])),
    routeWhileDragging: false,
    draggableWaypoints: false,
    addWaypoints: false,
    lineOptions: {
      styles: [{ color: 'red', weight: 5, opacity: 0.9 }]
    },
    createMarker: (i, wp, nWps) => {
      return L.marker(wp.latLng).bindPopup(path[i]);
    }
  }).addTo(map);

  routeControl.on('routesfound', function (e) {
    const route = e.routes[0];
    const coords = route.coordinates;

    animatedMarker = L.marker(coords[0], {
      icon: L.divIcon({
        className: 'bus-icon',
        html: '<div style="font-size: 30px;">🚌</div>',
        iconSize: [40, 40],
        iconAnchor: [20, 20]
      })
    }).addTo(map);

    let index = 0;

    function move() {
      if (index >= coords.length) return;
      animatedMarker.setLatLng(coords[index]);
      index++;
      setTimeout(move, 50); // adjust speed here
    }

    move();
  });
}

// API call
async function searchBus() {
  const from = fromSelect.value;
  const to = toSelect.value;

  resultDiv.textContent = "";

  if (from === to) {
    resultDiv.textContent = "Please select different stations for From and To.";
    return;
  }

  try {
    const res = await fetch("http://127.0.0.1:5000/api/dijkstra", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ start: from, end: to }),
    });

    const data = await res.json();

    if (!data.path || data.path.length === 0) {
      resultDiv.textContent = "No route found between selected stations.";
      return;
    }

    resultDiv.innerHTML = `
      <p><strong>Route:</strong> ${data.path.join(" → ")}</p>
      <p><strong>Total Travel Time:</strong> ${data.totalTime} minutes</p>
      <p><strong>Buses:</strong> ${data.buses.join(", ")}</p>
    `;

    const bookBtn = document.createElement("button");
    bookBtn.textContent = "Book Bus";
    bookBtn.style.padding = "12px 24px";
    bookBtn.style.fontSize = "16px";
    bookBtn.style.marginTop = "15px";
    bookBtn.style.backgroundColor = "#2563eb";
    bookBtn.style.color = "white";
    bookBtn.style.border = "none";
    bookBtn.style.borderRadius = "6px";
    bookBtn.style.cursor = "pointer";
    bookBtn.onmouseover = () => bookBtn.style.backgroundColor = "#1e40af";
    bookBtn.onmouseleave = () => bookBtn.style.backgroundColor = "#2563eb";

    bookBtn.onclick = () => {
      const busParam = encodeURIComponent(JSON.stringify(data.buses));
      const url = `busbooking.html?from=${encodeURIComponent(from)}&to=${encodeURIComponent(to)}&user=${encodeURIComponent("saksham")}&buses=${busParam}`;
      window.location.href = url;
    };

    resultDiv.appendChild(bookBtn);

    initMap(data.coordinates, data.path);

  } catch (err) {
    resultDiv.textContent = "Error fetching route from server.";
    console.error(err);
  }
}

// Init
populateStations();
searchBtn.addEventListener("click", searchBus);
