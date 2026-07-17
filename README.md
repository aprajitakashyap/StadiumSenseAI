# StadiumSense AI 🏟️

A smart stadium assistant for FIFA World Cup visitors — built with Python (Flask) and vanilla HTML/CSS/JS. No API key required. Works 100% offline.

---

## Chosen Vertical

**Stadium Navigation & Fan Experience Assistant**

Helps visitors navigate Lusail Iconic Stadium — find gates, seating blocks, restrooms, food courts, medical stations, merchandise stores, parking, metro, and accessible routes — in English, Spanish, or French.

---

## Architecture

```
Browser  (HTML / CSS / JS — single file, zero build step)
    │
    │  POST /chat   GET /faq   GET /locations   GET /routes   GET /health
    ▼
Flask Backend (Python 3, 1 dependency)
    │
    ├── assistant.py  →  Intent detection engine (13 intents, keyword scoring)
    ├── data.py       →  In-memory data store (stadium, locations, FAQs, routes)
    └── app.py        →  REST API + serves frontend
```

---

## How It Works

1. User types a question (or taps a FAQ chip) and picks a language (EN / ES / FR)
2. Frontend sends `POST /chat { message, language }` to the Flask backend
3. `assistant.py` scores the message against 13 intent categories using keyword matching
4. Best-matching intent returns a rich, structured response — gates, restrooms, food, accessible routes, etc.
5. If no intent matches, it falls back to FAQ keyword search, then a helpful menu response
6. Response rendered in the chat UI instantly — no external API calls, no latency

**13 supported intents:** greeting · gate · restroom · food · seat · parking · metro · medical · merchandise · accessible · prohibited · reentry · wifi

---

## Local Setup

### Requirements
- Python 3.8+
- Flask (only dependency)

### Run in 3 commands

```bash
git clone https://github.com/aprajitakashyap/MatchFlowAI.git
cd MatchFlowAI/backend
pip install -r requirements.txt
python app.py
```

Open **http://localhost:8000** in your browser. That's it.

---

## API Reference

| Method | Endpoint     | Description                          |
|--------|-------------|--------------------------------------|
| POST   | `/chat`      | Smart AI response (no API key needed)|
| GET    | `/faq`       | All 10 FAQs                          |
| GET    | `/locations` | All 18 stadium locations             |
| GET    | `/routes`    | 5 routes with accessibility flag     |
| GET    | `/health`    | Health check                         |
| GET    | `/`          | Serves the frontend                  |

### POST /chat

```json
// Request
{ "message": "Where is the restroom?", "language": "en" }

// Response
{ "response": "🚻 Restrooms:\n• Level 1 North – near Gate A\n• ♿ Accessible Restroom – Gate A, Level 1..." }
```

**Supported languages:** `en` · `es` · `fr`

---

## Project Structure

```
MatchFlowAI/
├── backend/
│   ├── app.py          # Flask app — REST endpoints, CORS, serves frontend
│   ├── assistant.py    # Intent detection engine — 13 intents, multi-language
│   ├── data.py         # In-memory store — 18 locations, 10 FAQs, 5 routes
│   └── requirements.txt  # 1 dependency: flask
├── frontend/
│   └── public/
│       └── index.html  # Complete chat UI — pure HTML/CSS/JS, no build step
├── .env.example
├── .gitignore
└── README.md
```

---

## Design Decisions

- **No API key / no external calls** — intent detection runs locally, instant responses
- **No database** — data is in `data.py`, zero infrastructure to set up
- **No frontend build** — single HTML file served directly by Flask
- **Multi-language** — all 13 intents have EN / ES / FR responses
- **Accessible UI** — semantic HTML, ARIA roles, keyboard navigation, sufficient contrast
- **Repo < 10 MB** — 504 KB total, no compiled artifacts or dependencies committed

---

## Assumptions

- Stadium data is based on Lusail Iconic Stadium (FIFA World Cup final venue, Qatar)
- Wi-Fi network name, parking zones, and re-entry policy reflect typical FIFA stadium standards
- The assistant intentionally stays in scope — it answers stadium-related questions only
