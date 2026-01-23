from pydantic import BaseModel
from typing import List

class InvigAssignmentRequest(BaseModel):
    exam_date_from: str
    exam_date_to: str
    teacher_names: List[str]
    teachers_per_day: int
    exam_time_start: str
    exam_time_end: str

class InvigDayAssignment(BaseModel):
    date: str
    teachers: List[str]

class InvigAssignmentResponse(BaseModel):
    assignments: List[InvigDayAssignment]
