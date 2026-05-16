'use client';
import React from 'react';

const Navbar = () => {
  return (
    <nav className="navbar glass">
      <div className="nav-container">
        <div className="logo-section">
          <div className="logo-icon gradient-bg">
            <svg viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2.5">
              <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
            </svg>
          </div>
          <span className="logo-text">
            Phish<span className="gradient-text">Guard AI</span>
          </span>
        </div>

        <div className="nav-links">
          <a href="#">Analyzer</a>
          <a href="#">Hindsight</a>
          <a href="#">CascadeFlow</a>
          <a href="#">Docs</a>
        </div>

        <div className="nav-actions">
          <div className="status-badge">
            <div className="status-dot animate-pulse"></div>
            <span>System Online</span>
          </div>
          <button className="cta-button gradient-bg">Get Started</button>
        </div>
      </div>

      <style jsx>{`
        .navbar {
          position: sticky;
          top: 0;
          z-index: 100;
          width: 100%;
          padding: 1rem 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }
        .nav-container {
          max-width: 1280px;
          margin: 0 auto;
          padding: 0 1.5rem;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }
        .logo-section {
          display: flex;
          align-items: center;
          gap: 0.75rem;
        }
        .logo-icon {
          width: 40px;
          height: 40px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
          box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        }
        .logo-icon svg {
          width: 24px;
          height: 24px;
        }
        .logo-text {
          font-size: 1.25rem;
          font-weight: 800;
          letter-spacing: -0.02em;
        }
        .nav-links {
          display: none;
        }
        @media (min-width: 768px) {
          .nav-links {
            display: flex;
            gap: 2rem;
          }
        }
        .nav-links a {
          color: #94a3b8;
          text-decoration: none;
          font-size: 0.875rem;
          font-weight: 500;
          transition: color 0.2s;
        }
        .nav-links a:hover {
          color: white;
        }
        .nav-actions {
          display: flex;
          align-items: center;
          gap: 1.5rem;
        }
        .status-badge {
          display: none;
          align-items: center;
          gap: 0.5rem;
          background: rgba(255, 255, 255, 0.05);
          padding: 0.4rem 0.8rem;
          border-radius: 100px;
          border: 1px solid rgba(255, 255, 255, 0.1);
        }
        @media (min-width: 640px) {
          .status-badge {
            display: flex;
          }
        }
        .status-dot {
          width: 8px;
          height: 8px;
          background: #43e97b;
          border-radius: 50%;
          box-shadow: 0 0 10px #43e97b;
        }
        .status-badge span {
          font-size: 0.75rem;
          color: #43e97b;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }
        .cta-button {
          padding: 0.6rem 1.25rem;
          border-radius: 100px;
          color: white;
          font-size: 0.875rem;
          font-weight: 700;
          border: none;
          cursor: pointer;
          transition: transform 0.2s, box-shadow 0.2s;
          box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        }
        .cta-button:hover {
          transform: translateY(-1px);
          box-shadow: 0 6px 20px rgba(79, 172, 254, 0.4);
        }
      `}</style>
    </nav>
  );
};

export default Navbar;
