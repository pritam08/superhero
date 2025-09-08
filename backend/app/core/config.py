from pydantic import BaseModel


class Settings(BaseModel):
    MONGODB_URI: str ="mongodb://localhost:27017"
    DB_NAME: str = "superhero_db"
    JWT_SECRET: str ="dummy-JWT_SECRET"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    SUPERHERO_API_TOKEN: str = "ff5e2d55a65d32946d6823bc3692943b"
    SEED_START_ID: int = 1
    SEED_END_ID: int = 200




settings = Settings()