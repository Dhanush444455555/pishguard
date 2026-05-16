'use client';

import React, { useState, useCallback } from 'react';
import Navbar from '../../components/Navbar';
import UrlInput from '../../components/UrlInput';
import RiskMeter from '../../components/RiskMeter';
import ThreatCard from '../../components/ThreatCard';
import { analyzeUrl, AnalysisResult } from '../../services/api';

type ScanState = 'idle' | 'scanning' | 'done' | 'error';

export default function ScanPage() {
  const [scanState, setScanState] = useState<ScanState>('idle');
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [errorMsg, setErrorMsg] = useState('');
  const [inputUrl, setInputUrl] = useState('');

  const handleScan = useCallback(async () => {
    const trimmed = inputUrl.trim();
    if (!trimmed) return;

    setScanState('scanning');
    setErrorMsg('');
    setResult(null);

    try {
      const data = await analyzeUrl(trimmed);
      setResult(data);
      setScanState('done');
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'An unexpected error occurred.';
      setErrorMsg(message);
      setScanState('error');
    }
  }, [inputUrl]);

  return (
    <main className="app-container">
      <Navbar />

      <section className="scan-hero">
        <div className="scan-hero-content">
          <div className="page-badge">URL Analyzer</div>
          <h1>Scan a <span className="gradient-text">Suspicious URL</span></h1>
          <p className="scan-sub">
            Enter any URL below to run a deep AI-powered phishing analysis.
          </p>
        </div>
        <div className="blob b1"></div>
        <div className="blob b2"></div>
      </section>

      {/* Custom URL Input with scan trigger */}
      <section className="scan-input-section container">
        <div className="custom-input glass">
          <div className="icon-box">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
            </svg>
          </div>
          <input
            type="text"
            placeholder="Enter suspicious URL for deep analysis..."
            value={inputUrl}
            onChange={(e) => setInputUrl(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleScan()}
            disabled={scanState === 'scanning'}
          />
          <button
            className="gradient-bg scan-btn"
            onClick={handleScan}
            disabled={scanState === 'scanning' || !inputUrl.trim()}
          >
            {scanState === 'scanning' ? (
              <>
                <span className="spinner"></span>
                <span>Analyzing...</span>
              </>
            ) : (
              <>
                <span>Analyze</span>
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
                  <path d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
              </>
            )}
          </button>
        </div>

        <div className="badges-row">
          <div className="badge"><span className="dot blue"></span> Hindsight Memory Active</div>
          <div className="badge"><span className="dot cyan"></span> CascadeFlow Routing</div>
          <div className="badge"><span className="dot purple"></span> Real-time Prediction</div>
        </div>
      </section>

      {/* Error State */}
      {scanState === 'error' && (
        <section className="container error-section">
          <div className="error-card glass">
            <svg viewBox="0 0 24 24" fill="none" stroke="#ff4e50" strokeWidth="2">
              <circle cx="12" cy="12" r="10" />
              <line x1="15" y1="9" x2="9" y2="15" />
              <line x1="9" y1="9" x2="15" y2="15" />
            </svg>
            <p>{errorMsg}</p>
            <button onClick={handleScan} className="gradient-bg retry-btn">Retry</button>
          </div>
        </section>
      )}

      {/* Scanning Animation */}
      {scanState === 'scanning' && (
        <section className="container scanning-section">
          <div className="scanning-card glass">
            <div className="scan-anim">
              <div className="ring r1"></div>
              <div className="ring r2"></div>
              <div className="ring r3"></div>
              <svg viewBox="0 0 24 24" fill="none" stroke="#4facfe" strokeWidth="2" className="shield-icon">
                <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
              </svg>
            </div>
            <h3>Analyzing URL...</h3>
            <p className="scan-detail">Running through CascadeFlow AI pipeline</p>
          </div>
        </section>
      )}

      {/* Results */}
      {scanState === 'done' && result && (
        <section className="results-grid container">
          <div className="res-left">
            <div className="scanned-url glass">
              <span className="url-label">Scanned URL</span>
              <span className="url-value">{result.url}</span>
            </div>
            <RiskMeter score={result.probability} />
          </div>
          <div className="res-right">
            <ThreatCard />
          </div>
        </section>
      )}

      <style jsx>{`
        .app-container { min-height:100vh; background:#05060a; color:white; padding-bottom:4rem; }
        .scan-hero { position:relative; padding:5rem 1rem 2rem; text-align:center; overflow:hidden; }
        .scan-hero-content { position:relative; z-index:10; }
        .page-badge { display:inline-block; padding:.3rem .8rem; background:rgba(79,172,254,.1); border:1px solid rgba(79,172,254,.2); border-radius:100px; color:#4facfe; font-size:.7rem; font-weight:800; text-transform:uppercase; letter-spacing:.1em; margin-bottom:1.5rem; }
        h1 { font-size:clamp(2rem,6vw,3.5rem); font-weight:900; line-height:1.1; letter-spacing:-.03em; margin-bottom:1rem; }
        .scan-sub { font-size:1rem; color:#94a3b8; max-width:500px; margin:0 auto; }
        .blob { position:absolute; width:400px; height:400px; border-radius:50%; filter:blur(80px); z-index:1; pointer-events:none; }
        .b1 { top:-80px; left:-80px; background:radial-gradient(circle,rgba(79,172,254,.12) 0%,transparent 70%); }
        .b2 { bottom:-80px; right:-80px; background:radial-gradient(circle,rgba(0,242,254,.1) 0%,transparent 70%); }

        .scan-input-section { margin-top:2rem; max-width:800px; }
        .custom-input { display:flex; align-items:center; padding:.5rem; border-radius:20px; gap:1rem; transition:border-color .3s,box-shadow .3s; }
        .custom-input:focus-within { border-color:rgba(79,172,254,.5); box-shadow:0 0 30px rgba(79,172,254,.15); }
        .icon-box { padding-left:1rem; display:flex; align-items:center; color:#64748b; }
        .icon-box svg { width:20px; height:20px; }
        input { flex:1; background:transparent; border:none; outline:none; color:white; font-size:1.125rem; padding:.75rem 0; }
        input:disabled { opacity:.5; }
        .scan-btn { padding:.75rem 1.75rem; border-radius:14px; border:none; color:white; font-weight:700; display:flex; align-items:center; gap:.5rem; cursor:pointer; transition:transform .2s; font-size:.95rem; }
        .scan-btn:hover:not(:disabled) { transform:scale(1.02); }
        .scan-btn:disabled { opacity:.6; cursor:not-allowed; }
        .scan-btn svg { width:16px; height:16px; }
        .spinner { width:16px; height:16px; border:2px solid rgba(255,255,255,.3); border-top-color:white; border-radius:50%; animation:spin .6s linear infinite; }

        .badges-row { display:flex; justify-content:center; gap:1.5rem; margin-top:1.5rem; flex-wrap:wrap; }
        .badge { display:flex; align-items:center; gap:.5rem; font-size:.75rem; font-weight:600; color:#64748b; text-transform:uppercase; letter-spacing:.05em; }
        .dot { width:6px; height:6px; border-radius:50%; }
        .dot.blue { background:#3b82f6; box-shadow:0 0 8px #3b82f6; }
        .dot.cyan { background:#06b6d4; box-shadow:0 0 8px #06b6d4; }
        .dot.purple { background:#a855f7; box-shadow:0 0 8px #a855f7; }

        .error-section { margin-top:2rem; max-width:600px; }
        .error-card { padding:2rem; border-radius:20px; text-align:center; display:flex; flex-direction:column; align-items:center; gap:1rem; border-color:rgba(255,78,80,.2); }
        .error-card svg { width:40px; height:40px; }
        .error-card p { color:#ff8a8c; font-size:.9rem; }
        .retry-btn { padding:.5rem 1.5rem; border:none; border-radius:10px; color:white; font-weight:700; cursor:pointer; font-size:.85rem; }

        .scanning-section { margin-top:3rem; max-width:500px; }
        .scanning-card { padding:3rem 2rem; border-radius:24px; text-align:center; display:flex; flex-direction:column; align-items:center; }
        .scan-anim { position:relative; width:100px; height:100px; margin-bottom:1.5rem; }
        .ring { position:absolute; inset:0; border:2px solid rgba(79,172,254,.15); border-radius:50%; }
        .r1 { animation:ping 1.5s cubic-bezier(0,0,.2,1) infinite; }
        .r2 { animation:ping 1.5s cubic-bezier(0,0,.2,1) infinite .3s; }
        .r3 { animation:ping 1.5s cubic-bezier(0,0,.2,1) infinite .6s; }
        .shield-icon { position:absolute; top:50%; left:50%; transform:translate(-50%,-50%); width:36px; height:36px; }
        .scanning-card h3 { font-size:1.125rem; font-weight:700; margin-bottom:.5rem; }
        .scan-detail { font-size:.8rem; color:#64748b; }

        .results-grid { display:grid; grid-template-columns:1fr; gap:2rem; margin-top:3rem; }
        @media(min-width:1024px) { .results-grid { grid-template-columns:1fr 1.5fr; } }
        .res-left { display:flex; flex-direction:column; gap:1.5rem; }
        .scanned-url { padding:1.25rem 1.5rem; border-radius:16px; display:flex; flex-direction:column; gap:.25rem; }
        .url-label { font-size:.65rem; font-weight:800; text-transform:uppercase; letter-spacing:.1em; color:#64748b; }
        .url-value { font-size:.9rem; font-weight:600; color:#cbd5e1; word-break:break-all; }

        @keyframes spin { to { transform:rotate(360deg); } }
        @keyframes ping { 75%,100% { transform:scale(2); opacity:0; } }
      `}</style>
    </main>
  );
}
