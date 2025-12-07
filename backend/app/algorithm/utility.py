# from typing import List, Any

# class Utility:
#     @staticmethod
#     def print_input_data(input_data: Any):
#         print("--- Input Data Summary ---")
#         print(f"No. Student Groups = {input_data.nostudentgroup}")
#         print(f"No. Teachers = {input_data.noteacher}")
#         print(f"Days per Week = {input_data.daysperweek}")
#         print(f"Hours per Day = {input_data.hoursperday}\n")
        
        
#         print("--- Student Group Requirements ---")
#         for i in range(input_data.nostudentgroup):
#             sg = input_data.student_group[i]
#             print(f"ID {sg.id}: {sg.name}")
            
#             for j in range(sg.nosubject):
                
#                 print(f"  - {sg.subject[j]} | {sg.hours[j]} hrs | Teacher ID: {sg.teacher_id[j]}")
#             print("-" * 20)
            
        
#         print("\n--- Teacher Details ---")
#         for i in range(input_data.noteacher):			
#             teacher = input_data.teacher[i]
#             print(f"ID {teacher.id}: {teacher.name} | Subject: {teacher.subject} | Assigned: {teacher.assigned}")

    
#     @staticmethod
#     def print_slots(input_data: Any, TimeTable: Any):
#         days = input_data.daysperweek
#         hours = input_data.hoursperday
#         nostgrp = input_data.nostudentgroup
        
#         total_slots = days * hours * nostgrp
#         slots_per_week_per_group = hours * days
        
#         print("\n---- Generated Slots Pool ----")
#         for i in range(total_slots):
#             current_slot = TimeTable.slot[i]
            
#             if current_slot is not None:
                
#                 print(f"{i:03} - Group: {current_slot.student_group.name} | Subject: {current_slot.subject} | Teacher ID: {current_slot.teacher_id}")
#             else:
#                 print(f"{i:03} - Free Period")
                
            
#             if (i + 1) % slots_per_week_per_group == 0: 
#                 print("******************************")