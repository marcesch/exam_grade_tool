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

# TODO remove exams from category -- instead, exams are kept in class, with each exam being assigned a category

class Category:
    def __init__(self, name: str, term: str, classname: str, weight: float, grading_type: str = "default"):
        """

        I use terms for correctness -- only exams

        :param name:  name of the category, e.g redaction
        :param weight: weight in float of entire cateogry
        :param grading_type: e.g. best 4 of 5 or so
        """

        # e.g. redaction
        self.name = name
        # e.g. hs23
        self.term = term
        # e.g. 4a
        self.classname = classname
        # self.id = f"{self.term}_{self.classname}_{self.name}"
        # TODO this is only used for the exams themselves
        self.term = term
        self.weight = weight
        self.grading_types = ["default"]
        self.grading_type = grading_type
        if self.grading_type not in self.grading_types:
            logging.error("Unknown grading type. Using default instead")
            self.grading_type = "default"

    def __str__(self):
        return f"{self.name} {self.term}"

    def __repr__(self):
        return f"C-{self.name}"

    def add_exam(self,
                 exam_name: str,
                 term: str,
                 classname: str,
                 max_points: int,
                 points_needed_for_6: int = None,
                 min_grade: int=1,
                 max_grade=6,
                 achieved_points= None,
                 achieved_grades=None,
                 computation_mode = "linear"):
        """

        :param exam:
        :return:
        """

        raise NotImplementedError

        if points_needed_for_6 is None:
            points_needed_for_6 = max_points
        exam = Exam(name=exam_name,
                    term=term,
                    classname=classname,
                    category=self.name,
                    max_points=max_points,
                    points=achieved_points,
                    points_needed_for_6=points_needed_for_6,
                    min_grade=min_grade,
                    max_grade=max_grade,
                    grades=achieved_grades,
                    grade_computation=computation_mode)
        self.exams.append(exam)
        return exam

    def add_grades_for_exam(self):
        """
        updates / adds grades for one single exam
        basically wrapper for caller
        :return:
        """
        raise NotImplementedError

    def update_grading_type(self):
        raise NotImplementedError

    def aggregate_grades(self, student: Student, grades: list[dict[Student, float]]):
        """
        aggregates the final grade for all exams. Usually simply average, but support other types (based on self.grading_tpe)
        :param exams_to_be_counted:  list for all exams that should be counted for a given student
        :return:
        """

        # TODO change that function to work with new layout (maybe receive list of grades from the exam objects, to avoid circular imports)

        # TODO what to do when students are not in all exams etc.
        # => I think caller takes care of it

        raise NotImplementedError

        if self.grading_type == "default":
            sum = 0
            for exam in exams_to_be_counted:
                sum = sum + exam.grades[student]
            return sum / len(exams_to_be_counted)
        elif self.grading_type == "streichnote":
            # cancels the worst result
            if len(exams_to_be_counted) == 1:
                return exams_to_be_counted[0]
            min = -1
            sum = 0
            for exam in exams_to_be_counted:
                sum = sum + exam.grades[student]
                if min == -1 or min > exam.grades[student]:
                    min = exam.grades[student]
            return (sum-min) / (len(exams_to_be_counted)-1)

        else:
            raise NotImplementedError

