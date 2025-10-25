import React, { createContext, useContext, useState, useEffect, useMemo } from 'react'
import PropTypes from 'prop-types'
import { api } from '../utils/api'

const AuthContext = createContext()

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [token, setToken] = useState(localStorage.getItem('token'))

  // Set up axios interceptor for token
  useEffect(() => {
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`
    } else {
      delete api.defaults.headers.common['Authorization']
    }
  }, [token])

  // Check if user is authenticated on app load
  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const response = await api.get('/users/me')
          setUser(response.data)
        } catch (error) {
          console.error('Auth check failed:', error)
          localStorage.removeItem('token')
          setToken(null)
        }
      }
      setLoading(false)
    }

    checkAuth()
  }, [token])

  const login = async (username, password) => {
    try {
      console.log('Attempting login for:', username)
      const response = await api.post('/auth/login', { username, password })
      const { access_token } = response.data
      
      localStorage.setItem('token', access_token)
      setToken(access_token)
      
      // Get user info
      const userResponse = await api.get('/users/me')
      setUser(userResponse.data)
      
      console.log('Login successful for:', username)
      return { success: true }
    } catch (error) {
      console.error('Login error:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Login failed' 
      }
    }
  }

  const signup = async (username, email, password) => {
    try {
      console.log('Attempting signup for:', username, email)
      await api.post('/auth/signup', { username, email, password })
      console.log('Signup successful for:', username)
      return { success: true }
    } catch (error) {
      console.error('Signup error:', error)
      return { 
        success: false, 
        error: error.response?.data?.detail || 'Signup failed' 
      }
    }
  }

  const logout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
  }

  const value = useMemo(() => ({
    user,
    token,
    login,
    signup,
    logout,
    loading
  }), [user, token, login, signup, logout, loading])

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  )
}

AuthProvider.propTypes = {
  children: PropTypes.node.isRequired
}
