'use client';

import React from 'react';
import Navbar from '../components/Navbar';
import UrlInput from '../components/UrlInput';
import RiskMeter from '../components/RiskMeter';
import ThreatCard from '../components/ThreatCard';
import ThreatHistory from '../components/ThreatHistory';

export default function Home() {
  return (
    <main className="app-container">
      <Navbar />
      
      {/* Hero Section */}
      <section className="hero">
        <div className="hero-content">
          <div className="badge-main">AI-Powered Cybersecurity</div>
          <h1>
            Stop Phishing <br />
            <span className="gradient-text">Before It Strikes.</span>
          </h1>
          <p className="hero-sub">
            PhishGuard AI uses intelligent Hindsight memory and CascadeFlow routing to detect 
            zero-day threats with unprecedented precision.
          </p>
          
          <UrlInput />
        </div>

        {/* Animated background blobs */}
        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
      </section>

      {/* Analysis Dashboard Preview */}
      <section className="dashboard-grid container">
        {/* Left Column: Result & Meter */}
        <div className="col-4">
          <div className="stack">
            <RiskMeter score={94} />
            
            <div className="glass quick-stats">
              <h4>Quick Stats</h4>
              <div className="stats-list">
                <div className="stat-row">
                  <span className="label">Domain Age</span>
                  <span className="value">2 Days</span>
                </div>
                <div className="stat-row">
                  <span className="label">SSL Status</span>
                  <span className="value danger">Self-Signed</span>
                </div>
                <div className="stat-row">
                  <span className="label">Global Reports</span>
                  <span className="value">12,402</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Center Column: AI Reasoning */}
        <div className="col-5">
          <ThreatCard />
        </div>

        {/* Right Column: History/Memory */}
        <div className="col-3">
          <ThreatHistory />
        </div>
      </section>

      <footer className="footer">
        <p>© 2026 PhishGuard AI. All rights reserved.</p>
      </footer>

      <style jsx>{`
        .app-container {
          min-height: 100vh;
          background-color: #05060a;
          color: white;
          padding-bottom: 5rem;
        }
        .hero {
          position: relative;
          padding: 6rem 1rem 4rem;
          text-align: center;
          overflow: hidden;
        }
        .hero-content {
          position: relative;
          z-index: 10;
          max-width: 900px;
          margin: 0 auto;
        }
        .badge-main {
          display: inline-block;
          padding: 0.4rem 1rem;
          background: rgba(79, 172, 254, 0.1);
          border: 1px solid rgba(79, 172, 254, 0.2);
          border-radius: 100px;
          color: #4facfe;
          font-size: 0.75rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          margin-bottom: 2rem;
        }
        h1 {
          font-size: clamp(2.5rem, 8vw, 4.5rem);
          font-weight: 900;
          line-height: 1.1;
          letter-spacing: -0.03em;
          margin-bottom: 1.5rem;
        }
        .hero-sub {
          font-size: 1.125rem;
          color: #94a3b8;
          max-width: 600px;
          margin: 0 auto 3rem;
          line-height: 1.6;
        }
        .blob {
          position: absolute;
          width: 500px;
          height: 500px;
          background: radial-gradient(circle, rgba(79, 172, 254, 0.15) 0%, rgba(0, 0, 0, 0) 70%);
          border-radius: 50%;
          filter: blur(80px);
          z-index: 1;
        }
        .blob-1 { top: -100px; left: -100px; }
        .blob-2 { bottom: -100px; right: -100px; }

        .dashboard-grid {
          display: grid;
          grid-template-columns: repeat(12, 1fr);
          gap: 3.5rem;
          margin-top: 3rem;
        }
        .col-4 { grid-column: span 12; }
        .col-5 { grid-column: span 12; }
        .col-3 { grid-column: span 12; }

        @media (min-width: 1024px) {
          .col-4 { grid-column: span 4; }
          .col-5 { grid-column: span 5; }
          .col-3 { grid-column: span 3; }
        }

        .stack {
          display: flex;
          flex-direction: column;
          gap: 2rem;
        }
        .quick-stats {
          padding: 1.5rem;
          border-radius: 24px;
        }
        h4 {
          font-size: 0.75rem;
          font-weight: 800;
          text-transform: uppercase;
          letter-spacing: 0.1em;
          color: #64748b;
          margin-bottom: 1.25rem;
        }
        .stats-list {
          display: flex;
          flex-direction: column;
          gap: 1rem;
        }
        .stat-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }
        .stat-row .label {
          font-size: 0.875rem;
          color: #94a3b8;
        }
        .stat-row .value {
          font-size: 0.875rem;
          font-weight: 700;
          font-family: monospace;
        }
        .stat-row .value.danger {
          color: #ff4e50;
          text-decoration: underline;
        }
        
        .footer {
          margin-top: 8rem;
          text-align: center;
          color: #475569;
          font-size: 0.875rem;
        }
      `}</style>
    </main>
  );
}
