import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import APIRouter, HTTPException
from app.db.mongodb import db

router = APIRouter(prefix="/heroes", tags=["heroes"])

@router.get("/")
def list_heroes(q: str = None, limit: int = 30, skip: int = 0, alignment: str = None):
    filter_q = {}
    if q:
        filter_q["name"] = {"$regex": q, "$options": "i"}
    if alignment:
        filter_q["alignment"] = alignment
    cursor = db.superheroes.find(filter_q, {"_id": 0}).skip(skip).limit(limit)
    return list(cursor)

@router.get("/{hero_id}")
def get_hero(hero_id: int):
    hero = db.superheroes.find_one({"id": hero_id}, {"_id": 0})
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.put("/{hero_id}")
def update_hero(hero_id: int, payload: dict):
    db.superheroes.update_one({"id": hero_id}, {"$set": payload})
    return {"ok": True}
