# Timetable & Invigilation Management System

This project started as a solution to a very practical problem faced in colleges: creating and managing timetables while respecting teacher availability, and later assigning invigilation duties without clashes or unfair distribution.

Instead of treating timetable generation and invigilation as separate problems, this system tries to model how things actually work in real institutions.

# Problem Statement

In most colleges:
- Teachers have fixed availabilities and assigned classes
- Timetables must avoid clashes and overload
- Invigilation duties during exams should:
  - Not clash with teaching schedules
  - Be evenly distributed
  - Respect constraints like maximum duties per teacher

Manually handling all this is time-consuming and error-prone. This project aims to automate that process logically and transparently.

# Features
## Timetable Management
- Maintains teacher availability
- Stores assigned lecture schedules
- Prevents time-slot clashes automatically
- Acts as the base constraint system for further modules
## Invigilation Assigner
- Accepts exam date ranges
- Assigns teachers based on availability
- Ensures:
  - No collision with existing timetable
  - Fair distribution of invigilation days
  - Maximum invigilation limits per teacher
- Flexible time-slot handling

# How It Works (High-Level)
1. Data Preparation
  - Teacher availability
  - Existing teaching timetable
  - Exam dates and time slots
2. Constraint Filtering
  - Remove teachers unavailable during exam slots
  - Eliminate clashes with teaching schedules
3. Assignment Logic
  - Track invigilation count per teacher
  - Assign duties evenly while respecting limits
  - Update availability dynamically after each assignment
4. Validation
  - Final output is checked for conflicts
  - Ensures institutional constraints are satisfied

# Why This Project?
This project was built to:
  - Understand real-world constraint-based scheduling
  - Move beyond simple CRUD systems
  - Apply logical thinking and data structures to practical problems
  - Simulate how academic administration systems actually work
It’s intentionally designed to be extensible rather than a one-off script.

# Tech Stack
- Core logic written in Python
- Data structures for efficient conflict checking
- Designed to integrate easily with backend systems and databases
- Frontend and database integration can be layered on top

# Possible Improvements
- GUI or web interface for administrators
- Database-backed persistent storage
- Support for multiple departments
- Priority-based invigilation assignment
- Export schedules as PDFs or spreadsheets

# Status
This is an actively evolving project. The core logic is implemented and tested, and further improvements are planned based on scalability and real-world use cases.

# Author
Built by a Computer Science student trying to solve problems that actually exist, not just textbook ones.
