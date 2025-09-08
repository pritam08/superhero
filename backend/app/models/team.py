from pydantic import BaseModel
from typing import List


class TeamRequest(BaseModel):
    heroes: List[int]


class TeamPrediction(BaseModel):
    winner: str
    details: str