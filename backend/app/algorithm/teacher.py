# teacher.py
from dataclasses import dataclass, field
from typing import Optional, List, Any

@dataclass
class Teacher:
    id: Optional[int] = None
    name: Optional[str] = None
    subject: Optional[str] = None
    assigned: int = 0
    
    # THIS LINE IS CRUCIAL AND MUST BE PRESENT:
    unavailable_slots: List[int] = field(default_factory=list) 
    
    # If your Teacher class is based on the older Java model with explicit __init__
    # (instead of dataclass), you must add 'self.unavailable_slots = []' 
    # to your constructor.