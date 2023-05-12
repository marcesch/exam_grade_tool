
"""
add different utilities like e.g. automatically export summary of exam:

- export average, standard deviation, ...
- plot distribution of grades
- ...

"""
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
from typing import Dict
from student import Student
from exam import Exam




points: Dict[Student, int] = {
    Student("John", "Doe"): 80,
    Student("Jane", "Doe"): 90,
    Student("Bob", "Smith"): 75,
    Student("Alice", "Johnson"): 85
}

# Create an exam object
exam = Exam(
    name="Math Exam",
    term="Spring 2023",
    classname="Math 101",
    category="Midterm",
    max_points=100,
    points=points,
    points_needed_for_6=90,
    min_grade=1,
    max_grade=6,
    grade_computation="linear"
)


exam.compute_grades()

exam.generate_summary_report("report.rm")