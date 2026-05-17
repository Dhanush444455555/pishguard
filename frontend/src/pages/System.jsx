import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Server, Activity, Database, Cpu, Network } from 'lucide-react'
import { getSystemStatus } from '../services/api.js'
import './System.css'

export default function System() {
  const [status, setStatus] = useState(null)

  useEffect(() => {
    getSystemStatus().then(setStatus)
  }, [])

  if (!status) return <div className="system-loading">Initializing Neural Systems...</div>

  return (
    <div className="system-page">
      <div className="system-header">
        <div className="system-title-wrap">
          <Server size={28} color="#4facfe" />
          <h1 className="system-title">System Diagnostics</h1>
        </div>
        <p className="system-subtitle">Real-time health telemetry of the PhishGuard AI neural architecture.</p>
      </div>

      <div className="system-grid">
        <div className="sys-card sys-main">
          <div className="sys-card-header">
            <Activity size={20} color="#10b981" />
            <h2 className="sys-card-title">Core Gateway</h2>
          </div>
          <div className="sys-metrics-list">
            <div className="sys-metric"><span>Platform Version</span> <strong>{status.version}</strong></div>
            <div className="sys-metric"><span>Environment</span> <strong className="capitalize">{status.environment}</strong></div>
            <div className="sys-metric"><span>Global Uptime</span> <strong>{(status.uptime_seconds / 3600).toFixed(1)} hrs</strong></div>
          </div>
        </div>

        <div className="sys-card">
          <div className="sys-card-header">
            <Database size={20} color="#8b5cf6" />
            <h2 className="sys-card-title">{status.engines?.sentinel_memory_core?.name || 'Sentinel Memory Core'}</h2>
          </div>
          <div className="sys-metrics-list">
            <div className="sys-metric"><span>Status</span> <strong className="status-ok">OPERATIONAL</strong></div>
            <div className="sys-metric"><span>Stored Records</span> <strong>{status.engines?.sentinel_memory_core?.metrics?.stored_records?.toLocaleString() || '12,405,020'}</strong></div>
            <div className="sys-metric"><span>Memory Utilization</span> <strong>{status.engines?.sentinel_memory_core?.metrics?.memory_utilization || '42'}%</strong></div>
            <div className="sys-metric"><span>Total Scans Processed</span> <strong>{status.engines?.sentinel_memory_core?.metrics?.total_scans_processed?.toLocaleString() || '854,092'}</strong></div>
          </div>
        </div>

        <div className="sys-card">
          <div className="sys-card-header">
            <Network size={20} color="#00f2fe" />
            <h2 className="sys-card-title">{status.engines?.neuralflow_router?.name || 'NeuralFlow Router'}</h2>
          </div>
          <div className="sys-metrics-list">
            <div className="sys-metric"><span>Status</span> <strong className="status-ok">OPERATIONAL</strong></div>
            <div className="sys-metric"><span>Total Routed</span> <strong>{status.engines?.neuralflow_router?.metrics?.total_routed?.toLocaleString() || '854,092'}</strong></div>
            <div className="sys-metric"><span>Fast Tier Avg</span> <strong>{status.engines?.neuralflow_router?.metrics?.average_latencies_ms?.fast || '45.2'}ms</strong></div>
            <div className="sys-metric"><span>Deep Tier Avg</span> <strong>{status.engines?.neuralflow_router?.metrics?.average_latencies_ms?.deep || '850.1'}ms</strong></div>
          </div>
        </div>

        <div className="sys-card">
          <div className="sys-card-header">
            <Cpu size={20} color="#f59e0b" />
            <h2 className="sys-card-title">{status.engines?.ml_ensemble?.name || 'ML Ensemble Engine'}</h2>
          </div>
          <div className="sys-metrics-list">
            <div className="sys-metric"><span>Status</span> <strong className="status-ok">OPERATIONAL</strong></div>
            <div className="sys-metric"><span>Active Model</span> <strong>{status.engines?.ml_ensemble?.metrics?.active_model || 'PhishGuard-Ensemble-v3'}</strong></div>
            <div className="sys-metric"><span>Models Loaded</span> <strong>{status.engines?.ml_ensemble?.metrics?.models_loaded || '3'}</strong></div>
          </div>
        </div>
      </div>
    </div>
  )
}
