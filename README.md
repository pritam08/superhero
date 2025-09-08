# Superhero Application - Docker Setup

A full-stack superhero application with React.js frontend, Python FastAPI backend, and SQLite database, fully containerized with Docker.

## 🏗️ Architecture

- **Frontend**: React.js with Vite, served by Nginx
- **Backend**: Python FastAPI with SQLite database
- **Database**: SQLite3 for data persistence
- **Containerization**: Docker & Docker Compose

## 📋 Prerequisites

Before running this application, make sure you have the following installed:

- [Docker](https://www.docker.com/get-started) (version 20.10 or higher)
- [Docker Compose](https://docs.docker.com/compose/install/) (version 2.0 or higher)

## 🚀 Quick Start

### 1. Clone and Navigate to Project
```bash
cd .\superhero
```

### 2. Build and Run with Docker Compose
```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

### 3. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

### 4. Stop the Application
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (this will delete the database)
docker-compose down -v
```

## 📁 Project Structure

```
superhero/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application entry point
│   │   ├── core/
│   │   ├── db/
│   │   │   ├── sqlite_db.py     # SQLite database operations
│   │   │   └── seed.py          # Database seeding
│   │   ├── models/
│   │   ├── routes/
│   │   └── services/
│   ├── data/                    # SQLite database storage (Docker volume)
│   ├── requirements.txt         # Python dependencies
│   ├── Dockerfile              # Backend Docker configuration
│   └── .dockerignore
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── services/            # API service layer
│   │   └── main.jsx            # React entry point
│   ├── package.json            # Node.js dependencies
│   ├── Dockerfile              # Frontend Docker configuration
│   ├── nginx.conf              # Nginx configuration
│   └── .dockerignore
├── docker-compose.yml          # Docker services orchestration
└── README.md                   # This file
```

## 🔧 Development Setup

### Running Individual Services

#### Backend Only
```bash
cd .\backend
docker build -t superhero-backend .
docker run -p 8000:8000 -v $(pwd)/data:/app/data superhero-backend
```

#### Frontend Only (requires backend running)
```bash
cd .\frontend
docker build -t superhero-frontend .
docker run -p 3000:80 superhero-frontend
```

### Local Development (Non-Docker)

#### Backend
```bash
cd .\backend
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
cd .\app
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd .\frontend
# Install dependencies
npm install

# Run development server
npm run dev
```

## 🗄️ Database

### SQLite Database
- **Location**: `backend/data/superheroes.db` (persisted via Docker volume)
- **Seeding**: The database is automatically seeded with superhero data on first run
- **Backup**: The database file is stored in a Docker volume for persistence

### Database Operations
```bash
# Access the database container
docker exec -it superhero-backend bash

# Run database operations
python -c "from app.db.seed import seed_database; seed_database()"
```

## 🌐 API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/token` - Login and get access token

### Heroes
- `GET /heroes` - List all heroes
- `GET /heroes/{hero_id}` - Get specific hero
- `GET /heroes/search` - Search heroes
- `GET /heroes/search/suggestions` - Get search suggestions

### Users
- `GET /users/favorites` - Get user's favorite heroes
- `POST /users/favorites/{hero_id}` - Add hero to favorites
- `DELETE /users/favorites/{hero_id}` - Remove hero from favorites

### Teams
- `GET /teams` - List user's teams
- `POST /teams` - Create new team
- `PUT /teams/{team_id}` - Update team
- `DELETE /teams/{team_id}` - Delete team

## 🔍 Monitoring & Logs

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs in real-time
docker-compose logs -f backend
```

### Health Checks
- Backend health check: `GET http://localhost:8000/docs`
- Frontend health: `GET http://localhost:3000`

## 🛠️ Troubleshooting

### Common Issues

#### Port Already in Use
```bash
# Check what's using the port
netstat -tulpn | grep :8000
netstat -tulpn | grep :3000

# Stop conflicting services
docker-compose down
```

#### Database Issues
```bash
# Reset database
docker-compose down -v
docker-compose up --build
```

#### Container Build Issues
```bash
# Clean rebuild
docker-compose down
docker system prune -a
docker-compose up --build
```

### Container Management
```bash
# List running containers
docker ps

# Access container shell
docker exec -it superhero-backend bash
docker exec -it superhero-frontend sh

# View container resources
docker stats

# Remove all containers and images
docker-compose down
docker system prune -a
```

## 🔒 Security Considerations

- JWT tokens for authentication
- Environment variables for sensitive data
- SQLite database with proper access controls
- Nginx reverse proxy for API calls

## 📝 Environment Variables

Create a `.env` file in the root directory for custom configuration:

```env
# Backend
DATABASE_PATH=/app/data/superheroes.db
JWT_SECRET_KEY=your-secret-key-here

# Frontend
REACT_APP_API_URL=http://localhost:8000
```

## 🚀 Production Deployment

For production deployment:

1. Update environment variables
2. Use production-ready database (PostgreSQL/MySQL)
3. Add SSL certificates
4. Configure proper logging
5. Set up monitoring and alerting

## 📄 License

This project is for educational purposes.

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

**Happy coding! 🦸‍♂️🦸‍♀️**
