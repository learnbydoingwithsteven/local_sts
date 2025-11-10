import { Activity, CheckCircle, XCircle } from 'lucide-react'
import { useAppStore } from '../stores/appStore'

export default function SystemStatus() {
  const { isHealthy } = useAppStore()
  
  return (
    <div className="glass rounded-2xl p-6 shadow-xl">
      <div className="flex items-center space-x-2 mb-4">
        <Activity className="w-5 h-5 text-gray-600" />
        <h3 className="font-semibold text-gray-800">System Status</h3>
      </div>
      
      <div className="space-y-3">
        <StatusItem
          label="Backend API"
          status={isHealthy}
        />
        <StatusItem
          label="STT Service"
          status={isHealthy}
        />
        <StatusItem
          label="Translation Service"
          status={isHealthy}
        />
        <StatusItem
          label="TTS Service"
          status={isHealthy}
        />
      </div>
      
      <div className="mt-4 pt-4 border-t border-gray-200">
        <p className="text-xs text-gray-500">
          Last check: {new Date().toLocaleTimeString()}
        </p>
      </div>
    </div>
  )
}

function StatusItem({ label, status }) {
  return (
    <div className="flex items-center justify-between">
      <span className="text-sm text-gray-600">{label}</span>
      <div className="flex items-center space-x-1">
        {status ? (
          <>
            <CheckCircle className="w-4 h-4 text-green-500" />
            <span className="text-xs text-green-600">Online</span>
          </>
        ) : (
          <>
            <XCircle className="w-4 h-4 text-red-500" />
            <span className="text-xs text-red-600">Offline</span>
          </>
        )}
      </div>
    </div>
  )
}
