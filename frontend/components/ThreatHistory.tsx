'use client';
import React from 'react';

const ThreatHistory = () => {
  const history = [
    { url: 'https://micr0soft-secure.net', risk: 94, date: '2 mins ago' },
    { url: 'https://google-auth-login.com', risk: 12, date: '15 mins ago' },
    { url: 'https://paypal-verify-account.info', risk: 88, date: '1 hour ago' },
    { url: 'https://amazon-security-alert.shop', risk: 76, date: '3 hours ago' },
  ];

  return (
    <div className="history-container">
      <div className="history-header">
        <div className="icon-badge">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
        </div>
        <h3>Hindsight Memory</h3>
      </div>

      <div className="history-list">
        {history.map((item, index) => (
          <div key={index} className="history-item glass">
            <div className="item-info">
              <span className="timestamp">{item.date}</span>
              <span className="url-text" title={item.url}>{item.url}</span>
            </div>
            
            <div className="item-score">
              <div className={`score-badge ${item.risk > 70 ? 'danger' : item.risk > 30 ? 'warning' : 'safe'}`}>
                {item.risk}%
              </div>
              <div className="mini-progress">
                <div 
                  className={`fill ${item.risk > 70 ? 'danger' : item.risk > 30 ? 'warning' : 'safe'}`}
                  style={{ width: `${item.risk}%` }}
                ></div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <button className="view-all">View All History</button>

      <style jsx>{`
        .history-container {
          width: 100%;
        }
        .history-header {
          display: flex;
          align-items: center;
          gap: 0.75rem;
          margin-bottom: 1.5rem;
        }
        .icon-badge {
          width: 32px;
          height: 32px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(0, 242, 254, 0.1);
          border-radius: 8px;
          color: #00f2fe;
        }
        .icon-badge svg {
          width: 18px;
          height: 18px;
        }
        h3 {
          font-size: 1rem;
          font-weight: 700;
          color: #f1f5f9;
        }
        .history-list {
          display: flex;
          flex-direction: column;
          gap: 1.25rem;
        }
        .history-item {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 1.25rem;
          border-radius: 20px;
          transition: all 0.2s;
          cursor: pointer;
        }
        .history-item:hover {
          background: rgba(255, 255, 255, 0.05);
          border-color: rgba(255, 255, 255, 0.2);
        }
        .item-info {
          display: flex;
          flex-direction: column;
          gap: 0.25rem;
          min-width: 0;
          flex: 1;
          margin-right: 1rem;
        }
        .timestamp {
          font-size: 0.65rem;
          font-weight: 600;
          color: #64748b;
          text-transform: uppercase;
        }
        .url-text {
          font-size: 0.8125rem;
          font-weight: 600;
          color: #cbd5e1;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .item-score {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 0.4rem;
          flex-shrink: 0;
        }
        .score-badge {
          font-size: 0.875rem;
          font-weight: 900;
        }
        .score-badge.danger { color: #ff4e50; }
        .score-badge.warning { color: #facc15; }
        .score-badge.safe { color: #43e97b; }

        .mini-progress {
          width: 60px;
          height: 3px;
          background: rgba(255, 255, 255, 0.05);
          border-radius: 10px;
          overflow: hidden;
        }
        .fill {
          height: 100%;
          border-radius: 10px;
        }
        .fill.danger { background: #ff4e50; }
        .fill.warning { background: #facc15; }
        .fill.safe { background: #43e97b; }

        .view-all {
          width: 100%;
          margin-top: 1.5rem;
          padding: 0.75rem;
          background: transparent;
          border: 1px solid rgba(255, 255, 255, 0.05);
          border-radius: 12px;
          color: #64748b;
          font-size: 0.75rem;
          font-weight: 700;
          cursor: pointer;
          transition: all 0.2s;
        }
        .view-all:hover {
          background: rgba(255, 255, 255, 0.03);
          color: white;
          border-color: rgba(255, 255, 255, 0.1);
        }
      `}</style>
    </div>
  );
};

export default ThreatHistory;
