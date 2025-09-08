from pydantic import BaseModel
from typing import Optional, Dict, Any


class Powerstats(BaseModel):
    intelligence: Optional[int] = 0
    strength: Optional[int] = 0
    speed: Optional[int] = 0
    durability: Optional[int] = 0
    power: Optional[int] = 0
    combat: Optional[int] = 0


class Superhero(BaseModel):
    id: int
    name: str
    alignment: Optional[str] = "neutral"
    powerstats: Powerstats
    biography: Optional[Dict[str, Any]] = {}
    appearance: Optional[Dict[str, Any]] = {}
    work: Optional[Dict[str, Any]] = {}
    connections: Optional[Dict[str, Any]] = {}
    image: Optional[Dict[str, Any]] = {}