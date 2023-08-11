import logging
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

from backend.student import Student

"""
TODO exam modes:
- best n-1 of n
- normal
- only if it improves grade
- voluntary / make way to "delete" exam
- absolut bonus (e.g. +0.25 or so)

"""

class Exam:
    def __init__(self, name: str, term: str, classname: str, category: str, max_points: int, points: dict[Student, int] = None, points_needed_for_6: int = None,
                 min_grade: int = 1, max_grade=6, grades: dict[Student, float] = None, grade_computation="linear"):
        self.name = name
        # term = hs23 etc.
        self.term = term
        self.class_obj: str = classname
        self.category: str = category
        self.max_points = max_points
        self.points_needed_for_6 = points_needed_for_6
        if min_grade != 1:
            logging.info(f"Exa: changing default for min_grade")
        self.min_grade = min_grade
        self.max_grade = max_grade
        self.points = {}
        if self.points != None:
            self.points = points
        self.computation_strategy = grade_computation
        self.computation_strategies = ["linear"]
        self.grades: dict[Student, float] = {}
        if grades != None:
            logging.warning("Manually overwriting grades with user input. Might be inconsistent with points received by students")
            self.grades: dict[Student, float] = grades

        if max_points < points_needed_for_6:
            raise RuntimeWarning("Maximum amount of points should be smaller than points needed for 6")

        if min_grade < 1:
            min_grade = 1
            logging.warning("Setting minimum grade to 1. Lower values don't make sense")

        if min_grade > max_grade:
            logging.error("Received higher min_grade than max_grade")

    def __str__(self):
        return f"{self.name}-{self.term}"

    def __repr__(self):
        return f"E-{self.name}-{self.term}"

    def rename(self, new_name: str):
        """
        Renams the exam
        :param new_name:
        :return:
        """
        # TODO maybe include some checks
        self.name = new_name

    def change_category(self, new_category: str):
        """
        Changes category of the exam:
        1. Add exam to class_obj.new_category
        2. Remove exam from class_obj.old_cat
        3. set self.cat
        :param new_category:
        :return:
        """

        # TODO the caller needs to take care of changing the category of exam / adding to appropriate lists -> can't deal with circular imports
        self.category = new_category

    def compute_single_grade(self, points):
        """
        :param points:
        :return:
        """

        if self.computation_strategy not in self.computation_strategies:
            raise NotImplementedError(f"Did not implement other ways to compute a grade yet\n Try using linear instead of {self.computation_strategy}")

        if points > self.max_points:
            logging.warning("Got too many points, capping at maximum")
            points = self.max_points

        if self.computation_strategy == "linear" or self.computation_strategy == "default":
            grade = self.min_grade + (self.max_grade - self.min_grade) * points / self.points_needed_for_6
            grade = round(grade, 4)
            if grade >= 6:
                grade = 6

        return grade

    def compute_grades(self):
        """
        Using the points, compute the corresponding grades according to grade_computation strategy
        :return:
        """

        if self.points == None:
            return

        old_grades = self.grades

        for student in self.points:
            self.grades[student] = self.compute_single_grade(self.points[student])

        student_changes = []
        for student in old_grades:
            if student not in self.grades or self.grades[student] != old_grades[student]:
                student_changes.append(student)

        for student in self.grades:
            if student not in old_grades:
                student_changes.append(student)

        if old_grades != self.grades:
            logging.warning(f"Grades changed after this update for the following students: \n{student_changes}")

    def add_grade_manually(self, student: Student, grade: float):
        """
        Manually add grade (used to overwrite stuff). Callers job to ensure student is in class
        :param student:
        :param grade:
        :return:
        """

        # TODO boundary checks on grade

        if grade < self.min_grade or grade > self.max_grade:
            logging.warning("Manually overwriting with an illegal grade")

        self.grades[student] = grade

    def add_points(self, points: dict[Student, int]):
        """
        Sets grades and computes respective grades
        :param points: dict mapping students to points
        :return:
        """

        for student in points:
            if student in self.points:
                if points[student] != self.points[student]:
                    logging.warning(f"Overwriting old grade {self.points[student]} for {student}")
            self.points[student] = points[student]

        self.compute_grades()

    def add_grade_from_points_single_student(self, student: Student, points: int):
        """
        calls compute_grade to set the grade
        :param student:
        :param points:
        :return:
        """
        self.grades[student] = self.compute_grade(points)

    def add_grades_mass_import(self, grades: dict[Student, float]):
        """
        Used to import entire table from frontend, I guess?
        :return:
        """

        for student in grades:
            if student in self.grades:
                if grades[student] != self.grades[student]:
                    logging.warning(f"New grade differs for student {student}; old grade {self.grades[student]}")
                    if student in self.points:
                        # need to remove student from points list -- if not, then grades will be overwritten next time they're recomputed
                        self.points.pop(student)
            self.grades[student] = grades[student]

    def generate_summary_report(self, filename):
        """
        Taken from chatGPT, might want to check how well that stuff works
        :param filename:
        :return:
        """
        # Compute summary statistics
        all_points = list(self.points.values())
        all_grades = list(self.grades.values())
        avg_points = np.mean(all_points)
        median_points = np.median(all_points)
        upper_quartile_points = np.percentile(all_points, 75)
        lower_quartile_points = np.percentile(all_points, 25)
        avg_grade = np.mean(all_grades)
        median_grade = np.median(all_grades)
        upper_quartile_grade = np.percentile(all_grades, 75)
        lower_quartile_grade = np.percentile(all_grades, 25)

        # Create a histogram of points and grades
        fig, ax = plt.subplots(1, 2, figsize=(10, 5))
        ax[0].hist(all_points)
        ax[0].set_xlabel('Points')
        ax[0].set_ylabel('Frequency')
        ax[1].hist(all_grades)
        ax[1].set_xlabel('Grades')
        ax[1].set_ylabel('Frequency')

        fig.savefig('histogram.png')

        # Generate a PDF report
        c = canvas.Canvas(filename, pagesize=letter)
        c.drawString(100, 700, f"Summary report for {self.name}")
        c.drawString(100, 675, f"Average points: {avg_points:.2f}")
        c.drawString(100, 650, f"Median points: {median_points:.2f}")
        c.drawString(100, 625, f"Upper quartile points: {upper_quartile_points:.2f}")
        c.drawString(100, 600, f"Lower quartile points: {lower_quartile_points:.2f}")
        c.drawString(100, 575, f"Average grade: {avg_grade:.2f}")
        c.drawString(100, 550, f"Median grade: {median_grade:.2f}")
        c.drawString(100, 525, f"Upper quartile grade: {upper_quartile_grade:.2f}")
        c.drawString(100, 500, f"Lower quartile grade: {lower_quartile_grade:.2f}")
        c.drawImage('histogram.png', 100, 350, width=400, height=200)
        c.showPage()
        c.save()

