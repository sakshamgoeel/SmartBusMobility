from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS so frontend JS can call this backend

stations = {
  "Clement Town": {
      "I.S.B.T": { "time": "25 mins", "cost": 15, "buses": ["Bus 101", "Bus 204"] },
  },
  "I.S.B.T": {
      "Clement Town": { "time": "25 mins", "cost": 15, "buses": ["Bus 101", "Bus 204"] },
      "Airport": { "time": "25 mins", "cost": 15, "buses": ["Bus 101", "Bus 204"] }
  },
  "Airport": {
      "Clement Town": { "time": "40 mins", "cost": 30, "buses": ["Bus 707"] },
      "I.S.B.T": { "time": "25 mins", "cost": 15, "buses": ["Bus 101", "Bus 204"] }
  },
  "Ghanta Ghar": {
      "I.S.B.T": { "time": "25 mins", "cost": 15, "buses": ["Bus 101", "Bus 204"] },
  },
  "Dilaram Chowk": {
      "Clement Town": { "time": "25 mins", "cost": 15, "buses": ["Bus 101", "Bus 204"] },
      "Airport": { "time": "25 mins", "cost": 15, "buses": ["Bus 101", "Bus 204"] }
  },
  "Jakhan": {
      "Clement Town": { "time": "40 mins", "cost": 30, "buses": ["Bus 707"] },
      "I.S.B.T": { "time": "25 mins", "cost": 15, "buses": ["Bus 101", "Bus 204"] }
  }
}

@app.route("/api/dijkstra", methods=["POST"])
def dijkstra_route():
    data = request.get_json()
    start = data.get("start")
    end = data.get("end")

    distances = {node: float('inf') for node in stations}
    previous = {node: None for node in stations}
    distances[start] = 0
    unvisited = set(stations.keys())

    while unvisited:
        current = min(unvisited, key=lambda node: distances[node])
        unvisited.remove(current)

        if current == end:
            break

        for neighbor in stations.get(current, {}):
            cost = stations[current][neighbor]["cost"]
            new_dist = distances[current] + cost
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                previous[neighbor] = current

    path = []
    node = end
    while node:
        path.insert(0, node)
        node = previous[node]

    if not path or path[0] != start:
        return jsonify({"path": [], "totalCost": 0, "buses": []})

    buses = []
    for i in range(len(path) - 1):
        buses += stations[path[i]][path[i + 1]]["buses"]

    return jsonify({
        "path": path,
        "totalCost": distances[end],
        "buses": buses
    })

if __name__ == "__main__":
    app.run(debug=True)
