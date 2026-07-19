"""
StadiumSenseAI — Data store + simulated live data.
All in-memory. No database required.
"""

import random
import time

# ── Stadium ───────────────────────────────────────────────────────────────────
STADIUM = {
    "name":     "Lusail Iconic Stadium",
    "city":     "Lusail",
    "country":  "Qatar",
    "capacity": 88966,
    "timezone": "AST (UTC+3)",
}

# ── Locations ─────────────────────────────────────────────────────────────────
LOCATIONS = [
    {"id": 1,  "name": "Gate A – North Entrance",        "category": "gate",        "accessible": True},
    {"id": 2,  "name": "Gate B – South Entrance",        "category": "gate",        "accessible": False},
    {"id": 3,  "name": "Gate C – VIP Entrance",          "category": "gate",        "accessible": True},
    {"id": 4,  "name": "Gate D – East Family Entrance",  "category": "gate",        "accessible": True},
    {"id": 5,  "name": "Block 101 – Lower North",        "category": "seat_block",  "accessible": True},
    {"id": 6,  "name": "Block 201 – Upper South",        "category": "seat_block",  "accessible": False},
    {"id": 7,  "name": "Block 305 – Premium West",       "category": "seat_block",  "accessible": False},
    {"id": 8,  "name": "Block 401 – Family Section",     "category": "seat_block",  "accessible": True},
    {"id": 9,  "name": "Restroom – Level 1 North",       "category": "restroom",    "accessible": False},
    {"id": 10, "name": "Restroom – Level 2 South",       "category": "restroom",    "accessible": False},
    {"id": 11, "name": "Accessible Restroom – Gate A",   "category": "restroom",    "accessible": True},
    {"id": 12, "name": "Accessible Restroom – Gate D",   "category": "restroom",    "accessible": True},
    {"id": 13, "name": "Quiet Room – Level 1 West",      "category": "quiet_room",  "accessible": True},
    {"id": 14, "name": "Food Court – Main Concourse",    "category": "food_court",  "accessible": True},
    {"id": 15, "name": "Food Court – Level 2 East",      "category": "food_court",  "accessible": False},
    {"id": 16, "name": "Halal Food Zone – Gate A",       "category": "food_court",  "accessible": True},
    {"id": 17, "name": "Water Refill Station – Level 1", "category": "sustainability", "accessible": True},
    {"id": 18, "name": "Water Refill Station – Level 2", "category": "sustainability", "accessible": True},
    {"id": 19, "name": "FIFA Store – Gate A",            "category": "merchandise", "accessible": True},
    {"id": 20, "name": "Merchandise Kiosk – Level 2",    "category": "merchandise", "accessible": False},
    {"id": 21, "name": "First Aid Station – Gate B",     "category": "medical",     "accessible": True},
    {"id": 22, "name": "Medical Center – Level 1",       "category": "medical",     "accessible": True},
    {"id": 23, "name": "AED Station – Gate A",           "category": "medical",     "accessible": True},
    {"id": 24, "name": "Lost & Found – Gate A Office",   "category": "services",    "accessible": True},
    {"id": 25, "name": "Volunteer Hub – Gate D",         "category": "services",    "accessible": True},
    {"id": 26, "name": "Family Help Desk – Gate D",      "category": "services",    "accessible": True},
    {"id": 27, "name": "Parking Zone P1 – North",        "category": "parking",     "accessible": False},
    {"id": 28, "name": "Parking Zone P2 – South",        "category": "parking",     "accessible": False},
    {"id": 29, "name": "Accessible Parking – Gate A",    "category": "parking",     "accessible": True},
    {"id": 30, "name": "Lusail Metro Station",           "category": "metro",       "accessible": True},
    {"id": 31, "name": "Bus Stop – North Plaza",         "category": "transport",   "accessible": True},
    {"id": 32, "name": "Taxi / Ride-share Zone",         "category": "transport",   "accessible": True},
    {"id": 33, "name": "Emergency Exit – North",         "category": "emergency",   "accessible": True},
    {"id": 34, "name": "Emergency Exit – South",         "category": "emergency",   "accessible": True},
    {"id": 35, "name": "Prayer Room – Level 1",          "category": "services",    "accessible": True},
]

# ── FAQs ──────────────────────────────────────────────────────────────────────
FAQS = [
    {"id": 1,  "question": "What time do gates open?",
               "answer": "Gates open 3 hours before kickoff. VIP Gate C and Family Gate D open 4 hours before."},
    {"id": 2,  "question": "Where is the nearest restroom?",
               "answer": "Restrooms are on every level. Accessible restrooms are at Gate A and Gate D on Level 1."},
    {"id": 3,  "question": "Is parking available?",
               "answer": "Yes — Zone P1 (North), Zone P2 (South), and accessible parking near Gate A. Metro is strongly recommended."},
    {"id": 4,  "question": "How do I get here by metro?",
               "answer": "Take the Lusail Metro Line to Lusail Station — 5-minute walk from Gate A. Trains run every 5 min on match days."},
    {"id": 5,  "question": "Where is the FIFA store?",
               "answer": "Official FIFA Store at Gate A. Merchandise kiosk on Level 2. Card and cash accepted."},
    {"id": 6,  "question": "What items are prohibited?",
               "answer": "No outside food/drinks, bags > 30×20×15 cm, umbrellas, professional cameras, drones, flares, or fireworks."},
    {"id": 7,  "question": "Is the stadium wheelchair accessible?",
               "answer": "Yes. Enter via Gate A or Gate D. Accessible restrooms on Level 1. Accessible seating in Block 101 and 401. Priority lane at all gates."},
    {"id": 8,  "question": "Where is first aid?",
               "answer": "First Aid at Gate B (ground floor). Medical Center on Level 1 near Block 101. AED stations at every gate."},
    {"id": 9,  "question": "Can I re-enter?",
               "answer": "Yes, with a valid ticket. Re-entry not allowed in the last 15 minutes or during half-time in some zones."},
    {"id": 10, "question": "Where is the food court?",
               "answer": "Main Food Court on the Main Concourse between Gates A & B. Second court on Level 2 East. Halal zone at Gate A."},
    {"id": 11, "question": "Is there free Wi-Fi?",
               "answer": "Yes. Network: StadiumSense_Guest. No password. Coverage may reduce during match time."},
    {"id": 12, "question": "What if I lose something?",
               "answer": "Visit Lost & Found at Gate A Office. Also contact any steward or volunteer immediately."},
]

# ── Routes ────────────────────────────────────────────────────────────────────
ROUTES = [
    {"id": 1, "from": "Lusail Metro Station",    "to": "Gate A – North Entrance",       "minutes": 5,  "accessible": True},
    {"id": 2, "from": "Gate A – North Entrance", "to": "Block 101 – Lower North",       "minutes": 4,  "accessible": True},
    {"id": 3, "from": "Gate B – South Entrance", "to": "Block 201 – Upper South",       "minutes": 6,  "accessible": False},
    {"id": 4, "from": "Gate A – North Entrance", "to": "First Aid Station – Gate B",    "minutes": 3,  "accessible": True},
    {"id": 5, "from": "Parking Zone P1 – North", "to": "Gate A – North Entrance",       "minutes": 8,  "accessible": False},
    {"id": 6, "from": "Gate D – East Family",    "to": "Block 401 – Family Section",    "minutes": 3,  "accessible": True},
    {"id": 7, "from": "Lusail Metro Station",    "to": "Gate D – East Family Entrance", "minutes": 7,  "accessible": True},
    {"id": 8, "from": "Gate A – North Entrance", "to": "Food Court – Main Concourse",   "minutes": 2,  "accessible": True},
]

# ── Match Schedule ────────────────────────────────────────────────────────────
MATCHES = [
    {"id": 1, "home": "Argentina", "away": "France",   "kickoff": "18:00 AST", "date": "Today",    "stage": "Final",        "venue": "Lusail Iconic Stadium"},
    {"id": 2, "home": "Brazil",    "away": "England",  "kickoff": "15:00 AST", "date": "Tomorrow", "stage": "3rd Place",     "venue": "Al Bayt Stadium"},
    {"id": 3, "home": "Spain",     "away": "Portugal", "kickoff": "21:00 AST", "date": "Jul 22",   "stage": "Friendly",     "venue": "Khalifa Stadium"},
]

# ── Simulated Live Data ───────────────────────────────────────────────────────
# These are updated dynamically to simulate real-time variation

_BASE_CROWD = {
    "Gate A – North": 45,
    "Gate B – South": 82,
    "Gate C – VIP":   20,
    "Gate D – East":  38,
}

_BASE_QUEUE = {
    "Food Court – Main Concourse": 5,
    "Food Court – Level 2 East":   18,
    "Halal Food Zone – Gate A":    8,
    "FIFA Store – Gate A":         12,
    "Merchandise Kiosk – Level 2": 3,
}

_BASE_PARKING = {
    "Zone P1 – North": 68,
    "Zone P2 – South": 91,
    "Accessible – Gate A": 22,
}

_BASE_METRO = {
    "next_train_mins":     3,
    "frequency_mins":      5,
    "platform_crowd":      "Moderate",
    "last_train":          "01:30 AST",
}

_BASE_WEATHER = {
    "temp_c":    32,
    "condition": "Clear",
    "humidity":  55,
    "advice":    "Stay hydrated. Water refill stations on Level 1 and 2.",
}


def _jitter(val: int, spread: int = 12) -> int:
    """Add realistic random variation to simulate live data."""
    return max(0, min(100, val + random.randint(-spread, spread)))


def get_crowd_status() -> dict:
    return {
        gate: {"pct": _jitter(pct), "level": _crowd_level(_jitter(pct))}
        for gate, pct in _BASE_CROWD.items()
    }


def get_queue_times() -> dict:
    return {
        place: {"wait_mins": max(1, _jitter(mins, 5))}
        for place, mins in _BASE_QUEUE.items()
    }


def get_parking_status() -> dict:
    return {
        zone: {"pct_full": _jitter(pct, 8), "level": _crowd_level(_jitter(pct, 8))}
        for zone, pct in _BASE_PARKING.items()
    }


def get_metro_info() -> dict:
    return {
        **_BASE_METRO,
        "next_train_mins": max(1, _BASE_METRO["next_train_mins"] + random.randint(-2, 4)),
    }


def get_weather() -> dict:
    return {
        **_BASE_WEATHER,
        "temp_c": _BASE_WEATHER["temp_c"] + random.randint(-1, 2),
    }


def _crowd_level(pct: int) -> str:
    if pct < 35:  return "Low 🟢"
    if pct < 65:  return "Moderate 🟡"
    if pct < 85:  return "High 🟠"
    return "Very High 🔴"
