import './openapp.css'

const OpenApp = ({ onGetStarted }) => {
  return (
    <div className="wrapper">
      <header>
        <h1>Find <span className="text-gradient">Superhero</span> Details Without the Hassle</h1>
        <div className="button-container">
          <button 
            onClick={onGetStarted}
            className="get-started-btn"
          >
            Get Started
          </button>
        </div>
      </header>
    </div>
  )
}

export default OpenApp
