import { useState, useEffect } from 'react'
import SuperheroCard from './SuperheroCard'
import SuperheroDetail from './SuperheroDetail'
import heroService from '../services/heroService'
import './SuperheroGrid.css'

const SuperheroGrid = ({ searchQuery, selectedHero: propSelectedHero }) => {
  const [superheroes, setSuperheroes] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [likedHeroes, setLikedHeroes] = useState([])
  const [selectedHero, setSelectedHero] = useState(null)
  const [isSearching, setIsSearching] = useState(false)

  // Use heroService for all API calls; no hardcoded backend URL

  // Load liked heroes from database on component mount
  useEffect(() => {
    loadFavorites()
  }, [])

  const loadFavorites = async () => {
    try {
      const favorites = await heroService.getFavorites()
      const favoriteIds = favorites.map(hero => hero.id)
      setLikedHeroes(favoriteIds)
    } catch (error) {
      console.error('Error loading favorites:', error)
      // Fallback to localStorage if API fails
      const savedLikes = localStorage.getItem('likedHeroes')
      if (savedLikes) {
        setLikedHeroes(JSON.parse(savedLikes))
      }
    }
  }

  useEffect(() => {
    if (searchQuery && searchQuery.trim().length >= 3) {
      performSearch(searchQuery)
    } else {
      fetchSuperheroes()
    }
  }, [searchQuery])

  // Handle hero selection from search suggestions
  useEffect(() => {
    if (propSelectedHero) {
      // Fetch full hero details and show detail view
      fetchHeroDetail(propSelectedHero.id)
    }
  }, [propSelectedHero])

  const performSearch = async (query) => {
    try {
      setIsSearching(true)
      setLoading(true)
      setError(null)
      
      const response = await heroService.searchHeroes(query, { limit: 20 })
      setSuperheroes(response.heroes || [])
    } catch (err) {
      console.error('Error searching heroes:', err)
      setError('Failed to search superheroes. Please try again.')
    } finally {
      setLoading(false)
      setIsSearching(false)
    }
  }

  const fetchHeroDetail = async (heroId) => {
    try {
      const hero = await heroService.getHero(heroId)
      setSelectedHero(hero)
    } catch (err) {
      console.error('Error fetching hero detail:', err)
    }
  }

  useEffect(() => {
    fetchSuperheroes()
  }, [])

  const fetchSuperheroes = async () => {
    try {
      setLoading(true)
      setError(null)
      
      // Use the new hero service to get heroes
  const response = await heroService.getHeroes({ limit: 20 })
  setSuperheroes(response|| [])
  console.log("---###########----")
    console.log(superheroes)
    console.log("--eeeeeeeee")
    } catch (err) {
      console.error('Error fetching superheroes:', err)
      setError('Failed to load superheroes. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleLike = async (heroId) => {
    const isCurrentlyLiked = likedHeroes.includes(heroId)
    
    try {
      if (isCurrentlyLiked) {
        // Unlike - remove from favorites
        await heroService.removeFromFavorites(heroId)
        setLikedHeroes(prev => prev.filter(id => id !== heroId))
      } else {
        // Like - add to favorites
        await heroService.addToFavorites(heroId)
        setLikedHeroes(prev => [...prev, heroId])
      }
    } catch (error) {
      console.error('Error updating favorite:', error)
      
      // Show user-friendly error message
      if (error.response?.status === 401) {
        alert('Please log in to add favorites')
      } else if (error.response?.status === 400 && error.response?.data?.detail === 'already in favorites') {
        // Hero was already in favorites, update local state
        setLikedHeroes(prev => [...prev, heroId])
      } else {
        alert('Failed to update favorite. Please try again.')
      }
    }
  }

  const handleRetry = () => {
    if (searchQuery && searchQuery.trim().length >= 3) {
      performSearch(searchQuery)
    } else {
      fetchSuperheroes()
    }
  }

  // Show loading message based on context
  const getLoadingMessage = () => {
    if (isSearching) return 'Searching superheroes...'
    if (searchQuery) return 'Loading search results...'
    return 'Loading superheroes...'
  }

  // Show appropriate title
  const getTitle = () => {
    if (searchQuery && searchQuery.trim().length >= 3) {
      return `Search Results for "${searchQuery}"`
    }
    return 'Discover Superheroes'
  }

  const handleShowDetail = (hero) => {
    setSelectedHero(hero)
  }

  const handleBackToGrid = () => {
    setSelectedHero(null)
  }

  // If a hero is selected, show the detail view
  if (selectedHero) {
    return (
      <SuperheroDetail 
        hero={selectedHero} 
        onBack={handleBackToGrid}
        isLiked={likedHeroes.includes(selectedHero.id)}
        onLike={handleLike}
      />
    )
  }

  if (loading) {
    return (
      <div className="superhero-grid-container">
        <h2 className="grid-title">{getTitle()}</h2>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>{getLoadingMessage()}</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="superhero-grid-container">
        <h2 className="grid-title">{getTitle()}</h2>
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button onClick={handleRetry} className="retry-btn">
            Try Again
          </button>
        </div>
      </div>
    )
  }

  // Show no results message for search
  if (searchQuery && searchQuery.trim().length >= 3 && superheroes.length === 0 && !loading) {
    return (
      <div className="superhero-grid-container">
        <h2 className="grid-title">{getTitle()}</h2>
        <div className="no-results-container">
          <p className="no-results-message">
            No superheroes found for "{searchQuery}". Try a different search term.
          </p>
          <button onClick={() => window.location.reload()} className="retry-btn">
            View All Heroes
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="superhero-grid-container">
      <h2 className="grid-title">{getTitle()}</h2>
      {searchQuery && superheroes.length > 0 && (
        <p className="results-count">Found {superheroes.length} superheroes</p>
      )}
      <div 
        className="superhero-grid" 
        data-item-count={superheroes.length <= 3 ? superheroes.length : null}
      >
        {superheroes.map((hero) => (
          <SuperheroCard
            key={hero.id}
            hero={hero}
            isLiked={likedHeroes.includes(hero.id)}
            onLike={() => handleLike(hero.id)}
            onDetail={handleShowDetail}
          />
        ))}
      </div>
    </div>
  )
}

export default SuperheroGrid
