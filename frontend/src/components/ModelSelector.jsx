import { Cpu } from 'lucide-react'
import { useAppStore } from '../stores/appStore'

export default function ModelSelector() {
  const { models, selectedModel, setModel, voices, selectedVoice, setVoice } = useAppStore()
  
  const getModelDisplayName = (name) => {
    // Extract model name and size
    const parts = name.split(':')
    return parts[0] || name
  }
  
  const getModelSize = (name) => {
    const match = name.match(/(\d+\.?\d*[bmBM])/i)
    return match ? match[0].toUpperCase() : ''
  }
  
  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2 flex items-center">
          <Cpu className="w-4 h-4 mr-2" />
          Translation Model
        </label>
        <select
          value={selectedModel || ''}
          onChange={(e) => setModel(e.target.value)}
          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          disabled={models.length === 0}
        >
          {models.length === 0 ? (
            <option>No models available</option>
          ) : (
            models.map((model) => (
              <option key={model.name} value={model.name}>
                {getModelDisplayName(model.name)} {getModelSize(model.name)}
              </option>
            ))
          )}
        </select>
        <p className="mt-2 text-xs text-gray-500">
          {models.length} model(s) available
        </p>
      </div>
      
      <div>
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Voice
        </label>
        <select
          value={selectedVoice || ''}
          onChange={(e) => setVoice(e.target.value)}
          className="w-full px-4 py-3 bg-white border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
          disabled={voices.length === 0}
        >
          {voices.length === 0 ? (
            <option>Auto-select</option>
          ) : (
            voices.map((voice) => (
              <option key={voice.name} value={voice.name}>
                {voice.full_name || voice.name}
              </option>
            ))
          )}
        </select>
      </div>
    </div>
  )
}
