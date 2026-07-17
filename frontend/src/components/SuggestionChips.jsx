import React from 'react'

export default function SuggestionChips({ faqs, onSelect, language }) {
  if (!faqs || faqs.length === 0) return null

  // Show first 4 FAQs as chips
  const chips = faqs.slice(0, 4)

  const label = {
    en: 'Quick questions:',
    es: 'Preguntas rápidas:',
    fr: 'Questions rapides:',
  }[language] || 'Quick questions:'

  return (
    <div className="px-4 pb-3">
      <p className="text-xs text-gray-500 mb-2">{label}</p>
      <div className="flex flex-wrap gap-2">
        {chips.map(faq => (
          <button
            key={faq.id}
            onClick={() => onSelect(faq.question)}
            className="
              text-xs px-3 py-2 rounded-full border border-accent-500/40 text-accent-400
              hover:bg-accent-500/10 hover:border-accent-500 transition-all duration-200
              text-left max-w-[200px] truncate
            "
            title={faq.question}
          >
            {faq.question}
          </button>
        ))}
      </div>
    </div>
  )
}
