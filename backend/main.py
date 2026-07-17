"""
StadiumSense AI — FastAPI backend
Endpoints:
  POST /chat       → Gemini-powered AI response with stadium context
  GET  /faq        → All FAQs
  GET  /locations  → All stadium locations
  GET  /routes     → All routes (with accessibility flag)
  GET  /health     → Health check
  GET  /           → Serves frontend (index.html)
"""

import os
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, field_validator

from db import FAQS, LOCATIONS, ROUTES, build_context

# ── Config ────────────────────────────────────────────────────────────────
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-1.5-flash"
FRONTEND_URL   = os.getenv("FRONTEND_URL", "*")

SYSTEM_PROMPT = (
    "You are StadiumSense AI, a helpful assistant for FIFA World Cup stadium visitors. "
    "Answer politely and accurately using the provided stadium context. "
    "Recommend accessible routes when relevant. "
    "If information is unavailable, say so clearly instead of guessing. "
    "Respond only in the language specified."
)

LANG_INSTRUCTIONS = {
    "en": "Respond in English.",
    "es": "Responde completamente en español.",
    "fr": "Réponds entièrement en français.",
}

FALLBACK_MESSAGES = {
    "en": "AI service not configured. Please set GEMINI_API_KEY in your .env file.",
    "es": "Servicio de IA no configurado. Por favor establece GEMINI_API_KEY en tu archivo .env.",
    "fr": "Service IA non configuré. Veuillez définir GEMINI_API_KEY dans votre fichier .env.",
}

# ── Gemini setup ──────────────────────────────────────────────────────────
gemini_client = None
if GEMINI_API_KEY:
    try:
        from google import genai
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
        print(f"[StadiumSense] Gemini client ready (model: {GEMINI_MODEL})")
    except Exception as e:
        print(f"[StadiumSense] Gemini init error: {e}")
else:
    print("[StadiumSense] GEMINI_API_KEY not set — chat will return fallback response")

# ── FastAPI app ───────────────────────────────────────────────────────────
app = FastAPI(
    title="StadiumSense AI",
    description="FIFA World Cup stadium assistant powered by Gemini",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "http://localhost:8000", "http://localhost:3000"],
    allow_origin_regex=r"https://.*\.run\.app",
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# ── Serve frontend static files ───────────────────────────────────────────
FRONTEND_DIR = Path(__file__).parent.parent / "frontend" / "public"

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(str(FRONTEND_DIR / "index.html"))


# ── Request / Response models ─────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str
    language: str = "en"

    @field_validator("message")
    @classmethod
    def message_not_empty(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("message must not be empty")
        return v

    @field_validator("language")
    @classmethod
    def valid_language(cls, v: str) -> str:
        return v if v in ("en", "es", "fr") else "en"


class ChatResponse(BaseModel):
    response: str


# ── Endpoints ─────────────────────────────────────────────────────────────
@app.get("/health", tags=["system"])
async def health():
    """Health check for Cloud Run / load balancers."""
    return {"status": "UP", "service": "StadiumSense AI"}


@app.get("/faq", tags=["data"])
async def get_faqs():
    """Return all FAQs."""
    return FAQS


@app.get("/locations", tags=["data"])
async def get_locations():
    """Return all stadium locations grouped by category."""
    return LOCATIONS


@app.get("/routes", tags=["data"])
async def get_routes():
    """Return all routes with accessibility flag."""
    return ROUTES


@app.post("/chat", response_model=ChatResponse, tags=["ai"])
async def chat(req: ChatRequest):
    """
    Main AI endpoint.
    Builds stadium context from DB, sends to Gemini, returns response.
    """
    if not gemini_client:
        return ChatResponse(response=FALLBACK_MESSAGES.get(req.language, FALLBACK_MESSAGES["en"]))

    context = build_context(req.message)
    lang_instruction = LANG_INSTRUCTIONS.get(req.language, LANG_INSTRUCTIONS["en"])

    prompt = (
        f"{SYSTEM_PROMPT}\n"
        f"{lang_instruction}\n\n"
        f"=== STADIUM CONTEXT ===\n{context}\n\n"
        f"=== VISITOR QUESTION ===\n{req.message}"
    )

    try:
        from google import genai as _genai
        result = gemini_client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        return ChatResponse(response=result.text.strip())
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI service error: {str(e)}")


# ── Dev server entry point ────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"[StadiumSense] Starting on http://localhost:{port}")
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
