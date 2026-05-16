import { useState } from 'react'
import { Search, ShieldAlert } from 'lucide-react'
import './UrlAnalyzerInput.css'

export default function UrlAnalyzerInput({ onScan, isScanning }) {
  const [url, setUrl] = useState('')

  const handleSubmit = (e) => {
    e.preventDefault()
    if (url.trim()) onScan(url.trim())
  }

  return (
    <form onSubmit={handleSubmit} className="scan-input-wrapper">
      <div className="scan-input-glow" />
      <div className="scan-input-inner">
        <Search size={20} color="#475569" />
        <input
          type="text"
          className="scan-input-field"
          placeholder="Enter suspicious URL or domain to analyze..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={isScanning}
        />
        <button type="submit" className="scan-input-btn" disabled={isScanning || !url.trim()}>
          {isScanning ? <><ShieldAlert size={16} className="animate-pulse-slow" /> Scanning...</> : 'Analyze Target'}
        </button>
      </div>
    </form>
  )
}
