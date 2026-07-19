"""
StadiumSenseAI — Flask REST API
Gemini-powered smart stadium assistant for FIFA World Cup 2026.
Backend only — frontend served separately via Vercel.
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify, Response
from data import (FAQS, LOCATIONS, ROUTES, MATCHES,
                  get_crowd_status, get_queue_times,
                  get_parking_status, get_metro_info, get_weather)
from assistant import get_response, build_context

# ── Gemini ────────────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
gemini_client  = None

if GEMINI_API_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        print("[StadiumSenseAI] ✓ Gemini ready")
    except Exception as e:
        print(f"[StadiumSenseAI] Gemini failed: {e}")
else:
    print("[StadiumSenseAI] Rule-based mode (set GEMINI_API_KEY for Gemini)")

SYSTEM_PROMPT = """You are StadiumSenseAI, the official smart AI assistant for FIFA World Cup 2026 stadiums.
You help fans navigate, find facilities, check live crowd levels and queue times, plan accessible routes, handle emergencies, and enjoy the match experience.
Use the live stadium data provided. Be warm, friendly, and conversational — not robotic.
Include emojis where appropriate. Give specific recommendations based on crowd and queue data.
Always respond only in the language specified."""

LANG_INST = {
    "en": "Respond in English.",
    "es": "Responde completamente en español.",
    "fr": "Réponds entièrement en français.",
}


def gemini_chat(message: str, language: str, context: list) -> str:
    live_ctx = build_context(message)
    history  = "\n".join([f"{c['role'].upper()}: {c['text']}" for c in context[-4:]])
    prompt = (
        f"{SYSTEM_PROMPT}\n{LANG_INST.get(language, LANG_INST['en'])}\n\n"
        f"=== LIVE STADIUM DATA ===\n{live_ctx}\n\n"
        f"{'=== CONVERSATION HISTORY ===' + chr(10) + history + chr(10) + chr(10) if history else ''}"
        f"=== CURRENT QUESTION ===\n{message}"
    )
    try:
        result = gemini_client.models.generate_content(
            model="gemini-1.5-flash", contents=prompt
        )
        return result.text.strip()
    except Exception as e:
        print(f"[Gemini error] {e}")
        return get_response(message, language)


# ── Flask app ─────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=None)


@app.after_request
def cors(resp):
    resp.headers["Access-Control-Allow-Origin"]  = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "service": "StadiumSenseAI",
        "ai": "gemini-1.5-flash" if gemini_client else "rule-based",
        "version": "2.0"
    })


@app.route("/faq")
def faq():
    return jsonify(FAQS)


@app.route("/locations")
def locations():
    return jsonify(LOCATIONS)


@app.route("/routes")
def routes_ep():
    return jsonify(ROUTES)


@app.route("/matches")
def matches():
    return jsonify(MATCHES)


@app.route("/live/crowd")
def live_crowd():
    return jsonify(get_crowd_status())


@app.route("/live/queues")
def live_queues():
    return jsonify(get_queue_times())


@app.route("/live/parking")
def live_parking():
    return jsonify(get_parking_status())


@app.route("/live/metro")
def live_metro():
    return jsonify(get_metro_info())


@app.route("/live/weather")
def live_weather():
    return jsonify(get_weather())


@app.route("/live/all")
def live_all():
    """Single endpoint to fetch all live data at once."""
    return jsonify({
        "crowd":   get_crowd_status(),
        "queues":  get_queue_times(),
        "parking": get_parking_status(),
        "metro":   get_metro_info(),
        "weather": get_weather(),
    })


@app.route("/chat", methods=["POST", "OPTIONS"])
def chat():
    if request.method == "OPTIONS":
        return Response("", status=204)

    body     = request.get_json(silent=True) or {}
    message  = (body.get("message") or "").strip()
    language = (body.get("language") or "en").strip()
    context  = body.get("context") or []

    if not message:
        return jsonify({"error": "message is required"}), 400
    if language not in ("en", "es", "fr"):
        language = "en"

    if gemini_client:
        text = gemini_chat(message, language, context)
    else:
        text = get_response(message, language)

    return jsonify({"response": text})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[StadiumSenseAI] Running on http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
