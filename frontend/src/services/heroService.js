import axios from 'axios'

// Use environment variable or default to development URL
const API_BASE_URL = process.env.NODE_ENV === 'production' 
  ? '/api'  // In production (Docker), use nginx proxy
  : 'http://127.0.0.1:8000'  // In development, direct backend connection

// Create axios instance with auth interceptor
const api = axios.create({
  baseURL: API_BASE_URL,
})

// Add token to requests automatically
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const heroService = {
  // Get search suggestions for autocomplete
  async getSearchSuggestions(query, limit = 10) {
    try {
      const response = await api.get('/heroes/search/suggestions', {
        params: { q: query, limit }
      })
      return response.data
    } catch (error) {
      console.error('Error fetching suggestions:', error)
      throw error
    }
  },

  // Enhanced search with multiple fields
  async searchHeroes(query, options = {}) {
    const { limit = 20, skip = 0, alignment } = options
    try {
      const params = { q: query, limit, skip }
      if (alignment) params.alignment = alignment
      
      const response = await api.get('/heroes/search', { params })
      return response.data
    } catch (error) {
      console.error('Error searching heroes:', error)
      throw error
    }
  },

  // Get all heroes (existing functionality)
  async getHeroes(options = {}) {
    const { q, limit = 30, skip = 0, alignment } = options
    try {
      const params = { limit, skip }
      if (q) params.q = q
      if (alignment) params.alignment = alignment
      
      const response = await api.get('/heroes', { params })
      return response.data
    } catch (error) {
      console.error('Error fetching heroes:', error)
      throw error
    }
  },

  // Get single hero
  async getHero(heroId) {
    try {
      const response = await api.get(`/heroes/${heroId}`)
      return response.data
    } catch (error) {
      console.error('Error fetching hero:', error)
      throw error
    }
  },

  // Get hero image
  async getHeroImage(heroId) {
    try {
      const response = await api.get(`/heroes/image/${heroId}`)
      return response.data
    } catch (error) {
      console.error('Error fetching hero image:', error)
      throw error
    }
  },

  // Update hero
  async updateHero(heroId, data) {
    try {
      const response = await api.put(`/heroes/${heroId}`, data)
      return response.data
    } catch (error) {
      console.error('Error updating hero:', error)
      throw error
    }
  },

  // Add hero to favorites
  async addToFavorites(heroId) {
    try {
      const response = await api.post(`/users/favorites/${heroId}`)
      return response.data
    } catch (error) {
      console.error('Error adding to favorites:', error)
      throw error
    }
  },

  // Remove hero from favorites
  async removeFromFavorites(heroId) {
    try {
      const response = await api.delete(`/users/favorites/${heroId}`)
      return response.data
    } catch (error) {
      console.error('Error removing from favorites:', error)
      throw error
    }
  },

  // Get user's favorite heroes
  async getFavorites() {
    try {
      const response = await api.get('/users/favorites')
      return response.data
    } catch (error) {
      console.error('Error fetching favorites:', error)
      throw error
    }
  },

  // Get current user info
  async getCurrentUser() {
    try {
      const response = await api.get('/users/me')
      return response.data
    } catch (error) {
      console.error('Error fetching current user:', error)
      throw error
    }
  }
}

export default heroService
