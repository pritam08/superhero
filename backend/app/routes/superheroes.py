import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import APIRouter, HTTPException
from app.db.sqlite_db import SuperheroDatabase

router = APIRouter(prefix="/heroes", tags=["heroes"])

@router.get("/")
def list_heroes(q: str = None, limit: int = 30, skip: int = 0, alignment: str = None):
    heroes = SuperheroDatabase.find_heroes(
        name_filter=q, 
        alignment_filter=alignment, 
        limit=limit, 
        skip=skip
    )
    return heroes

@router.get("/{hero_id}")
def get_hero(hero_id: int):
    hero = SuperheroDatabase.find_hero_by_id(hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero

@router.put("/{hero_id}")
def update_hero(hero_id: int, payload: dict):
    # For update operations, get existing hero and update with payload
    existing_hero = SuperheroDatabase.find_hero_by_id(hero_id)
    if not existing_hero:
        raise HTTPException(status_code=404, detail="Hero not found")
    
    # Update the hero data
    existing_hero.update(payload)
    SuperheroDatabase.insert_or_update_hero(existing_hero)
    return {"ok": True}

@router.get("/search/suggestions")
def get_search_suggestions(q: str, limit: int = 10):
    """
    Get search suggestions for autocomplete
    Returns suggestions only if query length > 3 characters
    """
    if len(q.strip()) < 3:
        return {"suggestions": [], "message": "Query must be at least 3 characters"}
    
    # Search heroes by name
    heroes = SuperheroDatabase.find_heroes(name_filter=q, limit=limit)
    
    # Return only name and id for suggestions
    suggestions = [{"name": hero["name"], "id": hero["id"]} for hero in heroes]
    
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
    
    # Get heroes using SQLite search
    heroes = SuperheroDatabase.find_heroes(
        name_filter=q, 
        alignment_filter=alignment, 
        limit=limit, 
        skip=skip
    )
    
    # Get total count for pagination
    total_count = SuperheroDatabase.count_heroes(
        name_filter=q, 
        alignment_filter=alignment
    )
    
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
    hero = SuperheroDatabase.find_hero_by_id(hero_id)
    if not hero:
        raise HTTPException(status_code=404, detail="Hero image not found")
    return {"image": hero["image"]}

