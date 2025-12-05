from pydantic import BaseModel
from typing import List, Dict

class Availability(BaseModel):
    teacher_id: str
    availability:   Dict[str, List[int]]
    submitted: bool = False