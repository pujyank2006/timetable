# from typing import List, Any
# # Assuming external classes and data are available via dependency injection 
# # or direct import from other modules.

# # Placeholder class for external dependencies (replace with actual imports/classes)
# # We assume the following objects are available in the scope where Utility is used:
# # - input_data: An object with configuration (nostudentgroup, noteacher, etc.)
# # - TimeTable: A class with a static list attribute 'slot'.

# class Utility:
#     """
#     Provides static helper methods for printing and debugging the input data 
#     and the generated slot pool.
#     """
    
#     @staticmethod
#     def print_input_data(input_data: Any):
#         """
#         Prints details about the configuration, student groups, and teachers.
#         Equivalent to Java's public static void printInputData().
#         """
#         print("--- Input Data Summary ---")
#         print(f"No. Student Groups = {input_data.nostudentgroup}")
#         print(f"No. Teachers = {input_data.noteacher}")
#         print(f"Days per Week = {input_data.daysperweek}")
#         print(f"Hours per Day = {input_data.hoursperday}\n")
        
#         # 1. Print Student Group Details
#         print("--- Student Group Requirements ---")
#         for i in range(input_data.nostudentgroup):
#             sg = input_data.student_group[i]
#             print(f"ID {sg.id}: {sg.name}")
            
#             for j in range(sg.nosubject):
#                 # Assumes subject, hours, and teacher_id lists are correctly populated
#                 print(f"  - {sg.subject[j]} | {sg.hours[j]} hrs | Teacher ID: {sg.teacher_id[j]}")
#             print("-" * 20)
            
#         # 2. Print Teacher Details
#         print("\n--- Teacher Details ---")
#         for i in range(input_data.noteacher):			
#             teacher = input_data.teacher[i]
#             print(f"ID {teacher.id}: {teacher.name} | Subject: {teacher.subject} | Assigned: {teacher.assigned}")

    
#     @staticmethod
#     def print_slots(input_data: Any, TimeTable: Any):
#         """
#         Prints the contents of the generated global slot list (lesson pool).
#         Equivalent to Java's public static void printSlots().
#         """
#         days = input_data.daysperweek
#         hours = input_data.hoursperday
#         nostgrp = input_data.nostudentgroup
        
#         total_slots = days * hours * nostgrp
#         slots_per_week_per_group = hours * days
        
#         print("\n---- Generated Slots Pool ----")
#         for i in range(total_slots):
#             current_slot = TimeTable.slot[i]
            
#             if current_slot is not None:
#                 # Assuming Slot object attributes are accessible via dot notation (e.g., dataclass)
#                 print(f"{i:03} - Group: {current_slot.student_group.name} | Subject: {current_slot.subject} | Teacher ID: {current_slot.teacher_id}")
#             else:
#                 print(f"{i:03} - Free Period")
                
#             # Print separator after every student group's full weekly schedule (e.g., every 40 slots)
#             if (i + 1) % slots_per_week_per_group == 0: 
#                 print("******************************")