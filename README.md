# StadiumSenseAI 🏟️

A smart, multilingual stadium assistant for FIFA World Cup visitors.
Answers questions about gates, seating, food, restrooms, parking, metro, medical, merchandise, accessible routes — in English, Spanish, and French.

**No API key. No database. No build step. One command to run.**

---

## Live Application

🚀 **https://stadiumsenseai.onrender.com**

---

## Architecture

```
Browser  (HTML / CSS / JS — single file, zero build step)
    │
    │  POST /chat   GET /faq   GET /locations   GET /routes   GET /health
    ▼
Flask + Gunicorn (Python 3.11)
    │
    ├── assistant.py  →  Intent detection engine (13 intents, keyword scoring)
    ├── data.py       →  In-memory store (18 locations · 10 FAQs · 5 routes)
    └── app.py        →  REST API + serves frontend
```

---

## Local Setup

### Requirements
- Python 3.8+

```bash
git clone https://github.com/aprajitakashyap/MatchFlowAI.git
cd MatchFlowAI/backend
pip install -r requirements.txt
python app.py
```

Open **http://localhost:8000**

---

## Docker

```bash
# Build
docker build -t stadiumsenseai .

# Run
docker run -p 8080:8080 stadiumsenseai

# Open
open http://localhost:8080
```

---

## API Reference

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/` | Frontend UI |
| `GET` | `/health` | Health check → `{"status":"UP"}` |
| `GET` | `/faq` | All 10 FAQs |
| `GET` | `/locations` | All 18 stadium locations |
| `GET` | `/routes` | 5 routes with accessibility flag |
| `POST` | `/chat` | AI response |

### POST /chat
```json
// Request
{ "message": "Where is the restroom?", "language": "en" }

// Response
{ "response": "🚻 Restrooms:\n• Level 1 North..." }
```
Languages: `en` · `es` · `fr`

---

## Render Deployment

Deployed as a **Docker Web Service** on Render Free Tier.

### Configuration
| Setting | Value |
|---------|-------|
| Runtime | Docker |
| Branch | main |
| Dockerfile | `./Dockerfile` |
| Health Check | `/health` |
| Auto Deploy | Enabled |
| Environment | `PORT=8080` |

### Deploy your own

1. Fork https://github.com/aprajitakashyap/MatchFlowAI
2. Go to [render.com](https://render.com) → New → Web Service
3. Connect your fork
4. Select **Docker** runtime
5. Set Health Check Path to `/health`
6. Deploy

The `render.yaml` in the repo auto-configures everything.

---

## Project Structure

```
MatchFlowAI/
├── backend/
│   ├── app.py          # Flask app — all endpoints + serves frontend
│   ├── assistant.py    # Intent engine — 13 intents, EN/ES/FR responses
│   ├── data.py         # In-memory data — 18 locations, 10 FAQs, 5 routes
│   └── requirements.txt  # flask + gunicorn
├── frontend/
│   └── public/
│       └── index.html  # Complete chat UI — single file
├── Dockerfile          # python:3.11-slim, non-root, gunicorn
├── render.yaml         # Render auto-configuration
├── .env.example
├── .gitignore
└── README.md
```

---

## Features

- **13 intent categories** — greeting, gate, restroom, food, seat, parking, metro, medical, merchandise, accessible, prohibited, reentry, wifi
- **3 languages** — English, Spanish, French — native responses per language
- **FAQ chips** — 4 quick-tap questions loaded on startup
- **Accessible UI** — ARIA roles, keyboard navigation, screen reader support
- **Mobile-first** — responsive layout, works on any device
- **Zero secrets** — no API keys, no credentials, nothing to configure
