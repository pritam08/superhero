import sqlite3
import json
import os
from pathlib import Path
from typing import List, Dict, Optional

# Database file path - use environment variable or default
DATABASE_PATH = os.getenv('DATABASE_PATH', '/app/data/superheroes.db')
DB_PATH = Path(DATABASE_PATH)

# Ensure the directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

def get_connection():
    """Get database connection"""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row  # This allows dict-like access to rows
    return conn

def init_database():
    """Initialize the database with required tables"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Create superheroes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS superheroes (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            alignment TEXT,
            powerstats TEXT,  -- JSON string
            biography TEXT,   -- JSON string
            appearance TEXT,  -- JSON string
            work TEXT,        -- JSON string
            connections TEXT, -- JSON string
            image TEXT        -- JSON string
        )
    ''')
    
    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            favorites TEXT DEFAULT '[]', -- JSON array of hero IDs
            role TEXT DEFAULT 'user'
        )
    ''')
    
    # Create indexes
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_hero_name ON superheroes(name)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_hero_alignment ON superheroes(alignment)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_username ON users(username)')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at: {DB_PATH}")

class SuperheroDatabase:
    """Database operations for superheroes"""
    
    @staticmethod
    def insert_or_update_hero(hero_data):
        """Insert or update a superhero"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO superheroes 
            (id, name, alignment, powerstats, biography, appearance, work, connections, image)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            hero_data['id'],
            hero_data['name'],
            hero_data.get('alignment', 'neutral'),
            json.dumps(hero_data.get('powerstats', {})),
            json.dumps(hero_data.get('biography', {})),
            json.dumps(hero_data.get('appearance', {})),
            json.dumps(hero_data.get('work', {})),
            json.dumps(hero_data.get('connections', {})),
            json.dumps(hero_data.get('image', {}))
        ))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def find_heroes(name_filter=None, alignment_filter=None, limit=30, skip=0):
        """Find heroes with optional filters"""
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT * FROM superheroes"
        params = []
        conditions = []
        
        if name_filter:
            conditions.append("name LIKE ?")
            params.append(f"%{name_filter}%")
        if alignment_filter:
            conditions.append("alignment = ?")
            params.append(alignment_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += f" LIMIT {limit} OFFSET {skip}"
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        heroes = []
        for row in rows:
            hero = {
                'id': row['id'],
                'name': row['name'],
                'alignment': row['alignment'],
                'powerstats': json.loads(row['powerstats']),
                'biography': json.loads(row['biography']),
                'appearance': json.loads(row['appearance']),
                'work': json.loads(row['work']),
                'connections': json.loads(row['connections']),
                'image': json.loads(row['image'])
            }
            heroes.append(hero)
        
        conn.close()
        return heroes
    
    @staticmethod
    def find_hero_by_id(hero_id):
        """Find a single hero by ID"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM superheroes WHERE id = ?", (hero_id,))
        row = cursor.fetchone()
        
        if row:
            hero = {
                'id': row['id'],
                'name': row['name'],
                'alignment': row['alignment'],
                'powerstats': json.loads(row['powerstats']),
                'biography': json.loads(row['biography']),
                'appearance': json.loads(row['appearance']),
                'work': json.loads(row['work']),
                'connections': json.loads(row['connections']),
                'image': json.loads(row['image'])
            }
            conn.close()
            return hero
        
        conn.close()
        return None
    
    @staticmethod
    def get_random_heroes(count=5):
        """Get random heroes"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM superheroes ORDER BY RANDOM() LIMIT ?", (count,))
        rows = cursor.fetchall()
        
        heroes = []
        for row in rows:
            hero = {
                'id': row['id'],
                'name': row['name'],
                'alignment': row['alignment'],
                'powerstats': json.loads(row['powerstats']),
                'biography': json.loads(row['biography']),
                'appearance': json.loads(row['appearance']),
                'work': json.loads(row['work']),
                'connections': json.loads(row['connections']),
                'image': json.loads(row['image'])
            }
            heroes.append(hero)
        
        conn.close()
        return heroes
    
    @staticmethod
    def search_heroes_by_power(power_type, min_value=50):
        """Search heroes by power type and minimum value"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM superheroes", ())
        rows = cursor.fetchall()
        
        filtered_heroes = []
        for row in rows:
            hero = {
                'id': row['id'],
                'name': row['name'],
                'alignment': row['alignment'],
                'powerstats': json.loads(row['powerstats']),
                'biography': json.loads(row['biography']),
                'appearance': json.loads(row['appearance']),
                'work': json.loads(row['work']),
                'connections': json.loads(row['connections']),
                'image': json.loads(row['image'])
            }
            
            power_value = hero['powerstats'].get(power_type, 0)
            if isinstance(power_value, (int, float)) and power_value >= min_value:
                filtered_heroes.append(hero)
        
        # Sort by power value (descending)
        filtered_heroes.sort(key=lambda h: h['powerstats'].get(power_type, 0), reverse=True)
        
        conn.close()
        return filtered_heroes
    
    @staticmethod
    def count_heroes(name_filter=None, alignment_filter=None):
        """Count heroes with optional filters"""
        conn = get_connection()
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM superheroes"
        params = []
        conditions = []
        
        if name_filter:
            conditions.append("name LIKE ?")
            params.append(f"%{name_filter}%")
        if alignment_filter:
            conditions.append("alignment = ?")
            params.append(alignment_filter)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        
        conn.close()
        return count

class UserDatabase:
    """Database operations for users"""
    
    @staticmethod
    def create_user(username, hashed_password):
        """Create a new user"""
        conn = get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO users (username, hashed_password, favorites, role)
                VALUES (?, ?, ?, ?)
            ''', (username, hashed_password, '[]', 'user'))
            
            user_id = cursor.lastrowid
            conn.commit()
            conn.close()
            
            return {
                'id': user_id,
                'username': username,
                'favorites': [],
                'role': 'user'
            }
        except sqlite3.IntegrityError:
            conn.close()
            return None
    
    @staticmethod
    def find_user_by_username(username):
        """Find user by username"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        
        if row:
            user = {
                'id': row['id'],
                'username': row['username'],
                'hashed_password': row['hashed_password'],
                'favorites': json.loads(row['favorites']),
                'role': row['role']
            }
            conn.close()
            return user
        
        conn.close()
        return None
    
    @staticmethod
    def update_user_favorites(username, favorites):
        """Update user favorites"""
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE users SET favorites = ? WHERE username = ?
        ''', (json.dumps(favorites), username))
        
        conn.commit()
        conn.close()

# Initialize database on import
if __name__ == "__main__":
    init_database()
    print(f"Database initialized at: {DB_PATH}")
