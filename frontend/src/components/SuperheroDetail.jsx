import { useState, useEffect } from 'react'
import heroService from '../services/heroService'
import './SuperheroDetail.css'

const SuperheroDetail = ({ hero, onBack, isLiked, onLike }) => {
  const [imageError, setImageError] = useState(false)
  const [liked, setLiked] = useState(false)
  const [updating, setUpdating] = useState(false)

  // Initialize liked state from props or fetch from API
  useEffect(() => {
    if (isLiked !== undefined) {
      setLiked(isLiked)
    } else {
      // Fetch user's favorites to check if this hero is liked
      checkIfLiked()
    }
  }, [hero.id, isLiked])

  const checkIfLiked = async () => {
    try {
      const favorites = await heroService.getFavorites()
      const isHeroLiked = favorites.some(fav => fav.id === hero.id)
      setLiked(isHeroLiked)
    } catch (error) {
      console.error('Error checking if hero is liked:', error)
      // Fallback to localStorage
      const savedLikes = localStorage.getItem('likedHeroes')
      if (savedLikes) {
        const likedHeroes = JSON.parse(savedLikes)
        setLiked(likedHeroes.includes(hero.id))
      }
    }
  }

  const handleLike = async () => {
    if (updating) return // Prevent double clicks
    
    setUpdating(true)
    
    if (onLike) {
      // Use parent's like handler if provided
      try {
        await onLike(hero.id)
        setLiked(!liked)
      } catch (error) {
        console.error('Error updating like via parent:', error)
      }
    } else {
      // Handle like/unlike directly
      try {
        if (liked) {
          await heroService.removeFromFavorites(hero.id)
        } else {
          await heroService.addToFavorites(hero.id)
        }
        setLiked(!liked)
      } catch (error) {
        console.error('Error updating favorite:', error)
        
        // Show user-friendly error messages
        if (error.response?.status === 401) {
          alert('Please log in to add favorites')
        } else if (error.response?.status === 400 && error.response?.data?.detail === 'already in favorites') {
          // Hero was already in favorites, update local state
          setLiked(true)
        } else {
          alert('Failed to update favorite. Please try again.')
        }
      }
    }
    
    setUpdating(false)
  }

  const handleImageError = () => {
    setImageError(true)
  }

  const handleImageLoad = () => {
    setImageError(false)
  }

  return (
    <div className="superhero-detail-container">
      <div className="detail-header">
        <button onClick={onBack} className="back-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
            <path d="m12 19-7-7 7-7"/>
            <path d="m19 12-7 7-7-7"/>
          </svg>
          Back to Heroes
        </button>
        <h1 className="detail-title">Hero Details</h1>
        <button 
          onClick={handleLike} 
          className={`detail-like-btn ${liked ? 'liked' : ''} ${updating ? 'updating' : ''}`}
          title={liked ? 'Remove from favorites' : 'Add to favorites'}
          disabled={updating}
        >
          {updating ? (
            <>
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 6v6l4 2"/>
              </svg>
              <span className="like-text">Updating...</span>
            </>
          ) : (
            <>
              <svg width="24" height="24" viewBox="0 0 24 24" fill={liked ? 'currentColor' : 'none'} stroke="currentColor" strokeWidth="2">
                <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
              </svg>
              <span className="like-text">{liked ? 'Liked' : 'Like'}</span>
            </>
          )}
        </button>
      </div>

      <div className="detail-content">
        <div className="detail-card">
          <div className="detail-image-section">
            {!imageError ? (
              <img
                src={hero.image?.url}
                alt={hero.name}
                className="detail-hero-image"
                onError={handleImageError}
                onLoad={handleImageLoad}
              />
            ) : (
              <div className="detail-image-placeholder">
                <span className="detail-placeholder-text">No Image Available</span>
              </div>
            )}
          </div>

          <div className="detail-info-section">
            <h2 className="detail-hero-name">{hero.name}</h2>
            
            {hero.biography?.['full-name'] && (
              <p className="detail-full-name">Real Name: {hero.biography['full-name']}</p>
            )}

            <div className="detail-section">
              <h3 className="section-title">Power Stats</h3>
              <div className="stats-grid">
                {hero.powerstats && Object.entries(hero.powerstats).map(([key, value]) => (
                  <div key={key} className="stat-item">
                    <span className="stat-name">{key.charAt(0).toUpperCase() + key.slice(1)}</span>
                    <div className="stat-bar">
                      <div 
                        className="stat-fill" 
                        style={{ width: `${value || 0}%` }}
                      ></div>
                      <span className="stat-number">{value || 'N/A'}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="detail-section">
              <h3 className="section-title">Biography</h3>
              <div className="bio-grid">
                {hero.biography?.publisher && (
                  <div className="bio-item">
                    <span className="bio-label">Publisher:</span>
                    <span className="bio-value">{hero.biography.publisher}</span>
                  </div>
                )}
                {hero.biography?.alignment && (
                  <div className="bio-item">
                    <span className="bio-label">Alignment:</span>
                    <span className="bio-value">{hero.biography.alignment}</span>
                  </div>
                )}
                {hero.biography?.['place-of-birth'] && (
                  <div className="bio-item">
                    <span className="bio-label">Place of Birth:</span>
                    <span className="bio-value">{hero.biography['place-of-birth']}</span>
                  </div>
                )}
                {hero.biography?.['first-appearance'] && (
                  <div className="bio-item">
                    <span className="bio-label">First Appearance:</span>
                    <span className="bio-value">{hero.biography['first-appearance']}</span>
                  </div>
                )}
              </div>
            </div>

            <div className="detail-section">
              <h3 className="section-title">Appearance</h3>
              <div className="appearance-grid">
                {hero.appearance?.gender && (
                  <div className="appearance-item">
                    <span className="appearance-label">Gender:</span>
                    <span className="appearance-value">{hero.appearance.gender}</span>
                  </div>
                )}
                {hero.appearance?.race && (
                  <div className="appearance-item">
                    <span className="appearance-label">Race:</span>
                    <span className="appearance-value">{hero.appearance.race}</span>
                  </div>
                )}
                {hero.appearance?.height && (
                  <div className="appearance-item">
                    <span className="appearance-label">Height:</span>
                    <span className="appearance-value">{hero.appearance.height.join(', ')}</span>
                  </div>
                )}
                {hero.appearance?.weight && (
                  <div className="appearance-item">
                    <span className="appearance-label">Weight:</span>
                    <span className="appearance-value">{hero.appearance.weight.join(', ')}</span>
                  </div>
                )}
                {hero.appearance?.['eye-color'] && (
                  <div className="appearance-item">
                    <span className="appearance-label">Eye Color:</span>
                    <span className="appearance-value">{hero.appearance['eye-color']}</span>
                  </div>
                )}
                {hero.appearance?.['hair-color'] && (
                  <div className="appearance-item">
                    <span className="appearance-label">Hair Color:</span>
                    <span className="appearance-value">{hero.appearance['hair-color']}</span>
                  </div>
                )}
              </div>
            </div>

            {hero.work && (
              <div className="detail-section">
                <h3 className="section-title">Work</h3>
                <div className="work-grid">
                  {hero.work.occupation && (
                    <div className="work-item">
                      <span className="work-label">Occupation:</span>
                      <span className="work-value">{hero.work.occupation}</span>
                    </div>
                  )}
                  {hero.work.base && hero.work.base !== '-' && (
                    <div className="work-item">
                      <span className="work-label">Base:</span>
                      <span className="work-value">{hero.work.base}</span>
                    </div>
                  )}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}

export default SuperheroDetail
