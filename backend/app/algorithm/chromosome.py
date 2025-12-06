import copy
from typing import List, Dict, Any, Optional
from gene import Gene
from input_data import InputData
from time_table import TimeTable

# Assuming 'inputdata' and 'TimeTable' are defined elsewhere, 
# likely containing configuration and the list of available slots/lessons.

# --- External Dependencies (Conceptual) ---
# We assume the existence of these external classes/objects:
# 1. inputdata: An object/module containing configuration constants.
# 2. TimeTable: A class/module containing the global 'slot' array/list.
# 3. Gene: A class representing the schedule for one student group.
# 4. Slot: A class representing a single lesson/time block.

# Note: In a real Python project, you would define inputdata, TimeTable, Gene, and Slot classes.

class Chromosome:
    """
    Represents a complete timetable solution (a chromosome) in a Genetic Algorithm.
    The timetable is an array of Genes, where each Gene schedules a student group.
    """
    
    # --- Constructor ---
    def __init__(self, config: InputData):
        self.config = config
        self.timetable_data = config
        
        self.crossover_rate = self.timetable_data.crossover_rate
        self.mutation_rate = self.timetable_data.mutation_rate
        
        self.days = self.timetable_data.daysperweek
        self.hours = self.timetable_data.hoursperday
        self.nostgrp = self.timetable_data.nostudentgroup
        
        self.total_slots = self.days * self.hours
        self.gene = []

        # Create a gene for each student group
        for group_index in range(self.nostgrp):
            self.gene.append(Gene(group_index, self.timetable_data))

        self.fitness = self.get_fitness()

    # --- Utility Methods ---
    
    def deep_clone(self) -> 'Chromosome':
        """
        Performs a deep copy of the Chromosome instance.
        Python's copy.deepcopy is generally used instead of manual serialization.
        """
        # The Java code used serialization for deep cloning, 
        # but Python's standard library provides a direct tool.
        return copy.deepcopy(self)

    # --- Fitness Calculation ---
    
    # chromosome.py (Modified get_fitness method)

    def get_fitness(self) -> float:
        self.point = 0
        
        # Total time blocks in the schedule (e.g., 40 total slots)
        for i in range(self.total_slots):
            teacher_list = [] 
            
            # Check every student group's schedule for this time slot 'i'
            for j in range(self.nostgrp):
                
                slot_index = self.gene[j].slotno[i]
                
                # Retrieve the actual lesson (Slot) object
                current_slot = TimeTable.slot[slot_index]
                
                if current_slot is not None:
                    teacher_id = current_slot.teacher_id
                    
                    # --- NEW HARD CONSTRAINT CHECK ---
                    
                    # Retrieve the Teacher object using the teacher_id
                    # Assumes InputData.teacher list is accessible
                    teacher_obj = self.timetable_data.teacher[teacher_id] 
                    
                    # Check if the global time slot 'i' is in the teacher's unavailable list
                    # This check ensures the class is not scheduled during the teacher's off-time.
                    if i in teacher_obj.unavailable_slots:
                        # Penalize heavily for a Hard Constraint violation
                        self.point += 700 # Use a large penalty value (e.g., 100)
                                        # to ensure solutions with this violation are discarded quickly.
                    
                    # --- EXISTING HARD CONSTRAINT CHECK (Teacher Conflict) ---
                    if teacher_id in teacher_list:
                        self.point += 250 # Normal conflict penalty
                    else:
                        teacher_list.append(teacher_id)
        
                # Calculation remains the same, but the high penalty value (100) 
                # for the new hard constraint ensures fitness drops close to zero.
                max_conflicts = (self.nostgrp - 1.0) * self.total_slots + (self.config.nostudentgroup * 100) # Adjust denominator to reflect Max Penalty
        
                if max_conflicts == 0:
                    self.fitness = 1.0
                else:
                    self.fitness = 1.0 - (self.point / max_conflicts)
            
            return self.fitness

    # --- Output Methods ---

    def print_time_table(self):
        """
        Prints the final timetable for each student group in a readable format.
        """
        for i in range(self.nostgrp):
            
            # Find the first non-free slot to get the student group name
            group_name = "Unknown Group"
            for l in range(self.total_slots):
                slot_index = self.gene[i].slotno[l]
                current_slot = TimeTable.slot[slot_index]
                if current_slot is not None:
                    # Assumes Slot object has a 'studentgroup' object with a 'name' attribute
                    group_name = current_slot.student_group.name
                    break
            
            print(f"Batch {group_name} Timetable:")
            
            # Loop for each day
            for j in range(self.days):
                day_schedule = []
                # Loop for each hour of the day
                for k in range(self.hours):
                    
                    slot_index = self.gene[i].slotno[k + j * self.hours]
                    current_slot = TimeTable.slot[slot_index]
                    
                    if current_slot is not None:
                        # Assumes Slot object has a 'subject' attribute
                        day_schedule.append(current_slot.subject)
                    else:
                        day_schedule.append("*FREE*")
                        
                print(" | ".join(day_schedule))
                
            print("\n\n")

    def print_chromosome(self):
        """
        Prints the raw chromosome structure (the sequence of slot indices).
        """
        for i in range(self.nostgrp):
            raw_gene_data = [str(self.gene[i].slotno[j]) for j in range(self.total_slots)]
            # print(" ".join(raw_gene_data))
        
    # --- Comparison Method (for sorting) ---

    def __lt__(self, other: 'Chromosome') -> bool:
        """
        Implements the comparison logic for Comparable (used for sorting).
        The Java compareTo returns -1 if self > other (higher fitness is better).
        Python's __lt__ returns True if self < other (lower fitness is worse).
        Since we want higher fitness to be sorted first, we use greater than.
        """
        # We want to sort in descending order of fitness (best first).
        # Python's sort is ascending, so we define < as > for descending sort.
        return self.fitness > other.fitness