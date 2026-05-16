import { ResponsiveContainer, PieChart, Pie, Cell, Tooltip } from 'recharts'
import { Activity, Zap, BrainCircuit, Shield } from 'lucide-react'
import './NeuralFlowActivity.css'

const tiers = [
  { name: 'Fast — Heuristics', value: 600000, color: '#10b981', avg: '45ms' },
  { name: 'Standard — ML', value: 200000, color: '#4facfe', avg: '210ms' },
  { name: 'Deep — LLM Reasoning', value: 54092, color: '#8b5cf6', avg: '850ms' },
]
const icons = [Zap, BrainCircuit, Shield]

export default function NeuralFlowActivity() {
  return (
    <div className="neuralflow">
      <div className="neuralflow-header">
        <h3 className="neuralflow-title"><Activity size={18} color="#00f2fe" />NeuralFlow Routing</h3>
        <span className="neuralflow-badge">LIVE</span>
      </div>
      <div className="neuralflow-chart">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie data={tiers} cx="50%" cy="50%" innerRadius={55} outerRadius={80} paddingAngle={4} dataKey="value">
              {tiers.map((t, i) => <Cell key={i} fill={t.color} />)}
            </Pie>
            <Tooltip contentStyle={{ background: '#0b0f19', border: '1px solid #1e293b', borderRadius: '0.5rem', color: '#fff', fontSize: '0.8rem' }} />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="neuralflow-tiers">
        {tiers.map((t, i) => {
          const Icon = icons[i]
          return (
            <div key={t.name} className="neuralflow-tier">
              <Icon size={16} color={t.color} style={{ margin: '0 auto 0.4rem' }} />
              <div className="neuralflow-tier-label">{['Fast', 'Standard', 'Deep'][i]}</div>
              <div className="neuralflow-tier-value">{t.avg}</div>
            </div>
          )
        })}
      </div>
    </div>
  )
}
