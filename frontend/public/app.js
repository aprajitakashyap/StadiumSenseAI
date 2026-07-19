/* StadiumSenseAI — Frontend App */

// Backend URL — set VITE_API_URL at Vercel or falls back to Render URL
const API = (window.__API_URL__ || 'https://stadiumsenseai.onrender.com').replace(/\/$/, '');

// Splash
window.addEventListener('load', () => {
  const s = document.getElementById('splash');
  if (s) { s.classList.add('hide'); setTimeout(() => s.remove(), 700); }
});

// DOM
const chatEl = document.getElementById('chat');
const chipsEl = document.getElementById('chips');
const inp = document.getElementById('inp');
const sendBtn = document.getElementById('send');
const statusBar = document.getElementById('status-bar');

// State
let lang = 'en', busy = false, chipsOn = true;
let sessionCtx = [];

// i18n
const PH = {
  en: 'Ask about crowds, queues, routes, emergencies…',
  es: 'Pregunta sobre afluencia, colas, rutas, emergencias…',
  fr: 'Questions sur la foule, files d\'attente, itinéraires…',
};
const CHIP_LBL = { en: 'Suggested:', es: 'Sugerencias:', fr: 'Suggestions:' };
const ERR_MSG  = {
  en: '⚠️ Connection issue. The server may be waking up — please try again in 15 seconds.',
  es: '⚠️ Error de conexión. El servidor puede estar iniciando — intenta en 15 segundos.',
  fr: '⚠️ Problème de connexion. Le serveur démarre peut-être — réessayez dans 15 secondes.',
};
const WELCOME = {
  en: `Welcome to StadiumSenseAI! 🏟️✨

I'm your AI-powered guide for FIFA World Cup 2026, built with Google Gemini.

I can help you with:
📊 Live crowd & queue status
🗺️ Smart route recommendations
♿ Accessibility & wheelchair routes
🚇 Metro, bus & transport info
🏥 Medical & emergency help
⚽ Match schedule & info
🌤️ Weather & stadium tips
👨‍👩‍👧 Family & child assistance
🙋 Volunteer guidance

Tap a quick action or ask me anything!`,
  es: `¡Bienvenido a StadiumSenseAI! 🏟️✨

Soy tu guía IA para la Copa del Mundo FIFA 2026, impulsado por Google Gemini.

Puedo ayudarte con afluencia en tiempo real, rutas accesibles, transporte, emergencias y mucho más.

¡Toca una acción rápida o pregúntame lo que necesites!`,
  fr: `Bienvenue sur StadiumSenseAI! 🏟️✨

Je suis votre guide IA pour la Coupe du Monde FIFA 2026, propulsé par Google Gemini.

Je peux vous aider avec l'affluence en direct, les itinéraires accessibles, les transports, les urgences et bien plus.

Appuyez sur une action rapide ou posez votre question!`,
};

// Quick action cards
const ACTIONS = [
  { ic:'📊', en:'Crowd',      es:'Afluencia', fr:'Foule',
    q:{ en:'Which gate is least crowded right now?', es:'¿Qué puerta está menos concurrida ahora?', fr:'Quelle porte est la moins fréquentée?' }},
  { ic:'⏱️', en:'Queues',     es:'Colas',     fr:'Files',
    q:{ en:'What are the current food queue times?', es:'¿Cuánto tiempo de espera en comida?', fr:"Quels sont les temps d'attente actuels?" }},
  { ic:'🚇', en:'Metro',      es:'Metro',     fr:'Métro',
    q:{ en:'When is the next metro train?', es:'¿Cuándo es el próximo metro?', fr:'Quand est le prochain métro?' }},
  { ic:'♿', en:'Access',     es:'Acceso',    fr:'Accès',
    q:{ en:'I use a wheelchair. What is the best accessible route?', es:'Uso silla de ruedas. ¿Cuál es la mejor ruta accesible?', fr:"J'utilise un fauteuil roulant. Quel est le meilleur itinéraire accessible?" }},
  { ic:'🚨', en:'Emergency',  es:'Emergencia',fr:'Urgence',
    q:{ en:'There is a medical emergency — what do I do?', es:'Hay una emergencia médica — ¿qué hago?', fr:"Il y a une urgence médicale — que faire?" }},
  { ic:'⚽', en:'Match',      es:'Partido',   fr:'Match',
    q:{ en:"What is today's match and kickoff time?", es:'¿Cuál es el partido de hoy y a qué hora?', fr:"Quel est le match d'aujourd'hui et à quelle heure?" }},
  { ic:'🍔', en:'Food',       es:'Comida',    fr:'Nourriture',
    q:{ en:'Where is the shortest food queue right now?', es:'¿Dónde hay la cola de comida más corta ahora?', fr:"Où est la file d'attente la plus courte pour la nourriture?" }},
  { ic:'🅿️', en:'Parking',    es:'Parking',   fr:'Parking',
    q:{ en:'Which parking zone has the most space?', es:'¿Qué zona de estacionamiento tiene más espacio?', fr:'Quel parking a le plus de place?' }},
];

function renderActions() {
  const el = document.getElementById('actions');
  el.innerHTML = '';
  ACTIONS.forEach(a => {
    const btn = document.createElement('button');
    btn.className = 'ac';
    btn.innerHTML = `<span class="ic">${a.ic}</span>${a[lang] || a.en}`;
    btn.addEventListener('click', () => send(a.q[lang] || a.q.en));
    el.appendChild(btn);
  });
}

// Language
document.querySelectorAll('.lang-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    lang = btn.dataset.lang;
    document.querySelectorAll('.lang-btn').forEach(b => {
      b.classList.toggle('active', b === btn);
      b.setAttribute('aria-pressed', String(b === btn));
    });
    inp.placeholder = PH[lang];
    renderActions();
  });
});

inp.addEventListener('input', () => {
  inp.style.height = 'auto';
  inp.style.height = Math.min(inp.scrollHeight, 120) + 'px';
  sendBtn.disabled = !inp.value.trim() || busy;
});
inp.addEventListener('keydown', e => {
  if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); if (!sendBtn.disabled) send(); }
});
sendBtn.addEventListener('click', () => send());

// Chat
function ts() { return new Date().toLocaleTimeString([], { hour:'2-digit', minute:'2-digit' }); }

function addMsg(role, text) {
  const row = document.createElement('div'); row.className = `row ${role}`;
  const av  = document.createElement('div'); av.className  = `av ${role}`;
  av.textContent = role === 'user' ? '👤' : '⚽'; av.setAttribute('aria-hidden','true');
  const bub = document.createElement('div'); bub.className = `bub ${role}`;
  bub.textContent = text;
  const t = document.createElement('span'); t.className = 'ts'; t.textContent = ts();
  bub.appendChild(t); row.append(av, bub); chatEl.appendChild(row);
  chatEl.scrollTop = chatEl.scrollHeight;
}

function showTyping() {
  const row = document.createElement('div'); row.className = 'row ai'; row.id = 'typing';
  const av  = document.createElement('div'); av.className  = 'av ai'; av.textContent = '⚽'; av.setAttribute('aria-hidden','true');
  const bub = document.createElement('div'); bub.className = 'bub ai';
  bub.innerHTML = '<div class="typing"><span></span><span></span><span></span></div>';
  row.append(av, bub); chatEl.appendChild(row); chatEl.scrollTop = chatEl.scrollHeight;
}
function hideTyping() { document.getElementById('typing')?.remove(); }
function showErr(m)   {
  const d = document.createElement('div'); d.className = 'err'; d.setAttribute('role','alert'); d.textContent = m;
  chatEl.appendChild(d); chatEl.scrollTop = chatEl.scrollHeight; setTimeout(() => d.remove(), 8000);
}

async function send(prefill) {
  const msg = typeof prefill === 'string' ? prefill : inp.value.trim();
  if (!msg || busy) return;
  if (chipsOn) { chipsEl.innerHTML = ''; chipsOn = false; }
  addMsg('user', msg);
  inp.value = ''; inp.style.height = 'auto'; sendBtn.disabled = true;
  busy = true; showTyping();
  sessionCtx.push({ role: 'user', text: msg });
  if (sessionCtx.length > 8) sessionCtx = sessionCtx.slice(-8);
  try {
    const res  = await fetch(`${API}/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: msg, language: lang, context: sessionCtx }),
    });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const { response } = await res.json();
    hideTyping(); addMsg('ai', response);
    sessionCtx.push({ role: 'assistant', text: response });
  } catch {
    hideTyping(); showErr(ERR_MSG[lang]);
  } finally {
    busy = false; sendBtn.disabled = !inp.value.trim();
  }
}

// Live status bar
async function loadStatus() {
  try {
    const d = await fetch(`${API}/live/all`).then(r => r.json());
    const quietest = Object.entries(d.crowd).sort((a,b) => a[1].pct - b[1].pct)[0];
    const shortestQ = Object.entries(d.queues).sort((a,b) => a[1].wait_mins - b[1].wait_mins)[0];
    statusBar.innerHTML = '';
    [
      { ic:'🟢', txt: `${quietest[0].split('–')[0].trim()}: ${quietest[1].level.split(' ')[0]}` },
      { ic:'⏱️', txt: `Shortest queue: ~${shortestQ[1].wait_mins}min` },
      { ic:'🚇', txt: `Metro: ${d.metro.next_train_mins}min` },
      { ic:'🌤️', txt: `${d.weather.temp_c}°C · ${d.weather.condition}` },
    ].forEach(c => {
      const el = document.createElement('div'); el.className = 'stat-chip';
      el.innerHTML = `${c.ic} <strong>${c.txt}</strong>`; statusBar.appendChild(el);
    });
  } catch { /* skip */ }
}

// FAQ chips
async function loadChips() {
  try {
    const faqs = await fetch(`${API}/faq`).then(r => r.json());
    if (!faqs.length) return;
    const lbl = document.createElement('div'); lbl.id='chips-label'; lbl.setAttribute('aria-hidden','true');
    lbl.textContent = CHIP_LBL[lang]; chipsEl.appendChild(lbl);
    faqs.slice(0,4).forEach(f => {
      const b = document.createElement('button'); b.className='chip';
      b.textContent = f.question; b.title = f.question;
      b.addEventListener('click', () => send(f.question)); chipsEl.appendChild(b);
    });
  } catch { /* skip */ }
}

// Init
renderActions();
addMsg('ai', WELCOME[lang] || WELCOME.en);
loadStatus();
loadChips();
setInterval(loadStatus, 45000);
