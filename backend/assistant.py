"""
StadiumSenseAI — Smart intent engine with simulated live data.
Handles 25+ intent categories. Feeds context to Gemini when available.
"""

from data import (STADIUM, LOCATIONS, FAQS, ROUTES, MATCHES,
                  get_crowd_status, get_queue_times, get_parking_status,
                  get_metro_info, get_weather)


# ── Context builder for Gemini ────────────────────────────────────────────────
def build_context(message: str) -> str:
    msg   = message.lower()
    words = [w for w in msg.split() if len(w) > 2]

    matched_locs = [
        l for l in LOCATIONS
        if any(w in l["name"].lower() or w in l["category"].lower() for w in words)
    ] or LOCATIONS[:10]

    matched_faqs = [
        f for f in FAQS
        if any(w in f["question"].lower() or w in f["answer"].lower() for w in words)
    ]

    crowd  = get_crowd_status()
    queues = get_queue_times()
    metro  = get_metro_info()
    wx     = get_weather()

    lines = [
        f"Stadium: {STADIUM['name']}, {STADIUM['city']} (cap {STADIUM['capacity']:,})",
        f"Weather: {wx['temp_c']}°C, {wx['condition']}, Humidity {wx['humidity']}%",
        "",
        "LIVE CROWD:",
        *[f"  {g}: {d['pct']}% — {d['level']}" for g, d in crowd.items()],
        "",
        "QUEUE TIMES:",
        *[f"  {p}: ~{d['wait_mins']} min" for p, d in queues.items()],
        "",
        f"METRO: Next train in {metro['next_train_mins']} min, every {metro['frequency_mins']} min",
        "",
        "LOCATIONS:",
        *[f"  - {l['name']} [{l['category']}]{'  ♿' if l['accessible'] else ''}" for l in matched_locs],
    ]

    if matched_faqs:
        lines += ["", "RELEVANT FAQs:"]
        for f in matched_faqs:
            lines += [f"  Q: {f['question']}", f"  A: {f['answer']}"]

    if MATCHES:
        m = MATCHES[0]
        lines += ["", f"NEXT MATCH: {m['home']} vs {m['away']} — {m['kickoff']} {m['date']} ({m['stage']})"]

    return "\n".join(lines)


# ── Intent map ────────────────────────────────────────────────────────────────
def _r(en, es=None, fr=None):
    return {"en": en, "es": es or en, "fr": fr or en}


INTENTS = [
    {
        "name": "greeting",
        "keywords": ["hello", "hi", "hey", "hola", "bonjour", "salut", "welcome", "start"],
        "handler": lambda lang: _greeting(lang),
    },
    {
        "name": "crowd",
        "keywords": ["crowd", "busy", "crowded", "less crowded", "quiet gate", "which gate", "multitud", "foule"],
        "handler": lambda lang: _crowd(lang),
    },
    {
        "name": "queue",
        "keywords": ["queue", "wait", "waiting", "how long", "line", "fila", "espera", "attente"],
        "handler": lambda lang: _queue(lang),
    },
    {
        "name": "route",
        "keywords": ["route", "how to get", "fastest", "shortest", "directions", "navigate", "ruta", "itinéraire"],
        "handler": lambda lang: _route(lang),
    },
    {
        "name": "accessible_route",
        "keywords": ["wheelchair", "accessible", "disability", "disabled", "mobility", "ramp", "lift",
                     "silla de ruedas", "discapacidad", "fauteuil", "handicapé", "autism", "quiet", "sensory"],
        "handler": lambda lang: _accessible(lang),
    },
    {
        "name": "transport",
        "keywords": ["metro", "subway", "train", "bus", "taxi", "uber", "transport", "shuttle",
                     "after match", "exit", "tren", "transporte", "métro"],
        "handler": lambda lang: _transport(lang),
    },
    {
        "name": "parking",
        "keywords": ["park", "parking", "car", "vehicle", "drive", "estacionamiento", "stationnement"],
        "handler": lambda lang: _parking(lang),
    },
    {
        "name": "gate",
        "keywords": ["gate", "entrance", "enter", "entry", "door", "puerta", "entrada", "porte"],
        "handler": lambda lang: _gate(lang),
    },
    {
        "name": "seat",
        "keywords": ["seat", "block", "section", "row", "stand", "ticket", "asiento", "bloque", "siège"],
        "handler": lambda lang: _seat(lang),
    },
    {
        "name": "restroom",
        "keywords": ["restroom", "toilet", "bathroom", "wc", "washroom", "baño", "toilette", "sanitaire"],
        "handler": lambda lang: _restroom(lang),
    },
    {
        "name": "food",
        "keywords": ["food", "eat", "hungry", "drink", "water", "snack", "meal", "halal",
                     "comida", "comer", "nourriture", "manger"],
        "handler": lambda lang: _food(lang),
    },
    {
        "name": "medical",
        "keywords": ["medical", "doctor", "first aid", "ambulance", "emergency", "sick", "hurt",
                     "injury", "aed", "defibrillator", "médico", "emergencia", "urgence"],
        "handler": lambda lang: _medical(lang),
    },
    {
        "name": "emergency",
        "keywords": ["emergency", "fire", "evacuate", "evacuation", "panic", "help", "danger",
                     "lost child", "missing child", "security", "threat", "emergencia"],
        "handler": lambda lang: _emergency(lang),
    },
    {
        "name": "lost_found",
        "keywords": ["lost", "found", "missing", "forgot", "left behind", "perdido", "perdu", "objets"],
        "handler": lambda lang: _lost_found(lang),
    },
    {
        "name": "merchandise",
        "keywords": ["shop", "store", "buy", "jersey", "souvenir", "merchandise", "kit",
                     "tienda", "boutique", "acheter"],
        "handler": lambda lang: _merchandise(lang),
    },
    {
        "name": "match",
        "keywords": ["match", "game", "kickoff", "score", "schedule", "fixture", "when",
                     "partido", "match", "horario"],
        "handler": lambda lang: _match(lang),
    },
    {
        "name": "weather",
        "keywords": ["weather", "hot", "rain", "cold", "temperature", "heat", "clima", "météo"],
        "handler": lambda lang: _weather(lang),
    },
    {
        "name": "sustainability",
        "keywords": ["water refill", "recycle", "waste", "bin", "eco", "bottle", "reusable",
                     "sostenible", "durabilité"],
        "handler": lambda lang: _sustainability(lang),
    },
    {
        "name": "family",
        "keywords": ["family", "child", "children", "baby", "kid", "stroller", "pram",
                     "familia", "niño", "enfant", "bébé"],
        "handler": lambda lang: _family(lang),
    },
    {
        "name": "volunteer",
        "keywords": ["volunteer", "staff", "steward", "help visitor", "vip guest", "guide visitor",
                     "voluntario", "bénévole"],
        "handler": lambda lang: _volunteer(lang),
    },
    {
        "name": "wifi",
        "keywords": ["wifi", "wi-fi", "internet", "network", "signal", "connect", "internet"],
        "handler": lambda lang: _wifi(lang),
    },
    {
        "name": "prohibited",
        "keywords": ["prohibited", "banned", "allowed", "permit", "bring", "bag", "camera",
                     "drone", "prohibido", "interdit"],
        "handler": lambda lang: _prohibited(lang),
    },
    {
        "name": "reentry",
        "keywords": ["re-entry", "reentry", "leave", "exit", "come back", "return",
                     "salir", "volver", "sortir"],
        "handler": lambda lang: _reentry(lang),
    },
    {
        "name": "prayer",
        "keywords": ["prayer", "pray", "mosque", "namaz", "salah", "religious", "oración", "prière"],
        "handler": lambda lang: _prayer(lang),
    },
]


# ── Handler functions ─────────────────────────────────────────────────────────

def _greeting(lang):
    m = MATCHES[0] if MATCHES else None
    match_str = f"Today's match: {m['home']} vs {m['away']} at {m['kickoff']}! 🏆" if m else ""
    return {
        "en": f"Hello! Welcome to {STADIUM['name']}! 🏟️✨\n{match_str}\nI'm StadiumSenseAI — your smart guide for FIFA World Cup 2026.\n\nI can help with:\n🚪 Gates & Entry  💺 Seating  🍔 Food & Queues\n🚻 Restrooms  🅿️ Parking  🚇 Metro  ♿ Accessibility\n🏥 Medical  🚨 Emergency  📦 Lost & Found  🌤️ Weather\n\nWhat do you need?",
        "es": f"¡Hola! Bienvenido a {STADIUM['name']}! 🏟️✨\n{match_str}\nSoy StadiumSenseAI — tu guía inteligente para la Copa del Mundo FIFA 2026.\n\n¿En qué puedo ayudarte?",
        "fr": f"Bonjour! Bienvenue au {STADIUM['name']}! 🏟️✨\n{match_str}\nJe suis StadiumSenseAI — votre guide intelligent pour la Coupe du Monde FIFA 2026.\n\nComment puis-je vous aider?",
    }.get(lang, "en")


def _crowd(lang):
    crowd = get_crowd_status()
    quietest = min(crowd.items(), key=lambda x: x[1]["pct"])
    lines_en = ["📊 Live Gate Crowd Status:\n"]
    lines_es = ["📊 Estado de afluencia en puertas:\n"]
    lines_fr = ["📊 Affluence en direct aux portes:\n"]
    for gate, d in crowd.items():
        lines_en.append(f"  {gate}: {d['level']} ({d['pct']}%)")
        lines_es.append(f"  {gate}: {d['level']} ({d['pct']}%)")
        lines_fr.append(f"  {gate}: {d['level']} ({d['pct']}%)")
    rec_en = f"\n✅ Recommended: {quietest[0]} is least crowded right now."
    rec_es = f"\n✅ Recomendado: {quietest[0]} está menos concurrida ahora."
    rec_fr = f"\n✅ Recommandé: {quietest[0]} est le moins fréquenté en ce moment."
    return {"en": "\n".join(lines_en) + rec_en,
            "es": "\n".join(lines_es) + rec_es,
            "fr": "\n".join(lines_fr) + rec_fr}.get(lang, "en")


def _queue(lang):
    queues = get_queue_times()
    shortest = min(queues.items(), key=lambda x: x[1]["wait_mins"])
    lines_en = ["⏱️ Current Queue Wait Times:\n"]
    for place, d in queues.items():
        icon = "🟢" if d["wait_mins"] < 8 else ("🟡" if d["wait_mins"] < 15 else "🔴")
        lines_en.append(f"  {icon} {place}: ~{d['wait_mins']} min")
    lines_en.append(f"\n💡 Shortest queue: {shortest[0]} (~{shortest[1]['wait_mins']} min)")
    txt = "\n".join(lines_en)
    return {"en": txt,
            "es": txt.replace("Current Queue Wait Times", "Tiempos de espera actuales").replace("Shortest queue", "Cola más corta"),
            "fr": txt.replace("Current Queue Wait Times", "Temps d'attente actuels").replace("Shortest queue", "File la plus courte")}.get(lang, txt)


def _route(lang):
    crowd = get_crowd_status()
    quietest_gate = min(crowd.items(), key=lambda x: x[1]["pct"])[0]
    return {
        "en": f"🗺️ Smart Route Recommendations:\n\n🏃 Fastest: Metro Station → Gate A (5 min walk)\n♿ Accessible: Metro → Gate A → Block 101 (ramps + lifts)\n🟢 Least Crowded: Head to {quietest_gate} — lowest crowd now\n🚌 Bus: North Plaza Bus Stop → Gate A (10 min)\n\n💡 Tip: Arrive via metro to avoid parking queues.",
        "es": f"🗺️ Rutas Recomendadas:\n\n🏃 Más rápida: Metro → Puerta A (5 min)\n♿ Accesible: Metro → Puerta A → Bloque 101\n🟢 Menos concurrida: {quietest_gate}\n\n💡 Consejo: Use el metro para evitar atascos.",
        "fr": f"🗺️ Itinéraires Recommandés:\n\n🏃 Plus rapide: Métro → Porte A (5 min)\n♿ Accessible: Métro → Porte A → Bloc 101\n🟢 Moins fréquenté: {quietest_gate}\n\n💡 Conseil: Prenez le métro pour éviter les embouteillages.",
    }.get(lang, "en")


def _accessible(lang):
    return {
        "en": "♿ Accessibility Guide:\n\n🚪 Enter via Gate A or Gate D (both fully accessible)\n🛗 Lifts and ramps available at all levels\n🚻 Accessible restrooms: Gate A Level 1, Gate D Level 1\n💺 Accessible seating: Block 101 (Lower North), Block 401 (Family)\n🤫 Quiet Room: Level 1 West (sensory-friendly, autism-friendly)\n👨‍👩‍👧 Family Help Desk: Gate D\n🚗 Accessible parking: Zone near Gate A\n🚇 Metro: Lusail Station is fully accessible\n\nPriority assistance available at all gates — speak to any steward.",
        "es": "♿ Guía de Accesibilidad:\n\n🚪 Entrada por Puerta A o Puerta D (totalmente accesibles)\n🛗 Ascensores y rampas en todos los niveles\n🚻 Baños accesibles: Puerta A Nivel 1, Puerta D Nivel 1\n💺 Asientos accesibles: Bloque 101, Bloque 401\n🤫 Sala tranquila: Nivel 1 Oeste (apta para autismo)\n\nAsistencia prioritaria disponible en todas las puertas.",
        "fr": "♿ Guide d'Accessibilité:\n\n🚪 Entrez par Porte A ou Porte D (entièrement accessibles)\n🛗 Ascenseurs et rampes à tous les niveaux\n🚻 Toilettes accessibles: Porte A Niveau 1, Porte D Niveau 1\n💺 Places accessibles: Bloc 101, Bloc 401\n🤫 Salle calme: Niveau 1 Ouest (adapté autisme)\n\nAssistance prioritaire disponible à toutes les portes.",
    }.get(lang, "en")


def _transport(lang):
    metro = get_metro_info()
    return {
        "en": f"🚇 Transport Guide:\n\n🚇 Metro: Next train in {metro['next_train_mins']} min, every {metro['frequency_mins']} min on match days\n   Last train: {metro['last_train']}\n🚌 Bus: North Plaza Bus Stop (5 min walk from Gate A)\n🚕 Taxi/Ride-share: Designated zone East of Gate B\n🏃 Walking: Metro Station → Gate A in 5 min (accessible)\n\n🏆 After match: Use Gate D exit → metro to avoid main crowd surge.",
        "es": f"🚇 Guía de Transporte:\n\nMetro: próximo en {metro['next_train_mins']} min, cada {metro['frequency_mins']} min\nÚltimo tren: {metro['last_train']}\nAutobús: Parada Norte (5 min de Puerta A)\nTaxi: Zona Este de Puerta B\n\n🏆 Después del partido: Salida Puerta D → metro.",
        "fr": f"🚇 Guide Transport:\n\nMétro: prochain dans {metro['next_train_mins']} min, toutes les {metro['frequency_mins']} min\nDernier train: {metro['last_train']}\nBus: Arrêt Nord Plaza (5 min de Porte A)\nTaxi: Zone Est de Porte B\n\n🏆 Après le match: Sortie Porte D → métro.",
    }.get(lang, "en")


def _parking(lang):
    pk = get_parking_status()
    best = min(pk.items(), key=lambda x: x[1]["pct_full"])
    lines = ["🅿️ Parking Status:\n"]
    for zone, d in pk.items():
        lines.append(f"  {zone}: {d['level']} ({d['pct_full']}% full)")
    lines.append(f"\n✅ Best option: {best[0]} ({best[1]['pct_full']}% full)")
    lines.append("\n💡 Metro recommended — parking fills 2h before kickoff.")
    txt = "\n".join(lines)
    return {"en": txt, "es": txt, "fr": txt}.get(lang, txt)


def _gate(lang):
    crowd = get_crowd_status()
    return {
        "en": f"🚪 Stadium Gates:\n• Gate A – North (main, accessible) | Crowd: {crowd.get('Gate A – North', {}).get('level','—')}\n• Gate B – South | Crowd: {crowd.get('Gate B – South', {}).get('level','—')}\n• Gate C – VIP (opens 4h early) | Crowd: {crowd.get('Gate C – VIP', {}).get('level','—')}\n• Gate D – East Family Entrance | Crowd: {crowd.get('Gate D – East', {}).get('level','—')}\n\nAll gates open 3h before kickoff.",
        "es": "🚪 Puertas del estadio:\n• Puerta A – Norte (principal, accesible)\n• Puerta B – Sur\n• Puerta C – VIP (abre 4h antes)\n• Puerta D – Este (Familias)\n\nTodas abren 3h antes del partido.",
        "fr": "🚪 Portes du stade:\n• Porte A – Nord (principale, accessible)\n• Porte B – Sud\n• Porte C – VIP (ouvre 4h avant)\n• Porte D – Est (Familles)\n\nToutes ouvrent 3h avant le match.",
    }.get(lang, "en")


def _seat(lang):
    return {
        "en": "💺 Seating Guide:\n• Block 101 – Lower North (Gate A) ♿ Accessible\n• Block 201 – Upper South (Gate B)\n• Block 305 – Premium West / VIP (Gate C)\n• Block 401 – Family Section (Gate D) ♿ Accessible\n\nCheck your ticket for block & row. Stewards at each gate can guide you.",
        "es": "💺 Asientos:\n• Bloque 101 – Norte Inferior (Puerta A) ♿\n• Bloque 201 – Sur Superior (Puerta B)\n• Bloque 305 – Oeste Premium/VIP (Puerta C)\n• Bloque 401 – Familias (Puerta D) ♿",
        "fr": "💺 Sièges:\n• Bloc 101 – Nord Inférieur (Porte A) ♿\n• Bloc 201 – Sud Supérieur (Porte B)\n• Bloc 305 – Ouest Premium/VIP (Porte C)\n• Bloc 401 – Section Familles (Porte D) ♿",
    }.get(lang, "en")


def _restroom(lang):
    return {
        "en": "🚻 Restrooms:\n• Level 1 North – near Gate A concourse\n• Level 2 South – near Block 201\n• ♿ Accessible – Gate A, Level 1\n• ♿ Accessible – Gate D, Level 1\n\nRestrooms on every level. Accessible facilities near Gates A and D.",
        "es": "🚻 Baños:\n• Nivel 1 Norte – cerca Puerta A\n• Nivel 2 Sur – cerca Bloque 201\n• ♿ Accesible – Puerta A, Nivel 1\n• ♿ Accesible – Puerta D, Nivel 1",
        "fr": "🚻 Toilettes:\n• Niveau 1 Nord – près Porte A\n• Niveau 2 Sud – près Bloc 201\n• ♿ Accessibles – Porte A, Niveau 1\n• ♿ Accessibles – Porte D, Niveau 1",
    }.get(lang, "en")


def _food(lang):
    queues = get_queue_times()
    best = min(queues.items(), key=lambda x: x[1]["wait_mins"])
    return {
        "en": f"🍔 Food & Drinks:\n• Main Food Court – Main Concourse (Gates A & B)\n• Food Court – Level 2 East\n• 🥙 Halal Food Zone – Gate A\n• 💧 Water refill stations: Level 1 & Level 2 (free)\n\n⏱️ Shortest queue now: {best[0]} (~{best[1]['wait_mins']} min)\n\nOutside food/drinks not permitted.",
        "es": f"🍔 Comida y bebidas:\n• Patio principal – entre Puertas A y B\n• Patio – Nivel 2 Este\n• 🥙 Zona Halal – Puerta A\n• 💧 Agua gratis: Nivel 1 y 2\n\n⏱️ Cola más corta: {best[0]} (~{best[1]['wait_mins']} min)",
        "fr": f"🍔 Nourriture:\n• Cour principale – entre Portes A et B\n• Cour – Niveau 2 Est\n• 🥙 Zone Halal – Porte A\n• 💧 Eau gratuite: Niveaux 1 et 2\n\n⏱️ File la plus courte: {best[0]} (~{best[1]['wait_mins']} min)",
    }.get(lang, "en")


def _medical(lang):
    return {
        "en": "🏥 Medical & First Aid:\n• First Aid Station – Gate B, Ground Floor\n• Medical Center – Level 1, near Block 101\n• AED Defibrillators – at every gate\n\n🚨 Emergency: Approach any steward or call +974-911\nFor non-urgent help, visit the Medical Center on Level 1.",
        "es": "🏥 Primeros Auxilios:\n• Puesto – Puerta B, Planta Baja\n• Centro Médico – Nivel 1, Bloque 101\n• DEA – en cada puerta\n\n🚨 Emergencia: Acuda a cualquier acomodador o llame al +974-911",
        "fr": "🏥 Médical:\n• Poste – Porte B, Rez-de-chaussée\n• Centre Médical – Niveau 1, Bloc 101\n• DAE – à chaque porte\n\n🚨 Urgence: Approchez un steward ou appelez le +974-911",
    }.get(lang, "en")


def _emergency(lang):
    return {
        "en": "🚨 EMERGENCY GUIDE:\n\n🔴 Medical Emergency: Shout for steward + call +974-911\n👶 Lost Child: Go to Family Help Desk at Gate D IMMEDIATELY\n🔥 Fire/Evacuation: Follow green exit signs → Emergency Exits North & South\n🔒 Security Threat: Alert nearest steward or security officer\n📦 Lost Item: Lost & Found at Gate A Office\n\n⚠️ Stay calm. Follow steward instructions. Do NOT use elevators during evacuation.",
        "es": "🚨 GUÍA DE EMERGENCIAS:\n\n🔴 Emergencia médica: Llama al +974-911\n👶 Niño perdido: Ir a Puerta D INMEDIATAMENTE\n🔥 Evacuación: Seguir salidas de emergencia\n📦 Objeto perdido: Oficina de Objetos Perdidos Puerta A",
        "fr": "🚨 GUIDE D'URGENCE:\n\n🔴 Urgence médicale: Appelez le +974-911\n👶 Enfant perdu: Porte D IMMÉDIATEMENT\n🔥 Évacuation: Suivre les sorties de secours\n📦 Objet perdu: Bureau des Objets Trouvés Porte A",
    }.get(lang, "en")


def _lost_found(lang):
    return {
        "en": "📦 Lost & Found:\n• Location: Gate A Office (near main entrance)\n• Hours: Open from gate opening until 2 hours after match\n• Contact any steward if you can't reach the office\n\nFor lost children: Go directly to the Family Help Desk at Gate D.",
        "es": "📦 Objetos Perdidos:\n• Ubicación: Oficina Puerta A\n• Horario: Desde apertura hasta 2h después del partido\n• Para niños perdidos: Puerta D — Mesa de Ayuda Familiar",
        "fr": "📦 Objets Trouvés:\n• Lieu: Bureau Porte A\n• Horaires: De l'ouverture à 2h après le match\n• Enfants perdus: Bureau Familles Porte D",
    }.get(lang, "en")


def _merchandise(lang):
    queues = get_queue_times()
    store_q = queues.get("FIFA Store – Gate A", {}).get("wait_mins", "?")
    kiosk_q = queues.get("Merchandise Kiosk – Level 2", {}).get("wait_mins", "?")
    return {
        "en": f"🛍️ Merchandise:\n• FIFA Official Store – Gate A | Queue: ~{store_q} min\n• Merchandise Kiosk – Level 2 | Queue: ~{kiosk_q} min\n\nOfficial jerseys, scarves, balls & souvenirs. Card and cash accepted.",
        "es": f"🛍️ Tienda:\n• Tienda Oficial FIFA – Puerta A | Espera: ~{store_q} min\n• Quiosco – Nivel 2 | Espera: ~{kiosk_q} min",
        "fr": f"🛍️ Boutique:\n• Boutique FIFA – Porte A | Attente: ~{store_q} min\n• Kiosque – Niveau 2 | Attente: ~{kiosk_q} min",
    }.get(lang, "en")


def _match(lang):
    if not MATCHES:
        return {"en": "No match data available.", "es": "No hay datos de partidos.", "fr": "Aucune donnée de match."}.get(lang, "en")
    m = MATCHES[0]
    upcoming = MATCHES[1:]
    txt = f"⚽ Today's Match:\n{m['home']} 🆚 {m['away']}\n📅 {m['date']}  ⏰ {m['kickoff']}\n🏟️ {m['venue']}\n🏆 {m['stage']}"
    if upcoming:
        txt += "\n\n📅 Coming Up:"
        for u in upcoming[:2]:
            txt += f"\n  {u['home']} vs {u['away']} — {u['date']} {u['kickoff']} ({u['stage']})"
    return {"en": txt, "es": txt, "fr": txt}.get(lang, txt)


def _weather(lang):
    wx = get_weather()
    return {
        "en": f"🌤️ Current Conditions:\n• Temperature: {wx['temp_c']}°C\n• Condition: {wx['condition']}\n• Humidity: {wx['humidity']}%\n\n💧 {wx['advice']}",
        "es": f"🌤️ Condiciones actuales:\n• Temperatura: {wx['temp_c']}°C\n• Condición: {wx['condition']}\n• Humedad: {wx['humidity']}%\n\n💧 {wx['advice']}",
        "fr": f"🌤️ Conditions actuelles:\n• Température: {wx['temp_c']}°C\n• Condition: {wx['condition']}\n• Humidité: {wx['humidity']}%\n\n💧 {wx['advice']}",
    }.get(lang, "en")


def _sustainability(lang):
    return {
        "en": "🌱 Sustainability:\n• 💧 Free water refill stations: Level 1 & Level 2\n• ♻️ Recycling bins throughout all concourses\n• 🧴 Reusable bottles encouraged (must be empty at entry)\n• 🥤 Avoid single-use plastics — FIFA Green Stadium initiative",
        "es": "🌱 Sostenibilidad:\n• 💧 Agua gratuita: Nivel 1 y 2\n• ♻️ Contenedores de reciclaje en toda la concesión\n• 🧴 Se recomienda botella reutilizable",
        "fr": "🌱 Durabilité:\n• 💧 Recharge d'eau gratuite: Niveaux 1 et 2\n• ♻️ Poubelles de tri dans toutes les concessions\n• 🧴 Bouteilles réutilisables encouragées",
    }.get(lang, "en")


def _family(lang):
    return {
        "en": "👨‍👩‍👧 Family Assistance:\n• Family Help Desk: Gate D (dedicated staff)\n• Family Seating: Block 401 – East Family Section ♿\n• Baby changing: Gate D, Level 1 restrooms\n• Strollers: Permitted (use Gate D for easiest access)\n• Lost child: Go to Family Help Desk at Gate D immediately\n• Quiet Room: Level 1 West (sensory-friendly for children with autism)",
        "es": "👨‍👩‍👧 Asistencia Familiar:\n• Mesa de ayuda: Puerta D\n• Asientos familiares: Bloque 401 ♿\n• Cambiador: Puerta D, Nivel 1\n• Sala tranquila: Nivel 1 Oeste\n• Niño perdido: Puerta D inmediatamente",
        "fr": "👨‍👩‍👧 Assistance Famille:\n• Bureau Familles: Porte D\n• Sièges familles: Bloc 401 ♿\n• Table à langer: Porte D, Niveau 1\n• Salle calme: Niveau 1 Ouest\n• Enfant perdu: Porte D immédiatement",
    }.get(lang, "en")


def _volunteer(lang):
    return {
        "en": "🙋 Volunteer Guidance:\n\n👤 Disabled visitor: Escort to Gate A/D, use accessible lane, assist to Block 101/401. Offer priority queue.\n👑 VIP guest: Direct to Gate C. Premium lounge on Level 3. Dedicated parking near Gate C.\n🗺️ Lost visitor: Take to Volunteer Hub at Gate D or nearest info point.\n👶 Family with young children: Direct to Gate D, Family Help Desk.\n🚑 Medical situation: Call +974-911, alert First Aid at Gate B.\n\nVolunteer Hub: Gate D — report there every 2 hours.",
        "es": "🙋 Guía para Voluntarios:\n\nVisitante discapacitado: Puerta A/D, carril accesible → Bloque 101/401\nHuésped VIP: Puerta C → Sala Premium Nivel 3\nPerdido: Hub Voluntarios Puerta D\nFamilia: Puerta D → Mesa Familiar\nEmergencia médica: +974-911, Puerta B",
        "fr": "🙋 Guide Bénévoles:\n\nVisiteur handicapé: Porte A/D, voie accessible → Bloc 101/401\nHôte VIP: Porte C → Salon Premium Niveau 3\nPerdu: Hub Bénévoles Porte D\nFamille: Porte D → Bureau Familles\nUrgence médicale: +974-911, Porte B",
    }.get(lang, "en")


def _wifi(lang):
    return {
        "en": "📶 Wi-Fi:\n• Network: StadiumSense_Guest\n• Password: None required\n• Coverage: All areas\n\nNote: Speed may reduce during match time due to high traffic.",
        "es": "📶 Wi-Fi:\n• Red: StadiumSense_Guest\n• Sin contraseña\n• Cobertura: Todas las áreas",
        "fr": "📶 Wi-Fi:\n• Réseau: StadiumSense_Guest\n• Sans mot de passe\n• Couverture: Toutes les zones",
    }.get(lang, "en")


def _prohibited(lang):
    return {
        "en": "🚫 Prohibited Items:\n• Outside food or beverages\n• Bags > 30×20×15 cm\n• Umbrellas\n• Professional cameras / video equipment\n• Drones\n• Flares / fireworks\n• Weapons of any kind\n\n✅ Allowed: Small bags, personal items, empty reusable bottles, phone.",
        "es": "🚫 Artículos prohibidos:\n• Comida/bebida exterior\n• Bolsas > 30×20×15 cm\n• Paraguas · Cámaras profesionales\n• Drones · Bengalas · Armas",
        "fr": "🚫 Articles interdits:\n• Nourriture/boissons extérieures\n• Sacs > 30×20×15 cm\n• Parapluies · Caméras pro\n• Drones · Fusées · Armes",
    }.get(lang, "en")


def _reentry(lang):
    return {
        "en": "🔄 Re-Entry Policy:\nPermitted with a valid match ticket. Ticket will be re-scanned.\n⚠️ Not allowed: last 15 minutes of play or at half-time in certain zones.",
        "es": "🔄 Reentrada:\nPermitida con boleto válido. No en últimos 15 min ni medio tiempo.",
        "fr": "🔄 Ré-entrée:\nPermise avec billet valide. Interdite 15 dernières min et mi-temps.",
    }.get(lang, "en")


def _prayer(lang):
    return {
        "en": "🕌 Prayer Room:\n• Location: Level 1 West, near Gate A\n• Open throughout the match day\n• Prayer mats provided\n• Direction of Qibla marked inside",
        "es": "🕌 Sala de oración:\n• Ubicación: Nivel 1 Oeste, cerca Puerta A\n• Abierta todo el día del partido",
        "fr": "🕌 Salle de prière:\n• Lieu: Niveau 1 Ouest, près Porte A\n• Ouverte toute la journée du match",
    }.get(lang, "en")


FALLBACK = {
    "en": "I can help with:\n🚪 Gates  💺 Seating  🍔 Food & Queues  🚻 Restrooms\n🅿️ Parking  🚇 Metro & Transport  🏥 Medical  🚨 Emergency\n♿ Accessibility  📦 Lost & Found  ⚽ Match Info  🌤️ Weather\n🛍️ Merchandise  📶 Wi-Fi  🌱 Sustainability  👨‍👩‍👧 Families\n\nTry: \"Which gate is least crowded?\" or \"How long is the food queue?\"",
    "es": "Puedo ayudarte con:\n🚪 Puertas  💺 Asientos  🍔 Comida  🅿️ Estacionamiento\n🚇 Transporte  🏥 Médico  🚨 Emergencias  ♿ Accesibilidad\n\nIntenta: \"¿Qué puerta está menos concurrida?\"",
    "fr": "Je peux vous aider avec:\n🚪 Portes  💺 Sièges  🍔 Nourriture  🅿️ Parking\n🚇 Transport  🏥 Médical  🚨 Urgences  ♿ Accessibilité\n\nEssayez: \"Quelle porte est la moins fréquentée?\"",
}


# ── Main response function ────────────────────────────────────────────────────
def detect_intent(message: str):
    msg = message.lower()
    best, score = None, 0
    for intent in INTENTS:
        s = sum(1 for kw in intent["keywords"] if kw in msg)
        if s > score:
            score, best = s, intent
    return best if score > 0 else None


def get_response(message: str, language: str = "en") -> str:
    lang    = language if language in ("en", "es", "fr") else "en"
    intent  = detect_intent(message)

    if intent:
        result = intent["handler"](lang)
        if isinstance(result, dict):
            return result.get(lang, result.get("en", ""))
        return result

    # FAQ fallback
    msg   = message.lower()
    words = [w for w in msg.split() if len(w) > 2]
    for faq in FAQS:
        if any(w in faq["question"].lower() or w in faq["answer"].lower() for w in words):
            prefix = {"es": "ℹ️ ", "fr": "ℹ️ "}.get(lang, "ℹ️ ")
            return prefix + faq["answer"]

    return FALLBACK.get(lang, FALLBACK["en"])
