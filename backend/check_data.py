from app.db.sqlite_db import SuperheroDatabase

# Check power stats for several heroes
heroes = SuperheroDatabase.find_heroes(limit=730)
print("Checking power stats for heroes:")
print("-" * 50)

for hero in heroes:
    print(f"Hero {hero['id']} - {hero['name']}:")
    print(f"  Power stats: {hero['powerstats']}")
    print(f"  Power stats type: {type(hero['powerstats'])}")
    
    # Check individual power values
    for power, value in hero['powerstats'].items():
        print(f"    {power}: {value} (type: {type(value)})")
    print()
