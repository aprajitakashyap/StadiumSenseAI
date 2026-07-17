import React from 'react'

export default function TypingIndicator() {
  return (
    <div className="flex items-end gap-2 animate-fade-in" role="status" aria-label="StadiumSense AI is typing">
      <div className="w-8 h-8 rounded-full bg-navy-600 border border-accent-500/30 flex items-center justify-center text-sm">
        ⚽
      </div>
      <div className="bg-navy-700 border border-navy-600 rounded-2xl rounded-bl-sm px-4 py-3">
        <div className="flex items-center gap-1.5" aria-hidden="true">
          {[0, 1, 2].map(i => (
            <span
              key={i}
              className="w-2 h-2 bg-accent-500 rounded-full inline-block"
              style={{
                animation: 'pulseDot 1.4s infinite',
                animationDelay: `${i * 0.2}s`
              }}
            />
          ))}
        </div>
      </div>
    </div>
  )
}
