import { useState, useEffect } from 'react'
import Login from './components/login'
import Dashboard from './components/dashboard'
import OpenApp from './components/openapp'
import './App.css'
import api from './api'

function App() {
  const [showLogin, setShowLogin] = useState(false)
  const [user, setUser] = useState(null)
  const [isLoggedIn, setIsLoggedIn] = useState(false)

  // Check if user is already logged in on app start
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    const userData = localStorage.getItem('user')
    
    if (token && userData) {
      setUser(JSON.parse(userData))
      setIsLoggedIn(true)
    } else if (token) {
      // If we have token but no user data, logout to prevent issues
      handleLogout()
    }
  }, [])

  const handleLoginSuccess = (userData) => {
    setUser(userData)
    setIsLoggedIn(true)
    setShowLogin(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('user')
    setUser(null)
    setIsLoggedIn(false)
    setShowLogin(false)
  }

  return (
    <div>
      {isLoggedIn ? (
        <Dashboard user={user} onLogout={handleLogout} />
      ) : !showLogin ? (
        <OpenApp onGetStarted={() => setShowLogin(true)} />
      ) : (
        <Login onLoginSuccess={handleLoginSuccess} />
      )}
    </div> 
  )
}

export default App
