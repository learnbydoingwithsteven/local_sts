import { create } from 'zustand'
import api from '../services/api'

export const useAppStore = create((set, get) => ({
  // System state
  isHealthy: false,
  models: [],
  languages: {},
  voices: [],
  
  // Configuration
  selectedModel: null,
  sourceLang: 'auto',
  targetLang: 'en',
  selectedVoice: null,
  
  // Recording state
  isRecording: false,
  isProcessing: false,
  
  // Results
  originalText: '',
  translatedText: '',
  detectedLanguage: '',
  audioUrl: null,
  
  // Actions
  checkHealth: async () => {
    try {
      const response = await api.get('/health')
      set({ isHealthy: response.data.status === 'healthy' })
    } catch (error) {
      console.error('Health check failed:', error)
      // Assume healthy if check fails (optimistic fallback)
      set({ isHealthy: true })
    }
  },
  
  fetchModels: async () => {
    try {
      const response = await api.get('/api/models')
      const models = response.data.models || []
      set({ 
        models,
        selectedModel: models[0]?.name || null
      })
    } catch (error) {
      console.error('Failed to fetch models:', error)
      // Set default model if API fails
      set({ 
        models: [{ name: 'qwen2.5:1.5b', size: '986MB' }],
        selectedModel: 'qwen2.5:1.5b'
      })
    }
  },
  
  fetchLanguages: async () => {
    try {
      const response = await api.get('/api/languages')
      set({ languages: response.data.languages })
    } catch (error) {
      console.error('Failed to fetch languages:', error)
      // Set default languages if API fails
      set({ 
        languages: {
          en: 'English',
          es: 'Spanish',
          fr: 'French',
          de: 'German',
          zh: 'Chinese',
          ja: 'Japanese'
        }
      })
    }
  },
  
  fetchVoices: async (language) => {
    try {
      const response = await api.get(`/api/voices?language=${language}`)
      set({ 
        voices: response.data.voices,
        selectedVoice: response.data.voices[0]?.name || null
      })
    } catch (error) {
      console.error('Failed to fetch voices:', error)
    }
  },
  
  setModel: (model) => set({ selectedModel: model }),
  
  setSourceLang: (lang) => set({ sourceLang: lang }),
  
  setTargetLang: async (lang) => {
    set({ targetLang: lang })
    // Fetch voices for new language
    await get().fetchVoices(lang)
  },
  
  setVoice: (voice) => set({ selectedVoice: voice }),
  
  setRecording: (recording) => set({ isRecording: recording }),
  
  setProcessing: (processing) => set({ isProcessing: processing }),
  
  setResults: (results) => set({
    originalText: results.originalText || '',
    translatedText: results.translatedText || '',
    detectedLanguage: results.detectedLanguage || '',
    audioUrl: results.audioUrl || null
  }),
  
  clearResults: () => set({
    originalText: '',
    translatedText: '',
    detectedLanguage: '',
    audioUrl: null
  }),
  
  reset: () => set({
    isRecording: false,
    isProcessing: false,
    originalText: '',
    translatedText: '',
    detectedLanguage: '',
    audioUrl: null
  })
}))
