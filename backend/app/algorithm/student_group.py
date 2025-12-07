from dataclasses import dataclass, field
from typing import List, Optional

DEFAULT_CAPACITY = 10 

@dataclass
class StudentGroup:
    id: Optional[int] = None
    name: Optional[str] = None
    nosubject: int = 0

    subject: List[str] = field(default_factory=lambda: [''] * DEFAULT_CAPACITY)
    teacher_id: List[int] = field(default_factory=lambda: [0] * DEFAULT_CAPACITY)
    hours: List[int] = field(default_factory=lambda: [0] * DEFAULT_CAPACITY)

    @property
    def num_subjects(self) -> int:
        return self.nosubject

    @num_subjects.setter
    def num_subjects(self, value: Any):
        if isinstance(value, str):
            try:
                self.nosubject = int(value)
            except ValueError:
                
                raise ValueError(f"Cannot convert '{value}' to an integer for nosubject.")
        elif isinstance(value, int):
            self.nosubject = value
        else:
            raise TypeError("num_subjects must be an integer or a string representing an integer.")

    @property
    def group_name(self) -> Optional[str]:
        return self.name

    @group_name.setter
    def group_name(self, value: str):
        self.name = value