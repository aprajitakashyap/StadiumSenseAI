import React from 'react'

const LANGUAGES = [
  { code: 'en', label: 'EN', full: 'English' },
  { code: 'es', label: 'ES', full: 'Español' },
  { code: 'fr', label: 'FR', full: 'Français' },
]

export default function LanguageSelector({ language, onChange }) {
  return (
    <div className="flex items-center gap-1 bg-navy-800 rounded-lg p-1" role="group" aria-label="Select language">
      {LANGUAGES.map(lang => (
        <button
          key={lang.code}
          onClick={() => onChange(lang.code)}
          title={lang.full}
          aria-pressed={language === lang.code}
          className={`
            px-3 py-1.5 rounded-md text-xs font-semibold transition-all duration-200
            ${language === lang.code
              ? 'bg-accent-500 text-navy-900 shadow-lg shadow-accent-500/20'
              : 'text-gray-400 hover:text-white hover:bg-navy-600'
            }
          `}
        >
          {lang.label}
        </button>
      ))}
    </div>
  )
}
