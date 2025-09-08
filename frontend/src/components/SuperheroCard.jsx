import { useState } from 'react'
import './SuperheroCard.css'

const SuperheroCard = ({ hero, isLiked, onLike, onDetail }) => {
  const [imageError, setImageError] = useState(false)

  const handleImageError = () => {
    setImageError(true)
  }

  const handleImageLoad = () => {
    setImageError(false)
  }

  return (
    <div className="superhero-card">
      <div className="card-image-container">
        {!imageError ? (
          <img
            src={hero.image?.url}
            alt={hero.name}
            className="hero-image"
            onError={handleImageError}
            onLoad={handleImageLoad}
          />
        ) : (
          <div className="image-placeholder">
            <span className="placeholder-text">No Image</span>
          </div>
        )}
        
        <button
          className={`like-btn ${isLiked ? 'liked' : ''}`}
          onClick={onLike}
          aria-label={isLiked ? 'Unlike' : 'Like'}
        >
          <svg
            width="20"
            height="20"
            viewBox="0 0 24 24"
            fill={isLiked ? '#ef4444' : 'none'}
            stroke={isLiked ? '#ef4444' : 'currentColor'}
            strokeWidth="2"
          >
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
          </svg>
        </button>
      </div>
      
      <div className="card-content">
        <h3 className="hero-name">{hero.name}</h3>
        
        <div className="hero-stats">
          {hero.powerstats && (
            <>
              <div className="stat">
                <span className="stat-label">Intelligence:</span>
                <span className="stat-value">{hero.powerstats.intelligence || 'N/A'}</span>
              </div>
              <div className="stat">
                <span className="stat-label">Strength:</span>
                <span className="stat-value">{hero.powerstats.strength || 'N/A'}</span>
              </div>
            </>
          )}
        </div>
        
        {hero.biography?.publisher && (
          <p className="hero-publisher">{hero.biography.publisher}</p>
        )}
        
        <button 
          onClick={() => onDetail(hero)}
          className="detail-btn"
        >
          Detail
        </button>
      </div>
    </div>
  )
}

export default SuperheroCard
