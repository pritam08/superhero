from fastapi import FastAPI
from routes import auth, users, superheroes, teams

app = FastAPI(title="Superhero Backend with FastAPI + MongoDB")

# register routers
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(superheroes.router)
app.include_router(teams.router)