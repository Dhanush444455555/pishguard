import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { getThreatHistory } from '../services/api.js'
import { Clock, ShieldAlert, ShieldCheck, Shield } from 'lucide-react'
import './History.css'

export default function History() {
  const [history, setHistory] = useState([])

  useEffect(() => { getThreatHistory().then(setHistory) }, [])

  const riskIcon = (r) => {
    if (r >= 90) return <ShieldAlert size={16} color="#ef4444" />
    if (r >= 60) return <Shield size={16} color="#f59e0b" />
    return <ShieldCheck size={16} color="#10b981" />
  }

  return (
    <div className="history-page">
      <div className="history-header">
        <h1 className="history-title">
          <Clock size={26} color="#4facfe" /> Threat Intelligence History
        </h1>
        <p className="history-subtitle">
          Historical attacks neutralized and logged by the Sentinel Memory Core.
        </p>
      </div>

      <div className="history-table-container">
        <table className="history-table">
          <thead>
            <tr>
              {['Date', 'Target URL', 'Risk Score', 'Status'].map(h => (
                <th key={h} className="history-th">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {history.map((item, i) => (
              <motion.tr key={item.id} className="history-tr"
                initial={{ opacity: 0, x: -12 }} animate={{ opacity: 1, x: 0 }} transition={{ delay: i * 0.08 }}
              >
                <td className="history-td history-date">{item.date}</td>
                <td className="history-td history-url">{item.url}</td>
                <td className="history-td">
                  <div className="history-risk-wrap">
                    {riskIcon(item.risk)}
                    <span className="history-risk-score">{item.risk}<span>/100</span></span>
                  </div>
                </td>
                <td className="history-td">
                  <span className="history-status-badge">{item.status}</span>
                </td>
              </motion.tr>
            ))}
          </tbody>
        </table>
        {history.length === 0 && (
          <div className="history-empty">No threat history found in the Sentinel Memory Core.</div>
        )}
      </div>
    </div>
  )
}
