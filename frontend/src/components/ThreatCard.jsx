import { motion } from 'framer-motion'
import { ShieldAlert, ShieldCheck, AlertTriangle, Info, Terminal, Activity } from 'lucide-react'
import './ThreatCard.css'

const levelColors = {
  critical: { text: '#ef4444', border: '#ef4444', bg: 'rgba(239,68,68,0.08)', glow: '0 0 20px rgba(239,68,68,0.2)' },
  high:     { text: '#f59e0b', border: '#f59e0b', bg: 'rgba(245,158,11,0.08)', glow: '0 0 20px rgba(245,158,11,0.2)' },
  medium:   { text: '#8b5cf6', border: '#8b5cf6', bg: 'rgba(139,92,246,0.08)', glow: '0 0 20px rgba(139,92,246,0.2)' },
  low:      { text: '#4facfe', border: '#4facfe', bg: 'rgba(79,172,254,0.08)', glow: '0 0 20px rgba(79,172,254,0.2)' },
  safe:     { text: '#10b981', border: '#10b981', bg: 'rgba(16,185,129,0.08)', glow: '0 0 20px rgba(16,185,129,0.2)' },
}

export default function ThreatCard({ result }) {
  const level = result.threat_level?.toLowerCase() || 'safe'
  const colors = levelColors[level] || levelColors.safe
  const IconComp = level === 'safe' ? ShieldCheck : ShieldAlert

  return (
    <motion.div className="threat-card"
      initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ duration: 0.5 }}
      style={{ border: `1px solid ${colors.border}`, borderTop: `4px solid ${colors.border}`, boxShadow: colors.glow }}
    >
      <div className="threat-card-header">
        <div className="threat-card-left">
          <div className="threat-card-icon-wrap" style={{ background: colors.bg }}>
            <IconComp size={36} color={colors.text} />
          </div>
          <div>
            <h2 className="threat-card-level">{result.threat_level} Risk</h2>
            <p className="threat-card-url">{result.url}</p>
          </div>
        </div>
        <div>
          <div className="threat-card-score">{result.risk_score}<span>/100</span></div>
          <p className="threat-card-confidence">AI CONFIDENCE: {result.confidence}%</p>
        </div>
      </div>

      <div className="threat-card-body">
        <div>
          <h3 className="threat-card-section-title"><Terminal size={16} color="#8b5cf6" /> AI Reasoning Explanation</h3>
          <p className="threat-card-explanation">{result.explainability?.summary || result.ai_explanation || 'No detailed reasoning provided.'}</p>
          <div className="threat-card-engines">
            <span className="threat-card-engine-tag">NeuralFlow: {result.routing?.tier_name || 'Standard'}</span>
            <span className="threat-card-engine-tag">Sentinel Memory Core</span>
            <span className="threat-card-engine-tag">ML Ensemble</span>
          </div>
        </div>
        <div>
          <h3 className="threat-card-section-title"><Activity size={16} color="#4facfe" /> Detected Anomalies</h3>
          <div className="threat-card-anomalies">
            {(result.anomalies || result.threat_intelligence?.anomalies)?.map((a, i) => (
              <div key={i} className="threat-card-anomaly">
                {a.impact === 'critical' || a.impact === 'Critical'
                  ? <AlertTriangle size={16} color="#ef4444" style={{ flexShrink: 0, marginTop: 2 }} />
                  : <Info size={16} color="#f59e0b" style={{ flexShrink: 0, marginTop: 2 }} />}
                <div>
                  <p className="threat-card-anomaly-title">{a.title}</p>
                  <p className="threat-card-anomaly-desc">{a.description || a.desc}</p>
                </div>
              </div>
            ))}
            {!(result.anomalies?.length || result.threat_intelligence?.anomalies?.length) && (
              <p className="threat-card-empty">No structural anomalies detected.</p>
            )}
          </div>
        </div>
      </div>
    </motion.div>
  )
}
