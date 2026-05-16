'use client';

import React from 'react';
import Link from 'next/link';
import Navbar from '../components/Navbar';

export default function Home() {
  return (
    <main className="app-container">
      <Navbar />

      <section className="hero">
        <div className="hero-content">
          <div className="badge-main">AI-Powered Cybersecurity</div>
          <h1>
            Stop Phishing <br />
            <span className="gradient-text">Before It Strikes.</span>
          </h1>
          <p className="hero-sub">
            PhishGuard AI uses intelligent Hindsight memory and CascadeFlow
            routing to detect zero-day threats with unprecedented precision.
          </p>

          <div className="cta-group">
            <Link href="/scan" className="hero-cta gradient-bg">
              <span>Start Scanning</span>
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                <path d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            </Link>
            <Link href="/dashboard" className="hero-cta-secondary">
              View Dashboard
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path d="M9 5l7 7-7 7" />
              </svg>
            </Link>
          </div>
        </div>

        <div className="blob blob-1"></div>
        <div className="blob blob-2"></div>
        <div className="blob blob-3"></div>
      </section>

      <section className="features container">
        <div className="features-grid">
          {[
            { icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z', title: 'Hindsight Memory', desc: 'Learns from every scan to build an evolving threat intelligence database.', bg: 'rgba(79,172,254,0.1)', fg: '#4facfe' },
            { icon: 'M13 10V3L4 14h7v7l9-11h-7z', title: 'CascadeFlow Routing', desc: 'Dynamically routes analysis through optimal AI models based on complexity.', bg: 'rgba(0,242,254,0.1)', fg: '#00f2fe' },
            { icon: 'M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z', title: 'Real-time Detection', desc: 'Sub-second analysis with 98%+ accuracy using multi-layered neural networks.', bg: 'rgba(168,85,247,0.1)', fg: '#a855f7' },
          ].map((f, i) => (
            <div key={i} className="feature-card glass">
              <div className="feature-icon" style={{ background: f.bg, color: f.fg }}>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d={f.icon} /></svg>
              </div>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="stats-section container">
        <div className="stats-grid">
          {[
            { val: '98.4%', label: 'Detection Accuracy' },
            { val: '<240ms', label: 'Avg Response Time' },
            { val: '12M+', label: 'Threats Blocked' },
            { val: '24/7', label: 'Active Monitoring' },
          ].map((s, i) => (
            <div key={i} className="stat-card">
              <span className="stat-value gradient-text">{s.val}</span>
              <span className="stat-label">{s.label}</span>
            </div>
          ))}
        </div>
      </section>

      <footer className="footer">
        <p>&copy; 2026 PhishGuard AI. All rights reserved.</p>
      </footer>

      <style jsx>{`
        .app-container { min-height:100vh; background:#05060a; color:white; padding-bottom:3rem; }
        .hero { position:relative; padding:8rem 1rem 6rem; text-align:center; overflow:hidden; }
        .hero-content { position:relative; z-index:10; max-width:900px; margin:0 auto; }
        .badge-main { display:inline-block; padding:.4rem 1rem; background:rgba(79,172,254,.1); border:1px solid rgba(79,172,254,.2); border-radius:100px; color:#4facfe; font-size:.75rem; font-weight:800; text-transform:uppercase; letter-spacing:.1em; margin-bottom:2rem; animation:fadeInDown .6s ease-out; }
        h1 { font-size:clamp(2.5rem,8vw,4.5rem); font-weight:900; line-height:1.1; letter-spacing:-.03em; margin-bottom:1.5rem; animation:fadeInUp .6s ease-out .1s both; }
        .hero-sub { font-size:1.125rem; color:#94a3b8; max-width:600px; margin:0 auto 3rem; line-height:1.6; animation:fadeInUp .6s ease-out .2s both; }
        .cta-group { display:flex; align-items:center; justify-content:center; gap:1.25rem; flex-wrap:wrap; animation:fadeInUp .6s ease-out .3s both; }
        .hero-cta { display:inline-flex; align-items:center; gap:.6rem; padding:.9rem 2rem; border-radius:100px; color:white; font-size:1rem; font-weight:700; text-decoration:none; transition:transform .2s,box-shadow .2s; box-shadow:0 4px 25px rgba(79,172,254,.35); }
        .hero-cta:hover { transform:translateY(-2px); box-shadow:0 8px 35px rgba(79,172,254,.5); }
        .hero-cta svg { width:18px; height:18px; }
        .hero-cta-secondary { display:inline-flex; align-items:center; gap:.5rem; padding:.9rem 2rem; border-radius:100px; color:#94a3b8; font-size:1rem; font-weight:600; text-decoration:none; border:1px solid rgba(255,255,255,.1); background:rgba(255,255,255,.03); transition:all .2s; }
        .hero-cta-secondary:hover { color:white; border-color:rgba(255,255,255,.25); }
        .hero-cta-secondary svg { width:16px; height:16px; }
        .blob { position:absolute; width:500px; height:500px; border-radius:50%; filter:blur(80px); z-index:1; pointer-events:none; }
        .blob-1 { top:-100px; left:-100px; background:radial-gradient(circle,rgba(79,172,254,.15) 0%,transparent 70%); }
        .blob-2 { bottom:-100px; right:-100px; background:radial-gradient(circle,rgba(0,242,254,.12) 0%,transparent 70%); }
        .blob-3 { top:50%; left:50%; transform:translate(-50%,-50%); width:700px; height:700px; background:radial-gradient(circle,rgba(168,85,247,.06) 0%,transparent 70%); }
        .features { margin-top:2rem; }
        .features-grid { display:grid; grid-template-columns:1fr; gap:1.5rem; }
        @media(min-width:768px) { .features-grid { grid-template-columns:repeat(3,1fr); } }
        .feature-card { padding:2rem; border-radius:24px; transition:transform .25s,border-color .25s; }
        .feature-card:hover { transform:translateY(-4px); border-color:rgba(255,255,255,.2); }
        .feature-icon { width:48px; height:48px; border-radius:14px; display:flex; align-items:center; justify-content:center; margin-bottom:1.25rem; }
        .feature-icon svg { width:24px; height:24px; }
        .feature-card h3 { font-size:1.125rem; font-weight:700; margin-bottom:.5rem; }
        .feature-card p { font-size:.875rem; color:#94a3b8; line-height:1.6; }
        .stats-section { margin-top:5rem; }
        .stats-grid { display:grid; grid-template-columns:repeat(2,1fr); gap:1.5rem; }
        @media(min-width:768px) { .stats-grid { grid-template-columns:repeat(4,1fr); } }
        .stat-card { text-align:center; padding:2rem 1rem; }
        .stat-value { display:block; font-size:2.5rem; font-weight:900; letter-spacing:-.03em; line-height:1; margin-bottom:.5rem; }
        .stat-label { font-size:.8rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:.05em; }
        .footer { margin-top:6rem; text-align:center; color:#475569; font-size:.875rem; }
        @keyframes fadeInDown { from{opacity:0;transform:translateY(-20px)} to{opacity:1;transform:translateY(0)} }
        @keyframes fadeInUp { from{opacity:0;transform:translateY(20px)} to{opacity:1;transform:translateY(0)} }
      `}</style>
    </main>
  );
}
