'use client';
import React from 'react';

interface RiskMeterProps {
  score: number;
}

const RiskMeter: React.FC<RiskMeterProps> = ({ score = 0 }) => {
  const getStatus = () => {
    if (score < 30) return { label: 'Safe', color: '#43e97b', glow: 'rgba(67, 233, 123, 0.3)' };
    if (score < 70) return { label: 'Suspicious', color: '#f9d423', glow: 'rgba(249, 212, 35, 0.3)' };
    return { label: 'High Risk', color: '#ff4e50', glow: 'rgba(255, 78, 80, 0.3)' };
  };

  const status = getStatus();
  const radius = 70;
  const circumference = 2 * Math.PI * radius;
  const offset = circumference - (score / 100) * circumference;

  return (
    <div className="risk-container glass">
      <div className="status-overlay" style={{ background: status.color }}></div>
      
      <div className="gauge-wrapper">
        <svg viewBox="0 0 200 200">
          <circle cx="100" cy="100" r={radius} className="bg-circle" />
          <circle 
            cx="100" cy="100" r={radius} 
            className="progress-circle"
            style={{ 
              stroke: status.color,
              strokeDasharray: circumference,
              strokeDashoffset: offset,
              filter: `drop-shadow(0 0 8px ${status.glow})`
            }}
          />
        </svg>

        <div className="text-overlay">
          <div className="score" style={{ color: status.color }}>{score}%</div>
          <div className="label">Threat Probability</div>
        </div>
      </div>

      <div className="status-footer">
        <div className="status-pill" style={{ 
          borderColor: `${status.color}40`, 
          color: status.color,
          background: `${status.color}15`
        }}>
          {status.label}
        </div>
        <p>Adaptive pattern analysis engine active.</p>
      </div>

      <style jsx>{`
        .risk-container {
          padding: 2.5rem;
          border-radius: 30px;
          display: flex;
          flex-direction: column;
          align-items: center;
          position: relative;
          overflow: hidden;
        }
        .status-overlay {
          position: absolute;
          inset: 0;
          opacity: 0.05;
          pointer-events: none;
        }
        .gauge-wrapper {
          position: relative;
          width: 200px;
          height: 200px;
        }
        svg {
          width: 100%;
          height: 100%;
          transform: rotate(-90deg);
        }
        .bg-circle {
          fill: none;
          stroke: rgba(255, 255, 255, 0.05);
          stroke-width: 12;
        }
        .progress-circle {
          fill: none;
          stroke-width: 12;
          stroke-linecap: round;
          transition: stroke-dashoffset 1s cubic-bezier(0.4, 0, 0.2, 1);
        }
        .text-overlay {
          position: absolute;
          inset: 0;
          display: flex;
          flex-direction: column;
          align-items: center;
          justify-content: center;
        }
        .score {
          font-size: 3.5rem;
          font-weight: 900;
          letter-spacing: -0.05em;
          line-height: 0.9;
          margin-bottom: 0.5rem;
        }
        .label {
          font-size: 0.7rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.15em;
          color: #94a3b8;
        }
        .status-footer {
          margin-top: 1.5rem;
          text-align: center;
          z-index: 10;
        }
        .status-pill {
          display: inline-block;
          padding: 0.25rem 1rem;
          border-radius: 100px;
          font-size: 0.875rem;
          font-weight: 800;
          border: 1px solid;
          margin-bottom: 0.75rem;
        }
        p {
          font-size: 0.875rem;
          color: #94a3b8;
          max-width: 200px;
          margin: 0 auto;
        }
      `}</style>
    </div>
  );
};

export default RiskMeter;
