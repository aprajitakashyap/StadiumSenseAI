"""
StadiumSenseAI — Flask backend
Gemini-powered stadium assistant with rule-based fallback.
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify, send_file
from data import FAQS, LOCATIONS, ROUTES
from assistant import get_response, build_context

FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "public"

# ── Gemini setup ──────────────────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
gemini_client  = None

if GEMINI_API_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        print("[StadiumSenseAI] Gemini client ready ✓")
    except Exception as e:
        print(f"[StadiumSenseAI] Gemini init failed: {e}")
else:
    print("[StadiumSenseAI] No GEMINI_API_KEY — using rule-based fallback")

SYSTEM_PROMPT = (
    "You are StadiumSenseAI, a friendly and helpful assistant for FIFA World Cup stadium visitors. "
    "Use the stadium context provided to give accurate, concise answers. "
    "Recommend accessible routes when relevant. "
    "If you don't know something, say so clearly. "
    "Respond only in the language specified."
)
LANG_INSTRUCTIONS = {
    "en": "Respond in English.",
    "es": "Responde completamente en español.",
    "fr": "Réponds entièrement en français.",
}

def gemini_chat(message: str, language: str) -> str:
    context = build_context(message)
    lang_instr = LANG_INSTRUCTIONS.get(language, LANG_INSTRUCTIONS["en"])
    prompt = (
        f"{SYSTEM_PROMPT}\n{lang_instr}\n\n"
        f"=== STADIUM DATA ===\n{context}\n\n"
        f"=== QUESTION ===\n{message}"
    )
    try:
        result = gemini_client.models.generate_content(
            model="gemini-1.5-flash", contents=prompt
        )
        return result.text.strip()
    except Exception as e:
        print(f"[Gemini error] {e} — falling back to rule-based")
        return get_response(message, language)

# ── App ───────────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=None)

@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"]  = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/", defaults={"path": ""}, methods=["OPTIONS"])
@app.route("/<path:path>", methods=["OPTIONS"])
def preflight(_path=""):
    return "", 204

@app.route("/")
def index():
    return send_file(str(FRONTEND_DIR / "index.html"))

@app.route("/health")
def health():
    return jsonify({"status": "UP", "service": "StadiumSenseAI",
                    "ai": "gemini" if gemini_client else "rule-based"})

@app.route("/faq")
def faq():
    return jsonify(FAQS)

@app.route("/locations")
def locations():
    return jsonify(LOCATIONS)

@app.route("/routes")
def routes():
    return jsonify(ROUTES)

@app.route("/chat", methods=["POST"])
def chat():
    body     = request.get_json(silent=True) or {}
    message  = (body.get("message") or "").strip()
    language = (body.get("language") or "en").strip()

    if not message:
        return jsonify({"error": "message is required"}), 400
    if language not in ("en", "es", "fr"):
        language = "en"

    if gemini_client:
        response_text = gemini_chat(message, language)
    else:
        response_text = get_response(message, language)

    return jsonify({"response": response_text})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"[StadiumSenseAI] http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)
