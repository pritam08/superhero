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

@router.get("/search/suggestions")
def get_search_suggestions(q: str, limit: int = 10):
    """
    Get search suggestions for autocomplete
    Returns suggestions only if query length > 3 characters
    """
    if len(q.strip()) < 3:
        return {"suggestions": [], "message": "Query must be at least 3 characters"}
    
    # Search in hero names with case-insensitive regex
    filter_query = {
        "name": {"$regex": q, "$options": "i"}
    }
    
    # Get only name and id fields for suggestions
    cursor = db.superheroes.find(
        filter_query, 
        {"name": 1, "id": 1, "_id": 0}
    ).limit(limit)
    
    suggestions = list(cursor)
    
    return {
        "suggestions": suggestions,
        "count": len(suggestions),
        "query": q
    }

@router.get("/search")
def search_heroes(q: str, limit: int = 20, skip: int = 0, alignment: str = None):
    """
    Enhanced search endpoint with multiple fields
    Searches in name, full_name, and aliases
    """
    if len(q.strip()) < 3:
        return {
            "heroes": [], 
            "total": 0, 
            "message": "Query must be at least 3 characters"
        }
    
    # Build search filter
    search_conditions = [
        {"name": {"$regex": q, "$options": "i"}},
        {"biography.full_name": {"$regex": q, "$options": "i"}},
        {"biography.aliases": {"$regex": q, "$options": "i"}}
    ]
    
    filter_query = {"$or": search_conditions}
    
    # Add alignment filter if provided
    if alignment:
        filter_query["alignment"] = alignment
    
    # Get total count for pagination
    total_count = db.superheroes.count_documents(filter_query)
    
    # Get heroes
    cursor = db.superheroes.find(filter_query, {"_id": 0}).skip(skip).limit(limit)
    heroes = list(cursor)
    
    return {
        "heroes": heroes,
        "total": total_count,
        "limit": limit,
        "skip": skip,
        "query": q,
        "has_more": total_count > (skip + limit)
    }

@router.get("/image/{hero_id}")
def get_image(hero_id: int):
    hero_image = db.superheroes.find_one({"id": hero_id}, { "image":1,"_id": 0})
    if not hero_image:
        raise HTTPException(status_code=404, detail="Hero image not found")
    return hero_image

