from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import networkx as nx
from datetime import datetime

# Dataset imports
from stations_data import buses as local_buses, edges as local_edges, stations as local_stations
from interstate_stations_data import interstate_stations, interstate_edges

app = Flask(__name__)
CORS(app)
DB_NAME = 'auth_users.db'

# ================= INIT =================
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        bus TEXT NOT NULL,
        seat TEXT NOT NULL,
        start TEXT NOT NULL,
        end TEXT NOT NULL,
        fare INTEGER NOT NULL,
        time TEXT NOT NULL
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS seats (
        bus TEXT NOT NULL,
        seat TEXT NOT NULL,
        status TEXT NOT NULL,
        UNIQUE(bus, seat)
    )''')
    conn.commit()
    conn.close()

# ================= AUTH =================
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    name, username, password = data['name'], data['username'], data['password']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (name, username, password) VALUES (?, ?, ?)", (name, username, password))
        conn.commit()
        return jsonify({"status": "success"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "fail", "message": "Username already exists."})
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username, password = data['username'], data['password']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return jsonify({"status": "success" if user else "fail"})

# ================= DIJKSTRA =================
def build_graph(edges):
    G = nx.DiGraph()
    for (start, end), attr in edges.items():
        G.add_edge(start, end, time=attr['time'], buses=attr['buses'])
    return G

@app.route('/api/dijkstra', methods=['POST'])
def dijkstra():
    data = request.json
    start, end, mode = data['start'], data['end'], data.get('mode', 'local')

    if mode == 'interstate':
        stations, edges = interstate_stations, interstate_edges
    elif mode == 'women':
        stations = interstate_stations
        edges = {k: v for k, v in interstate_edges.items() if v.get('category') == 'women'}
    else:
        stations, edges = local_stations, local_edges

    if start not in stations or end not in stations:
        return jsonify({"error": "Invalid station"}), 400

    G = build_graph(edges)
    try:
        path = nx.dijkstra_path(G, start, end, weight='time')
        total_time = nx.dijkstra_path_length(G, start, end, weight='time')
        buses, coords = [], []
        for i in range(len(path)):
            coords.append(stations[path[i]])
            if i < len(path) - 1:
                buses.append(G[path[i]][path[i+1]]['buses'])
        return jsonify({"path": path, "totalTime": total_time, "buses": buses, "coordinates": coords})
    except nx.NetworkXNoPath:
        return jsonify({"error": "No path found"}), 404

# ================= SEAT BOOKING =================
@app.route('/book', methods=['POST'])
def book():
    data = request.json
    username = data['username']
    bus = data['bus']
    seat = data['seat']
    start = data['from']
    end = data['to']
    fare = data.get('fare', 500)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT status FROM seats WHERE bus=? AND seat=?", (bus, seat))
    row = c.fetchone()
    if row and row[0] == 'booked':
        return jsonify({"status": "fail", "message": "Seat already booked."})

    c.execute("INSERT OR REPLACE INTO seats (bus, seat, status) VALUES (?, ?, ?)", (bus, seat, 'booked'))
    c.execute("INSERT INTO bookings (username, bus, seat, start, end, fare, time) VALUES (?, ?, ?, ?, ?, ?, ?)",
              (username, bus, seat, start, end, fare, now))
    conn.commit()
    conn.close()
    return jsonify({"status": "success", "message": "Seat booked."})

@app.route('/mybookings', methods=['POST'])
def mybookings():
    username = request.json['username']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT bus, seat, start, end, fare, time FROM bookings WHERE username=?", (username,))
    bookings = c.fetchall()
    conn.close()
    return jsonify([
        {"bus": b, "seat": s, "from": f, "to": t, "fare": fare, "time": tm}
        for (b, s, f, t, fare, tm) in bookings
    ])

@app.route('/booked_seats', methods=['POST'])
def booked_seats():
    data = request.json
    bus = data['bus']
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT seat FROM seats WHERE bus=? AND status='booked'", (bus,))
    rows = c.fetchall()
    conn.close()
    return jsonify([seat[0] for seat in rows])

# ================= RUN =================
if __name__ == '__main__':
    init_db()
    app.run(debug=True)