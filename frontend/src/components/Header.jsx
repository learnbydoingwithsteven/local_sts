import { Mic, Globe, Volume2 } from 'lucide-react'

export default function Header() {
  return (
    <header className="glass border-b border-white/20">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2">
              <Mic className="w-8 h-8 text-primary-600" />
              <h1 className="text-3xl font-bold bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
                Speech Translation
              </h1>
            </div>
          </div>
          
          <div className="hidden md:flex items-center space-x-6 text-sm text-gray-600">
            <div className="flex items-center space-x-2">
              <Mic className="w-4 h-4" />
              <span>Whisper STT</span>
            </div>
            <div className="flex items-center space-x-2">
              <Globe className="w-4 h-4" />
              <span>Ollama</span>
            </div>
            <div className="flex items-center space-x-2">
              <Volume2 className="w-4 h-4" />
              <span>Edge TTS</span>
            </div>
          </div>
        </div>
        
        <p className="mt-2 text-gray-600 text-sm">
          Real-time speech-to-text translation with natural voice output
        </p>
      </div>
    </header>
  )
}
