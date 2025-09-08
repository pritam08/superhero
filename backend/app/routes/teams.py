import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import APIRouter
from random import sample
from app.db.mongodb import db

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/random")
def random_team(size: int = 5):
    heroes = list(db.superheroes.aggregate([{"$sample": {"size": size}}]))
    for h in heroes:
        h.pop("_id", None)
    return {"team": heroes}

@router.get("/balanced")
def balanced_team(size: int = 5):
    heroes = list(db.superheroes.find({}, {"_id": 0}))
    good = [h for h in heroes if h.get("alignment") == "good"]
    bad = [h for h in heroes if h.get("alignment") == "bad"]
    neutral = [h for h in heroes if h.get("alignment") not in ["good", "bad"]]
    team = []
    if good: team.append(sample(good, 1)[0])
    if bad: team.append(sample(bad, 1)[0])
    if neutral: team.append(sample(neutral, 1)[0])
    while len(team) < size and heroes:
        team.append(sample(heroes, 1)[0])
    return {"team": team}
