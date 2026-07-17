"""
Smart rule-based assistant engine.
No API key required — uses intent detection + data matching.
"""

from data import STADIUM, LOCATIONS, FAQS, ROUTES

# ── Intent definitions ────────────────────────────────────────────────────────
INTENTS = [
    {
        "name": "greeting",
        "keywords": ["hello", "hi", "hey", "hola", "bonjour", "good morning", "good evening"],
        "response": {
            "en": "Hello! Welcome to {stadium}! 🏟️ I'm StadiumSense AI, your guide for today's match. You can ask me about gates, seating, food, restrooms, parking, accessible routes, and more. How can I help?",
            "es": "¡Hola! Bienvenido a {stadium}! 🏟️ Soy StadiumSense AI, tu guía para el partido de hoy. Puedo ayudarte con puertas, asientos, comida, baños, estacionamiento y rutas accesibles.",
            "fr": "Bonjour! Bienvenue au {stadium}! 🏟️ Je suis StadiumSense AI, votre guide pour le match d'aujourd'hui. Posez-moi des questions sur les portes, places, nourriture, toilettes, parking et itinéraires accessibles.",
        },
    },
    {
        "name": "gate",
        "keywords": ["gate", "entrance", "enter", "entry", "puerta", "entrada", "porte", "entrée"],
        "response": {
            "en": "🚪 **Stadium Gates:**\n• Gate A – North Entrance (main entry, accessible)\n• Gate B – South Entrance\n• Gate C – VIP Entrance (opens 4 hours before kickoff)\n\nAll gates open 3 hours before kickoff. Accessible routes available from Gate A.",
            "es": "🚪 **Puertas del estadio:**\n• Puerta A – Entrada Norte (entrada principal, accesible)\n• Puerta B – Entrada Sur\n• Puerta C – Entrada VIP (abre 4 horas antes del partido)\n\nTodas las puertas abren 3 horas antes del inicio.",
            "fr": "🚪 **Portes du stade:**\n• Porte A – Entrée Nord (entrée principale, accessible)\n• Porte B – Entrée Sud\n• Porte C – Entrée VIP (ouvre 4h avant le coup d'envoi)\n\nToutes les portes ouvrent 3 heures avant le match.",
        },
    },
    {
        "name": "restroom",
        "keywords": ["restroom", "toilet", "bathroom", "wc", "washroom", "baño", "toilette", "sanitaire"],
        "response": {
            "en": "🚻 **Restrooms:**\n• Level 1 North – near Gate A concourse\n• Level 2 South – near Block 201\n• ♿ Accessible Restroom – Gate A, Level 1 (wheelchair accessible)\n\nRestrooms are available on every level near the concourse.",
            "es": "🚻 **Baños:**\n• Nivel 1 Norte – cerca de la concesión Puerta A\n• Nivel 2 Sur – cerca del Bloque 201\n• ♿ Baño Accesible – Puerta A, Nivel 1\n\nHay baños en cada nivel cerca de la concesión.",
            "fr": "🚻 **Toilettes:**\n• Niveau 1 Nord – près de la concession Porte A\n• Niveau 2 Sud – près du Bloc 201\n• ♿ Toilettes Accessibles – Porte A, Niveau 1\n\nDes toilettes sont disponibles à chaque niveau.",
        },
    },
    {
        "name": "food",
        "keywords": ["food", "eat", "drink", "restaurant", "cafe", "snack", "hungry", "court", "comida", "comer", "beber", "nourriture", "manger", "boire", "restaurante"],
        "response": {
            "en": "🍔 **Food & Drinks:**\n• Main Food Court – Main Concourse (between Gates A & B)\n• Food Court – Level 2 East\n\nBoth courts offer hot meals, snacks, and beverages. Outside food and drinks are not permitted inside the stadium.",
            "es": "🍔 **Comida y bebidas:**\n• Patio de comidas principal – Concesión Principal (entre Puertas A y B)\n• Patio de comidas – Nivel 2 Este\n\nNo se permite comida ni bebida del exterior.",
            "fr": "🍔 **Nourriture et boissons:**\n• Cour alimentaire principale – Concession principale (entre Portes A et B)\n• Cour alimentaire – Niveau 2 Est\n\nNourriture et boissons extérieures ne sont pas autorisées.",
        },
    },
    {
        "name": "seat",
        "keywords": ["seat", "block", "section", "row", "ticket", "asiento", "bloque", "sección", "siège", "place", "billet"],
        "response": {
            "en": "💺 **Seating Blocks:**\n• Block 101 – Lower North (accessible via Gate A)\n• Block 201 – Upper South (via Gate B)\n• Block 305 – Premium West (VIP, via Gate C)\n\nCheck your ticket for your block and row number. Gate A serves Blocks 101–150, Gate B serves 201–250.",
            "es": "💺 **Bloques de asientos:**\n• Bloque 101 – Norte Inferior (accesible por Puerta A)\n• Bloque 201 – Sur Superior (por Puerta B)\n• Bloque 305 – Oeste Premium (VIP, por Puerta C)\n\nRevisa tu boleto para el bloque y fila.",
            "fr": "💺 **Blocs de sièges:**\n• Bloc 101 – Nord Inférieur (accessible via Porte A)\n• Bloc 201 – Sud Supérieur (via Porte B)\n• Bloc 305 – Ouest Premium (VIP, via Porte C)\n\nVérifiez votre billet pour le bloc et la rangée.",
        },
    },
    {
        "name": "parking",
        "keywords": ["park", "parking", "car", "vehicle", "drive", "estacionamiento", "carro", "coche", "stationnement", "voiture"],
        "response": {
            "en": "🅿️ **Parking:**\n• Zone P1 – North (near Gate A)\n• Zone P2 – South (near Gate B)\n\n💡 Tip: Metro is strongly recommended. Parking fills up fast. Lusail Metro Station is a 5-minute walk from Gate A.",
            "es": "🅿️ **Estacionamiento:**\n• Zona P1 – Norte (cerca Puerta A)\n• Zona P2 – Sur (cerca Puerta B)\n\n💡 Consejo: Se recomienda el metro. El estacionamiento se llena rápido.",
            "fr": "🅿️ **Parking:**\n• Zone P1 – Nord (près de la Porte A)\n• Zone P2 – Sud (près de la Porte B)\n\n💡 Conseil: Le métro est fortement recommandé. Le parking se remplit vite.",
        },
    },
    {
        "name": "metro",
        "keywords": ["metro", "subway", "train", "transit", "transport", "bus", "tren", "transporte", "métro", "transport en commun"],
        "response": {
            "en": "🚇 **Metro / Public Transport:**\n• Lusail Metro Station → 5-minute walk to Gate A\n• Fully accessible route (wheelchair friendly)\n• Recommended to arrive 2+ hours before kickoff to avoid crowds\n\nThis is the fastest and easiest way to reach the stadium.",
            "es": "🚇 **Metro / Transporte público:**\n• Estación de Metro Lusail → 5 min caminando a Puerta A\n• Ruta totalmente accesible (apto para sillas de ruedas)\n• Se recomienda llegar 2+ horas antes para evitar aglomeraciones.",
            "fr": "🚇 **Métro / Transports en commun:**\n• Station de Métro Lusail → 5 minutes à pied de la Porte A\n• Itinéraire entièrement accessible (fauteuil roulant)\n• Arrivez 2h+ avant le coup d'envoi pour éviter la foule.",
        },
    },
    {
        "name": "medical",
        "keywords": ["medical", "first aid", "doctor", "ambulance", "emergency", "sick", "hurt", "injury", "médico", "primeros auxilios", "emergencia", "médical", "secours", "urgence", "blessé"],
        "response": {
            "en": "🏥 **Medical & First Aid:**\n• First Aid Station – Gate B, Ground Floor\n• Medical Center – Level 1, near Block 101\n\nIn case of emergency, approach any steward or call stadium security immediately. Defibrillators are located at each gate.",
            "es": "🏥 **Médico y Primeros Auxilios:**\n• Puesto de Primeros Auxilios – Puerta B, Planta Baja\n• Centro Médico – Nivel 1, cerca del Bloque 101\n\nEn caso de emergencia, acuda a cualquier acomodador o llame a seguridad.",
            "fr": "🏥 **Médical et Premiers Secours:**\n• Poste de Premiers Secours – Porte B, Rez-de-chaussée\n• Centre Médical – Niveau 1, près du Bloc 101\n\nEn cas d'urgence, approchez n'importe quel steward ou appelez la sécurité.",
        },
    },
    {
        "name": "merchandise",
        "keywords": ["shop", "store", "merchandise", "souvenir", "buy", "jersey", "kit", "tienda", "mercancía", "boutique", "magasin", "acheter", "maillot"],
        "response": {
            "en": "🛍️ **Merchandise & Shopping:**\n• FIFA Official Store – Gate A (main entrance)\n• Merchandise Kiosk – Level 2\n\nFind official FIFA jerseys, scarves, balls, and souvenirs. Card and cash payments accepted.",
            "es": "🛍️ **Tienda y Mercancía:**\n• Tienda Oficial FIFA – Puerta A (entrada principal)\n• Quiosco de Mercancía – Nivel 2\n\nEncuentra camisetas, bufandas, balones y souvenirs oficiales.",
            "fr": "🛍️ **Boutique et Marchandises:**\n• Boutique Officielle FIFA – Porte A (entrée principale)\n• Kiosque Marchandises – Niveau 2\n\nTrouvez maillots, écharpes, ballons et souvenirs officiels FIFA.",
        },
    },
    {
        "name": "accessible",
        "keywords": ["wheelchair", "accessible", "disability", "disabled", "mobility", "handicap", "silla de ruedas", "accesible", "discapacidad", "fauteuil", "handicapé", "accessibilité"],
        "response": {
            "en": "♿ **Accessible Routes & Facilities:**\n• Enter via Gate A – North Entrance (fully accessible)\n• Accessible restroom on Level 1 near Gate A\n• Accessible seating in Block 101 (Lower North)\n• Accessible route: Metro Station → Gate A → Block 101 (all ramp/lift access)\n• Priority assistance available — speak to any steward at Gate A",
            "es": "♿ **Rutas y facilidades accesibles:**\n• Entrada por Puerta A – Norte (totalmente accesible)\n• Baño accesible en Nivel 1 cerca de Puerta A\n• Asientos accesibles en Bloque 101\n• Ruta accesible: Estación Metro → Puerta A → Bloque 101\n• Asistencia prioritaria disponible en Puerta A",
            "fr": "♿ **Itinéraires et équipements accessibles:**\n• Entrez par la Porte A – Nord (entièrement accessible)\n• Toilettes accessibles Niveau 1 près de la Porte A\n• Places accessibles au Bloc 101\n• Itinéraire: Station Métro → Porte A → Bloc 101 (rampes/ascenseurs)\n• Assistance prioritaire disponible à la Porte A",
        },
    },
    {
        "name": "prohibited",
        "keywords": ["prohibited", "banned", "allowed", "permit", "bring", "bag", "camera", "drone", "prohibido", "permitido", "bolsa", "interdit", "autorisé", "sac"],
        "response": {
            "en": "🚫 **Prohibited Items:**\nThe following are NOT allowed inside the stadium:\n• Outside food or beverages\n• Bags larger than 30×20×15 cm\n• Umbrellas\n• Professional cameras or recording equipment\n• Drones\n• Flares or fireworks\n\nSmall bags and personal items are permitted after security screening.",
            "es": "🚫 **Artículos prohibidos:**\nNo está permitido ingresar con:\n• Comida o bebidas del exterior\n• Bolsas mayores de 30×20×15 cm\n• Paraguas\n• Cámaras profesionales o equipos de grabación\n• Drones · Bengalas o fuegos artificiales",
            "fr": "🚫 **Articles interdits:**\nIl est interdit d'entrer avec:\n• Nourriture ou boissons extérieures\n• Sacs de plus de 30×20×15 cm\n• Parapluies · Caméras professionnelles\n• Drones · Fusées éclairantes ou feux d'artifice",
        },
    },
    {
        "name": "reentry",
        "keywords": ["re-entry", "reentry", "leave", "exit", "come back", "return", "salir", "volver", "sortir", "revenir"],
        "response": {
            "en": "🔄 **Re-Entry Policy:**\nRe-entry is permitted with a valid match ticket. Your ticket will be scanned again on re-entry. Note that re-entry is not allowed during the last 15 minutes of the match or at half-time in some zones.",
            "es": "🔄 **Política de re-entrada:**\nSe permite la reentrada con un boleto válido. Tu boleto será escaneado nuevamente. No se permite en los últimos 15 minutos ni en el medio tiempo en algunas zonas.",
            "fr": "🔄 **Politique de ré-entrée:**\nLa ré-entrée est permise avec un billet valide. Votre billet sera scanné à nouveau. La ré-entrée n'est pas autorisée pendant les 15 dernières minutes ni à la mi-temps dans certaines zones.",
        },
    },
    {
        "name": "wifi",
        "keywords": ["wifi", "wi-fi", "internet", "network", "connect", "signal", "phone", "internet", "red"],
        "response": {
            "en": "📶 **Wi-Fi:**\nFree stadium Wi-Fi is available throughout the venue.\n• Network: StadiumSense_Guest\n• No password required\n\nCoverage may be reduced during peak match times due to high traffic.",
            "es": "📶 **Wi-Fi:**\nWi-Fi gratuito disponible en todo el recinto.\n• Red: StadiumSense_Guest\n• Sin contraseña\n\nLa cobertura puede reducirse durante el partido por alto tráfico.",
            "fr": "📶 **Wi-Fi:**\nWi-Fi gratuit disponible dans tout le stade.\n• Réseau: StadiumSense_Guest\n• Sans mot de passe\n\nLa couverture peut être réduite pendant le match en raison du trafic élevé.",
        },
    },
]

FALLBACK = {
    "en": "I'm not sure about that specific question. Here's what I can help with:\n🚪 Gates & Entry  💺 Seating  🍔 Food Courts  🚻 Restrooms  🅿️ Parking  🚇 Metro  🏥 Medical  🛍️ Merchandise  ♿ Accessible Routes\n\nTry asking something like: \"Where is Gate A?\" or \"Is there accessible parking?\"",
    "es": "No estoy seguro sobre esa pregunta. Puedo ayudarte con:\n🚪 Puertas  💺 Asientos  🍔 Comida  🚻 Baños  🅿️ Estacionamiento  🚇 Metro  🏥 Médico  🛍️ Tienda  ♿ Accesibilidad\n\nIntenta preguntar: \"¿Dónde está la Puerta A?\" o \"¿Hay estacionamiento accesible?\"",
    "fr": "Je ne suis pas sûr de cette question. Je peux vous aider avec:\n🚪 Portes  💺 Sièges  🍔 Nourriture  🚻 Toilettes  🅿️ Parking  🚇 Métro  🏥 Médical  🛍️ Boutique  ♿ Accessibilité\n\nEssayez: \"Où est la Porte A?\" ou \"Y a-t-il un parking accessible?\"",
}


def detect_intent(message: str) -> str | None:
    """Return the best matching intent name, or None."""
    msg = message.lower()
    best_intent = None
    best_score = 0

    for intent in INTENTS:
        score = sum(1 for kw in intent["keywords"] if kw in msg)
        if score > best_score:
            best_score = score
            best_intent = intent["name"]

    return best_intent if best_score > 0 else None


def get_response(message: str, language: str = "en") -> str:
    """
    Smart response engine:
    1. Check intent match
    2. Check FAQ keyword match
    3. Return helpful fallback
    """
    lang = language if language in ("en", "es", "fr") else "en"
    intent_name = detect_intent(message)

    # Intent matched — return structured response
    if intent_name:
        for intent in INTENTS:
            if intent["name"] == intent_name:
                tmpl = intent["response"].get(lang, intent["response"]["en"])
                return tmpl.replace("{stadium}", STADIUM["name"])

    # No intent — try FAQ keyword match
    msg = message.lower()
    words = [w for w in msg.split() if len(w) > 3]
    for faq in FAQS:
        if any(w in faq["question"].lower() or w in faq["answer"].lower() for w in words):
            answer = faq["answer"]
            if lang == "es":
                return f"Según nuestra información: {answer}"
            elif lang == "fr":
                return f"Selon nos informations: {answer}"
            return answer

    # Nothing matched — helpful fallback
    return FALLBACK.get(lang, FALLBACK["en"])
