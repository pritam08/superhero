import { useState, useEffect, useRef } from 'react'
import heroService from '../services/heroService'
import './SearchBar.css'

const SearchBar = ({ onSearch, onHeroSelect, placeholder = "Search superheroes..." }) => {
  const [query, setQuery] = useState('')
  const [suggestions, setSuggestions] = useState([])
  const [showSuggestions, setShowSuggestions] = useState(false)
  const [loading, setLoading] = useState(false)
  const [selectedIndex, setSelectedIndex] = useState(-1)
  
  const searchRef = useRef(null)
  const suggestionsRef = useRef(null)
  const debounceRef = useRef(null)

  // Debounced search for suggestions
  useEffect(() => {
    if (debounceRef.current) {
      clearTimeout(debounceRef.current)
    }

    if (query.trim().length >= 3) {
      debounceRef.current = setTimeout(async () => {
        try {
          setLoading(true)
          const response = await heroService.getSearchSuggestions(query.trim(), 8)
          setSuggestions(response.suggestions || [])
          setShowSuggestions(true)
        } catch (error) {
          console.error('Error fetching suggestions:', error)
          setSuggestions([])
        } finally {
          setLoading(false)
        }
      }, 300) // 300ms delay
    } else {
      setSuggestions([])
      setShowSuggestions(false)
    }

    return () => {
      if (debounceRef.current) {
        clearTimeout(debounceRef.current)
      }
    }
  }, [query])

  // Handle click outside to close suggestions
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowSuggestions(false)
        setSelectedIndex(-1)
      }
    }

    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleInputChange = (e) => {
    const value = e.target.value
    setQuery(value)
    setSelectedIndex(-1)
  }

  const handleKeyDown = (e) => {
    if (!showSuggestions || suggestions.length === 0) {
      if (e.key === 'Enter') {
        handleSearch()
      }
      return
    }

    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault()
        setSelectedIndex(prev => 
          prev < suggestions.length - 1 ? prev + 1 : prev
        )
        break
      case 'ArrowUp':
        e.preventDefault()
        setSelectedIndex(prev => prev > 0 ? prev - 1 : -1)
        break
      case 'Enter':
        e.preventDefault()
        if (selectedIndex >= 0) {
          handleSuggestionClick(suggestions[selectedIndex])
        } else {
          handleSearch()
        }
        break
      case 'Escape':
        setShowSuggestions(false)
        setSelectedIndex(-1)
        break
    }
  }

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion.name)
    setShowSuggestions(false)
    setSelectedIndex(-1)
    
    // Call the onHeroSelect callback if provided
    if (onHeroSelect) {
      onHeroSelect(suggestion)
    }
  }

  const handleSearch = () => {
    if (query.trim().length >= 3) {
      setShowSuggestions(false)
      if (onSearch) {
        onSearch(query.trim())
      }
    }
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    handleSearch()
  }

  const highlightMatch = (text, searchQuery) => {
    if (!searchQuery) return text
    
    const regex = new RegExp(`(${searchQuery})`, 'gi')
    const parts = text.split(regex)
    
    return parts.map((part, index) => 
      regex.test(part) ? (
        <mark key={index} className="highlight">{part}</mark>
      ) : part
    )
  }

  return (
    <div className="search-container" ref={searchRef}>
      <form onSubmit={handleSubmit} className="search-form">
        <div className="search-input-container">
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            className="search-input"
            autoComplete="off"
          />
          <button type="submit" className="search-button" disabled={query.trim().length < 3}>
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <circle cx="11" cy="11" r="8"></circle>
              <path d="m21 21-4.35-4.35"></path>
            </svg>
          </button>
        </div>
      </form>

      {showSuggestions && (
        <div className="suggestions-container" ref={suggestionsRef}>
          {loading ? (
            <div className="suggestion-item loading">
              <div className="loading-spinner"></div>
              Searching...
            </div>
          ) : suggestions.length > 0 ? (
            <>
              {suggestions.map((suggestion, index) => (
                <div
                  key={suggestion.id}
                  className={`suggestion-item ${index === selectedIndex ? 'selected' : ''}`}
                  onClick={() => handleSuggestionClick(suggestion)}
                  onMouseEnter={() => setSelectedIndex(index)}
                >
                  <div className="suggestion-content">
                    <span className="suggestion-name">
                      {highlightMatch(suggestion.name, query)}
                    </span>
                    <span className="suggestion-id">#{suggestion.id}</span>
                  </div>
                </div>
              ))}
              <div className="suggestions-footer">
                <small>Press Enter to search for "{query}"</small>
              </div>
            </>
          ) : query.trim().length >= 3 ? (
            <div className="suggestion-item no-results">
              No suggestions found for "{query}"
            </div>
          ) : null}
        </div>
      )}
    </div>
  )
}

export default SearchBar
