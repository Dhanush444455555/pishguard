import { useState } from 'react'
import UrlAnalyzerInput from '../components/scan/UrlAnalyzerInput.jsx'
import AnimatedScanProgress from '../components/scan/AnimatedScanProgress.jsx'
import ThreatCard from '../components/ThreatCard.jsx'
import { scanUrl } from '../services/api.js'
import { ShieldAlert } from 'lucide-react'
import './Scan.css'

export default function Scan() {
  const [isScanning, setIsScanning] = useState(false)
  const [result, setResult] = useState(null)
  const [pendingResult, setPendingResult] = useState(null)

  const handleScan = (url) => {
    setIsScanning(true)
    setResult(null)
    setPendingResult(scanUrl(url))
  }

  const handleComplete = async () => {
    try {
      const data = await pendingResult
      setResult(data)
    } catch {
      setResult(null)
    } finally {
      setIsScanning(false)
      setPendingResult(null)
    }
  }

  return (
    <div className="scan-page">
      <div className="scan-header">
        <div className="scan-title-wrap">
          <ShieldAlert size={28} color="#4facfe" />
          <h1 className="scan-title">URL Threat Scanner</h1>
        </div>
        <p className="scan-subtitle">
          Deploy the <strong>Sentinel Memory Core</strong> and <strong>NeuralFlow Router</strong> to instantly analyze any URL for zero-day phishing indicators.
        </p>
      </div>

      <UrlAnalyzerInput onScan={handleScan} isScanning={isScanning} />
      <AnimatedScanProgress isScanning={isScanning} onComplete={handleComplete} />
      {!isScanning && result && <ThreatCard result={result} />}
    </div>
  )
}
