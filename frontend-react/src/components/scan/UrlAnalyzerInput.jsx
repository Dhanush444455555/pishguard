import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Target, ShieldAlert, Fingerprint } from 'lucide-react'
import './UrlAnalyzerInput.css'

export default function UrlAnalyzerInput({ onScan, isScanning, initialUrl = '' }) {
  const [url, setUrl] = useState(initialUrl)

  useEffect(() => {
    if (initialUrl) setUrl(initialUrl)
  }, [initialUrl])

  const handleSubmit = (e) => {
    e.preventDefault()
    if (url.trim()) onScan(url.trim())
  }

  return (
    <form onSubmit={handleSubmit} className={`scan-input-wrapper ${isScanning ? 'scanning' : ''}`}>
      {/* Targeting brackets */}
      <div className="target-bracket top-left"></div>
      <div className="target-bracket top-right"></div>
      <div className="target-bracket bottom-left"></div>
      <div className="target-bracket bottom-right"></div>

      <div className="scan-input-inner">
        <Target size={24} color={isScanning ? '#ef4444' : '#4facfe'} className={isScanning ? 'animate-spin-slow' : ''} />
        
        <input
          type="text"
          className="scan-input-field"
          placeholder="ENTER SUSPICIOUS URL OR DOMAIN..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={isScanning}
          spellCheck="false"
        />

        <button type="submit" className="scan-input-btn" disabled={isScanning || !url.trim()}>
          {isScanning ? (
            <>
              <Fingerprint size={16} className="animate-pulse-fast" />
              ANALYZING
            </>
          ) : (
            'INITIALIZE SCAN'
          )}
        </button>
      </div>

      {/* Cyber scanning animation layer */}
      <AnimatePresence>
        {isScanning && (
          <motion.div 
            className="scanner-overlay"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
          >
            <div className="scanner-line"></div>
            <div className="scanner-grid"></div>
          </motion.div>
        )}
      </AnimatePresence>
    </form>
  )
}
