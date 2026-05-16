import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Navbar from './components/layout/Navbar.jsx'
import Home from './pages/Home.jsx'
import Scan from './pages/Scan.jsx'
import Dashboard from './pages/Dashboard.jsx'
import History from './pages/History.jsx'
import Similar from './pages/Similar.jsx'
import System from './pages/System.jsx'

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-cyber-base text-foreground cyber-grid-bg relative">
        <Navbar />
        <main className="relative z-10 min-h-[calc(100vh-4rem)]">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/scan" element={<Scan />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/history" element={<History />} />
            <Route path="/similar" element={<Similar />} />
            <Route path="/system" element={<System />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  )
}

export default App
