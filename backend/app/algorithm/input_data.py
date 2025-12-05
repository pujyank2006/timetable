import os
from typing import List, Any
import random 
import re 
# Assuming external classes are available (replace with actual imports)
from student_group import StudentGroup
from teacher import Teacher

# --- Placeholder Classes for Dependencies (if needed for isolated testing) ---
# NOTE: Delete these placeholders if your environment can correctly import 
# the actual StudentGroup and Teacher classes from their modules.
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
# -------------------------------------------------------------------


class InputData:
    """
    Handles initialization of configuration constants and loads scheduling 
    data (Student Groups, Teachers) from an input file.
    """
    
    # Class Variables (accessed statically, equivalent to Java's public static fields)
    student_group: List[StudentGroup]
    teacher: List[Teacher]
    
    crossover_rate: float = 1.0
    mutation_rate: float = 0.1
    nostudentgroup: int = 0
    noteacher: int = 0
    hoursperday: int = 0
    daysperweek: int = 0

    MAX_SIZE = 100 
    
    def __init__(self, input_file_path: str = "input.txt"):
        """Initializes data arrays and loads data from the specified file."""
        
        # Initialize static/class lists
        InputData.student_group = [] 
        InputData.teacher = []
        
        self.input_file_path = input_file_path
        
        # NEW: Temporary storage for unavailability data
        self.unavailability_data = {} 
        
        # Execute data loading, assignment, and final merge
        self._take_input()
        self._assign_teacher() # Assigns subject teachers based on load
        self._merge_unavailability_data() # NEW: Assigns off-times
    
    # --- Data Loading (Modified to save unavailability data temporarily) ---

    def _take_input(self):
        """ Loads scheduling data from the input file. """
        
        # Hardcoded values for development (as per Java)
        InputData.hoursperday = 7
        InputData.daysperweek = 5

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
                
                # --- Mode Transitions ---
                if line.lower() == "studentgroups":
                    mode = "studentgroups"; continue
                elif line.lower() == "teachers":
                    mode = "teachers"; continue
                elif line.lower() == "teacherunavailability":
                    mode = "unavailability"; continue
                elif line.lower() == "end":
                    mode = None; continue
                
                # --- Data Parsing Logic ---
                
                if mode == "teachers":
                    # This section CREATES the Teacher objects
                    parts = line.split()
                    if len(parts) < 2: continue

                    teacher = Teacher() 
                    teacher.id = teacher_index
                    teacher.name = parts[0]
                    teacher.subject = parts[1]
                    
                    InputData.teacher.append(teacher)
                    teacher_index += 1
                
                elif mode == "studentgroups":
                    # This section CREATES StudentGroup objects
                    parts = line.split()
                    if not parts: continue
                        
                    sg = StudentGroup()
                    sg.id = student_group_index
                    sg.name = parts[0]
                    
                    j = 0
                    subject_data = parts[1:]
                    for sub, hrs in zip(subject_data[::2], subject_data[1::2]):
                        if j < 10: # Use fixed size 10 (or MAX_SIZE)
                            sg.subject[j] = sub
                            sg.hours[j] = int(hrs)
                            j += 1
                        
                    sg.nosubject = j
                    InputData.student_group.append(sg)
                    student_group_index += 1
                    
                elif mode == "unavailability":
                    # This section SAVES data temporarily
                    parts = line.split()
                    if len(parts) < 2: continue
                        
                    teacher_name = parts[0]
                    slot_indices = [int(p) for p in parts[1:]] 
                    
                    # SAVE TO DICTIONARY INSTEAD OF ASSIGNING IMMEDIATELY
                    self.unavailability_data[teacher_name.lower()] = slot_indices
                    
            # Update static counters after reading
            InputData.nostudentgroup = len(InputData.student_group)
            InputData.noteacher = len(InputData.teacher)
            
        except FileNotFoundError:
            print(f"Error: Input file not found at {file_path}")

    # --- NEW: Final Merge Method ---
    def _merge_unavailability_data(self):
        """
        Assigns the loaded unavailability data from the temporary dict to the Teacher objects.
        This runs AFTER all Teacher objects are created.
        """
        
        for teacher in InputData.teacher:
            teacher_name_lower = teacher.name.lower()
            
            if teacher_name_lower in self.unavailability_data:
                teacher.unavailable_slots.extend(
                    self.unavailability_data[teacher_name_lower]
                )
    
    # --- Assignment Logic (Load Balancing) ---

    def _assign_teacher(self):
        """
        Assigns the appropriate teacher ID to each subject required by a student group 
        using a simple load-balancing mechanism.
        """

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