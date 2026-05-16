'use client';
import React from 'react';

const ThreatCard = () => {
  const anomalies = [
    { title: 'Suspicious Domain', desc: 'Domain structure mimics microsoft-login but uses .net TLD.', impact: 'High' },
    { title: 'Redirect Pattern', desc: 'Found 3 hidden redirects before landing page.', impact: 'Medium' },
    { title: 'UI Clone Detected', desc: 'Visual features match known phishing templates in memory.', impact: 'Critical' },
  ];

  return (
    <div className="threat-card glass">
      <div className="card-header">
        <div className="title-group">
          <svg viewBox="0 0 24 24" fill="none" stroke="#4facfe" strokeWidth="2">
            <path d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
          </svg>
          <h3>AI Reasoning Engine</h3>
        </div>
        <div className="route-badge">Premium Route</div>
      </div>

      <div className="anomalies-list">
        {anomalies.map((item, index) => (
          <div key={index} className="anomaly-item">
            <div className={`impact-bar ${item.impact.toLowerCase()}`}></div>
            <div className="anomaly-content">
              <div className="anomaly-header">
                <span className="anomaly-title">{item.title}</span>
                <span className={`impact-label ${item.impact.toLowerCase()}`}>{item.impact}</span>
              </div>
              <p className="anomaly-desc">{item.desc}</p>
            </div>
          </div>
        ))}
      </div>

      <div className="card-footer">
        <div className="stats-row">
          <span>ML Confidence: 98.4%</span>
          <span>Latency: 240ms</span>
        </div>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: '98.4%' }}></div>
        </div>
      </div>

      <style jsx>{`
        .threat-card {
          padding: 2rem;
          border-radius: 30px;
          height: 100%;
        }
        .card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 2rem;
        }
        .title-group {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        .title-group svg {
          width: 20px;
          height: 20px;
        }
        h3 {
          font-size: 1.125rem;
          font-weight: 700;
          color: white;
        }
        .route-badge {
          font-size: 0.65rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.05em;
          color: #4facfe;
          background: rgba(79, 172, 254, 0.1);
          padding: 0.25rem 0.75rem;
          border-radius: 6px;
          border: 1px solid rgba(79, 172, 254, 0.2);
        }
        .anomalies-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .anomaly-item {
          display: flex;
          gap: 1rem;
          padding: 1rem;
          background: rgba(255, 255, 255, 0.03);
          border-radius: 16px;
          border: 1px solid rgba(255, 255, 255, 0.03);
          transition: background 0.2s;
        }
        .anomaly-item:hover {
          background: rgba(255, 255, 255, 0.05);
        }
        .impact-bar {
          width: 4px;
          height: 40px;
          border-radius: 10px;
          flex-shrink: 0;
        }
        .impact-bar.critical { background: #ff4e50; }
        .impact-bar.high { background: #f97316; }
        .impact-bar.medium { background: #facc15; }

        .anomaly-content {
          flex: 1;
        }
        .anomaly-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 0.25rem;
        }
        .anomaly-title {
          font-weight: 700;
          color: #e2e8f0;
          font-size: 0.9375rem;
        }
        .impact-label {
          font-size: 0.65rem;
          font-weight: 900;
          text-transform: uppercase;
          padding: 0.1rem 0.4rem;
          border-radius: 4px;
        }
        .impact-label.critical { background: rgba(255, 78, 80, 0.15); color: #ff4e50; }
        .impact-label.high { background: rgba(249, 115, 22, 0.15); color: #f97316; }
        .impact-label.medium { background: rgba(250, 204, 21, 0.15); color: #facc15; }

        .anomaly-desc {
          font-size: 0.8125rem;
          color: #94a3b8;
          line-height: 1.4;
        }
        .card-footer {
          margin-top: 2rem;
          padding-top: 1.5rem;
          border-top: 1px solid rgba(255, 255, 255, 0.05);
        }
        .stats-row {
          display: flex;
          justify-content: space-between;
          font-size: 0.75rem;
          font-weight: 600;
          color: #64748b;
          margin-bottom: 0.75rem;
        }
        .progress-bar {
          width: 100%;
          height: 4px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 10px;
          overflow: hidden;
        }
        .progress-fill {
          height: 100%;
          background: #4facfe;
          border-radius: 10px;
        }
      `}</style>
    </div>
  );
};

export default ThreatCard;
