# FastAPI Superhero Backend Documentation
## For Beginners - Complete Guide

This is a complete guide to understand the FastAPI backend for a Superhero application. I'll explain everything in simple English so you can understand how each part works.

## 🌟 What is this project?

This is a **web backend** (server) built with **FastAPI** that manages:
- **Users** (people who use the app)
- **Superheroes** (like Superman, Batman, etc.)
- **Teams** (groups of superheroes)
- **Authentication** (login/signup)

Think of it like the "brain" of a superhero website where users can:
- Create accounts and log in
- Search for superheroes
- Save favorite superheroes
- Create teams of superheroes

---

## 📁 Project Structure Explained

```
backend/
├── app/                    # Main application folder
│   ├── main.py            # Entry point - starts the server
│   ├── core/              # Core functionality
│   │   └── security.py    # Password hashing, JWT tokens
│   ├── db/                # Database operations
│   │   └── sqlite_db.py   # Database functions
│   ├── models/            # Data structures
│   │   ├── user.py        # User data format
│   │   ├── superhero.py   # Superhero data format
│   │   └── team.py        # Team data format
│   ├── routes/            # API endpoints (URLs)
│   │   ├── auth.py        # Login/Register APIs
│   │   ├── users.py       # User management APIs
│   │   ├── superheroes.py # Superhero APIs
│   │   └── teams.py       # Team creation APIs
│   └── services/          # Business logic (currently empty)
├── requirements.txt       # List of required packages
├── Dockerfile            # Instructions to run in container
└── start.sh             # Script to start the server
```

---

## 🚀 How to Start the Server

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   uvicorn app.main:app --reload
   ```

3. **Access the API:**
   - Server: http://localhost:8000
   - Interactive docs: http://localhost:8000/docs

---

## 📊 Core Concepts

### 1. **FastAPI Framework**
- **What it is:** A modern Python framework for building APIs
- **Why use it:** Fast, automatic documentation, type checking
- **How it works:** You define functions that handle HTTP requests

### 2. **SQLite Database**
- **What it is:** A simple file-based database
- **Why use it:** No setup required, perfect for development
- **What it stores:** Users, superheroes data

### 3. **JWT Authentication**
- **What it is:** JSON Web Tokens for secure login
- **How it works:** User logs in → gets token → uses token for protected actions
- **Why secure:** Token expires, contains user info safely

### 4. **Pydantic Models**
- **What it is:** Python classes that define data structure
- **Why use it:** Automatic validation, clear data format
- **Example:** Ensures email is valid format, password is required

---

## 🔐 Authentication System

### How Login Works:
1. **User registers** → Password gets hashed (encrypted)
2. **User logs in** → Password verified → JWT token created
3. **User makes requests** → Token validated → Access granted

### Security Features:
- **Password hashing:** Plain passwords never stored
- **JWT tokens:** Secure, time-limited access
- **Token expiration:** Automatic logout for security

---

## 📝 API Endpoints Explained

## 🔑 Authentication APIs (`/auth`)

### 1. Register New User
```http
POST /auth/register
```
**What it does:** Creates a new user account

**Input (JSON):**
```json
{
  "username": "john_doe",
  "password": "secret123"
}
```

**How it works:**
1. Checks if username already exists
2. Hashes the password (encrypts it)
3. Saves user to database
4. Returns user info (without password)

**Output:**
```json
{
  "id": "1",
  "username": "john_doe",
  "favorites": [],
  "role": "user"
}
```

### 2. Login User
```http
POST /auth/login
```
**What it does:** Logs in existing user

**Input (Form data):**
- username: john_doe
- password: secret123

**How it works:**
1. Finds user by username
2. Verifies password matches hashed version
3. Creates JWT access token
4. Returns token for future requests

**Output:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

---

## 👤 User Management APIs (`/users`)

### 3. Get Current User Info
```http
GET /users/me
```
**What it does:** Gets logged-in user's information

**Authentication:** Requires valid JWT token in header

**How it works:**
1. Extracts token from request header
2. Verifies token is valid
3. Gets user info from database
4. Returns user details

**Output:**
```json
{
  "id": "1",
  "username": "john_doe",
  "favorites": [1, 15, 23],
  "role": "user"
}
```

### 4. Add Superhero to Favorites
```http
POST /users/favorites/{hero_id}
```
**What it does:** Adds a superhero to user's favorite list

**Example:** `POST /users/favorites/1` (adds hero with ID 1)

**How it works:**
1. Verifies user is logged in
2. Checks if hero already in favorites
3. Adds hero ID to user's favorites list
4. Updates database

### 5. Remove from Favorites
```http
DELETE /users/favorites/{hero_id}
```
**What it does:** Removes superhero from favorites

**How it works:**
1. Gets user's current favorites
2. Removes the hero ID from list
3. Updates database

### 6. Get User's Favorite Heroes
```http
GET /users/favorites
```
**What it does:** Returns full details of user's favorite superheroes

**Output:**
```json
[
  {
    "id": 1,
    "name": "A-Bomb",
    "alignment": "good",
    "powerstats": {
      "intelligence": 38,
      "strength": 100,
      "speed": 17
    },
    "image": {"url": "..."}
  }
]
```

---

## 🦸 Superhero APIs (`/heroes`)

### 7. Get All Heroes
```http
GET /heroes/?q=spider&limit=10&skip=0&alignment=good
```
**What it does:** Searches and lists superheroes

**Parameters:**
- `q`: Search by name (optional)
- `limit`: How many results (default: 30)
- `skip`: How many to skip (for pagination)
- `alignment`: Filter by good/bad/neutral

**How it works:**
1. Builds database query with filters
2. Searches heroes by name pattern
3. Applies alignment filter if specified
4. Returns limited results for pagination

**Example Output:**
```json
[
  {
    "id": 620,
    "name": "Spider-Man",
    "alignment": "good",
    "powerstats": {
      "intelligence": 90,
      "strength": 55,
      "speed": 67,
      "durability": 75,
      "power": 74,
      "combat": 85
    },
    "biography": {
      "full_name": "Peter Benjamin Parker",
      "alter_egos": "No alter egos found"
    },
    "appearance": {
      "height": ["5'10", "178 cm"],
      "weight": ["167 lb", "76 kg"]
    },
    "image": {
      "url": "https://www.superherodb.com/pictures2/portraits/10/100/133.jpg"
    }
  }
]
```

### 8. Get Single Hero
```http
GET /heroes/{hero_id}
```
**What it does:** Gets detailed info about one superhero

**Example:** `GET /heroes/620` gets Spider-Man

**How it works:**
1. Searches database for hero with that ID
2. Returns full hero details or 404 error

### 9. Update Hero
```http
PUT /heroes/{hero_id}
```
**What it does:** Updates superhero information

**Input:** JSON with fields to update
```json
{
  "name": "Updated Spider-Man",
  "powerstats": {
    "intelligence": 95
  }
}
```

### 10. Search Suggestions
```http
GET /heroes/search/suggestions?q=bat&limit=5
```
**What it does:** Provides autocomplete suggestions for search

**How it works:**
1. Requires at least 3 characters
2. Searches hero names
3. Returns only name and ID for dropdown

**Output:**
```json
{
  "suggestions": [
    {"name": "Batman", "id": 69},
    {"name": "Batgirl", "id": 63}
  ],
  "count": 2,
  "query": "bat"
}
```

### 11. Enhanced Search
```http
GET /heroes/search?q=spider&limit=20&skip=0
```
**What it does:** Advanced search with pagination info

**Output includes:**
- `heroes`: Array of matching heroes
- `total`: Total count of matches
- `has_more`: Boolean if more results available

### 12. Get Hero Image
```http
GET /heroes/image/{hero_id}
```
**What it does:** Gets just the image URL for a hero

---

## 👥 Team Management APIs (`/teams`)

### 13. Random Team
```http
GET /teams/random
```
**What it does:** Creates a team of 5 random superheroes

**How it works:**
1. Gets random heroes from database
2. Returns team with metadata

**Output:**
```json
{
  "team": [
    {"id": 1, "name": "A-Bomb", ...},
    {"id": 15, "name": "Abin Sur", ...}
  ],
  "team_size": 5,
  "team_type": "random"
}
```

### 14. Balanced Team
```http
GET /teams/balanced
```
**What it does:** Creates a balanced team with good, bad, and neutral heroes

**How it works:**
1. Gets heroes of each alignment type
2. Picks at least one from each category
3. Fills remaining slots randomly
4. Tracks team composition

**Output:**
```json
{
  "team": [...],
  "team_size": 5,
  "team_type": "balanced",
  "composition": {
    "good": 2,
    "bad": 1,
    "neutral": 2
  }
}
```

### 15. Power-Based Team
```http
GET /teams/power-based?power=strength
```
**What it does:** Creates team based on specific power type

**Power types:** intelligence, strength, speed, durability, power, combat

**How it works:**
1. Finds heroes with minimum 50 in specified power
2. Sorts by power level
3. Takes top performers + some random ones
4. Calculates team statistics

**Output:**
```json
{
  "team": [...],
  "team_type": "power_based_strength",
  "focus_power": "strength",
  "min_power_requirement": 50,
  "team_stats": {
    "avg_power": 87.4,
    "min_power_in_team": 78,
    "max_power_in_team": 100
  }
}
```

### 16. Power Statistics
```http
GET /teams/power-stats
```
**What it does:** Gets statistics about all power types

**Output:**
```json
{
  "available_powers": ["intelligence", "strength", "speed", "durability", "power", "combat"],
  "power_statistics": {
    "strength": {
      "average": 45.2,
      "minimum": 0,
      "maximum": 100,
      "total_heroes": 563
    }
  }
}
```

---

## 🛠️ Technical Components

### 1. **Database Layer (`sqlite_db.py`)**
**What it does:** All database operations

**Key Classes:**
- `SuperheroDatabase`: Manages superhero data
- `UserDatabase`: Manages user accounts

**Key Functions:**
- `find_heroes()`: Search heroes with filters
- `find_hero_by_id()`: Get single hero
- `create_user()`: Add new user
- `update_user_favorites()`: Modify user favorites

### 2. **Security Layer (`security.py`)**
**What it does:** Handles authentication and password security

**Key Functions:**
- `get_password_hash()`: Encrypts passwords
- `verify_password()`: Checks if password is correct
- `create_access_token()`: Makes JWT tokens
- `decode_token()`: Validates JWT tokens

### 3. **Data Models (`models/`)**
**What they do:** Define the structure of data

**User Models:**
- `UserIn`: Data for registration (username, password)
- `UserOut`: Safe user data (no password)
- `UserInDB`: Database version (with hashed password)

**Superhero Models:**
- `Powerstats`: Hero power levels
- `Superhero`: Complete hero information

**Team Models:**
- `TeamRequest`: Request to create custom team
- `TeamPrediction`: Team comparison results

---

## 🔄 How Requests Flow

### Example: User wants to add favorite hero

1. **Frontend sends request:**
   ```http
   POST /users/favorites/620
   Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
   ```

2. **FastAPI receives request:**
   - Extracts JWT token from header
   - Calls `get_current_user()` function

3. **Authentication check:**
   - `decode_token()` validates JWT
   - Finds user in database
   - Returns user info or error

4. **Business logic:**
   - Checks if hero 620 already in favorites
   - Adds hero ID to favorites list
   - Updates database

5. **Response sent:**
   ```json
   {"ok": true}
   ```

---

## 🌐 CORS (Cross-Origin Resource Sharing)

**What it is:** Security feature that allows/blocks web requests

**Why needed:** Frontend (React) runs on different port than backend

**Configuration in `main.py`:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**What this means:**
- Allows requests from React app (ports 3000, 5173)
- Allows cookies/tokens
- Allows all HTTP methods (GET, POST, PUT, DELETE)
- Allows all headers

---

## 🐳 Docker Support

**What Docker does:** Packages the app with all dependencies

**Dockerfile explained:**
1. **Base image:** Python 3.11 slim
2. **Dependencies:** Installs from requirements.txt
3. **App code:** Copies all files
4. **Database:** Creates data directory
5. **Port:** Exposes port 8000
6. **Start command:** Runs uvicorn server

**To run with Docker:**
```bash
docker build -t superhero-backend .
docker run -p 8000:8000 superhero-backend
```

---

## 📈 Error Handling

### Common HTTP Status Codes:
- **200 OK:** Request successful
- **400 Bad Request:** Invalid input data
- **401 Unauthorized:** Login required or invalid token
- **404 Not Found:** Resource doesn't exist
- **500 Internal Server Error:** Server problem

### Example Error Response:
```json
{
  "detail": "Invalid credentials"
}
```

---

## 🔧 Configuration

**Environment Variables:**
- `DATABASE_PATH`: Where to store SQLite database
- `JWT_SECRET`: Secret key for tokens
- `ACCESS_TOKEN_EXPIRE_MINUTES`: How long tokens last

**Default Settings:**
- Database: `superheroes.db`
- Token expiry: 30 minutes
- Server port: 8000

---

## 🧪 Testing the APIs

### Using FastAPI Docs (Recommended for beginners):
1. Start server: `uvicorn app.main:app --reload`
2. Open browser: http://localhost:8000/docs
3. Try each endpoint interactively

### Using curl (Command line):
```bash
# Register user
curl -X POST "http://localhost:8000/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"username": "test", "password": "test123"}'

# Login
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test&password=test123"

# Get heroes (no auth needed)
curl "http://localhost:8000/heroes/?q=spider&limit=5"
```

---

## 🚀 Next Steps for Learning

1. **Try the API:** Use the interactive docs
2. **Modify endpoints:** Add new features
3. **Add validation:** Improve data checking
4. **Add more models:** Create new data types
5. **Learn databases:** Try PostgreSQL instead of SQLite
6. **Add tests:** Write unit tests
7. **Deploy:** Put it on a cloud server

---

## 💡 Common Beginner Questions

**Q: What's the difference between FastAPI and Flask?**
A: FastAPI is newer, faster, has automatic documentation, and better type checking.

**Q: Why use JWT tokens instead of sessions?**
A: JWT tokens work better for APIs, are stateless, and work across different servers.

**Q: What's Pydantic?**
A: It's a library that validates data automatically and creates clear data models.

**Q: Why SQLite instead of MySQL/PostgreSQL?**
A: SQLite is simpler for development, no server setup required.

**Q: How do I add new API endpoints?**
A: Create functions in route files, use decorators like `@router.get("/new-endpoint")`

---

This documentation covers all the basics you need to understand this FastAPI backend. Start by trying the interactive documentation at `/docs` when you run the server!
