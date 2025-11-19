from pydantic import BaseModel
from typing import Optional, List

class Teacher(BaseModel):
    id: str
    name: str
    department: str
    link_token: Optional[str] = None