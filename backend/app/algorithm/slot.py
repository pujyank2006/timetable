from dataclasses import dataclass
from typing import Optional, Any

StudentGroup = Any 

@dataclass
class Slot:
    student_group: Optional[StudentGroup] = None
    teacher_id: Optional[int] = None
    subject: Optional[str] = None