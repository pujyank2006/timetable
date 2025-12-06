import copy
import random
from typing import List, Any
from input_data import InputData
# Assuming TimeTable is available elsewhere

class Gene:
    """
    Represents the schedule for a single student group (a gene in the chromosome).
    The slotno attribute holds a random permutation of global slot indices 
    assigned to this group's time block.
    """

    # Static configuration accessed via a placeholder for inputdata
    # Note: In a real Python project, you would define these in input_data.py
    days: input_data.daysperweek
    hours: input_data.hoursperday
    # Instance attributes
    slotno: List[int] # Array/List holding the global Slot indices
    
    def __init__(self, group_index: int, config: Any):
        """
        Initializes the Gene with a random permutation of slots for the given group.

        :param group_index: The index corresponding to this student group (i).
        :param config: Object containing hoursperday and daysperweek.
        """
        self.days = config.daysperweek
        self.hours = config.hoursperday
        # print(self.days)
        self.total_slots = self.days * self.hours
        
        self.slotno: List[int] = [0] * self.total_slots
        
        # --- Java Initialization Logic Explained and Converted ---
        
        # 1. Determine the range of slot indices specific to this group 'i'.
        #    The range is from i * total_slots to (i + 1) * total_slots - 1.
        slot_base_index = group_index * self.total_slots
        
        # 2. Create a list representing the indices within this group's block.
        #    Example: If total_slots=40, this list is [0, 1, ..., 39].
        #    The Java loop used 'rnd' for this.
        local_indices = list(range(self.total_slots))
        
        # 3. Create a random permutation of these local indices.
        #    This is the core of the timetable randomization.
        random.shuffle(local_indices)
        
        # 4. Map the permuted local indices to the final global slot numbers.
        #    slotno[j] = i * days * hours + rnd
        for j in range(self.total_slots):
            # The 'j'th time block in the schedule is assigned the slot 
            # determined by the j'th element of the shuffled list.
            local_offset = local_indices[j]
            self.slotno[j] = slot_base_index + local_offset

    def deep_clone(self) -> 'Gene':
        """
        Performs a deep copy of the Gene instance.
        """
        # Replacing Java's serialization clone with Python's standard library
        return copy.deepcopy(self)
    
    # def print_raw_gene(self):
        """
        Helper method to display the raw slot indices (for debugging).
        """
        # print(f"Slot Indices: {self.slotno}")