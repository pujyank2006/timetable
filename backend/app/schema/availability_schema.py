from pydantic import BaseModel
from typing import List, Dict

class Availability(BaseModel):
    teacher_id: str
    authentic_unavailability: List[int] | None = None
    current_unavailability: List[int]
    submitted: bool = False

    class Config:
        extra = "forbid"