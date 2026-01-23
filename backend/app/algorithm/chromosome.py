import copy
from typing import List, Dict, Any, Optional
from app.algorithm.gene import Gene
from app.algorithm.input_data import InputData
from app.algorithm.time_table import TimeTable
from app.algorithm.time_table_storing_service import store_time_table

class Chromosome:   
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

        for group_index in range(self.nostgrp):
            self.gene.append(Gene(group_index, self.timetable_data))

        self.fitness = self.get_fitness()

    def deep_clone(self) -> 'Chromosome':
        return copy.deepcopy(self)

    def get_fitness(self) -> float:
        self.point = 0

        
        for i in range(self.total_slots):
            teacher_list = []

            
            for j in range(self.nostgrp):
                slot_index = self.gene[j].slotno[i]

                
                if slot_index is None or slot_index >= len(TimeTable.slot) or slot_index < 0:
                    continue

                current_slot = TimeTable.slot[slot_index]
                if current_slot is None:
                    continue

                teacher_id = current_slot.teacher_id

                
                if teacher_id is None or teacher_id >= len(self.timetable_data.teacher):
                    continue

                teacher_obj = self.timetable_data.teacher[teacher_id]

                
                if hasattr(teacher_obj, 'unavailable_slots') and i in teacher_obj.unavailable_slots:
                    self.point += 1000

                
                if teacher_id in teacher_list:
                    self.point += 500
                else:
                    teacher_list.append(teacher_id)

        worst_conflict_penalty = (self.nostgrp - 1) * self.total_slots * 250
        worst_unavail_penalty = len(self.timetable_data.teacher) * self.total_slots * 700
        max_conflicts = max(1.0, worst_conflict_penalty + worst_unavail_penalty)

        self.fitness = 1.0 - (self.point / max_conflicts)
        if self.fitness < 0:
            self.fitness = 0.0

        return self.fitness

    
    def print_time_table(self):
        import json
        timetable_dict = {}
        for i in range(self.nostgrp):
            
            group_name = "Unknown Group"
            for l in range(self.total_slots):
                slot_index = self.gene[i].slotno[l]
                current_slot = TimeTable.slot[slot_index]
                if current_slot is not None:
                    group_name = current_slot.student_group.name
                    break

            
            subject_positions = {}
            for pos in range(self.total_slots):
                slot_index = self.gene[i].slotno[pos]
                current_slot = TimeTable.slot[slot_index]
                if current_slot is not None and hasattr(current_slot, 'subject') and current_slot.subject:
                    subj = str(current_slot.subject)
                    subject_positions.setdefault(subj, []).append(pos)

            timetable_dict[group_name] = subject_positions
        print(timetable_dict)
        print(store_time_table(timetable_dict))

    def print_chromosome(self):
        for i in range(self.nostgrp):
            raw_gene_data = [str(self.gene[i].slotno[j]) for j in range(self.total_slots)]
            
        
    
    def __lt__(self, other: 'Chromosome') -> bool:
        return self.fitness > other.fitness