import { useState } from 'react'
import { motion } from 'framer-motion'
import { getSimilarThreats } from '../services/api.js'
import { Target, Search } from 'lucide-react'
import './Similar.css'

export default function Similar() {
  const [url, setUrl] = useState('')
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [searched, setSearched] = useState(false)

  const handleSearch = async (e) => {
    e.preventDefault()
    if (!url.trim()) return
    setLoading(true)
    setSearched(true)
    const data = await getSimilarThreats(url)
    setResults(data)
    setLoading(false)
  }

  return (
    <div className="similar-page">
      <div className="similar-header">
        <h1 className="similar-title">
          <Target size={26} color="#8b5cf6" /> Vector Similarity Analysis
        </h1>
        <p className="similar-subtitle">
          Query the Sentinel Memory Core to find historical patterns matching a target URL.
        </p>
      </div>

      <form onSubmit={handleSearch} className="similar-form">
        <div className="similar-input-wrap">
          <Search size={16} color="#475569" className="similar-input-icon" />
          <input
            type="text"
            className="similar-input"
            placeholder="Enter URL to find similar architectural patterns..."
            value={url}
            onChange={e => setUrl(e.target.value)}
          />
        </div>
        <button type="submit" className="similar-btn" disabled={loading || !url.trim()}>
          {loading ? 'Querying Vector DB...' : 'Analyze Similarity'}
        </button>
      </form>

      {searched && !loading && (
        <div>
          <p className="similar-results-count">
            {results.length} neural embedding match{results.length !== 1 ? 'es' : ''} found
          </p>
          <div className="similar-results-list">
            {results.map((r, i) => (
              <motion.div key={r.url} className="similar-result-card"
                initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: i * 0.08 }}
              >
                <div>
                  <p className="similar-result-url">{r.url}</p>
                  <div className="similar-result-meta">
                    <span className="similar-result-date">First seen: {new Date(r.scanned_at).toLocaleDateString()}</span>
                    <span className="similar-result-level">{r.threat_level}</span>
                  </div>
                </div>
                <div className="similar-result-score-wrap">
                  <div className="similar-result-score">{(r.similarity_score * 100).toFixed(1)}%</div>
                  <div className="similar-result-label">SIMILARITY</div>
                </div>
              </motion.div>
            ))}
            {results.length === 0 && (
              <div className="similar-empty">
                No statistically significant matches found in the Sentinel Memory Core.
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
