import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import NeuralFlowActivity from '../components/dashboard/NeuralFlowActivity.jsx'
import SentinelMemoryActivity from '../components/dashboard/SentinelMemoryActivity.jsx'
import { getSystemStatus } from '../services/api.js'
import { Activity, Shield, Server, ArrowUpRight, Cpu } from 'lucide-react'
import './Dashboard.css'

const kpis = [
  { label: 'Total Scans', value: '854,092', sub: '+12% today', color: '#4facfe', icon: Activity },
  { label: 'Threats Blocked', value: '142,304', sub: '16.7% threat ratio', color: '#8b5cf6', icon: Shield },
  { label: 'Avg AI Latency', value: '145ms', sub: 'Optimal routing active', color: '#00f2fe', icon: Cpu },
  { label: 'Uptime', value: '99.99%', sub: 'All engines nominal', color: '#10b981', icon: Server },
]

export default function Dashboard() {
  const [status, setStatus] = useState(null)

  useEffect(() => { getSystemStatus().then(setStatus) }, [])

  return (
    <div className="dashboard-page">
      <div className="dashboard-header">
        <div>
          <h1 className="dashboard-title">Threat Intelligence Dashboard</h1>
          <p className="dashboard-subtitle">Real-time telemetry from PhishGuard AI engines</p>
        </div>
        <div className="dashboard-status">
          <div className="dashboard-status-dot">
            <span className="ping" />
            <span className="dot" />
          </div>
          <span className="dashboard-status-text">LIVE MONITORING</span>
        </div>
      </div>

      <div className="dashboard-kpis">
        {kpis.map((k, i) => (
          <motion.div key={k.label} className="kpi-card"
            initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }}
            style={{ borderTop: `3px solid ${k.color}` }}
          >
            <div className="kpi-header">
              <p className="kpi-label">{k.label}</p>
              <div className="kpi-icon-wrap" style={{ background: `${k.color}15` }}>
                <k.icon size={16} color={k.color} />
              </div>
            </div>
            <div className="kpi-value">{k.value}</div>
            <div className="kpi-sub">
              <ArrowUpRight size={13} color="#10b981" />
              <span className="kpi-sub-text">{k.sub}</span>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="dashboard-charts">
        <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.4 }}>
          <NeuralFlowActivity />
        </motion.div>
        <motion.div initial={{ opacity: 0, scale: 0.97 }} animate={{ opacity: 1, scale: 1 }} transition={{ delay: 0.5 }}>
          <SentinelMemoryActivity />
        </motion.div>
      </div>
    </div>
  )
}
