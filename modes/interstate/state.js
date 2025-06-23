const stations = [
  "New Delhi", "Mumbai", "Kolkata", "Chennai", "Bengaluru", "Hyderabad", "Ahmedabad",
  "Pune", "Surat", "Jaipur", "Lucknow", "Kanpur", "Patna", "Bhopal", "Indore",
  "Nagpur", "Vadodara", "Kochi", "Coimbatore", "Madurai", "Visakhapatnam",
  "Bhubaneswar", "Patiala", "Ranchi", "Raipur", "Dehradun", "Agra", "Jodhpur",
  "Thiruvananthapuram", "Guwahati"
];

const fromSelect = document.getElementById("fromStation");
const toSelect = document.getElementById("toStation");
const resultDiv = document.getElementById("result");
const mapDiv = document.getElementById("map");
const mapPlaceholder = document.getElementById("mapPlaceholder");
const searchBtn = document.getElementById("searchBtn");

let map;
let routeControl;

// Populate dropdowns
stations.forEach((st) => {
  const option1 = document.createElement("option");
  option1.value = st;
  option1.textContent = st;
  fromSelect.appendChild(option1);

  const option2 = document.createElement("option");
  option2.value = st;
  option2.textContent = st;
  toSelect.appendChild(option2);
});

searchBtn.addEventListener("click", () => {
  const from = fromSelect.value;
  const to = toSelect.value;

  resultDiv.innerHTML = "";
  mapDiv.style.display = "none";
  mapPlaceholder.style.display = "block";

  if (from === to) {
    resultDiv.innerHTML = '<p style="color:red;">Please select different stations.</p>';
    return;
  }

  fetch("http://127.0.0.1:5000/api/dijkstra", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      start: from,
      end: to,
      mode: "interstate"
    })
  })
    .then((res) => res.json())
    .then((data) => {
      if (!data.path || data.path.length === 0) {
        resultDiv.innerHTML = "<p>No route found.</p>";
        return;
      }

      resultDiv.innerHTML = `
        <p><strong>Route:</strong> ${data.path.join(" → ")}</p>
        <p><strong>Total Travel Time:</strong> ${data.totalTime} minutes</p>
        <p><strong>Buses:</strong> ${data.buses.join(", ")}</p>
      `;

      if (!data.coordinates || data.coordinates.length === 0) {
        resultDiv.innerHTML += '<p style="color:red;">No coordinates available to display map.</p>';
        return;
      }

      mapPlaceholder.style.display = "none";
      mapDiv.style.display = "block";

      if (!map) {
        map = L.map("map").setView(data.coordinates[0], 6);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 18,
          attribution: '© OpenStreetMap contributors',
        }).addTo(map);
      } else {
        map.setView(data.coordinates[0], 6);
        if (routeControl) map.removeControl(routeControl);
      }

      routeControl = L.Routing.control({
        waypoints: data.coordinates.map(c => L.latLng(c[0], c[1])),
        routeWhileDragging: false,
        addWaypoints: false,
        draggableWaypoints: false,
        lineOptions: {
          styles: [{ color: 'orange', weight: 6, opacity: 0.9 }]
        },
        createMarker: function(i, wp, n) {
          return L.marker(wp.latLng).bindPopup(data.path[i]);
        }
      }).addTo(map);
    })
    .catch((err) => {
      resultDiv.innerHTML = '<p style="color:red;">Error fetching route from server.</p>';
      console.error(err);
    });
});
