"""
StadiumSense AI — Flask backend
No API key required. Smart rule-based assistant with intent detection.
"""

import os
import json
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file

from data import FAQS, LOCATIONS, ROUTES
from assistant import get_response

# ── App setup ─────────────────────────────────────────────────────────────────
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "public"

app = Flask(__name__, static_folder=None)

# ── CORS ──────────────────────────────────────────────────────────────────────
@app.after_request
def add_cors(response):
    origin = request.headers.get("Origin", "*")
    response.headers["Access-Control-Allow-Origin"]  = origin
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
@app.route("/<path:path>", methods=["OPTIONS"])
def options(_path=""):
    return "", 204

# ── Frontend ──────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_file(str(FRONTEND_DIR / "index.html"))

# ── Health ────────────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "UP", "service": "StadiumSense AI"})

# ── Data endpoints ─────────────────────────────────────────────────────────────
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
    body = request.get_json(silent=True) or {}
    message  = (body.get("message") or "").strip()
    language = (body.get("language") or "en").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400

    if language not in ("en", "es", "fr"):
        language = "en"

    response_text = get_response(message, language)
    return jsonify({"response": response_text})

# ── Entry point ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"StadiumSense AI running → http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
