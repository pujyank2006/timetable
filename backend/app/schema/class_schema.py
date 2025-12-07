from pydantic import BaseModel
from typing import List, Dict

class Classes(BaseModel):
    name: str
    subjects: List[str]