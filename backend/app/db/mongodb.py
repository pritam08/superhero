from pymongo import MongoClient
from app.core.config import settings

client = MongoClient(settings.MONGODB_URI)
db = client[settings.DB_NAME]

def create_indexes():
    db.users.create_index("username", unique=True)
    db.superheroes.create_index("id", unique=True)