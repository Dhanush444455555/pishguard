import { ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'
import { Database, TrendingUp, Search } from 'lucide-react'
import './SentinelMemoryActivity.css'

const data = [
  { t: '00:00', q: 4000 }, { t: '04:00', q: 2800 }, { t: '08:00', q: 8200 },
  { t: '12:00', q: 12400 }, { t: '16:00', q: 15100 }, { t: '20:00', q: 9300 }, { t: '24:00', q: 5100 },
]

export default function SentinelMemoryActivity() {
  return (
    <div className="sentinel">
      <div className="sentinel-header">
        <h3 className="sentinel-title"><Database size={18} color="#8b5cf6" />Sentinel Memory Core</h3>
        <span className="sentinel-badge">VECTOR DB</span>
      </div>
      <div className="sentinel-stats">
        <div className="sentinel-stat">
          <div className="sentinel-stat-label"><Search size={13} /> Active Vectors</div>
          <div className="sentinel-stat-value">12.4M</div>
        </div>
        <div className="sentinel-stat">
          <div className="sentinel-stat-label"><TrendingUp size={13} /> Matches</div>
          <div className="sentinel-stat-value highlight">854K</div>
        </div>
      </div>
      <div className="sentinel-chart">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data} margin={{ top: 4, right: 0, left: -24, bottom: 0 }}>
            <defs>
              <linearGradient id="smGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" vertical={false} />
            <XAxis dataKey="t" stroke="#334155" fontSize={11} tickLine={false} axisLine={false} />
            <YAxis stroke="#334155" fontSize={11} tickLine={false} axisLine={false} tickFormatter={(v) => `${v / 1000}k`} />
            <Tooltip contentStyle={{ background: '#0b0f19', border: '1px solid #1e293b', borderRadius: '0.5rem', color: '#fff', fontSize: '0.8rem' }} />
            <Area type="monotone" dataKey="q" stroke="#8b5cf6" strokeWidth={2} fill="url(#smGrad)" />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}
