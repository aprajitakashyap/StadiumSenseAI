"""
Lightweight in-memory data store — no external DB needed.
Seeded with FIFA World Cup stadium data.
"""

STADIUM = {
    "name": "Lusail Iconic Stadium",
    "city": "Lusail",
    "country": "Qatar",
    "capacity": 88966,
}

LOCATIONS = [
    {"id": 1,  "name": "Gate A – North Entrance",      "category": "gate"},
    {"id": 2,  "name": "Gate B – South Entrance",      "category": "gate"},
    {"id": 3,  "name": "Gate C – VIP Entrance",        "category": "gate"},
    {"id": 4,  "name": "Block 101 – Lower North",      "category": "seat_block"},
    {"id": 5,  "name": "Block 201 – Upper South",      "category": "seat_block"},
    {"id": 6,  "name": "Block 305 – Premium West",     "category": "seat_block"},
    {"id": 7,  "name": "Restroom – Level 1 North",     "category": "restroom"},
    {"id": 8,  "name": "Restroom – Level 2 South",     "category": "restroom"},
    {"id": 9,  "name": "Accessible Restroom – Gate A", "category": "restroom"},
    {"id": 10, "name": "Food Court – Main Concourse",  "category": "food_court"},
    {"id": 11, "name": "Food Court – Level 2 East",    "category": "food_court"},
    {"id": 12, "name": "FIFA Store – Gate A",          "category": "merchandise"},
    {"id": 13, "name": "Merchandise Kiosk – Level 2",  "category": "merchandise"},
    {"id": 14, "name": "First Aid Station – Gate B",   "category": "medical"},
    {"id": 15, "name": "Medical Center – Level 1",     "category": "medical"},
    {"id": 16, "name": "Parking Zone P1 – North",      "category": "parking"},
    {"id": 17, "name": "Parking Zone P2 – South",      "category": "parking"},
    {"id": 18, "name": "Lusail Metro Station",         "category": "metro"},
]

FAQS = [
    {
        "id": 1,
        "question": "What time do gates open?",
        "answer": "Gates open 3 hours before kickoff. VIP Gate C opens 4 hours before the match.",
    },
    {
        "id": 2,
        "question": "Where is the nearest restroom?",
        "answer": "Restrooms are on every level near the concourse. Accessible restroom is at Gate A, Level 1.",
    },
    {
        "id": 3,
        "question": "Is parking available?",
        "answer": "Yes — Zone P1 (North) and Zone P2 (South). Metro is recommended for faster access.",
    },
    {
        "id": 4,
        "question": "How do I reach the stadium by metro?",
        "answer": "Take the Lusail Metro Line to Lusail Metro Station — 5 minutes walk from Gate A.",
    },
    {
        "id": 5,
        "question": "Where is the FIFA merchandise store?",
        "answer": "Official FIFA Store is at Gate A. A kiosk is also on Level 2.",
    },
    {
        "id": 6,
        "question": "What items are prohibited?",
        "answer": "No outside food/drinks, umbrellas, bags over 30×20×15 cm, drones, or professional cameras.",
    },
    {
        "id": 7,
        "question": "Are there accessible routes for wheelchair users?",
        "answer": "Yes — accessible routes from Gate A and the metro. Accessible restrooms on Level 1 near Gate A.",
    },
    {
        "id": 8,
        "question": "Where is the first aid station?",
        "answer": "First Aid is at Gate B (ground floor). Medical Center is on Level 1 near Block 101.",
    },
    {
        "id": 9,
        "question": "Can I re-enter after leaving?",
        "answer": "Re-entry is allowed with a valid match ticket. Check your ticket for specific conditions.",
    },
    {
        "id": 10,
        "question": "Where is the food court?",
        "answer": "Main food court is on the Main Concourse between Gates A and B. Second food court on Level 2 East.",
    },
]

ROUTES = [
    {"id": 1, "from": "Lusail Metro Station",    "to": "Gate A – North Entrance",   "accessible": True},
    {"id": 2, "from": "Gate A – North Entrance", "to": "Block 101 – Lower North",   "accessible": True},
    {"id": 3, "from": "Gate B – South Entrance", "to": "Block 201 – Upper South",   "accessible": False},
    {"id": 4, "from": "Gate A – North Entrance", "to": "First Aid Station – Gate B","accessible": True},
    {"id": 5, "from": "Parking Zone P1 – North", "to": "Gate A – North Entrance",   "accessible": False},
]


def build_context(message: str) -> str:
    """Return relevant stadium context based on keywords in the user message."""
    msg = message.lower()
    words = set(w for w in msg.replace("?", " ").replace(",", " ").split() if len(w) > 3)

    # Match locations
    matched_locations = [
        loc for loc in LOCATIONS
        if any(w in loc["name"].lower() or w in loc["category"].lower() for w in words)
    ]
    if not matched_locations:
        matched_locations = LOCATIONS  # fallback: all locations

    # Match FAQs
    matched_faqs = [
        faq for faq in FAQS
        if any(w in faq["question"].lower() or w in faq["answer"].lower() for w in words)
    ]

    lines = [
        f"Stadium: {STADIUM['name']}, {STADIUM['city']}, {STADIUM['country']} (capacity {STADIUM['capacity']:,})\n",
        "Relevant Locations:",
        *[f"  - {loc['name']} [{loc['category']}]" for loc in matched_locations],
    ]

    if matched_faqs:
        lines.append("\nRelevant FAQs:")
        for faq in matched_faqs:
            lines.append(f"  Q: {faq['question']}")
            lines.append(f"  A: {faq['answer']}")

    return "\n".join(lines)
