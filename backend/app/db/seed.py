

import requests
import os, sys
import time
import json
from requests.exceptions import ConnectTimeout, ConnectionError, Timeout, RequestException
sys.path.append( os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from app.db.sqlite_db import SuperheroDatabase, init_database
from app.core.config import settings




BASE = f"https://superheroapi.com/api/{settings.SUPERHERO_API_TOKEN}"


def fetch_hero(hero_id: int, max_retries: int = 3, timeout: int = 10):
    """
    Fetch hero data from API with retry logic and error handling
    """
    for attempt in range(max_retries):
        try:
            print(f"Fetching hero {hero_id} (attempt {attempt + 1}/{max_retries})")
            r = requests.get(f"{BASE}/{hero_id}", timeout=timeout)
           
            if r.status_code == 200:
                return r.json()
            elif r.status_code == 404:
                print(f"Hero {hero_id} not found (404)")
                return None
            else:
                print(f"API returned status code {r.status_code} for hero {hero_id}")
               
        except ConnectTimeout:
            print(f"Connection timeout for hero {hero_id} on attempt {attempt + 1}")
        except ConnectionError:
            print(f"Connection error for hero {hero_id} on attempt {attempt + 1}")
        except Timeout:
            print(f"Request timeout for hero {hero_id} on attempt {attempt + 1}")
        except RequestException as e:
            print(f"Request exception for hero {hero_id}: {e}")
        except Exception as e:
            print(f"Unexpected error for hero {hero_id}: {e}")
           
        # Wait before retrying (exponential backoff)
        if attempt < max_retries - 1:
            wait_time = (2 ** attempt) + 1  # 2, 5, 9 seconds
            print(f"Waiting {wait_time} seconds before retry...")
            time.sleep(wait_time)
   
    print(f"Failed to fetch hero {hero_id} after {max_retries} attempts")
    return None


def create_sample_heroes():
    """
    Create sample heroes when API is not accessible
    """
    sample_heroes = [
        {
            "id": 1,
            "name": "A-Bomb",
            "alignment": "good",
            "powerstats": {"intelligence": 38, "strength": 100, "speed": 17, "durability": 80, "power": 24, "combat": 64},
            "biography": {
                "full-name": "Richard Milhouse Jones",
                "alter-egos": "No alter egos found.",
                "aliases": ["Rick Jones"],
                "place-of-birth": "Scarsdale, Arizona",
                "first-appearance": "Hulk Vol 2 #2 (April, 2008) (as A-Bomb)",
                "publisher": "Marvel Comics",
                "alignment": "good"
            },
            "appearance": {
                "gender": "Male",
                "race": "Human",
                "height": ["6'8", "203 cm"],
                "weight": ["980 lb", "441 kg"],
                "eye-color": "Yellow",
                "hair-color": "No Hair"
            },
            "work": {
                "occupation": "Musician, adventurer, author; formerly talk show host",
                "base": "-"
            },
            "connections": {
                "group-affiliation": "Hulk Family; Excelsior (sponsor), Avengers (honorary member)",
                "relatives": "Marlo Chandler-Jones (wife); Polly (aunt)"
            },
            "image": {
                "url": "https://www.superherodb.com/pictures2/portraits/10/100/10060.jpg"
            }
        },
        {
            "id": 2,
            "name": "Abe Sapien",
            "alignment": "good",
            "powerstats": {"intelligence": 88, "strength": 28, "speed": 35, "durability": 65, "power": 100, "combat": 85},
            "biography": {
                "full-name": "Abraham Sapien",
                "alter-egos": "No alter egos found.",
                "aliases": ["Langdon Everett Caul", "Abraham Sapien", "Abe Sapien"],
                "place-of-birth": "-",
                "first-appearance": "Hellboy: Seed of Destruction (1993)",
                "publisher": "Dark Horse Comics",
                "alignment": "good"
            },
            "appearance": {
                "gender": "Male",
                "race": "Icthyo Sapien",
                "height": ["6'3", "191 cm"],
                "weight": ["145 lb", "65 kg"],
                "eye-color": "Blue",
                "hair-color": "No Hair"
            },
            "work": {
                "occupation": "Paranormal Investigator",
                "base": "-"
            },
            "connections": {
                "group-affiliation": "Bureau for Paranormal Research and Defense",
                "relatives": "Edith Howard (wife, deceased)"
            },
            "image": {
                "url": "https://www.superherodb.com/pictures2/portraits/10/100/956.jpg"
            }
        },
        {
            "id": 3,
            "name": "Abin Sur",
            "alignment": "good",
            "powerstats": {"intelligence": 50, "strength": 90, "speed": 53, "durability": 64, "power": 99, "combat": 65},
            "biography": {
                "full-name": "Abin Sur",
                "alter-egos": "No alter egos found.",
                "aliases": ["-"],
                "place-of-birth": "Ungara",
                "first-appearance": "Showcase #22 (October, 1959)",
                "publisher": "DC Comics",
                "alignment": "good"
            },
            "appearance": {
                "gender": "Male",
                "race": "Ungaran",
                "height": ["6'1", "185 cm"],
                "weight": ["200 lb", "90 kg"],
                "eye-color": "Blue",
                "hair-color": "No Hair"
            },
            "work": {
                "occupation": "Green Lantern, former history professor",
                "base": "Oa"
            },
            "connections": {
                "group-affiliation": "Green Lantern Corps, formerly White Lantern Corps",
                "relatives": "Amon Sur (son), Arin Sur (sister), Thaal Sinestro (nephew)"
            },
            "image": {
                "url": "https://www.superherodb.com/pictures2/portraits/10/100/1460.jpg"
            }
        }
    ]
    return sample_heroes


def seed_superheroes(start: int = None, end: int = None, use_api: bool = True):
    """
    Seed database with superhero data
   
    Args:
        start: Starting hero ID
        end: Ending hero ID  
        use_api: Whether to try fetching from API first
    """
    print("Initializing database...")
    init_database()
   
    # Check if database already has data
    # existing_heroes = SuperheroDatabase.find_heroes(limit=1)
    # if existing_heroes:
    #     print(f"Database already contains {len(existing_heroes)} heroes. Skipping seeding.")
    #     return
   
    s = start or settings.SEED_START_ID
    e = end or 50  # Limit to first 50 heroes to avoid long waits


    s = 1
    e = 731
    inserted = 0
    failed_count = 0
    max_failures = 10  # Stop if too many consecutive failures
   
    if use_api:
        print(f"Attempting to seed heroes {s} to {e} from API...")
       
        for i in range(s, e + 1):
            hero = fetch_hero(i)
           
            if hero and hero.get("response") == "success":
                try:
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
                    failed_count = 0  # Reset failure count on success
                    print(f"✓ Seeded hero {i}: {hero_obj['name']} (total: {inserted})")
                   
                except Exception as e:
                    print(f"✗ Error processing hero {i}: {e}")
                    failed_count += 1
            else:
                failed_count += 1
                print(f"✗ Failed to fetch or invalid hero {i}")
           
            # If too many consecutive failures, fall back to sample data
            if failed_count >= max_failures:
                print(f"Too many failures ({failed_count}). Falling back to sample data...")
                break
               
            # Small delay to be respectful to the API
            time.sleep(0.5)
   
    # If API seeding failed or was skipped, use sample data
    if inserted == 0:
        print("Using sample hero data...")
        sample_heroes = create_sample_heroes()
       
        for hero_obj in sample_heroes:
            try:
                SuperheroDatabase.insert_or_update_hero(hero_obj)
                inserted += 1
                print(f"✓ Seeded sample hero: {hero_obj['name']} (total: {inserted})")
            except Exception as e:
                print(f"✗ Error seeding sample hero {hero_obj.get('name', 'Unknown')}: {e}")
   
    print(f"\n🎉 Seeding complete! Successfully seeded {inserted} heroes")
   
    if inserted == 0:
        print("⚠️  Warning: No heroes were seeded. Please check your configuration and try again.")


def seed_database():
    """
    Main seeding function with full error handling
    """
    try:
        seed_superheroes()
    except Exception as e:
        print(f"💥 Critical error during seeding: {e}")
        print("Attempting to seed with sample data as fallback...")
        try:
            seed_superheroes(use_api=False)
        except Exception as fallback_error:
            print(f"💥 Fallback seeding also failed: {fallback_error}")
            raise


if __name__ == "__main__":
    seed_database()



