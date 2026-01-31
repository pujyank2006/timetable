import copy
import random
from typing import List, Any
from app.algorithm.input_data import InputData
from app.algorithm.time_table import TimeTable

class Gene:
    
    slotno: List[int]
    
    def __init__(self, group_index: int, config: Any):
        self.days = config.daysperweek
        self.hours = config.hoursperday
        self.total_slots = self.days * self.hours
        
        self.slotno: List[int] = [0] * self.total_slots
        slot_base_index = group_index * self.total_slots
        local_indices = list(range(self.total_slots))

        subject_to_offsets = {}
        for local_offset in local_indices:
            global_index = slot_base_index + local_offset
            slot_obj = None
            try:
                slot_obj = TimeTable.slot[global_index]
            except Exception:
                slot_obj = None

            subj_name = None
            if slot_obj is not None and hasattr(slot_obj, 'subject') and slot_obj.subject:
                subj_name = str(slot_obj.subject)
            else:
                subj_name = None

            subject_to_offsets.setdefault(subj_name, []).append(local_offset)

        blocks: List[List[int]] = []
        singles: List[int] = []

        for subj, offsets in subject_to_offsets.items():
            if subj is not None and subj.lower().endswith('_lab') and len(offsets) > 0:
                blocks.append(list(offsets))
            else:
                singles.extend(offsets)

        random.shuffle(blocks)
        random.shuffle(singles)

        placement = [None] * self.total_slots
        free_positions = set(range(self.total_slots))

        def find_block_position(m):
            candidates = list(free_positions)
            random.shuffle(candidates)

            for pos in candidates:
                day_hour = pos % self.hours

                if day_hour >= self.hours - m:
                    continue
                
                L = config.lunch_hour
                crosses_lunch = (
                    day_hour < L and day_hour + m > L
                )

                if crosses_lunch:
                    continue

                ok = True
                for q in range(pos, pos + m):
                    if q not in free_positions:
                        ok = False
                        break
                if ok:
                    return pos
            return None

        for block in blocks:
            m = len(block)
            start = find_block_position(m)
            if start is None:
                seq_start = None
                sorted_free = sorted(free_positions)
                for idx in range(len(sorted_free) - m + 1):
                    if sorted_free[idx + m - 1] - sorted_free[idx] == m - 1:
                        seq_start = sorted_free[idx]
                        break
                if seq_start is None:
                    chosen = []
                    for _ in range(m):
                        p = random.choice(list(free_positions))
                        chosen.append(p)
                        free_positions.remove(p)
                    for i_offset, local_off in enumerate(block):
                        placement[chosen[i_offset]] = local_off
                    continue
                else:
                    start = seq_start
            for idx_in_block, local_off in enumerate(block):
                pos = start + idx_in_block
                placement[pos] = local_off
                free_positions.remove(pos)

        remaining_positions = list(free_positions)
        random.shuffle(remaining_positions)
        for pos, local_off in zip(remaining_positions, singles):
            placement[pos] = local_off

        assigned_local_offsets = set(x for x in placement if x is not None)
        remaining_offsets = [o for o in local_indices if o not in assigned_local_offsets]
        remaining_positions = [i for i, v in enumerate(placement) if v is None]
        random.shuffle(remaining_offsets)

        for pos, local_off in zip(remaining_positions, remaining_offsets):
            placement[pos] = local_off

        for j in range(self.total_slots):
            local_offset = placement[j]
            if local_offset is None:
                local_offset = j
            self.slotno[j] = slot_base_index + local_offset

    def deep_clone(self) -> 'Gene':
        return copy.deepcopy(self)