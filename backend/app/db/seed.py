
import requests
import os, sys
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.db.sqlite_db import SuperheroDatabase, init_database
from app.core.config import settings


BASE = f"https://superheroapi.com/api/{settings.SUPERHERO_API_TOKEN}"

def fetch_hero(hero_id: int):
    r = requests.get(f"{BASE}/{hero_id}")
    if r.status_code == 200:
        return r.json()
    return None

def seed_superheroes(start: int = None, end: int = None):
    init_database()
    s = start or settings.SEED_START_ID
    e = 100 # Change back to full seeding or settings.SEED_END_ID
    inserted = 0
    for i in range(s, e + 1):
        hero = fetch_hero(i)
        if hero and hero.get("response") == "success":
            hero_obj = {
                "id": int(hero.get("id")),
                "name": hero.get("name"),
                "alignment": hero.get("biography", {}).get("alignment", "neutral"),
                "powerstats": {k: int(v) if v and v.isdigit() else 0 for k, v in (hero.get("powerstats") or {}).items()},
                "biography": hero.get("biography", {}),
                "appearance": hero.get("appearance", {}),
                "work": hero.get("work", {}),
                "connections": hero.get("connections", {}),
                "image": hero.get("image", {}),
            }
            SuperheroDatabase.insert_or_update_hero(hero_obj)
            inserted += 1
            print(f"Seeded/updated {inserted} heroes")
    print(f"Seeded/updated {inserted} heroes")

if __name__ == "__main__":
    seed_superheroes()
