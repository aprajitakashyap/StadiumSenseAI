# StadiumSense AI 🏟️

A smart GenAI assistant for FIFA World Cup stadium visitors — built with Python (FastAPI) + Gemini AI + vanilla HTML/CSS/JS. No build tools required.

---

## Chosen Vertical

**Stadium Navigation & Fan Experience Assistant**

Helps visitors find gates, seats, restrooms, food courts, medical stations, accessible routes, and answers common FAQs — in English, Spanish, or French.

---

## Architecture

```
Browser (HTML/CSS/JS)
        │
        │  POST /chat  GET /faq  GET /locations  GET /routes
        ▼
  FastAPI Backend (Python)
        │
        ├── Keyword-match user message → pull relevant DB context
        ├── Build prompt: system + context + user question + language
        └── Gemini 1.5 Flash API → response → browser
        
  Data: in-memory store (db.py)
        1 stadium · 18 locations · 10 FAQs · 5 routes
```

---

## How It Works

1. User types a question (or taps a FAQ chip) and selects a language (EN/ES/FR)
2. Frontend sends `POST /chat` with `{ message, language }`
3. Backend extracts keywords, matches relevant locations + FAQs from the data store
4. Injects that context into a Gemini prompt alongside the system instructions
5. Gemini returns a grounded, language-correct response
6. Response is displayed as a chat bubble

**Smart context injection** means the AI answers with real stadium data, not hallucinations.

---

## Local Setup

### Prerequisites
- Python 3.10+
- A free Gemini API key → [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey)

### Run in 3 steps

```bash
# 1. Clone
git clone https://github.com/aprajitakashyap/MatchFlowAI.git
cd MatchFlowAI

# 2. Install dependencies
cd backend
pip install -r requirements.txt

# 3. Set your API key and start
echo "GEMINI_API_KEY=your_key_here" > .env
python main.py
```

Open **http://localhost:8000** — the backend serves the frontend automatically.

---

## API Endpoints

| Method | Path         | Description                              |
|--------|-------------|------------------------------------------|
| POST   | `/chat`      | Send message, receive AI response        |
| GET    | `/faq`       | All FAQs (shown as suggestion chips)     |
| GET    | `/locations` | All stadium locations by category        |
| GET    | `/routes`    | All routes with accessibility flag       |
| GET    | `/health`    | Health check                             |

### POST /chat

```json
// Request
{ "message": "Where is the nearest restroom?", "language": "en" }

// Response  
{ "response": "The nearest accessible restroom is at Gate A on Level 1." }
```

**Supported languages:** `en` · `es` · `fr`

---

## Project Structure

```
MatchFlowAI/
├── backend/
│   ├── main.py          # FastAPI app — all endpoints + Gemini integration
│   ├── db.py            # In-memory data store + context builder
│   └── requirements.txt # 4 dependencies only
├── frontend/
│   └── public/
│       └── index.html   # Complete UI — single file, zero build step
├── .env.example         # Environment variable template
├── .gitignore
└── README.md
```

---

## Design Decisions

- **No database server** — data lives in `db.py` (in-memory). Zero infra to spin up.
- **No frontend build step** — pure HTML/CSS/JS, opens directly in browser.
- **Keyword-matched context** — only relevant locations/FAQs are sent to Gemini, keeping prompts focused and responses fast (< 3s target).
- **Multilingual** — language is passed per-request; Gemini handles the translation natively.
- **Accessible** — semantic HTML, ARIA labels, keyboard navigation, sufficient color contrast.
- **Repo < 10 MB** — no compiled artifacts, no `node_modules`, no large binaries.

---

## Assumptions

- Gemini API key is provided via environment variable (never hardcoded)
- Stadium data is seeded for Lusail Iconic Stadium (FIFA World Cup final venue)
- The assistant stays in scope — it answers stadium questions only, not general queries
- Re-entry policy, prohibited items, and accessibility info reflect standard FIFA guidelines
