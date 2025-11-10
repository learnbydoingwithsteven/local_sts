import { useState, useEffect } from 'react'
import { Toaster } from 'react-hot-toast'
import Header from './components/Header'
import AudioRecorder from './components/AudioRecorder'
import LanguageSelector from './components/LanguageSelector'
import ModelSelector from './components/ModelSelector'
import TranscriptionDisplay from './components/TranscriptionDisplay'
import SystemStatus from './components/SystemStatus'
import { useAppStore } from './stores/appStore'
import './App.css'

function App() {
  const { fetchModels, fetchLanguages, checkHealth } = useAppStore()
  const [isInitialized, setIsInitialized] = useState(false)

  useEffect(() => {
    const initialize = async () => {
      try {
        // Set timeout for initialization (10 seconds)
        const timeoutPromise = new Promise((resolve) => 
          setTimeout(() => {
            console.warn('Initialization timeout - proceeding anyway')
            resolve()
          }, 10000)
        )
        
        // Race between initialization and timeout
        await Promise.race([
          Promise.all([
            checkHealth(),
            fetchModels(),
            fetchLanguages()
          ]),
          timeoutPromise
        ])
        
        setIsInitialized(true)
      } catch (error) {
        console.error('Initialization failed:', error)
        // Initialize anyway after error
        setIsInitialized(true)
      }
    }

    initialize()
  }, [])

  return (
    <div className="min-h-screen">
      <Toaster position="top-right" />
      
      <Header />

      <main className="container mx-auto px-4 py-8">
        {!isInitialized ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Left Column - Controls */}
            <div className="lg:col-span-1 space-y-6">
              <div className="glass rounded-2xl p-6 shadow-xl">
                <h2 className="text-xl font-bold mb-4 text-gray-800">
                  Configuration
                </h2>
                
                <LanguageSelector />
                
                <div className="mt-6">
                  <ModelSelector />
                </div>
              </div>

              <SystemStatus />
            </div>

            {/* Right Column - Main Interface */}
            <div className="lg:col-span-2 space-y-6">
              <AudioRecorder />
              
              <TranscriptionDisplay />
            </div>
          </div>
        )}
      </main>

      <footer className="container mx-auto px-4 py-8 text-center text-gray-600">
        <p>
          Powered by{' '}
          <a href="https://github.com/openai/whisper" className="text-primary-600 hover:underline">
            Whisper
          </a>
          {', '}
          <a href="https://ollama.ai" className="text-primary-600 hover:underline">
            Ollama
          </a>
          {', and '}
          <a href="https://github.com/rany2/edge-tts" className="text-primary-600 hover:underline">
            Edge TTS
          </a>
        </p>
      </footer>
    </div>
  )
}

export default App
