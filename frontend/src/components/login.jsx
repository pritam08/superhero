import { useState } from 'react'
import axios from 'axios'
import './login.css'

const Login = ({ onLoginSuccess }) => {
  const [isLogin, setIsLogin] = useState(true)
  const [formData, setFormData] = useState({
    username: '',
    password: ''
  })
  const [errors, setErrors] = useState({})
  const [isLoading, setIsLoading] = useState(false)

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }))
    }
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.username.trim()) {
      newErrors.username = 'Username is required'
    } else if (formData.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters'
    }
    
    if (!formData.password.trim()) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters'
    }
    
    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (validateForm()) {
      setIsLoading(true)
      
      try {
        if (isLogin) {
          // Handle login - Send as form data for OAuth2PasswordRequestForm
          const loginFormData = new FormData()
          loginFormData.append('username', formData.username)
          loginFormData.append('password', formData.password)
          
          const response = await axios.post('http://127.0.0.1:8000/auth/login', loginFormData, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          })
          
          console.log('Login successful:', response.data)
          
          // Store token if provided by the API
          if (response.data.access_token) {
            localStorage.setItem('access_token', response.data.access_token)
            
            // Always store user info (create it if not provided by API)
            const userData = response.data.user || { username: formData.username, id: Date.now().toString() }
            localStorage.setItem('user', JSON.stringify(userData))
            
            // Call the success callback to update parent component
            if (onLoginSuccess) {
              onLoginSuccess(userData)
            }
          }
          
        } else {
          // Handle registration
          const response = await axios.post('http://127.0.0.1:8000/auth/register', {
            username: formData.username,
            password: formData.password
          })
          
          console.log('Registration successful:', response.data)
          alert('Registration successful!')
          
          // Optionally switch to login mode after successful registration
          setIsLogin(true)
        }
        
        // Reset form
        setFormData({ username: '', password: '' })
        setErrors({})
        
      } catch (error) {
        console.error('API Error:', error)
        
        if (error.response) {
          // Server responded with error status
          const status = error.response.status
          const errorData = error.response.data
          
          let errorMessage = ''
          
          if (isLogin) {
            // Handle specific login errors
            if (status === 401) {
              errorMessage = 'Invalid username or password. Please try again.'
            } else if (status === 404) {
              errorMessage = 'User not found. Please check your username or sign up.'
            } else if (status === 422) {
              errorMessage = 'Please enter valid credentials.'
            } else if (status === 429) {
              errorMessage = 'Too many login attempts. Please try again later.'
            } else {
              errorMessage = errorData?.detail || 
                           errorData?.message || 
                           'Login failed. Please try again.'
            }
          } else {
            // Handle registration errors
            if (status === 409 || status === 400) {
              errorMessage = errorData?.detail || 
                           errorData?.message || 
                           'Username already exists. Please choose a different username.'
            } else if (status === 422) {
              errorMessage = 'Please enter valid registration details.'
            } else {
              errorMessage = errorData?.detail || 
                           errorData?.message || 
                           'Registration failed. Please try again.'
            }
          }
          
          setErrors({ submit: errorMessage })
          
          // Clear any stored tokens on login failure
          if (isLogin && status === 401) {
            localStorage.removeItem('access_token')
            localStorage.removeItem('user')
          }
          
        } else if (error.request) {
          // Request was made but no response received
          setErrors({ submit: 'Network error. Please check your connection and try again.' })
        } else {
          // Something else happened
          setErrors({ submit: 'An unexpected error occurred. Please try again.' })
        }
      } finally {
        setIsLoading(false)
      }
    }
  }

  const toggleMode = () => {
    setIsLogin(!isLogin)
    setFormData({ username: '', password: '' })
    setErrors({})
  }

  return (
    <div className="auth-container">
      <div className="auth-card">
        <div className="auth-header">
          <h2 className="auth-title">
            {isLogin ? 'Welcome Back' : 'Join Us'}
          </h2>
          <p className="auth-subtitle">
            {isLogin 
              ? 'Sign in to your superhero account' 
              : 'Create your superhero account'
            }
          </p>
        </div>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="input-group">
            <label htmlFor="username" className="input-label">
              Username
            </label>
            <input
              type="text"
              id="username"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              className={`input-field ${errors.username ? 'input-error' : ''}`}
              placeholder="Enter your username"
            />
            {errors.username && (
              <span className="error-message">{errors.username}</span>
            )}
          </div>

          <div className="input-group">
            <label htmlFor="password" className="input-label">
              Password
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              className={`input-field ${errors.password ? 'input-error' : ''}`}
              placeholder="Enter your password"
            />
            {errors.password && (
              <span className="error-message">{errors.password}</span>
            )}
          </div>

          <button type="submit" className="submit-btn" disabled={isLoading}>
            {isLoading ? 'Processing...' : (isLogin ? 'Sign In' : 'Sign Up')}
          </button>
          
          {errors.submit && (
            <div className="submit-error">
              {errors.submit}
            </div>
          )}
        </form>

        <div className="auth-toggle">
          <p className="toggle-text">
            {isLogin 
              ? "Don't have an account? " 
              : "Already have an account? "
            }
            <button 
              type="button" 
              onClick={toggleMode}
              className="toggle-btn"
            >
              {isLogin ? 'Sign Up' : 'Sign In'}
            </button>
          </p>
        </div>
      </div>
    </div>
  )
}

export default Login