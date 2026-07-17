import React from 'react'

function formatTime(date) {
  return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

export default function MessageBubble({ message }) {
  const isUser = message.role === 'user'

  return (
    <div
      className={`flex items-end gap-2 animate-slide-up ${isUser ? 'flex-row-reverse' : 'flex-row'}`}
      role="listitem"
    >
      {/* Avatar */}
      <div className={`
        flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold
        ${isUser
          ? 'bg-accent-500 text-navy-900'
          : 'bg-navy-600 text-accent-500 border border-accent-500/30'
        }
      `}>
        {isUser ? 'Y' : '⚽'}
      </div>

      {/* Bubble */}
      <div className={`
        max-w-[75%] md:max-w-[65%] rounded-2xl px-4 py-3 shadow-lg
        ${isUser
          ? 'bg-accent-500 text-navy-900 rounded-br-sm'
          : 'bg-navy-700 text-gray-100 rounded-bl-sm border border-navy-600'
        }
      `}>
        <p className="text-sm leading-relaxed whitespace-pre-wrap break-words">{message.text}</p>
        <p className={`text-xs mt-1.5 ${isUser ? 'text-navy-600 text-right' : 'text-gray-500'}`}>
          {formatTime(message.timestamp)}
        </p>
      </div>
    </div>
  )
}
