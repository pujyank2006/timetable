from dataclasses import dataclass
from typing import Optional, Any

# Assuming StudentGroup class is defined elsewhere (e.g., student_group.py)
# Placeholder for type definition:
StudentGroup = Any 

@dataclass
class Slot:
    """
    Represents a single lesson block in the timetable. 
    If a slot is None, it implies a free period.
    """
    
    # Python dataclasses automatically generate the constructor (__init__) 
    # and default arguments (like the non-parameterized Slot() constructor).
    
    student_group: Optional[StudentGroup] = None
    teacher_id: Optional[int] = None
    subject: Optional[str] = None

    # The Java code had two constructors:
    # 1. Slot() -> Used for free periods (all fields default to null/None here)
    # 2. Slot(StudentGroup, int, String) -> Used for scheduled lessons
    
    # Usage Notes:
    # - To create a FREE period (like the Java Slot() constructor):
    #   free_slot = Slot()  # All fields will be None
    
    # - To create a scheduled lesson:
    #   lesson_slot = Slot(student_group=group_301, teacher_id=105, subject="Math")