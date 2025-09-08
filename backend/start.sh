#!/bin/bash

# Wait for database to be ready
echo "Initializing database..."

# Run database seeding
python -c "
from app.db.sqlite_db import init_database
from app.db.seed import seed_database
import os

print('Initializing database tables...')
init_database()

# Check if database is empty and seed if needed
db_path = os.getenv('DATABASE_PATH', '/app/data/superheroes.db')
if os.path.exists(db_path):
    from app.db.sqlite_db import SuperheroDatabase
    heroes = SuperheroDatabase.find_heroes(limit=1)
    if not heroes:
        print('Database is empty, seeding with data...')
        seed_database()
        print('Database seeded successfully!')
    else:
        print('Database already contains data.')
else:
    print('Creating new database and seeding...')
    seed_database()
    print('Database created and seeded successfully!')
"

echo "Database initialization complete."

# Start the FastAPI server
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
