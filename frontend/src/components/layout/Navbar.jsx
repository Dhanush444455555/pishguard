import { Link, useLocation } from 'react-router-dom'
import { Shield, Activity, Search, Clock, Target, Server } from 'lucide-react'
import { motion } from 'framer-motion'
import './Navbar.css'

const navItems = [
  { name: 'Scan', to: '/scan', icon: Search },
  { name: 'Dashboard', to: '/dashboard', icon: Activity },
  { name: 'History', to: '/history', icon: Clock },
  { name: 'Similar', to: '/similar', icon: Target },
  { name: 'System', to: '/system', icon: Server },
]

export default function Navbar() {
  const { pathname } = useLocation()

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <div className="navbar-logo-icon">
            <Shield size={18} color="#4facfe" />
          </div>
          <span className="navbar-logo-text">
            PhishGuard <span>AI</span>
          </span>
        </Link>

        <div className="navbar-links">
          {navItems.map((item) => {
            const isActive = pathname === item.to
            return (
              <Link
                key={item.name}
                to={item.to}
                className={`navbar-link ${isActive ? 'active' : ''}`}
              >
                <item.icon size={15} />
                {item.name}
                {isActive && (
                  <motion.div
                    layoutId="nav-indicator"
                    className="navbar-indicator"
                    transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                  />
                )}
              </Link>
            )
          })}
        </div>

        <div className="navbar-status">
          <div className="navbar-status-dot">
            <span className="ping" />
            <span className="dot" />
          </div>
          <span className="navbar-status-text">OPERATIONAL</span>
        </div>
      </div>
    </nav>
  )
}
