"""
StadiumSenseAI — Intent detection engine + context builder.
Used as primary response when Gemini is unavailable,
and as context supplier when Gemini is active.
"""

from data import STADIUM, LOCATIONS, FAQS, ROUTES

# ── Context builder for Gemini prompt ─────────────────────────────────────────
def build_context(message: str) -> str:
    """Build relevant stadium context string from user message keywords."""
    msg   = message.lower()
    words = [w for w in msg.split() if len(w) > 3]

    matched_locs = [
        loc for loc in LOCATIONS
        if any(w in loc["name"].lower() or w in loc["category"].lower() for w in words)
    ] or LOCATIONS  # fallback: all locations

    matched_faqs = [
        faq for faq in FAQS
        if any(w in faq["question"].lower() or w in faq["answer"].lower() for w in words)
    ]

    lines = [
        f"Stadium: {STADIUM['name']}, {STADIUM['city']}, {STADIUM['country']} (capacity {STADIUM['capacity']:,})",
        "",
        "Locations:",
        *[f"  - {l['name']} [{l['category']}]" for l in matched_locs],
    ]
    if matched_faqs:
        lines += ["", "Relevant FAQs:"]
        for f in matched_faqs:
            lines += [f"  Q: {f['question']}", f"  A: {f['answer']}"]

    routes_accessible = [r for r in ROUTES if r["accessible"]]
    lines += ["", "Accessible Routes:"]
    lines += [f"  {r['from']} → {r['to']}" for r in routes_accessible]

    return "\n".join(lines)


# ── Intent definitions ─────────────────────────────────────────────────────────
INTENTS = [
    {
        "name": "greeting",
        "keywords": ["hello", "hi", "hey", "hola", "bonjour", "good morning", "good evening"],
        "response": {
            "en": "Hello! Welcome to {stadium}! 🏟️ I'm StadiumSenseAI, your guide for today's match. Ask me about gates, seating, food, restrooms, parking, accessible routes, and more!",
            "es": "¡Hola! Bienvenido a {stadium}! 🏟️ Soy StadiumSenseAI, tu guía para el partido de hoy.",
            "fr": "Bonjour! Bienvenue au {stadium}! 🏟️ Je suis StadiumSenseAI, votre guide pour le match.",
        },
    },
    {
        "name": "gate",
        "keywords": ["gate", "entrance", "enter", "entry", "puerta", "entrada", "porte", "entrée"],
        "response": {
            "en": "🚪 **Stadium Gates:**\n• Gate A – North Entrance (main entry, accessible)\n• Gate B – South Entrance\n• Gate C – VIP Entrance (opens 4 hours before kickoff)\n\nAll gates open 3 hours before kickoff.",
            "es": "🚪 **Puertas del estadio:**\n• Puerta A – Norte (principal, accesible)\n• Puerta B – Sur\n• Puerta C – VIP (abre 4h antes)\n\nTodas las puertas abren 3h antes del partido.",
            "fr": "🚪 **Portes du stade:**\n• Porte A – Nord (principale, accessible)\n• Porte B – Sud\n• Porte C – VIP (ouvre 4h avant)\n\nToutes les portes ouvrent 3h avant le match.",
        },
    },
    {
        "name": "restroom",
        "keywords": ["restroom", "toilet", "bathroom", "wc", "washroom", "baño", "toilette", "sanitaire"],
        "response": {
            "en": "🚻 **Restrooms:**\n• Level 1 North – near Gate A\n• Level 2 South – near Block 201\n• ♿ Accessible Restroom – Gate A, Level 1",
            "es": "🚻 **Baños:**\n• Nivel 1 Norte – cerca Puerta A\n• Nivel 2 Sur – cerca Bloque 201\n• ♿ Baño Accesible – Puerta A, Nivel 1",
            "fr": "🚻 **Toilettes:**\n• Niveau 1 Nord – près Porte A\n• Niveau 2 Sud – près Bloc 201\n• ♿ Accessible – Porte A, Niveau 1",
        },
    },
    {
        "name": "food",
        "keywords": ["food", "eat", "drink", "restaurant", "cafe", "snack", "hungry", "court", "comida", "comer", "beber", "nourriture", "manger", "boire"],
        "response": {
            "en": "🍔 **Food & Drinks:**\n• Main Food Court – Main Concourse (Gates A & B)\n• Food Court – Level 2 East\n\nOutside food/drinks not permitted.",
            "es": "🍔 **Comida y bebidas:**\n• Patio principal – entre Puertas A y B\n• Patio – Nivel 2 Este\n\nNo se permite comida del exterior.",
            "fr": "🍔 **Nourriture:**\n• Cour principale – entre Portes A et B\n• Cour – Niveau 2 Est\n\nNourriture extérieure interdite.",
        },
    },
    {
        "name": "seat",
        "keywords": ["seat", "block", "section", "row", "ticket", "asiento", "bloque", "sección", "siège", "place", "billet"],
        "response": {
            "en": "💺 **Seating:**\n• Block 101 – Lower North (Gate A)\n• Block 201 – Upper South (Gate B)\n• Block 305 – Premium West / VIP (Gate C)\n\nCheck your ticket for block & row.",
            "es": "💺 **Asientos:**\n• Bloque 101 – Norte Inferior (Puerta A)\n• Bloque 201 – Sur Superior (Puerta B)\n• Bloque 305 – Oeste Premium/VIP (Puerta C)",
            "fr": "💺 **Sièges:**\n• Bloc 101 – Nord Inférieur (Porte A)\n• Bloc 201 – Sud Supérieur (Porte B)\n• Bloc 305 – Ouest Premium/VIP (Porte C)",
        },
    },
    {
        "name": "parking",
        "keywords": ["park", "parking", "car", "vehicle", "drive", "estacionamiento", "carro", "coche", "stationnement", "voiture"],
        "response": {
            "en": "🅿️ **Parking:**\n• Zone P1 – North (near Gate A)\n• Zone P2 – South (near Gate B)\n\n💡 Metro recommended — parking fills fast.",
            "es": "🅿️ **Estacionamiento:**\n• Zona P1 – Norte (Puerta A)\n• Zona P2 – Sur (Puerta B)\n\n💡 Se recomienda el metro.",
            "fr": "🅿️ **Parking:**\n• Zone P1 – Nord (Porte A)\n• Zone P2 – Sud (Porte B)\n\n💡 Métro recommandé.",
        },
    },
    {
        "name": "metro",
        "keywords": ["metro", "subway", "train", "transit", "transport", "bus", "tren", "transporte", "métro"],
        "response": {
            "en": "🚇 **Metro:**\n• Lusail Metro Station → 5-min walk to Gate A\n• Fully accessible (wheelchair friendly)\n• Arrive 2+ hours early to avoid crowds.",
            "es": "🚇 **Metro:**\n• Estación Lusail → 5 min a Puerta A\n• Ruta accesible para sillas de ruedas\n• Llegue 2h antes para evitar aglomeraciones.",
            "fr": "🚇 **Métro:**\n• Station Lusail → 5 min à pied Porte A\n• Itinéraire accessible fauteuil roulant\n• Arrivez 2h+ avant le coup d'envoi.",
        },
    },
    {
        "name": "medical",
        "keywords": ["medical", "first aid", "doctor", "ambulance", "emergency", "sick", "hurt", "injury", "médico", "emergencia", "urgence", "blessé"],
        "response": {
            "en": "🏥 **Medical & First Aid:**\n• First Aid Station – Gate B, Ground Floor\n• Medical Center – Level 1, near Block 101\n\nIn emergency: approach any steward immediately.",
            "es": "🏥 **Primeros Auxilios:**\n• Puesto – Puerta B, Planta Baja\n• Centro Médico – Nivel 1, Bloque 101\n\nEmergencia: acuda a cualquier acomodador.",
            "fr": "🏥 **Médical:**\n• Poste – Porte B, Rez-de-chaussée\n• Centre Médical – Niveau 1, Bloc 101\n\nUrgence: approchez n'importe quel steward.",
        },
    },
    {
        "name": "merchandise",
        "keywords": ["shop", "store", "merchandise", "souvenir", "buy", "jersey", "kit", "tienda", "boutique", "acheter", "maillot"],
        "response": {
            "en": "🛍️ **Merchandise:**\n• FIFA Official Store – Gate A\n• Kiosk – Level 2\n\nOfficial jerseys, scarves, balls & souvenirs.",
            "es": "🛍️ **Tienda:**\n• Tienda Oficial FIFA – Puerta A\n• Quiosco – Nivel 2",
            "fr": "🛍️ **Boutique:**\n• Boutique FIFA Officielle – Porte A\n• Kiosque – Niveau 2",
        },
    },
    {
        "name": "accessible",
        "keywords": ["wheelchair", "accessible", "disability", "disabled", "mobility", "handicap", "silla de ruedas", "accesible", "fauteuil", "handicapé"],
        "response": {
            "en": "♿ **Accessible Routes:**\n• Enter via Gate A – North (fully accessible)\n• Accessible restroom – Gate A, Level 1\n• Accessible seating – Block 101\n• Route: Metro Station → Gate A → Block 101\n• Priority assistance at Gate A stewards",
            "es": "♿ **Accesibilidad:**\n• Entrada por Puerta A (accesible)\n• Baño accesible – Puerta A, Nivel 1\n• Asientos accesibles – Bloque 101\n• Ruta: Metro → Puerta A → Bloque 101",
            "fr": "♿ **Accessibilité:**\n• Entrez par Porte A (accessible)\n• Toilettes – Porte A, Niveau 1\n• Places – Bloc 101\n• Itinéraire: Métro → Porte A → Bloc 101",
        },
    },
    {
        "name": "prohibited",
        "keywords": ["prohibited", "banned", "allowed", "permit", "bring", "bag", "camera", "drone", "prohibido", "bolsa", "interdit", "sac"],
        "response": {
            "en": "🚫 **Prohibited Items:**\n• Outside food/drinks\n• Bags > 30×20×15 cm\n• Umbrellas\n• Professional cameras / recording equipment\n• Drones · Flares · Fireworks",
            "es": "🚫 **Artículos prohibidos:**\n• Comida/bebida exterior\n• Bolsas > 30×20×15 cm\n• Paraguas · Cámaras profesionales\n• Drones · Bengalas",
            "fr": "🚫 **Articles interdits:**\n• Nourriture/boissons extérieures\n• Sacs > 30×20×15 cm\n• Parapluies · Caméras pro\n• Drones · Fusées",
        },
    },
    {
        "name": "reentry",
        "keywords": ["re-entry", "reentry", "leave", "exit", "come back", "return", "salir", "volver", "sortir", "revenir"],
        "response": {
            "en": "🔄 **Re-Entry:** Permitted with a valid match ticket. Not allowed in the last 15 minutes or at half-time in some zones.",
            "es": "🔄 **Re-entrada:** Permitida con boleto válido. No en los últimos 15 min ni medio tiempo en algunas zonas.",
            "fr": "🔄 **Ré-entrée:** Permise avec billet valide. Interdite pendant les 15 dernières minutes et à la mi-temps dans certaines zones.",
        },
    },
    {
        "name": "wifi",
        "keywords": ["wifi", "wi-fi", "internet", "network", "connect", "signal", "phone"],
        "response": {
            "en": "📶 **Wi-Fi:** Free throughout the stadium.\n• Network: StadiumSense_Guest\n• No password required",
            "es": "📶 **Wi-Fi:** Gratuito en todo el estadio.\n• Red: StadiumSense_Guest\n• Sin contraseña",
            "fr": "📶 **Wi-Fi:** Gratuit dans tout le stade.\n• Réseau: StadiumSense_Guest\n• Sans mot de passe",
        },
    },
]

FALLBACK = {
    "en": "I can help with:\n🚪 Gates  💺 Seating  🍔 Food  🚻 Restrooms  🅿️ Parking  🚇 Metro  🏥 Medical  🛍️ Merchandise  ♿ Accessibility  📶 Wi-Fi\n\nTry: \"Where is Gate A?\" or \"Is there accessible parking?\"",
    "es": "Puedo ayudarte con:\n🚪 Puertas  💺 Asientos  🍔 Comida  🚻 Baños  🅿️ Estacionamiento  🚇 Metro  🏥 Médico  🛍️ Tienda  ♿ Accesibilidad\n\nIntenta: \"¿Dónde está la Puerta A?\"",
    "fr": "Je peux vous aider avec:\n🚪 Portes  💺 Sièges  🍔 Nourriture  🚻 Toilettes  🅿️ Parking  🚇 Métro  🏥 Médical  🛍️ Boutique  ♿ Accessibilité\n\nEssayez: \"Où est la Porte A?\"",
}


def detect_intent(message: str) -> str | None:
    msg = message.lower()
    best, score = None, 0
    for intent in INTENTS:
        s = sum(1 for kw in intent["keywords"] if kw in msg)
        if s > score:
            score, best = s, intent["name"]
    return best if score > 0 else None


def get_response(message: str, language: str = "en") -> str:
    lang = language if language in ("en", "es", "fr") else "en"
    intent_name = detect_intent(message)

    if intent_name:
        for intent in INTENTS:
            if intent["name"] == intent_name:
                return intent["response"].get(lang, intent["response"]["en"]).replace("{stadium}", STADIUM["name"])

    msg   = message.lower()
    words = [w for w in msg.split() if len(w) > 3]
    for faq in FAQS:
        if any(w in faq["question"].lower() or w in faq["answer"].lower() for w in words):
            prefix = {"es": "Según nuestra información: ", "fr": "Selon nos informations: "}.get(lang, "")
            return prefix + faq["answer"]

    return FALLBACK.get(lang, FALLBACK["en"])
