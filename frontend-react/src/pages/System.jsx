import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { getSystemStatus } from '../services/api.js'
import { Server, Activity, Database, BrainCircuit, ShieldAlert } from 'lucide-react'
import './System.css'

export default function System() {
  const [status, setStatus] = useState(null)

  useEffect(() => { getSystemStatus().then(setStatus) }, [])

  if (!status) return <div className="system-loading"><Activity className="animate-pulse-slow" size={32} /></div>

  const engineIcons = {
    sentinel_memory_core: Database,
    neuralflow_router: Activity,
    ml_ensemble: BrainCircuit,
  }
  const engineColors = {
    sentinel_memory_core: '#8b5cf6',
    neuralflow_router: '#00f2fe',
    ml_ensemble: '#4facfe',
  }

  return (
    <div className="system-page">
      <div className="system-header">
        <div>
          <h1 className="system-title">
            <Server size={26} color="#10b981" /> System Diagnostics
          </h1>
          <p className="system-subtitle">
            PhishGuard Core OS & Engine Subsystems Telemetry
          </p>
        </div>
        <div className="system-env-wrap">
          <div className="system-env-label">Environment</div>
          <div className="system-env-value">{status.environment}</div>
        </div>
      </div>

      <div className="system-grid">
        {Object.entries(status.engines).map(([key, engine], i) => {
          const Icon = engineIcons[key] || ShieldAlert
          const color = engineColors[key] || '#94a3b8'

          return (
            <motion.div key={key} className="system-card"
              initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
            >
              <div className="system-card-header">
                <h3 className="system-card-title">{engine.name}</h3>
                <Icon size={20} color={color} />
              </div>
              <div className="system-card-row">
                <span className="system-card-row-label">Status</span>
                <span className={`system-card-row-value ${engine.status === 'operational' ? 'operational' : 'error'}`}>
                  {engine.status}
                </span>
              </div>
              <div className="system-card-row">
                <span className="system-card-row-label">Version</span>
                <span className="system-card-row-value">{engine.version}</span>
              </div>
              <div className="system-card-row">
                <span className="system-card-row-label">Uptime</span>
                <span className="system-card-row-value">{(engine.uptime_seconds / 3600).toFixed(1)}h</span>
              </div>

              <div className="system-metrics-title">Live Metrics</div>
              <div className="system-metrics-box">
                {Object.entries(engine.metrics).map(([mKey, mVal]) => {
                  if (typeof mVal === 'object') return null
                  return (
                    <div key={mKey} className="system-metric">
                      <span className="system-metric-label">{mKey.replace(/_/g, ' ')}</span>
                      <span className="system-metric-value">
                        {typeof mVal === 'number' && mVal > 1000 ? mVal.toLocaleString() : mVal}
                        {mKey.includes('utilization') ? '%' : ''}
                      </span>
                    </div>
                  )
                })}
              </div>
            </motion.div>
          )
        })}
      </div>
    </div>
  )
}
