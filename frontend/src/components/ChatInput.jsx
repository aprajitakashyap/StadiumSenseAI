import React, { useState, useRef } from 'react'

export default function ChatInput({ onSend, disabled, language }) {
  const [value, setValue] = useState('')
  const textareaRef = useRef(null)

  const placeholder = {
    en: 'Ask about gates, seats, food, accessible routes...',
    es: 'Pregunta sobre puertas, asientos, comida, rutas accesibles...',
    fr: 'Posez des questions sur les portes, sièges, nourriture, itinéraires...',
  }[language] || 'Ask about gates, seats, food, accessible routes...'

  const handleSubmit = (e) => {
    e.preventDefault()
    if (value.trim() && !disabled) {
      onSend(value)
      setValue('')
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleInput = (e) => {
    setValue(e.target.value)
    // Auto-resize textarea
    const ta = textareaRef.current
    if (ta) {
      ta.style.height = 'auto'
      ta.style.height = Math.min(ta.scrollHeight, 120) + 'px'
    }
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-end gap-2 p-4 border-t border-navy-600 bg-navy-800"
      aria-label="Send a message"
    >
      <textarea
        ref={textareaRef}
        value={value}
        onChange={handleInput}
        onKeyDown={handleKeyDown}
        placeholder={placeholder}
        disabled={disabled}
        rows={1}
        className="
          flex-1 bg-navy-700 text-white placeholder-gray-500 rounded-xl px-4 py-3
          border border-navy-600 focus:border-accent-500 focus:outline-none focus:ring-1
          focus:ring-accent-500/50 resize-none text-sm leading-relaxed
          disabled:opacity-50 transition-colors duration-200 min-h-[44px]
        "
        aria-label="Message input"
      />
      <button
        type="submit"
        disabled={disabled || !value.trim()}
        className="
          w-11 h-11 flex-shrink-0 bg-accent-500 hover:bg-accent-400 disabled:bg-navy-600
          disabled:text-gray-500 text-navy-900 rounded-xl flex items-center justify-center
          transition-all duration-200 shadow-lg shadow-accent-500/20 disabled:shadow-none
          focus:outline-none focus:ring-2 focus:ring-accent-500/50
        "
        aria-label="Send message"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" className="w-5 h-5">
          <path d="M3.478 2.405a.75.75 0 00-.926.94l2.432 7.905H13.5a.75.75 0 010 1.5H4.984l-2.432 7.905a.75.75 0 00.926.94 60.519 60.519 0 0018.445-8.986.75.75 0 000-1.218A60.517 60.517 0 003.478 2.405z" />
        </svg>
      </button>
    </form>
  )
}
