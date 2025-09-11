from app.db.sqlite_db import SuperheroDatabase
import json

# Test specific hero that might be causing issues
hero_id = 1
hero = SuperheroDatabase.find_hero_by_id(hero_id)

print(f"Testing Hero ID: {hero_id}")
print(f"Hero Name: {hero['name']}")
print(f"Power Stats: {hero['powerstats']}")

# Test JSON serialization (what the API would return)
json_response = json.dumps(hero)
print(f"\nJSON Response Length: {len(json_response)}")
print("JSON Response Preview:")
print(json_response[:500] + "..." if len(json_response) > 500 else json_response)

# Test parsing back from JSON
parsed_hero = json.loads(json_response)
print(f"\nParsed Power Stats: {parsed_hero['powerstats']}")
print(f"Power Stats Match: {hero['powerstats'] == parsed_hero['powerstats']}")

# Check each power stat individually
for power, value in hero['powerstats'].items():
    print(f"{power}: {value} ({type(value)})")
