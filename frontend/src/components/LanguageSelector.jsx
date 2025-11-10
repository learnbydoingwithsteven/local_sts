import { ArrowRight } from 'lucide-react'
import { useAppStore } from '../stores/appStore'

export default function LanguageSelector() {
  const { languages, sourceLang, targetLang, setSourceLang, setTargetLang } = useAppStore()
  
  const languageOptions = [
    { code: 'auto', name: 'Auto-detect' },
    ...Object.entries(languages).map(([code, name]) => ({ code, name }))
  ]
  
  const targetLanguages = Object.entries(languages).map(([code, name]) => ({ code, name }))
  
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Source Language
        </label>
        <select
          value={sourceLang}
          onChange={(e) => setSourceLang(e.target.value)}
          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          {languageOptions.map(({ code, name }) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>
      </div>
      
      <div className="flex justify-center">
        <ArrowRight className="w-6 h-6 text-gray-400" />
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Target Language
        </label>
        <select
          value={targetLang}
          onChange={(e) => setTargetLang(e.target.value)}
          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
        >
          {targetLanguages.map(({ code, name }) => (
            <option key={code} value={code}>
              {name}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
