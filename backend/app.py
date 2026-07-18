"""
StadiumSenseAI — Flask backend
Smart rule-based stadium assistant. No external API required.

Endpoints:
  GET  /          → frontend UI (index.html)
  GET  /health    → health check (used by Render)
  GET  /faq       → all FAQs
  GET  /locations → all stadium locations
  GET  /routes    → all routes with accessibility flag
  POST /chat      → intent-based AI response
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify, send_file

from data import FAQS, LOCATIONS, ROUTES
from assistant import get_response

# ── Paths ─────────────────────────────────────────────────────────────────────
# Works both locally (python app.py) and inside Docker (/app/backend/app.py)
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "public"

# ── App ───────────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=None)

# ── CORS ──────────────────────────────────────────────────────────────────────
@app.after_request
def add_cors(response):
    """Allow cross-origin requests — safe because we serve no auth cookies."""
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
@app.route("/<path:path>", methods=["OPTIONS"])
def preflight(_path=""):
    return "", 204

# ── Frontend ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_file(str(FRONTEND_DIR / "index.html"))

# ── Health check ──────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "UP", "service": "StadiumSenseAI"})

# ── Data endpoints ────────────────────────────────────────────────────────────
@app.route("/faq")
def faq():
    return jsonify(FAQS)

@app.route("/locations")
def locations():
    return jsonify(LOCATIONS)

@app.route("/routes")
def routes():
    return jsonify(ROUTES)

# ── Chat ──────────────────────────────────────────────────────────────────────
@app.route("/chat", methods=["POST"])
def chat():
    body     = request.get_json(silent=True) or {}
    message  = (body.get("message") or "").strip()
    language = (body.get("language") or "en").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    if language not in ("en", "es", "fr"):
        language = "en"

    return jsonify({"response": get_response(message, language)})

# ── Dev entry point ───────────────────────────────────────────────────────────
# Production uses gunicorn (see Dockerfile CMD).
# This block is only reached when running `python app.py` locally.
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[StadiumSenseAI] http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
