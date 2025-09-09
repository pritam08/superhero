from fastapi import FastAPI
from app.routes import auth, users, superheroes, teams
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Superhero Backend with FastAPI + MongoDB")

# CORS setup to allow requests from React
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Add your React app's origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# register routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(superheroes.router)
app.include_router(teams.router)