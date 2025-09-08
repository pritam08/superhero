import { useState, useEffect } from 'react'
import SuperheroCard from './SuperheroCard'
import SuperheroDetail from './SuperheroDetail'
import heroService from '../services/heroService'
import './SuperheroGrid.css'

const FavoritesPage = () => {
  const [favorites, setFavorites] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [selectedHero, setSelectedHero] = useState(null)

  useEffect(() => {
    loadFavorites()
  }, [])

  const loadFavorites = async () => {
    try {
      setLoading(true)
      const favoritesData = await heroService.getFavorites()
      setFavorites(favoritesData)
      setError(null)
    } catch (err) {
      console.error('Error loading favorites:', err)
      if (err.response?.status === 401) {
        setError('Please log in to view your favorites.')
      } else {
        setError('Failed to load favorites. Please try again.')
      }
    } finally {
      setLoading(false)
    }
  }

  const handleLike = async (heroId) => {
    try {
      await heroService.removeFromFavorites(heroId)
      // Remove from local state
      setFavorites(prev => prev.filter(hero => hero.id !== heroId))
    } catch (error) {
      console.error('Error removing from favorites:', error)
      alert('Failed to remove from favorites. Please try again.')
    }
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
        isLiked={true} // All heroes in favorites are liked
        onLike={handleLike}
      />
    )
  }

  if (loading) {
    return (
      <div className="superhero-grid-container">
        <h2 className="grid-title">My Favorite Heroes</h2>
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p>Loading your favorites...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="superhero-grid-container">
        <h2 className="grid-title">My Favorite Heroes</h2>
        <div className="error-container">
          <p className="error-message">{error}</p>
          <button onClick={loadFavorites} className="retry-btn">
            Try Again
          </button>
        </div>
      </div>
    )
  }

  if (favorites.length === 0) {
    return (
      <div className="superhero-grid-container">
        <h2 className="grid-title">My Favorite Heroes</h2>
        <div className="no-results-container">
          <p className="no-results-message">
            You haven't added any heroes to your favorites yet.
          </p>
          <p className="no-results-message">
            Start exploring and click the heart icon to add heroes you like!
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="superhero-grid-container">
      <h2 className="grid-title">My Favorite Heroes</h2>
      <p className="results-count">You have {favorites.length} favorite heroes</p>
      <div 
        className="superhero-grid" 
        data-item-count={favorites.length <= 3 ? favorites.length : null}
      >
        {favorites.map((hero) => (
          <SuperheroCard
            key={hero.id}
            hero={hero}
            isLiked={true} // All heroes in favorites are liked
            onLike={() => handleLike(hero.id)}
            onDetail={handleShowDetail}
          />
        ))}
      </div>
    </div>
  )
}

export default FavoritesPage
