from pydantic import BaseModel
from typing import List

class Input_data(BaseModel):
    classid: str
    details: List[str]