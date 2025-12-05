from dataclasses import dataclass, field
from typing import List, Optional

# --- Configuration ---
# The Java constructor uses a fixed size of 10 for arrays. 
# In Python, we initialize as empty lists which are dynamic, 
# but we can set defaults based on the Java logic.
DEFAULT_CAPACITY = 10 

@dataclass
class StudentGroup:
    """
    Represents a single group of students, along with their course requirements.
    """
    
    # 1. Attributes (Public fields in Java become standard attributes)
    id: Optional[int] = None
    name: Optional[str] = None
    nosubject: int = 0  # Number of subjects this group is taking
    
    # 2. Array/List Attributes (Initialized in the Java constructor)
    # Using field(default_factory=...) ensures each instance gets its own unique list.
    subject: List[str] = field(default_factory=lambda: [''] * DEFAULT_CAPACITY)
    teacher_id: List[int] = field(default_factory=lambda: [0] * DEFAULT_CAPACITY)
    hours: List[int] = field(default_factory=lambda: [0] * DEFAULT_CAPACITY)

    # Note: Explicit getters and setters are often omitted in Python unless 
    # specific validation or logic is required. If necessary, you can use 
    # Python's built-in @property decorator to define them, as shown below.

    # --- Custom Setter for nosubject (Mimicking Java's Integer.parseInt) ---
    
    @property
    def num_subjects(self) -> int:
        """Mimics getNosubject()"""
        return self.nosubject

    @num_subjects.setter
    def num_subjects(self, value: Any):
        """
        Mimics setNosubject(String snosubject), handling string conversion.
        """
        if isinstance(value, str):
            try:
                self.nosubject = int(value)
            except ValueError:
                # Handle error if the string is not a valid integer representation
                raise ValueError(f"Cannot convert '{value}' to an integer for nosubject.")
        elif isinstance(value, int):
            self.nosubject = value
        else:
            raise TypeError("num_subjects must be an integer or a string representing an integer.")

    # --- Example of a Standard Getter/Setter (Optional) ---
    
    @property
    def group_name(self) -> Optional[str]:
        """Mimics getName()"""
        return self.name

    @group_name.setter
    def group_name(self, value: str):
        """Mimics setName(String name)"""
        self.name = value