from dataclasses import dataclass, field
from typing import Optional, List, Any

@dataclass
class Teacher:
    id: Optional[int] = None
    name: Optional[str] = None
    subject: Optional[str] = None
    assigned: int = 0
    unavailable_slots: List[int] = field(default_factory=list)  