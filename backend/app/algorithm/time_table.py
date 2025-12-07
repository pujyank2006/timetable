from typing import List, Optional, Any

from app.algorithm.slot import Slot 
from app.algorithm.student_group import StudentGroup 

class PlaceholderInputData:
    def __init__(self, groups: List[StudentGroup], days: int, hours: int):
        self.daysperweek = days
        self.hoursperday = hours
        self.nostudentgroup = len(groups)
        self.studentgroup = groups

class TimeTable:
    slot: List[Optional[Slot]] = []

    def __init__(self, input_data: PlaceholderInputData):
        days = input_data.daysperweek
        hours = input_data.hoursperday
        nostgrp = input_data.nostudentgroup
        
        total_possible_slots = hours * days * nostgrp
        
        TimeTable.slot = [None] * total_possible_slots
        
        k = 0
        for i in range(nostgrp):
            sg = input_data.student_group[i]
            
            subject_no = 0
            hour_count = 1
    
            for j in range(hours * days):
                if subject_no >= sg.nosubject:
                    TimeTable.slot[k] = None 
                    k += 1
                else:
                    current_subject = sg.subject[subject_no]
                    current_teacher_id = sg.teacher_id[subject_no]
                    required_hours = sg.hours[subject_no]
                    TimeTable.slot[k] = Slot(
                        student_group=sg, 
                        teacher_id=current_teacher_id, 
                        subject=current_subject
                    )
                    k += 1
                    if hour_count < required_hours:
                        hour_count += 1
                    else:
                        
                        hour_count = 1
                        subject_no += 1

    @staticmethod
    def return_slots() -> List[Optional[Slot]]:
        return TimeTable.slot