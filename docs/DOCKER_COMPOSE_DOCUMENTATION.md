# Docker Compose Documentation - Superhero Application
## Complete Application Setup Guide

This document explains how the **entire Superhero application** works using Docker Compose. It's written in simple English so anyone can understand how all the pieces fit together.

---

## 🌟 What is This Application?

The **Superhero Application** is a complete web application that lets users:
- **Search** for superheroes (like Batman, Superman, Wonder Woman)
- **View detailed information** about each superhero
- **Save favorite heroes** to a personal list
- **Create superhero teams** by combining different heroes
- **Login and register** to save their preferences

Think of it like **IMDb for superheroes** - a database where you can explore, save, and organize superhero information.

---

## 🏗️ Application Architecture (How Everything Works Together)

Our application has **3 main parts**:

### 1. **Frontend** (What Users See)
- **Technology**: React.js website
- **Port**: http://localhost:3000
- **What it does**: 
  - Shows the website interface
  - Handles user clicks and interactions
  - Displays superhero information beautifully

### 2. **Backend** (The Brain)
- **Technology**: Python FastAPI server
- **Port**: http://localhost:8000
- **What it does**:
  - Manages user accounts (login/register)
  - Stores and retrieves superhero data
  - Handles favorites and teams
  - Provides security (authentication)

### 3. **Database** (The Memory)
- **Technology**: SQLite database file
- **Location**: `./backend/data/superheroes.db`
- **What it does**:
  - Stores all user information
  - Keeps superhero data
  - Remembers favorites and teams

---

## 🐳 What is Docker Compose?

**Docker Compose** is like a **conductor of an orchestra**. Just like a conductor makes sure all musicians play together in harmony, Docker Compose makes sure all parts of our application work together perfectly.

### Why Use Docker Compose?

**Without Docker Compose** (the hard way):
1. Install Python manually
2. Install Node.js manually  
3. Set up database manually
4. Start backend manually
5. Start frontend manually
6. Hope everything works together

**With Docker Compose** (the easy way):
1. Run one command: `docker-compose up`
2. Everything starts automatically
3. Everything works together perfectly

---

## 📋 Docker Compose File Explained

Let's break down our `docker-compose.yml` file in simple terms:

```yaml
services:
  # Backend service
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: superhero-backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend/data:/app/data
    environment:
      - PYTHONPATH=/app
      - DATABASE_PATH=/app/data/superheroes.db
    networks:
      - superhero-network
    restart: unless-stopped
```

### Backend Service Breakdown:

| Setting | What It Means | Why We Need It |
|---------|---------------|----------------|
| `build: ./backend` | Build the backend from the backend folder | Creates our Python API server |
| `container_name: superhero-backend` | Name the container "superhero-backend" | Easy to identify in Docker |
| `ports: "8000:8000"` | Make port 8000 available | So frontend can talk to backend |
| `volumes: ./backend/data:/app/data` | Share the data folder | Keep database safe outside container |
| `environment` | Set up environment variables | Tell the app where to find things |
| `networks: superhero-network` | Put on shared network | Let services talk to each other |

```yaml
  # Frontend service
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: superhero-frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
    networks:
      - superhero-network
    restart: unless-stopped
```

### Frontend Service Breakdown:

| Setting | What It Means | Why We Need It |
|---------|---------------|----------------|
| `build: ./frontend` | Build the frontend from the frontend folder | Creates our React website |
| `container_name: superhero-frontend` | Name the container "superhero-frontend" | Easy to identify in Docker |
| `ports: "3000:80"` | Map port 3000 to internal port 80 | So users can access the website |
| `depends_on: backend` | Start backend first | Frontend needs backend to work |
| `networks: superhero-network` | Put on shared network | Let frontend talk to backend |

```yaml
networks:
  superhero-network:
    driver: bridge

volumes:
  superhero-data:
    driver: local
```

### Networks and Volumes:

| Setting | What It Means | Why We Need It |
|---------|---------------|----------------|
| `superhero-network` | Create a private network | Let our services talk securely |
| `superhero-data` | Create a storage volume | Keep data safe (though we use folder mounting) |

---

## 🚀 How to Use Docker Compose

### Starting the Application:

```bash
# Build and start everything
docker-compose up --build

# Or run in background (detached mode)
docker-compose up --build -d
```

**What happens when you run this:**
1. Docker builds the backend container (installs Python, dependencies)
2. Docker builds the frontend container (installs Node.js, builds React app)
3. Docker creates a network for them to communicate
4. Docker starts the backend first
5. Docker starts the frontend (which connects to backend)
6. Your application is ready!

### Accessing the Application:

| Service | URL | What You'll See |
|---------|-----|-----------------|
| **Frontend** | http://localhost:3000 | The superhero website |
| **Backend API** | http://localhost:8000 | API endpoints (raw data) |
| **API Documentation** | http://localhost:8000/docs | Interactive API documentation |

### Stopping the Application:

```bash
# Stop all services
docker-compose down

# Stop and remove everything (but keeps database)
docker-compose down -v
```

---

## 🔄 Application Flow (How Everything Connects)

Here's how a typical user interaction works:

### 1. User Opens Website
```
User → http://localhost:3000 → Frontend Container (React App)
```

### 2. User Searches for Superhero
```
Frontend → API Request → Backend Container (Python FastAPI)
Backend → Database Query → SQLite Database
Database → Returns Data → Backend
Backend → API Response → Frontend
Frontend → Shows Results → User
```

### 3. User Saves Favorite
```
Frontend → Save Request → Backend Container
Backend → Checks User Login → Database
Backend → Saves Favorite → Database
Database → Confirms Save → Backend
Backend → Success Response → Frontend
Frontend → Shows "Saved!" → User
```

---

## 🗂️ Data Persistence (How Data is Saved)

### Database Location:
- **Inside Container**: `/app/data/superheroes.db`
- **On Your Computer**: `./backend/data/superheroes.db`

### Why This Matters:
- When you stop Docker containers, data normally disappears
- We use **volume mounting** to keep data on your computer
- Even if you delete containers, your data stays safe

---

## 🌐 Network Communication

Our Docker Compose creates a **private network** called `superhero-network`:

```
Frontend Container ←→ superhero-network ←→ Backend Container
```

### How They Talk:
- **Frontend** makes HTTP requests to **backend**
- **Backend** processes requests and queries database
- **Backend** sends responses back to **frontend**
- **Frontend** updates the user interface

### Network Benefits:
- **Security**: Services only talk to each other, not outside world
- **Isolation**: Our app is separate from other Docker apps
- **Reliability**: Network is managed automatically by Docker

---

## 🛠️ Development vs Production

### Development Mode:
- **Frontend**: Hot reload (changes appear instantly)
- **Backend**: Auto-restart when code changes
- **Debugging**: Easy to see logs and errors

### Production Mode:
- **Frontend**: Optimized, compressed files served by Nginx
- **Backend**: Stable, no auto-restart
- **Performance**: Faster loading, better security

---

## 🔧 Troubleshooting Common Issues

### Issue: "Port already in use"
**Problem**: Another app is using port 3000 or 8000
**Solution**: 
```bash
# Stop other Docker containers
docker ps
docker stop <container-name>

# Or change ports in docker-compose.yml
ports:
  - "3001:80"  # Changed from 3000 to 3001
```

### Issue: "Cannot connect to backend"
**Problem**: Frontend can't reach backend
**Solution**:
```bash
# Check if backend is running
docker-compose ps

# Check backend logs
docker-compose logs backend

# Restart everything
docker-compose down
docker-compose up --build
```

### Issue: "Database not found"
**Problem**: Database file is missing
**Solution**:
```bash
# Make sure data folder exists
mkdir -p backend/data

# Restart the application
docker-compose down
docker-compose up --build
```

---

## 📚 Next Steps

Now that you understand how Docker Compose orchestrates the entire application:

1. **For Frontend Details**: Read `frontend/React_Components_Documentation.md`
2. **For Backend Details**: Read `backend/DOCUMENTATION.md`
3. **For Docker Details**: Read `frontend/Dockerfile_Documentation.md`

---

## 🎯 Summary

**Docker Compose** makes our superhero application easy to run by:
- **Building** both frontend and backend automatically
- **Connecting** them through a private network
- **Managing** the database and data persistence
- **Providing** a single command to start everything

Instead of setting up Python, Node.js, databases, and configurations manually, Docker Compose does it all with one command: `docker-compose up --build`

This is the power of **containerization** - packaging applications so they work the same everywhere, every time!
