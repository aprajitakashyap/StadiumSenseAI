import React, { useState, useEffect } from 'react'
import LanguageSelector from './components/LanguageSelector'
import ChatWindow from './components/ChatWindow'
import ChatInput from './components/ChatInput'
import SuggestionChips from './components/SuggestionChips'
import { useChat } from './hooks/useChat'
import { fetchFaqs } from './utils/api'

export default function App() {
  const [language, setLanguage] = useState('en')
  const [faqs, setFaqs] = useState([])
  const [showChips, setShowChips] = useState(true)
  const { messages, loading, error, sendMessage } = useChat(language)

  useEffect(() => {
    fetchFaqs()
      .then(setFaqs)
      .catch(() => setFaqs([]))
  }, [])

  const handleSend = (text) => {
    setShowChips(false)
    sendMessage(text)
  }

  const handleChipSelect = (question) => {
    setShowChips(false)
    sendMessage(question)
  }

  return (
    <div className="flex flex-col h-screen bg-navy-900 max-w-2xl mx-auto shadow-2xl">
      {/* Header */}
      <header className="flex items-center justify-between px-4 py-3 bg-navy-800 border-b border-navy-600 shadow-lg">
        <div className="flex items-center gap-3">
          {/* Logo */}
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-accent-500 to-accent-600 flex items-center justify-center shadow-lg shadow-accent-500/30">
            <span className="text-xl" role="img" aria-label="stadium">🏟️</span>
          </div>
          <div>
            <h1 className="text-base font-bold text-white leading-tight">StadiumSense AI</h1>
            <p className="text-xs text-accent-500 font-medium">FIFA World Cup Assistant</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {/* Online indicator */}
          <div className="hidden sm:flex items-center gap-1.5">
            <span className="w-2 h-2 bg-accent-500 rounded-full animate-pulse" aria-hidden="true" />
            <span className="text-xs text-gray-400">Online</span>
          </div>
          <LanguageSelector language={language} onChange={setLanguage} />
        </div>
      </header>

      {/* Chat area */}
      <ChatWindow messages={messages} loading={loading} error={error} />

      {/* Suggestion chips — shown once on load */}
      {showChips && faqs.length > 0 && (
        <SuggestionChips faqs={faqs} onSelect={handleChipSelect} language={language} />
      )}

      {/* Input */}
      <ChatInput onSend={handleSend} disabled={loading} language={language} />
    </div>
  )
}
