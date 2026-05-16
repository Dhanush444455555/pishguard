/**
 * PhishGuard AI API Service
 * Connects to the FastAPI backend at http://127.0.0.1:8000
 * Provides typed interfaces and graceful error handling with mock fallbacks
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

// ─── Type Definitions ───────────────────────────────────────────────────────

export interface Anomaly {
  title: string;
  description: string;
  impact: 'Critical' | 'High' | 'Medium' | 'Low';
}

export interface AnalysisResult {
  url: string;
  threatLevel: 'low' | 'medium' | 'high';
  probability: number;
  anomalies: Anomaly[];
  latency: number;
  confidence: number;
}

export interface HistoryEntry {
  url: string;
  risk: number;
  date: string;
}

export interface HealthStatus {
  status: string;
  version?: string;
  uptime?: number;
}

// ─── Error Class ────────────────────────────────────────────────────────────

export class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
  }
}

// ─── HTTP Helper ────────────────────────────────────────────────────────────

async function apiFetch<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`;

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);

  try {
    const response = await fetch(url, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorBody = await response.text().catch(() => 'Unknown error');
      throw new ApiError(
        `API request failed: ${response.statusText} — ${errorBody}`,
        response.status
      );
    }

    return (await response.json()) as T;
  } catch (error) {
    if (error instanceof ApiError) throw error;

    if (error instanceof DOMException && error.name === 'AbortError') {
      throw new ApiError('Request timed out. The backend may be unreachable.', 408);
    }

    throw new ApiError(
      `Network error: Unable to reach backend at ${API_BASE_URL}. Is the server running?`,
      0
    );
  } finally {
    clearTimeout(timeout);
  }
}

// ─── Mock Data (fallback when backend is offline) ───────────────────────────

const MOCK_ANALYSIS: AnalysisResult = {
  url: '',
  threatLevel: 'high',
  probability: 94,
  confidence: 98.4,
  latency: 240,
  anomalies: [
    {
      title: 'Suspicious Domain',
      description: 'Domain structure mimics microsoft-login but uses .net TLD.',
      impact: 'High',
    },
    {
      title: 'Redirect Pattern',
      description: 'Found 3 hidden redirects before landing page.',
      impact: 'Medium',
    },
    {
      title: 'UI Clone Detected',
      description: 'Visual features match known phishing templates in memory.',
      impact: 'Critical',
    },
  ],
};

const MOCK_HISTORY: HistoryEntry[] = [
  { url: 'https://micr0soft-secure.net', risk: 94, date: '2 mins ago' },
  { url: 'https://google-auth-login.com', risk: 12, date: '15 mins ago' },
  { url: 'https://paypal-verify-account.info', risk: 88, date: '1 hour ago' },
  { url: 'https://amazon-security-alert.shop', risk: 76, date: '3 hours ago' },
];

// ─── API Methods ────────────────────────────────────────────────────────────

/**
 * Submit a URL for phishing analysis.
 * POST /api/scan
 */
export const analyzeUrl = async (url: string): Promise<AnalysisResult> => {
  try {
    const result = await apiFetch<AnalysisResult>('/api/scan', {
      method: 'POST',
      body: JSON.stringify({ url }),
    });
    return result;
  } catch (error) {
    console.warn('[PhishGuard] Backend unavailable, using mock analysis:', error);
    // Simulate realistic latency for demo mode
    await new Promise((resolve) => setTimeout(resolve, 1200));
    return { ...MOCK_ANALYSIS, url };
  }
};

/**
 * Retrieve the Hindsight Memory (scan history).
 * GET /api/memory/history
 */
export const getHindsightHistory = async (): Promise<HistoryEntry[]> => {
  try {
    const history = await apiFetch<HistoryEntry[]>('/api/memory/history');
    return history;
  } catch (error) {
    console.warn('[PhishGuard] Backend unavailable, using mock history:', error);
    return MOCK_HISTORY;
  }
};

/**
 * Check backend health status.
 * GET /api/health
 */
export const checkHealth = async (): Promise<HealthStatus> => {
  try {
    return await apiFetch<HealthStatus>('/api/health');
  } catch {
    return { status: 'offline' };
  }
};

/**
 * Determine the CascadeFlow route based on query complexity.
 */
export const getCascadeRoute = (complexity: 'simple' | 'complex'): string => {
  return complexity === 'complex' ? 'Premium (GPT-4o)' : 'Standard (Haiku)';
};
