import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
})

const mockScan = (url) => ({
  scan_id: 'mock-001',
  url,
  timestamp: new Date().toISOString(),
  risk_score: 94.5,
  threat_level: 'critical',
  confidence: 98.2,
  analysis_time_ms: 840,
  zero_day_probability: 0.85,
  engines_used: ['sentinel_memory_core', 'neuralflow_router:deep', 'ml_ensemble_v3'],
  threat_intelligence: {
    anomalies: [
      { title: 'Brand Impersonation', desc: 'Domain embeds a well-known brand name outside any official TLD.', impact: 'Critical' },
      { title: 'Urgency Keywords', desc: 'URL path contains "update" and "secure" to manufacture urgency.', impact: 'High' },
      { title: 'Suspicious TLD', desc: 'The .net TLD is heavily abused for credential-harvesting campaigns.', impact: 'Medium' },
    ],
  },
  ai_explanation: 'This URL impersonates a major brand by embedding brand keywords in a non-official domain. The pattern matches 94 prior confirmed phishing campaigns in the Sentinel Memory Core. The NeuralFlow Router escalated this to Deep-tier LLM reasoning due to the high zero-day probability score.',
})

const mockStatus = {
  status: 'operational',
  version: '2.0.0',
  project: 'PhishGuard AI',
  environment: 'development',
  uptime_seconds: 43233,
  engines: {
    sentinel_memory_core: {
      name: 'Sentinel Memory Core',
      status: 'operational',
      version: '2.0.0',
      uptime_seconds: 43233,
      metrics: { stored_records: 12405020, memory_utilization: 42, total_scans_processed: 854092 },
    },
    neuralflow_router: {
      name: 'NeuralFlow Router',
      status: 'operational',
      version: '2.0.0',
      uptime_seconds: 43233,
      metrics: {
        total_routed: 854092,
        tier_distribution: { fast: 600000, standard: 200000, deep: 54092 },
        average_latencies_ms: { fast: 45.2, standard: 210.5, deep: 850.1 },
      },
    },
    ml_ensemble: {
      name: 'ML Ensemble Engine',
      status: 'operational',
      version: 'Ensemble-v3',
      uptime_seconds: 43233,
      metrics: { models_loaded: 3, active_model: 'PhishGuard-Ensemble-v3' },
    },
  },
}

const mockHistory = [
  { id: '1', url: 'http://paypal-verification-center.com', date: '2026-05-16', risk: 92, status: 'Blocked' },
  { id: '2', url: 'https://amazon-rewards-claim.xyz', date: '2026-05-15', risk: 88, status: 'Blocked' },
  { id: '3', url: 'http://netflix-billing-update.net', date: '2026-05-14', risk: 95, status: 'Blocked' },
  { id: '4', url: 'https://chase-secure-auth.info', date: '2026-05-12', risk: 91, status: 'Blocked' },
  { id: '5', url: 'http://apple-id-verify.tk', date: '2026-05-10', risk: 98, status: 'Blocked' },
]

const mockSimilar = [
  { id: 's1', url: 'https://microsoft-login-verify.net', similarity: 0.94, date: '2026-05-10', threat_level: 'critical' },
  { id: 's2', url: 'http://microsoft-secure-update.com', similarity: 0.88, date: '2026-04-22', threat_level: 'critical' },
  { id: 's3', url: 'https://microsoft-auth-center.xyz', similarity: 0.85, date: '2026-03-15', threat_level: 'high' },
]

export async function scanUrl(url) {
  try {
    const res = await api.post('/scan', { url })
    return res.data
  } catch (error) {
    console.error("Scan failed:", error)
    throw error
  }
}

export async function getSystemStatus() {
  try {
    const res = await api.get('/system-status')
    return res.data
  } catch (error) {
    console.error("Failed to fetch system status:", error)
    throw error
  }
}

export async function getThreatHistory() {
  try {
    const res = await api.get('/threat-history')
    return res.data?.history || []
  } catch (error) {
    console.error("Failed to fetch threat history:", error)
    return []
  }
}

export async function getSimilarThreats(url) {
  try {
    const res = await api.post('/similar-threats', { url })
    return res.data?.similar_threats || []
  } catch (error) {
    console.error("Failed to fetch similar threats:", error)
    return []
  }
}
