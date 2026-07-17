// Base URL: use VITE_BACKEND_URL at build time (Cloud Run), fallback to /api proxy for local dev
const BASE_URL = import.meta.env.VITE_BACKEND_URL || ''

export async function sendChat(message, language = 'en') {
  const res = await fetch(`${BASE_URL}/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, language }),
  })
  if (!res.ok) throw new Error(`Chat API error: ${res.status}`)
  return res.json()
}

export async function fetchFaqs() {
  const res = await fetch(`${BASE_URL}/faq`)
  if (!res.ok) throw new Error(`FAQ API error: ${res.status}`)
  return res.json()
}

export async function fetchLocations() {
  const res = await fetch(`${BASE_URL}/locations`)
  if (!res.ok) throw new Error(`Locations API error: ${res.status}`)
  return res.json()
}

export async function fetchRoutes() {
  const res = await fetch(`${BASE_URL}/routes`)
  if (!res.ok) throw new Error(`Routes API error: ${res.status}`)
  return res.json()
}
