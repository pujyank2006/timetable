import os
from typing import List, Any
import random 
import re 

from app.algorithm.student_group import StudentGroup
from app.algorithm.teacher import Teacher

class StudentGroup:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.nosubject = 0
        self.subject: List[str] = [''] * 10
        self.teacher_id: List[int] = [0] * 10
        self.hours: List[int] = [0] * 10

class Teacher:
    def __init__(self):
        self.id = 0
        self.name = ""
        self.subject = ""
        self.assigned = 0 
        self.unavailable_slots: List[int] = [] 

class InputData:
    
    student_group: List[StudentGroup]
    teacher: List[Teacher]
    
    crossover_rate: float = 1.0
    mutation_rate: float = 0.1
    nostudentgroup: int = 0
    noteacher: int = 0
    hoursperday: int = 0
    daysperweek: int = 0
    lunch_hour: int = 4

    MAX_SIZE = 100 
    
    def __init__(self, input_file_path: str = "input.txt"):
        InputData.student_group = [] 
        InputData.teacher = []
        
        self.input_file_path = input_file_path
        
        
        self.unavailability_data = {} 
        
        
        self._take_input()
        self._assign_teacher() 
        self._merge_unavailability_data() 
    
    def _take_input(self):
    
        InputData.hoursperday = 7
        InputData.daysperweek = 5
        InputData.lunch_hour = 4

        try:
            file_path = self.input_file_path
            
            with open(file_path, 'r') as file:
                lines = file.readlines()

            mode = None
            student_group_index = 0
            teacher_index = 0
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
        
                if line.lower() == "studentgroups":
                    mode = "studentgroups"; continue
                elif line.lower() == "teachers":
                    mode = "teachers"; continue
                elif line.lower() == "teacherunavailability":
                    mode = "unavailability"; continue
                elif line.lower() == "end":
                    mode = None; continue

                if mode == "teachers":
                    
                    parts = line.split()
                    if len(parts) < 2: continue

                    teacher = Teacher() 
                    teacher.id = teacher_index
                    teacher.name = parts[0]
                    teacher.subject = parts[1]
                    
                    InputData.teacher.append(teacher)
                    teacher_index += 1
                
                elif mode == "studentgroups":
                    
                    parts = line.split()
                    if not parts: continue
                        
                    sg = StudentGroup()
                    sg.id = student_group_index
                    sg.name = parts[0]
                    
                    j = 0
                    subject_data = parts[1:]
                    for sub, hrs in zip(subject_data[::2], subject_data[1::2]):
                        if j < 10: 
                            sg.subject[j] = sub
                            try:
                                hrs_int = int(hrs)
                            except ValueError:
                                hrs_int = 0

                            
                            
                            if sub.lower().endswith('_lab') and hrs_int == 1:
                                sg.hours[j] = 2
                            else:
                                sg.hours[j] = hrs_int

                            j += 1
                        
                    sg.nosubject = j
                    InputData.student_group.append(sg)
                    student_group_index += 1
                    
                elif mode == "unavailability":
                    
                    parts = line.split()
                    if len(parts) < 2: continue
                        
                    teacher_name = parts[0]
                    slot_indices = [int(p) for p in parts[1:]] 
                    
                    
                    self.unavailability_data[teacher_name.lower()] = slot_indices
                    
            
            InputData.nostudentgroup = len(InputData.student_group)
            InputData.noteacher = len(InputData.teacher)
            
        except FileNotFoundError:
            print(f"Error: Input file not found at {file_path}")

    
    def _merge_unavailability_data(self):
        for teacher in InputData.teacher:
            teacher_name_lower = teacher.name.lower()
            
            if teacher_name_lower in self.unavailability_data:
                teacher.unavailable_slots.extend(
                    self.unavailability_data[teacher_name_lower]
                )
    
    

    def _assign_teacher(self):
        for sg in InputData.student_group:
            for j in range(sg.nosubject):
                
                teacher_id = -1
                assigned_min = -1
                subject = sg.subject[j]

                for k, teacher in enumerate(InputData.teacher):

                    if teacher.subject.lower() == subject.lower():

                        if assigned_min == -1 or teacher.assigned < assigned_min:
                            assigned_min = teacher.assigned
                            teacher_id = k 
                
                if teacher_id != -1:
                    InputData.teacher[teacher_id].assigned += 1 
                    sg.teacher_id[j] = teacher_id