'use client';
import React, { useState } from 'react';

const UrlInput = () => {
  const [url, setUrl] = useState('');

  return (
    <div className="search-container">
      <div className="input-wrapper glass">
        <div className="icon-box">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9a9 9 0 01-9-9m9 9c1.657 0 3-4.03 3-9s-1.343-9-3-9m0 18c-1.657 0-3-4.03-3-9s1.343-9 3-9m-9 9a9 9 0 019-9" />
          </svg>
        </div>
        <input
          type="text"
          placeholder="Enter suspicious URL for deep analysis..."
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <button className="gradient-bg">
          <span>Analyze</span>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5">
            <path d="M13 10V3L4 14h7v7l9-11h-7z" />
          </svg>
        </button>
      </div>

      <div className="badges-row">
        <div className="badge"><span className="dot blue"></span> Hindsight Memory Active</div>
        <div className="badge"><span className="dot cyan"></span> CascadeFlow Routing</div>
        <div className="badge"><span className="dot purple"></span> Real-time Prediction</div>
      </div>

      <style jsx>{`
        .search-container {
          width: 100%;
          max-width: 800px;
          margin: 0 auto;
        }
        .input-wrapper {
          display: flex;
          align-items: center;
          padding: 0.5rem;
          border-radius: 20px;
          gap: 1rem;
          transition: border-color 0.3s, box-shadow 0.3s;
        }
        .input-wrapper:focus-within {
          border-color: rgba(79, 172, 254, 0.5);
          box-shadow: 0 0 30px rgba(79, 172, 254, 0.15);
        }
        .icon-box {
          padding-left: 1rem;
          display: flex;
          align-items: center;
          color: #64748b;
        }
        .icon-box svg {
          width: 20px;
          height: 20px;
        }
        input {
          flex: 1;
          background: transparent;
          border: none;
          outline: none;
          color: white;
          font-size: 1.125rem;
          padding: 0.75rem 0;
        }
        button {
          padding: 0.75rem 1.75rem;
          border-radius: 14px;
          border: none;
          color: white;
          font-weight: 700;
          display: flex;
          align-items: center;
          gap: 0.5rem;
          cursor: pointer;
          transition: transform 0.2s;
        }
        button:hover {
          transform: scale(1.02);
        }
        button svg {
          width: 16px;
          height: 16px;
        }
        .badges-row {
          display: flex;
          justify-content: center;
          gap: 1.5rem;
          margin-top: 1.5rem;
          flex-wrap: wrap;
        }
        .badge {
          display: flex;
          align-items: center;
          gap: 0.5rem;
          font-size: 0.75rem;
          font-weight: 600;
          color: #64748b;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        .dot {
          width: 6px;
          height: 6px;
          border-radius: 50%;
        }
        .dot.blue { background: #3b82f6; box-shadow: 0 0 8px #3b82f6; }
        .dot.cyan { background: #06b6d4; box-shadow: 0 0 8px #06b6d4; }
        .dot.purple { background: #a855f7; box-shadow: 0 0 8px #a855f7; }
      `}</style>
    </div>
  );
};

export default UrlInput;
