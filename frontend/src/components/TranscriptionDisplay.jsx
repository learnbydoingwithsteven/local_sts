import { FileText, Languages, Volume2, Download } from 'lucide-react'
import { useAppStore } from '../stores/appStore'

export default function TranscriptionDisplay() {
  const { originalText, translatedText, detectedLanguage, audioUrl, languages } = useAppStore()
  
  const hasResults = originalText || translatedText
  
  const getLanguageName = (code) => {
    return languages[code] || code.toUpperCase()
  }
  
  const handleDownloadAudio = () => {
    if (audioUrl) {
      const a = document.createElement('a')
      a.href = audioUrl
      a.download = 'translation.mp3'
      a.click()
    }
  }
  
  const handlePlayAudio = () => {
    if (audioUrl) {
      const audio = new Audio(audioUrl)
      audio.play()
    }
  }
  
  if (!hasResults) {
    return (
      <div className="glass rounded-2xl p-8 shadow-xl">
        <div className="text-center text-gray-500">
          <FileText className="w-16 h-16 mx-auto mb-4 opacity-50" />
          <p className="text-lg">No transcription yet</p>
          <p className="text-sm mt-2">Record some audio to see results</p>
        </div>
      </div>
    )
  }
  
  return (
    <div className="space-y-4">
      {/* Original Text */}
      {originalText && (
        <div className="glass rounded-2xl p-6 shadow-xl">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <FileText className="w-5 h-5 text-gray-600" />
              <h3 className="font-semibold text-gray-800">Original Text</h3>
              {detectedLanguage && (
                <span className="px-2 py-1 bg-blue-100 text-blue-700 text-xs rounded-full">
                  {getLanguageName(detectedLanguage)}
                </span>
              )}
            </div>
          </div>
          <p className="text-gray-700 leading-relaxed">{originalText}</p>
        </div>
      )}
      
      {/* Translated Text */}
      {translatedText && (
        <div className="glass rounded-2xl p-6 shadow-xl border-2 border-primary-200">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center space-x-2">
              <Languages className="w-5 h-5 text-primary-600" />
              <h3 className="font-semibold text-gray-800">Translation</h3>
            </div>
            
            <div className="flex items-center space-x-2">
              {audioUrl && (
                <>
                  <button
                    onClick={handlePlayAudio}
                    className="flex items-center space-x-1 px-3 py-2 bg-primary-100 text-primary-700 rounded-lg hover:bg-primary-200 transition-colors"
                    title="Play audio"
                  >
                    <Volume2 className="w-4 h-4" />
                    <span className="text-sm">Play</span>
                  </button>
                  
                  <button
                    onClick={handleDownloadAudio}
                    className="flex items-center space-x-1 px-3 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors"
                    title="Download audio"
                  >
                    <Download className="w-4 h-4" />
                  </button>
                </>
              )}
            </div>
          </div>
          <p className="text-gray-700 leading-relaxed text-lg">{translatedText}</p>
        </div>
      )}
    </div>
  )
}
