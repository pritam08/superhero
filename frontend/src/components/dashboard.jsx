import { useState } from 'react'
import SuperheroGrid from './SuperheroGrid'
import SearchBar from './SearchBar'
import FavoritesPage from './FavoritesPage'
import Teams from './Teams'
import './dashboard.css'

const Dashboard = ({ user, onLogout }) => {
  const [searchQuery, setSearchQuery] = useState('')
  const [selectedHero, setSelectedHero] = useState(null)
  const [currentView, setCurrentView] = useState('home') // 'home', 'favorites', or 'teams'

  const handleSearch = (query) => {
    setSearchQuery(query)
    setSelectedHero(null) // Reset selected hero when searching
    setCurrentView('home') // Switch to home view when searching
  }

  const handleHeroSelect = (hero) => {
    setSelectedHero(hero)
    setCurrentView('home') // Switch to home view when hero is selected
    // You can navigate to hero detail or show more info
    console.log('Selected hero:', hero)
  }

  const handleViewChange = (view) => {
    setCurrentView(view)
    setSearchQuery('') // Clear search when changing views
    setSelectedHero(null) // Clear selected hero when changing views
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-all-in-one">
          <h1>Find <span className="text-gradient">Superhero</span> Details</h1>
          
          <div className="nav-buttons-compact">
            <button 
              onClick={() => handleViewChange('home')} 
              className={`nav-btn ${currentView === 'home' ? 'active' : ''}`}
            >
              🏠 Home
            </button>
            <button 
              onClick={() => handleViewChange('favorites')} 
              className={`nav-btn ${currentView === 'favorites' ? 'active' : ''}`}
            >
              ❤️ Favorites
            </button>
            <button 
              onClick={() => handleViewChange('teams')} 
              className={`nav-btn ${currentView === 'teams' ? 'active' : ''}`}
            >
              👥 Teams
            </button>
          </div>
        </div>
        
        {/* Search Bar Row - only show on home view */}
        {currentView === 'home' && (
          <div className="search-row">
            <div className="search-section-full">
              <SearchBar 
                onSearch={handleSearch}
                onHeroSelect={handleHeroSelect}
                placeholder="Search heroes..."
              />
            </div>
          </div>
        )}
      </header>
      <main className="main-content">
        {currentView === 'home' ? (
          <SuperheroGrid searchQuery={searchQuery} selectedHero={selectedHero} />
        ) : currentView === 'favorites' ? (
          <FavoritesPage />
        ) : (
          <Teams />
        )}
      </main>
      
      {/* Bottom User Section */}
      <footer className="bottom-user-section">
        <div className="user-info">
          <span className="username">{user?.username || 'User'}</span>
          <button onClick={onLogout} className="logout-btn">
            Logout
          </button>
        </div>
      </footer>
    </div>
  )
}

export default Dashboard
