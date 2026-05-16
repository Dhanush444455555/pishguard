import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { ShieldAlert, Zap, Network, ChevronRight, Activity, Shield } from 'lucide-react'
import './Hero.css'

const features = [
  { icon: Zap, color: '#00f2fe', border: 'rgba(0,242,254,0.3)', bg: 'rgba(0,242,254,0.05)', title: 'NeuralFlow Router', desc: 'Intelligently routes analysis across Fast, Standard, and Deep AI tiers — optimizing for latency and accuracy in real time.' },
  { icon: Network, color: '#8b5cf6', border: 'rgba(139,92,246,0.3)', bg: 'rgba(139,92,246,0.05)', title: 'Sentinel Memory Core', desc: 'Persistent threat memory using vector embeddings to detect novel attacks matching historical architectural patterns.' },
  { icon: Shield, color: '#4facfe', border: 'rgba(79,172,254,0.3)', bg: 'rgba(79,172,254,0.05)', title: 'Explainable AI', desc: 'Chain-of-thought reasoning engine translates complex neural weights into human-readable forensic threat narratives.' },
]

export default function Hero() {
  return (
    <div className="hero">
      <div className="hero-glow" />
      <div className="hero-content">
        <motion.div initial={{ opacity: 0, y: 16 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }}>
          <span className="hero-badge">
            <span className="hero-badge-dot" />
            PhishGuard OS 2.0 — Now Live
          </span>
        </motion.div>

        <motion.h1 className="hero-headline" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.1 }}>
          Zero-Day Threat Detection<br />
          <span className="hero-gradient-text">Powered by AI</span>
        </motion.h1>

        <motion.p className="hero-subtitle" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.2 }}>
          Enterprise-grade cybersecurity using <strong>Sentinel Memory Core</strong> and{' '}
          <strong>NeuralFlow Router</strong> to neutralize phishing campaigns before they breach your network.
        </motion.p>

        <motion.div className="hero-ctas" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.7, delay: 0.3 }}>
          <Link to="/scan" className="hero-cta-primary">
            <ShieldAlert size={18} /> Initialize Scan <ChevronRight size={16} />
          </Link>
          <Link to="/dashboard" className="hero-cta-secondary">
            <Activity size={18} /> View Dashboard
          </Link>
        </motion.div>
      </div>

      <div className="hero-features">
        {features.map((f, i) => (
          <motion.div key={f.title} className="hero-feature-card"
            style={{ border: `1px solid ${f.border}` }}
            initial={{ opacity: 0, y: 24 }} whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }} transition={{ duration: 0.5, delay: i * 0.1 }}
          >
            <div className="hero-feature-icon" style={{ background: f.bg, border: `1px solid ${f.border}` }}>
              <f.icon size={22} color={f.color} />
            </div>
            <h3 className="hero-feature-title">{f.title}</h3>
            <p className="hero-feature-desc">{f.desc}</p>
          </motion.div>
        ))}
      </div>
    </div>
  )
}
