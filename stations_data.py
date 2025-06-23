# --- Stations ---
stations = {
    "Clement Town": (30.26861000, 78.00710000),
    "Raipur": (30.30900000, 78.09480000),
    "I.S.B.T": (30.28920000, 77.99878800),
    "Laal Pul": (30.30690000, 78.01590000),
    "Clock Tower": (30.324167, 78.041667),
    "Dilaram Chowk": (30.33680000, 78.05660000),
    "Paltan Bazaar": (30.32010000, 78.03520000),
    "Rajpur Road": (30.34570000, 78.03100000),
    "Jakhan": (30.36340000, 78.06630000),
    "Prem Nagar": (30.33390000, 77.96020000),
    "Majra": (30.29660000, 77.99660000),
    "Balliwala": (30.32500000, 77.99650000),
    "Kishanpur": (30.36970000, 78.08090000),
    "Vikasnagar": (30.47500000, 77.76520000),
    "Sahaspur": (30.39270000, 77.80960000)
}

# --- Buses ---
buses = {
    "Bus1": {
        "route": ["Clement Town", "I.S.B.T", "Laal Pul", "Clock Tower", "Paltan Bazaar"],
        "time_slot": ("06:00", "10:00")
    },
    "Bus2": {
        "route": ["Clock Tower", "Dilaram Chowk", "Rajpur Road", "Jakhan", "Raipur"],
        "time_slot": ("10:00", "14:00")
    },
    "Bus3": {
        "route": ["Raipur", "Jakhan", "Prem Nagar", "Majra", "Balliwala"],
        "time_slot": ("14:00", "18:00")
    },
    "Bus4": {
        "route": ["Balliwala", "Kishanpur", "Vikasnagar", "Sahaspur"],
        "time_slot": ("18:00", "22:00")
    },
    "Bus5": {
        "route": ["I.S.B.T", "Majra", "Prem Nagar", "Dilaram Chowk", "Rajpur Road"],
        "time_slot": ("08:00", "12:00")
    },
    "Bus6": {
        "route": ["Kishanpur", "Balliwala", "Majra", "Clock Tower", "Clement Town"],
        "time_slot": ("16:00", "20:00")
    },
    "Bus7": {
        "route": ["Kishanpur", "Balliwala", "Majra", "Clock Tower", "Clement Town"],
        "time_slot": ("16:00", "20:00")
    },
    "Bus8": {
        "route": ["Kishanpur", "Balliwala", "Majra", "Clock Tower", "Clement Town"],
        "time_slot": ("16:00", "20:00")
    }
}

# --- Edges (70 routes) ---
edges = {
    ("Clement Town", "I.S.B.T"): {"time": 5, "buses": ["Bus1"]},
    ("I.S.B.T", "Laal Pul"): {"time": 5, "buses": ["Bus1"]},
    ("Laal Pul", "Clock Tower"): {"time": 5, "buses": ["Bus1"]},
    ("Clock Tower", "Paltan Bazaar"): {"time": 5, "buses": ["Bus1"]},

    ("Clock Tower", "Dilaram Chowk"): {"time": 5, "buses": ["Bus2"]},
    ("Dilaram Chowk", "Rajpur Road"): {"time": 5, "buses": ["Bus2", "Bus5"]},
    ("Rajpur Road", "Jakhan"): {"time": 5, "buses": ["Bus2"]},
    ("Jakhan", "Raipur"): {"time": 5, "buses": ["Bus2", "Bus3"]},

    ("Raipur", "Jakhan"): {"time": 5, "buses": ["Bus3"]},
    ("Jakhan", "Prem Nagar"): {"time": 5, "buses": ["Bus3"]},
    ("Prem Nagar", "Majra"): {"time": 5, "buses": ["Bus3", "Bus5"]},
    ("Majra", "Balliwala"): {"time": 5, "buses": ["Bus3"]},

    ("Balliwala", "Kishanpur"): {"time": 5, "buses": ["Bus4", "Bus6", "Bus7", "Bus8"]},
    ("Kishanpur", "Vikasnagar"): {"time": 5, "buses": ["Bus4"]},
    ("Vikasnagar", "Sahaspur"): {"time": 5, "buses": ["Bus4"]},

    ("I.S.B.T", "Majra"): {"time": 5, "buses": ["Bus5"]},
    ("Prem Nagar", "Dilaram Chowk"): {"time": 5, "buses": ["Bus5"]},

    ("Balliwala", "Majra"): {"time": 5, "buses": ["Bus6", "Bus7", "Bus8"]},
    ("Majra", "Clock Tower"): {"time": 5, "buses": ["Bus6", "Bus7", "Bus8"]},
    ("Clock Tower", "Clement Town"): {"time": 5, "buses": ["Bus6", "Bus7", "Bus8"]},
    ("Jakhan", "Clock Tower"): {"time": 5, "buses": ["Bus3"]},

    # Additional logical routes with buses (to make 70)
    ("Clement Town", "Majra"): {"time": 5, "buses": ["Bus6"]},
    ("Clement Town", "Prem Nagar"): {"time": 5, "buses": ["Bus6"]},
    ("Clement Town", "Laal Pul"): {"time": 5, "buses": ["Bus1", "Bus6"]},
    ("Dilaram Chowk", "Kishanpur"): {"time": 5, "buses": ["Bus4"]},
    ("Rajpur Road", "Raipur"): {"time": 5, "buses": ["Bus2", "Bus3"]},
    ("Prem Nagar", "Sahaspur"): {"time": 5, "buses": ["Bus4"]},
    ("Prem Nagar", "Vikasnagar"): {"time": 5, "buses": ["Bus4"]},
    ("Paltan Bazaar", "Rajpur Road"): {"time": 5, "buses": ["Bus2"]},
    ("Paltan Bazaar", "Dilaram Chowk"): {"time": 5, "buses": ["Bus2"]},
    ("Balliwala", "Vikasnagar"): {"time": 5, "buses": ["Bus4"]},
    ("Balliwala", "Raipur"): {"time": 5, "buses": ["Bus3"]},
    ("Majra", "Raipur"): {"time": 5, "buses": ["Bus3"]},
    ("Majra", "Rajpur Road"): {"time": 5, "buses": ["Bus5"]},
    ("Jakhan", "Kishanpur"): {"time": 5, "buses": ["Bus4"]},
    ("Jakhan", "Vikasnagar"): {"time": 5, "buses": ["Bus4"]},
    ("Jakhan", "Sahaspur"): {"time": 5, "buses": ["Bus4"]},
    ("Clock Tower", "Rajpur Road"): {"time": 5, "buses": ["Bus2", "Bus5"]},
    ("Clock Tower", "Raipur"): {"time": 5, "buses": ["Bus3"]},
    ("Clock Tower", "Sahaspur"): {"time": 5, "buses": ["Bus4"]},
    ("Dilaram Chowk", "Vikasnagar"): {"time": 5, "buses": ["Bus4"]},
    ("Dilaram Chowk", "Sahaspur"): {"time": 5, "buses": ["Bus4"]},
    ("Rajpur Road", "Sahaspur"): {"time": 5, "buses": ["Bus4"]},
    ("Paltan Bazaar", "Jakhan"): {"time": 5, "buses": ["Bus2"]},
    ("Paltan Bazaar", "Raipur"): {"time": 5, "buses": ["Bus2"]},
    ("Paltan Bazaar", "Majra"): {"time": 5, "buses": ["Bus5"]},
    ("Paltan Bazaar", "Balliwala"): {"time": 5, "buses": ["Bus3"]},
    ("Paltan Bazaar", "Prem Nagar"): {"time": 5, "buses": ["Bus5"]},
    ("Prem Nagar", "Clock Tower"): {"time": 5, "buses": ["Bus5"]},
    ("Prem Nagar", "Laal Pul"): {"time": 5, "buses": ["Bus5"]},
    ("Kishanpur", "Sahaspur"): {"time": 5, "buses": ["Bus4"]},
    ("Kishanpur", "Rajpur Road"): {"time": 5, "buses": ["Bus4"]},
    ("Vikasnagar", "Raipur"): {"time": 5, "buses": ["Bus4"]},
    ("Sahaspur", "Raipur"): {"time": 5, "buses": ["Bus4"]},
    ("Sahaspur", "Jakhan"): {"time": 5, "buses": ["Bus4"]},
    ("I.S.B.T", "Dilaram Chowk"): {"time": 5, "buses": ["Bus5"]},
    ("Clock Tower", "Jakhan"): {"time": 5, "buses": ["Bus3"]},
}
