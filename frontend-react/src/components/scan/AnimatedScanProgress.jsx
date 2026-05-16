import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Database, Network, BrainCircuit, Activity, CheckCircle } from 'lucide-react'
import './AnimatedScanProgress.css'

const steps = [
  { id: 'dns', label: 'Resolving Domain Topology', icon: Network },
  { id: 'memory', label: 'Querying Sentinel Memory Core', icon: Database },
  { id: 'route', label: 'NeuralFlow AI Routing Decision', icon: Activity },
  { id: 'reason', label: 'AI Reasoning & Threat Synthesis', icon: BrainCircuit },
]

export default function AnimatedScanProgress({ isScanning, onComplete }) {
  const [step, setStep] = useState(0)

  useEffect(() => {
    if (!isScanning) { setStep(0); return }
    let current = 0
    setStep(0)
    const iv = setInterval(() => {
      current++
      setStep(current)
      if (current >= steps.length) {
        clearInterval(iv)
        setTimeout(onComplete, 400)
      }
    }, 550)
    return () => clearInterval(iv)
  }, [isScanning])

  if (!isScanning) return null

  return (
    <div className="scan-progress">
      <div className="scan-progress-header">
        <Activity size={20} color="#4facfe" className="animate-pulse-slow" />
        <span className="scan-progress-title">Neural Analysis Sequence Initiated</span>
      </div>
      <div className="scan-progress-steps">
        {steps.map((s, i) => {
          const done = i < step
          const active = i === step
          const state = done ? 'done' : active ? 'active' : 'pending'
          return (
            <div key={s.id} className="scan-step">
              <div className={`scan-step-icon ${state}`}>
                {done ? <CheckCircle size={16} color="#4facfe" /> : <s.icon size={16} color={active ? '#4facfe' : '#475569'} />}
              </div>
              <div className="scan-step-body">
                <p className={`scan-step-label ${state}`}>{s.label}</p>
                {active && (
                  <div className="scan-step-bar">
                    <motion.div className="scan-step-fill" initial={{ width: 0 }} animate={{ width: '100%' }} transition={{ duration: 0.55, ease: 'linear' }} />
                  </div>
                )}
              </div>
              <span className={`scan-step-status ${state}`}>
                {done ? 'OK' : active ? 'RUNNING' : 'PENDING'}
              </span>
            </div>
          )
        })}
      </div>
    </div>
  )
}
