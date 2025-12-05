from dataclasses import dataclass, field
from typing import List, Optional, Any

# Assuming the Teacher class is defined elsewhere (e.g., teacher.py)
# Placeholder for Teacher type definition:
Teacher = Any 

@dataclass
class Subject:
    """
    Data model representing a course subject and its assigned teachers.
    """
    
    # 1. Basic Attributes
    id: Optional[int] = None
    name: Optional[str] = None
    noteachers: int = 0  # Number of teachers assigned to the subject
    
    # 2. Array/List Attribute (Initialized in the Java constructor)
    # The Java code allocated a fixed array size of 20 for teachers.
    # We use a dynamic list, initialized with None placeholders.
    DEFAULT_TEACHER_CAPACITY = 20
    teacher: List[Optional[Teacher]] = field(
        default_factory=lambda: [None] * DEFAULT_TEACHER_CAPACITY
    )