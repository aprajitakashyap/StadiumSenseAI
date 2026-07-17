import React, { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'
import TypingIndicator from './TypingIndicator'

export default function ChatWindow({ messages, loading, error }) {
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  return (
    <div
      className="flex-1 overflow-y-auto px-4 py-4 space-y-4 scrollbar-hide"
      role="list"
      aria-label="Chat messages"
      aria-live="polite"
      aria-atomic="false"
    >
      {messages.map(msg => (
        <MessageBubble key={msg.id} message={msg} />
      ))}

      {loading && <TypingIndicator />}

      {error && (
        <div
          className="text-center text-xs text-red-400 bg-red-900/20 border border-red-800/40 rounded-lg px-4 py-2 mx-4 animate-fade-in"
          role="alert"
        >
          {error}
        </div>
      )}

      <div ref={bottomRef} />
    </div>
  )
}
