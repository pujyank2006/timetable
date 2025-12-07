from pydantic import BaseModel
from typing import List, Dict

class Availability(BaseModel):
    teacher_id: str
    slots:   List[int]
    submitted: bool = False