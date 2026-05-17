import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import UrlAnalyzerInput from '../components/scan/UrlAnalyzerInput.jsx'
import AnimatedScanProgress from '../components/scan/AnimatedScanProgress.jsx'
import ThreatCard from '../components/ThreatCard.jsx'
import { scanUrl } from '../services/api.js'
import { ShieldAlert } from 'lucide-react'
import './Scan.css'

export default function Scan() {
  const location = useLocation()
  const [isScanning, setIsScanning] = useState(false)
  const [result, setResult] = useState(null)
  const [pendingResult, setPendingResult] = useState(null)
  const [initialUrl, setInitialUrl] = useState('')
  const [hasAutoScanned, setHasAutoScanned] = useState(false)

  const handleScan = (url) => {
    setIsScanning(true)
    setResult(null)
    setPendingResult(scanUrl(url))
  }

  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const urlFromQuery = params.get('url')
    if (urlFromQuery && !hasAutoScanned) {
      setInitialUrl(urlFromQuery)
      setHasAutoScanned(true)
      handleScan(urlFromQuery)
    }
  }, [location.search, hasAutoScanned])

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
      <div className="scan-content-wrapper">
        <div className="scan-header">
          <div className="scan-title-wrap">
            <ShieldAlert size={28} color="#4facfe" />
            <h1 className="scan-title">URL Threat Scanner</h1>
          </div>
          <p className="scan-subtitle">
            Deploy the <strong>Sentinel Memory Core</strong> and <strong>NeuralFlow Router</strong> to instantly analyze any URL for zero-day phishing indicators.
          </p>
        </div>

        <UrlAnalyzerInput onScan={handleScan} isScanning={isScanning} initialUrl={initialUrl} />
        <AnimatedScanProgress isScanning={isScanning} onComplete={handleComplete} />
        {!isScanning && result && <ThreatCard result={result} />}
      </div>
    </div>
  )
}
