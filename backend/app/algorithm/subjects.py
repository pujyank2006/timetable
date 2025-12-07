from dataclasses import dataclass, field
from typing import List, Optional, Any

Teacher = Any 

@dataclass
class Subject:
    id: Optional[int] = None
    name: Optional[str] = None
    noteachers: int = 0  
    DEFAULT_TEACHER_CAPACITY = 20
    teacher: List[Optional[Teacher]] = field(
        default_factory=lambda: [None] * DEFAULT_TEACHER_CAPACITY
    )