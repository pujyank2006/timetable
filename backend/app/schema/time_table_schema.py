from pydantic import BaseModel
from typing import List, Dict

class Time_table(BaseModel):
    class_id: str
    ttable: List[int]