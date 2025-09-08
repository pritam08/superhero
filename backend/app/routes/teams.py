import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from fastapi import APIRouter, Query
from random import sample
from app.db.sqlite_db import SuperheroDatabase

router = APIRouter(prefix="/teams", tags=["teams"])

@router.get("/random")
def random_team():
    """Generate a random team of 5 superheroes"""
    size = 5
    heroes = SuperheroDatabase.get_random_heroes(size)
    return {
        "team": heroes,
        "team_size": len(heroes),
        "team_type": "random"
    }

@router.get("/balanced")
def balanced_team():
    """Generate a balanced team of 5 heroes with good, bad, and neutral alignment"""
    size = 5
    heroes = SuperheroDatabase.find_heroes(limit=1000)  # Get a large sample
    good = [h for h in heroes if h.get("alignment") == "good"]
    bad = [h for h in heroes if h.get("alignment") == "bad"]
    neutral = [h for h in heroes if h.get("alignment") not in ["good", "bad"]]
    
    team = []
    team_composition = {"good": 0, "bad": 0, "neutral": 0}
    
    # Try to get at least one from each alignment if available
    if good and len(team) < size: 
        hero = sample(good, 1)[0]
        team.append(hero)
        team_composition["good"] += 1
        
    if bad and len(team) < size: 
        hero = sample(bad, 1)[0]
        team.append(hero)
        team_composition["bad"] += 1
        
    if neutral and len(team) < size: 
        hero = sample(neutral, 1)[0]
        team.append(hero)
        team_composition["neutral"] += 1
    
    # Fill remaining slots randomly
    used_ids = {h["id"] for h in team}
    remaining_heroes = [h for h in heroes if h["id"] not in used_ids]
    
    while len(team) < size and remaining_heroes:
        hero = sample(remaining_heroes, 1)[0]
        team.append(hero)
        alignment = hero.get("alignment", "neutral")
        if alignment in team_composition:
            team_composition[alignment] += 1
        else:
            team_composition["neutral"] += 1
        remaining_heroes.remove(hero)
    
    return {
        "team": team,
        "team_size": len(team),
        "team_type": "balanced",
        "composition": team_composition
    }

@router.get("/power-based")
def power_based_team(
    power: str = Query(..., description="Power type: intelligence, strength, speed, durability, power, combat")
):
    """Generate a team of 5 heroes based on specific power (minimum 50 power level)"""
    size = 5
    min_power = 50
    valid_powers = ["intelligence", "strength", "speed", "durability", "power", "combat"]
    
    if power not in valid_powers:
        return {
            "error": f"Invalid power type. Valid options: {', '.join(valid_powers)}",
            "valid_powers": valid_powers
        }
    
    # Query heroes with the specified minimum power level using SQLite
    heroes = SuperheroDatabase.search_heroes_by_power(power, min_power)
    
    if not heroes:
        return {
            "team": [],
            "message": f"No heroes found with {power} >= {min_power}",
            "team_type": f"power_based_{power}"
        }
    
    # Select top heroes or sample if we have more than needed
    if len(heroes) <= size:
        team = heroes
    else:
        # Take top performers and some random ones for variety
        top_count = min(size // 2 + 1, len(heroes))
        top_heroes = heroes[:top_count]
        remaining_heroes = heroes[top_count:]
        
        if remaining_heroes and len(top_heroes) < size:
            additional_count = size - len(top_heroes)
            additional_heroes = sample(remaining_heroes, min(additional_count, len(remaining_heroes)))
            team = top_heroes + additional_heroes
        else:
            team = top_heroes[:size]
    
    # Calculate team stats
    team_stats = {
        "avg_power": sum(h.get("powerstats", {}).get(power, 0) for h in team) / len(team) if team else 0,
        "min_power_in_team": min(h.get("powerstats", {}).get(power, 0) for h in team) if team else 0,
        "max_power_in_team": max(h.get("powerstats", {}).get(power, 0) for h in team) if team else 0
    }
    
    return {
        "team": team,
        "team_size": len(team),
        "team_type": f"power_based_{power}",
        "focus_power": power,
        "min_power_requirement": min_power,
        "team_stats": team_stats
    }

@router.get("/power-stats")
def get_power_stats():
    """Get available power types and their statistics"""
    powers = ["intelligence", "strength", "speed", "durability", "power", "combat"]
    stats = {}
    
    # Get all heroes to calculate statistics
    heroes = SuperheroDatabase.find_heroes(limit=1000)  # Get a large sample
    
    for power in powers:
        power_values = []
        for hero in heroes:
            power_value = hero.get("powerstats", {}).get(power, 0)
            if isinstance(power_value, (int, float)):
                power_values.append(power_value)
        
        if power_values:
            stats[power] = {
                "average": round(sum(power_values) / len(power_values), 2),
                "minimum": min(power_values),
                "maximum": max(power_values),
                "total_heroes": len(power_values)
            }
    
    return {
        "available_powers": powers,
        "power_statistics": stats,
        "description": "Use these power types with /teams/power-based endpoint"
    }
