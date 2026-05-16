/**
 * PhishGuard AI API Service
 * Handles interaction with the backend and mock data management
 */

export interface AnalysisResult {
  url: string;
  threatLevel: 'low' | 'medium' | 'high';
  probability: number;
  anomalies: {
    title: string;
    description: string;
    impact: 'Critical' | 'High' | 'Medium' | 'Low';
  }[];
  latency: number;
  confidence: number;
}

export const analyzeUrl = async (url: string): Promise<AnalysisResult> => {
  // Simulate API call latency
  await new Promise(resolve => setTimeout(resolve, 1200));

  return {
    url,
    threatLevel: 'high',
    probability: 94,
    confidence: 98.4,
    latency: 240,
    anomalies: [
      {
        title: 'Suspicious Domain',
        description: 'Domain structure mimics microsoft-login but uses .net TLD.',
        impact: 'High'
      },
      {
        title: 'Redirect Pattern',
        description: 'Found 3 hidden redirects before landing page.',
        impact: 'Medium'
      },
      {
        title: 'UI Clone Detected',
        description: 'Visual features match known phishing templates in memory.',
        impact: 'Critical'
      }
    ]
  };
};

export const getHindsightHistory = async () => {
  return [
    { url: 'https://micr0soft-secure.net', risk: 94, date: '2 mins ago' },
    { url: 'https://google-auth-login.com', risk: 12, date: '15 mins ago' },
    { url: 'https://paypal-verify-account.info', risk: 88, date: '1 hour ago' },
    { url: 'https://amazon-security-alert.shop', risk: 76, date: '3 hours ago' },
  ];
};

export const getCascadeRoute = (complexity: 'simple' | 'complex'): string => {
  return complexity === 'complex' ? 'Premium (GPT-4o)' : 'Standard (Haiku)';
};
