from pydantic import BaseModel, Field
from typing import List, Optional


class UserIn(BaseModel):
    username: str
    password: str


class UserOut(BaseModel):
    id: Optional[str]
    username: str
    favorites: List[int] = []
    role: str = "user"


class UserInDB(UserOut):
    hashed_password: str