from pydantic import BaseModel
from typing import Optional, List

class Teacher(BaseModel):
    id: str
    name: str
    department: str
    email: str
    phone: str
    link_token: Optional[str] = None