import { useState, useRef, useEffect } from 'react'
import { Mic, Square, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'
import { useAppStore } from '../stores/appStore'
import api from '../services/api'

export default function AudioRecorder() {
  const {
    isRecording,
    isProcessing,
    setRecording,
    setProcessing,
    setResults,
    selectedModel,
    targetLang,
    selectedVoice
  } = useAppStore()
  
  const [audioLevel, setAudioLevel] = useState(0)
  const mediaRecorderRef = useRef(null)
  const audioChunksRef = useRef([])
  const analyserRef = useRef(null)
  const animationFrameRef = useRef(null)
  const silenceTimerRef = useRef(null)
  const lastSoundTimeRef = useRef(Date.now())
  
  // Auto-stop settings
  const SILENCE_THRESHOLD = 20 // Audio level below this is considered silence (0-100 scale)
  const SILENCE_DURATION = 2000 // 2 seconds of silence before auto-stop
  
  useEffect(() => {
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current)
      }
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop()
      }
    }
  }, [])
  
  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      
      // Set up audio analysis
      const audioContext = new AudioContext()
      const source = audioContext.createMediaStreamSource(stream)
      const analyser = audioContext.createAnalyser()
      analyser.fftSize = 256
      source.connect(analyser)
      analyserRef.current = analyser
      
      // Start level monitoring
      monitorAudioLevel()
      
      // Set up recorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      })
      
      // Clear previous recording
      audioChunksRef.current = []
      
      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunksRef.current.push(event.data)
        }
      }
      
      mediaRecorder.onstop = async () => {
        // Stop all tracks
        stream.getTracks().forEach(track => track.stop())
        
        // Stop audio monitoring
        if (animationFrameRef.current) {
          cancelAnimationFrame(animationFrameRef.current)
        }
        
        setAudioLevel(0)
        await processRecording()
      }
      
      mediaRecorder.start()
      mediaRecorderRef.current = mediaRecorder
      setRecording(true)
      
      // Reset silence detection
      lastSoundTimeRef.current = Date.now()
      silenceTimerRef.current = null
      
      toast.success('🎤 Recording... Will auto-stop after 2s of silence')
    } catch (error) {
      console.error('Failed to start recording:', error)
      toast.error('Failed to access microphone')
    }
  }
  
  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop()
      setRecording(false)
    }
    
    // Clear silence timer
    if (silenceTimerRef.current) {
      clearTimeout(silenceTimerRef.current)
      silenceTimerRef.current = null
    }
    
    // Stop audio monitoring
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current)
      animationFrameRef.current = null
    }
    
    // Reset audio level
    setAudioLevel(0)
    analyserRef.current = null
  }
  
  const monitorAudioLevel = () => {
    if (!analyserRef.current || !isRecording) return
    
    const dataArray = new Uint8Array(analyserRef.current.frequencyBinCount)
    analyserRef.current.getByteFrequencyData(dataArray)
    
    const average = dataArray.reduce((a, b) => a + b) / dataArray.length
    const level = Math.min(100, (average / 128) * 100)
    setAudioLevel(level)
    
    // Silence detection for auto-stop
    if (level > SILENCE_THRESHOLD) {
      // Sound detected - reset silence start time
      lastSoundTimeRef.current = Date.now()
      if (silenceTimerRef.current) {
        clearTimeout(silenceTimerRef.current)
        silenceTimerRef.current = null
      }
    } else {
      // Silence detected - check duration
      const silenceDuration = Date.now() - lastSoundTimeRef.current
      
      // If we've been silent for 2 seconds and no timer is set yet, auto-stop
      if (silenceDuration >= SILENCE_DURATION && !silenceTimerRef.current && isRecording) {
        toast.info('🔇 Auto-stopping after silence...')
        stopRecording()
        return // Don't schedule more animation frames
      }
    }
    
    // Continue monitoring
    animationFrameRef.current = requestAnimationFrame(monitorAudioLevel)
  }
  
  const processRecording = async () => {
    if (audioChunksRef.current.length === 0) {
      toast.error('No audio recorded')
      return
    }
    
    setProcessing(true)
    const loadingToast = toast.loading('Processing audio...')
    
    try {
      const audioBlob = new Blob(audioChunksRef.current, { type: 'audio/webm' })
      const formData = new FormData()
      formData.append('file', audioBlob, 'recording.webm')
      formData.append('target_lang', targetLang)
      if (selectedModel) formData.append('model', selectedModel)
      if (selectedVoice) formData.append('voice', selectedVoice)
      
      const response = await api.post('/api/full-pipeline', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        responseType: 'blob'
      })
      
      // Extract metadata from headers (decode URL-encoded text)
      const originalText = decodeURIComponent(response.headers['x-original-text'] || '')
      const translatedText = decodeURIComponent(response.headers['x-translated-text'] || '')
      const detectedLanguage = response.headers['x-source-lang'] || ''
      const ttsStatus = response.headers['x-tts-status'] || 'ok'
      
      // Create audio URL
      const audioUrl = URL.createObjectURL(response.data)
      
      setResults({
        originalText,
        translatedText,
        detectedLanguage,
        audioUrl
      })
      
      // Show appropriate notification
      if (ttsStatus === 'failed') {
        toast.success('✅ Translation complete! (Audio unavailable - TTS service issue)', { 
          id: loadingToast,
          duration: 5000
        })
      } else {
        toast.success('✅ Translation complete!', { id: loadingToast })
        
        // Auto-play audio only if TTS succeeded
        const audio = new Audio(audioUrl)
        audio.play().catch(err => console.error('Audio playback error:', err))
      }
      
    } catch (error) {
      console.error('Processing failed:', error)
      toast.error('Failed to process audio', { id: loadingToast })
    } finally {
      setProcessing(false)
    }
  }
  
  return (
    <div className="glass rounded-2xl p-8 shadow-xl">
      <div className="flex flex-col items-center space-y-6">
        <div className="relative">
          <button
            onClick={isRecording ? stopRecording : startRecording}
            disabled={isProcessing}
            className={`
              w-32 h-32 rounded-full flex items-center justify-center
              transition-all duration-300 shadow-lg
              ${isRecording 
                ? 'bg-red-500 hover:bg-red-600 recording-active' 
                : 'bg-primary-500 hover:bg-primary-600'
              }
              ${isProcessing ? 'opacity-50 cursor-not-allowed' : ''}
              disabled:opacity-50 disabled:cursor-not-allowed
            `}
          >
            {isProcessing ? (
              <Loader2 className="w-12 h-12 text-white animate-spin" />
            ) : isRecording ? (
              <Square className="w-12 h-12 text-white fill-white" />
            ) : (
              <Mic className="w-12 h-12 text-white" />
            )}
          </button>
          
          {isRecording && (
            <div 
              className="absolute -bottom-4 left-0 right-0 h-1 bg-gray-200 rounded-full overflow-hidden"
            >
              <div 
                className="h-full bg-gradient-to-r from-green-500 to-blue-500 transition-all duration-100"
                style={{ width: `${audioLevel}%` }}
              />
            </div>
          )}
        </div>
        
        <div className="text-center">
          <h3 className="text-2xl font-bold text-gray-800">
            {isProcessing 
              ? 'Processing...' 
              : isRecording 
                ? 'Recording...' 
                : 'Ready to Record'
            }
          </h3>
          <p className="text-gray-600 mt-2">
            {isProcessing 
              ? 'Transcribing, translating, and synthesizing speech' 
              : isRecording 
                ? '🔴 Recording... Click ■ to STOP (or wait 2s silence)' 
                : 'Click the microphone to start recording'
            }
          </p>
          {isRecording && (
            <p className="text-sm text-blue-600 mt-1">
              Auto-stops after 2 seconds of silence
            </p>
          )}
        </div>
      </div>
    </div>
  )
}
