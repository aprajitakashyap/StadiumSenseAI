import { useState, useCallback } from 'react'
import { sendChat } from '../utils/api'

export function useChat(language) {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      role: 'assistant',
      text: "👋 Welcome to StadiumSense AI! I'm here to help you navigate the FIFA World Cup stadium. Ask me about gates, seats, food, restrooms, accessible routes, and more!",
      timestamp: new Date(),
    }
  ])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const sendMessage = useCallback(async (text) => {
    if (!text.trim()) return

    const userMsg = {
      id: `user-${Date.now()}`,
      role: 'user',
      text: text.trim(),
      timestamp: new Date(),
    }

    setMessages(prev => [...prev, userMsg])
    setLoading(true)
    setError(null)

    try {
      const data = await sendChat(text.trim(), language)
      const aiMsg = {
        id: `ai-${Date.now()}`,
        role: 'assistant',
        text: data.response,
        timestamp: new Date(),
      }
      setMessages(prev => [...prev, aiMsg])
    } catch (err) {
      setError('Failed to get a response. Please try again.')
      console.error(err)
    } finally {
      setLoading(false)
    }
  }, [language])

  return { messages, loading, error, sendMessage }
}
