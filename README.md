# Student and Course Management with Linked Lists (Tkinter)

This is a Python desktop application for managing students and their courses using **linked lists**. The app features a graphical interface built with **Tkinter** and allows adding, deleting, and listing students and their courses.

---

## Features

- Add a new student by student number.
- Add a course to a student with a grade.
- Delete a course from a student.
- Delete a student.
- List all students (sorted by student number).
- List all courses for a specific student (sorted by course code).
- Interactive GUI for easy use.

---

## Data Structure

- **StudentNode**: Represents a student with a unique student number. Each student maintains their own linked list of courses.
- **CourseNode**: Represents a course with a course code and a grade.
- **StudentList**: Manages the linked list of all students and their courses.

---

## Installation

1. Make sure you have Python 3.x installed.
2. Install Tkinter (usually included with Python):

```bash
# On Linux
sudo apt-get install python3-tk
