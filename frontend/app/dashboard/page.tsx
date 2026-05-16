'use client';

import React, { useState, useEffect } from 'react';
import Navbar from '../../components/Navbar';
import ThreatHistory from '../../components/ThreatHistory';
import { checkHealth, HealthStatus } from '../../services/api';

export default function DashboardPage() {
  const [health, setHealth] = useState<HealthStatus>({ status: 'checking' });

  useEffect(() => {
    let mounted = true;
    checkHealth().then((data) => {
      if (mounted) setHealth(data);
    });
    return () => { mounted = false; };
  }, []);

  const isOnline = health.status !== 'offline' && health.status !== 'checking';

  return (
    <main className="app-container">
      <Navbar />

      <section className="dash-hero">
        <div className="dash-hero-content">
          <div className="page-badge">Dashboard</div>
          <h1>Threat <span className="gradient-text">Intelligence</span></h1>
          <p className="dash-sub">
            Monitor scan history, system health, and AI pipeline performance in real time.
          </p>
        </div>
        <div className="blob b1"></div>
        <div className="blob b2"></div>
      </section>

      {/* Status Cards */}
      <section className="status-cards container">
        <div className="scard glass">
          <div className="scard-icon" style={{ background: 'rgba(67,233,123,.1)', color: '#43e97b' }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <div className="scard-info">
            <span className="scard-label">System Status</span>
            <span className={`scard-value ${isOnline ? 'online' : 'offline'}`}>
              <span className={`status-dot ${isOnline ? 'online' : 'offline'}`}></span>
              {health.status === 'checking' ? 'Checking...' : isOnline ? 'Online' : 'Offline'}
            </span>
          </div>
        </div>

        <div className="scard glass">
          <div className="scard-icon" style={{ background: 'rgba(79,172,254,.1)', color: '#4facfe' }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
          </div>
          <div className="scard-info">
            <span className="scard-label">AI Pipeline</span>
            <span className="scard-value">CascadeFlow Active</span>
          </div>
        </div>

        <div className="scard glass">
          <div className="scard-icon" style={{ background: 'rgba(0,242,254,.1)', color: '#00f2fe' }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          <div className="scard-info">
            <span className="scard-label">Memory Engine</span>
            <span className="scard-value">Hindsight Active</span>
          </div>
        </div>

        <div className="scard glass">
          <div className="scard-icon" style={{ background: 'rgba(168,85,247,.1)', color: '#a855f7' }}>
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6m6 0h6m-6 0V9a2 2 0 012-2h2a2 2 0 012 2v10m6 0v-4a2 2 0 00-2-2h-2a2 2 0 00-2 2v4" />
            </svg>
          </div>
          <div className="scard-info">
            <span className="scard-label">Total Scans</span>
            <span className="scard-value">12,402</span>
          </div>
        </div>
      </section>

      {/* Threat History */}
      <section className="history-section container">
        <div className="history-wrapper glass">
          <ThreatHistory />
        </div>
      </section>

      <footer className="footer">
        <p>&copy; 2026 PhishGuard AI. All rights reserved.</p>
      </footer>

      <style jsx>{`
        .app-container { min-height:100vh; background:#05060a; color:white; padding-bottom:3rem; }
        .dash-hero { position:relative; padding:5rem 1rem 2rem; text-align:center; overflow:hidden; }
        .dash-hero-content { position:relative; z-index:10; }
        .page-badge { display:inline-block; padding:.3rem .8rem; background:rgba(79,172,254,.1); border:1px solid rgba(79,172,254,.2); border-radius:100px; color:#4facfe; font-size:.7rem; font-weight:800; text-transform:uppercase; letter-spacing:.1em; margin-bottom:1.5rem; }
        h1 { font-size:clamp(2rem,6vw,3.5rem); font-weight:900; line-height:1.1; letter-spacing:-.03em; margin-bottom:1rem; }
        .dash-sub { font-size:1rem; color:#94a3b8; max-width:500px; margin:0 auto; }
        .blob { position:absolute; width:400px; height:400px; border-radius:50%; filter:blur(80px); z-index:1; pointer-events:none; }
        .b1 { top:-80px; left:-80px; background:radial-gradient(circle,rgba(79,172,254,.12) 0%,transparent 70%); }
        .b2 { bottom:-80px; right:-80px; background:radial-gradient(circle,rgba(0,242,254,.1) 0%,transparent 70%); }

        .status-cards { display:grid; grid-template-columns:repeat(2,1fr); gap:1rem; margin-top:2rem; }
        @media(min-width:768px) { .status-cards { grid-template-columns:repeat(4,1fr); } }
        .scard { padding:1.5rem; border-radius:20px; display:flex; align-items:center; gap:1rem; transition:transform .2s,border-color .2s; }
        .scard:hover { transform:translateY(-2px); border-color:rgba(255,255,255,.2); }
        .scard-icon { width:44px; height:44px; border-radius:12px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
        .scard-icon svg { width:22px; height:22px; }
        .scard-info { display:flex; flex-direction:column; gap:.2rem; min-width:0; }
        .scard-label { font-size:.65rem; font-weight:800; text-transform:uppercase; letter-spacing:.1em; color:#64748b; }
        .scard-value { font-size:.9rem; font-weight:700; display:flex; align-items:center; gap:.4rem; }
        .status-dot { width:8px; height:8px; border-radius:50%; flex-shrink:0; }
        .status-dot.online { background:#43e97b; box-shadow:0 0 10px #43e97b; animation:pulse 2s ease-in-out infinite; }
        .status-dot.offline { background:#ff4e50; box-shadow:0 0 10px #ff4e50; }
        .scard-value.online { color:#43e97b; }
        .scard-value.offline { color:#ff4e50; }

        .history-section { margin-top:2.5rem; }
        .history-wrapper { padding:2rem; border-radius:24px; }

        .footer { margin-top:5rem; text-align:center; color:#475569; font-size:.875rem; }
        @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }
      `}</style>
    </main>
  );
}
