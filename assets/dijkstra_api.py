from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import networkx as nx

# Dataset imports
from stations_data import stations as local_stations, edges as local_edges
from interstate_stations_data import interstate_stations, interstate_edges
from religious_stations_data import religious_stations, religious_edges

# App setup
app = Flask(__name__)
CORS(app)

# SQLite Database setup
DB_NAME = 'auth_users.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# ================= AUTH ROUTES =================

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)",
                       (name, username, password))
        conn.commit()
        return jsonify({"status": "success", "message": "Signup successful!"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "fail", "message": "Username already exists."})
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        return jsonify({"status": "success", "message": f"Welcome back, {user[1]}!"})
    else:
        return jsonify({"status": "fail", "message": "Invalid username or password."})

# ================= DIJKSTRA ROUTE =================

def build_graph(edges):
    G = nx.DiGraph()
    for (start, end), attr in edges.items():
        G.add_edge(start, end, time=attr["time"], buses=attr["buses"])
    return G

@app.route('/api/dijkstra', methods=['POST'])
def dijkstra():
    data = request.json
    start = data.get("start")
    end = data.get("end")
    mode = data.get("mode", "local")

    if mode == "interstate":
        stations = interstate_stations
        edges = interstate_edges
    elif mode == "women":
        stations = interstate_stations
        edges = {
            (u, v): attr
            for (u, v), attr in interstate_edges.items()
            if attr.get("category") == "women"
        }
    elif mode == "religious":
        stations = religious_stations
        edges = religious_edges
    else:
        stations = local_stations
        edges = local_edges

    if start not in stations or end not in stations:
        return jsonify({"error": "Start or end station not found"}), 400

    G = build_graph(edges)

    try:
        path = nx.dijkstra_path(G, start, end, weight='time')
        total_time = nx.dijkstra_path_length(G, start, end, weight='time')

        buses = []
        coords = []
        for i in range(len(path)):
            coords.append(stations[path[i]])
            if i < len(path) - 1:
                edge_data = G.get_edge_data(path[i], path[i + 1])
                buses.append(edge_data['buses'])

        return jsonify({
            "path": path,
            "totalTime": total_time,
            "buses": buses,
            "coordinates": coords
        })
    except nx.NetworkXNoPath:
        return jsonify({"error": "No route found"}), 404

# ================= RUN APP =================

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
