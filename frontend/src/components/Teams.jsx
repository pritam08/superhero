import { useState, useEffect } from 'react'
import { heroService } from '../services/heroService'
import SuperheroCard from './SuperheroCard'
import './Teams.css'

const Teams = () => {
  const [team, setTeam] = useState([])
  const [loading, setLoading] = useState(false)
  const [teamType, setTeamType] = useState('random')
  const [selectedPower, setSelectedPower] = useState('strength')
  const [powerStats, setPowerStats] = useState(null)
  const [teamStats, setTeamStats] = useState(null)

  const powers = [
    { value: 'intelligence', label: 'Intelligence' },
    { value: 'strength', label: 'Strength' },
    { value: 'speed', label: 'Speed' },
    { value: 'durability', label: 'Durability' },
    { value: 'power', label: 'Power' },
    { value: 'combat', label: 'Combat' }
  ]

  useEffect(() => {
    fetchPowerStats()
  }, [])

  const fetchPowerStats = async () => {
    try {
      const data = await heroService.getPowerStats()
      setPowerStats(data)
    } catch (error) {
      console.error('Error fetching power stats:', error)
    }
  }

  const generateTeam = async () => {
    setLoading(true)
    try {
      let response
      
      switch (teamType) {
        case 'random':
          response = await heroService.generateRandomTeam()
          break
        case 'balanced':
          response = await heroService.generateBalancedTeam()
          break
        case 'power-based':
          response = await heroService.generatePowerBasedTeam(selectedPower)
          break
        default:
          throw new Error('Invalid team type')
      }
      
      setTeam(response.team || [])
      setTeamStats(response.team_stats || null)
    } catch (error) {
      console.error('Error generating team:', error)
      setTeam([])
    } finally {
      setLoading(false)
    }
  }

  const getTeamTypeDescription = () => {
    switch (teamType) {
      case 'random':
        return 'Generate a completely random team of 5 superheroes'
      case 'balanced':
        return 'Create a balanced team of 5 heroes with good, bad, and neutral alignment'
      case 'power-based':
        return `Form a team of 5 heroes focused on ${selectedPower} abilities`
      default:
        return ''
    }
  }

  return (
    <div className="teams-container">
      <div className="teams-header">
        <h2>Team Builder</h2>
        <p>Create your perfect superhero team</p>
      </div>

      <div className="team-controls">
        <div className="control-section">
          <h3>Team Configuration</h3>
          
          <div className="control-group">
            <label>Team Type:</label>
            <select 
              value={teamType} 
              onChange={(e) => setTeamType(e.target.value)}
              className="control-select"
            >
              <option value="random">Random Team</option>
              <option value="balanced">Balanced Team</option>
              <option value="power-based">Power-Based Team</option>
            </select>
          </div>

          {teamType === 'power-based' && (
            <div className="control-group">
              <label>Focus Power:</label>
              <select 
                value={selectedPower} 
                onChange={(e) => setSelectedPower(e.target.value)}
                className="control-select"
              >
                {powers.map(power => (
                  <option key={power.value} value={power.value}>
                    {power.label}
                  </option>
                ))}
              </select>
            </div>
          )}

          <div className="team-description">
            <p>{getTeamTypeDescription()}</p>
          </div>

          <button 
            onClick={generateTeam} 
            disabled={loading}
            className="generate-btn"
          >
            {loading ? 'Generating...' : 'Generate Team'}
          </button>
        </div>
      </div>

      {teamStats && (
        <div className="team-stats">
          <h3>Team Statistics</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <span className="stat-label">Average {selectedPower}:</span>
              <span className="stat-value">{teamStats.avg_power?.toFixed(1)}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Min {selectedPower}:</span>
              <span className="stat-value">{teamStats.min_power_in_team}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Max {selectedPower}:</span>
              <span className="stat-value">{teamStats.max_power_in_team}</span>
            </div>
          </div>
        </div>
      )}

      {team.length > 0 && (
        <div className="team-display">
          <h3>Your Team ({team.length} members)</h3>
          <div className="team-grid">
            {team.map((hero, index) => (
              <div key={hero.id} className="team-member">
                <div className="member-position">#{index + 1}</div>
                <SuperheroCard hero={hero} />
                {teamType === 'power-based' && hero.powerstats && (
                  <div className="power-display">
                    <strong>{selectedPower}:</strong> {hero.powerstats[selectedPower] || 0}/100
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default Teams
