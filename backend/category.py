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

# TODO rewrite category also with subclasses -- each subclass contains aggregate_grades() based on respective fields

class BaseCategory:
    def __init__(self, name: str):
        """

        I use terms for correctness -- only exams

        :param name:  name of the category, e.g redaction
        :param weight: weight in float of entire cateogry
        :param grading_type: e.g. best 4 of 5 or so
        """

        # e.g. redaction
        self.name = name



    def __str__(self):
        return f"{self.name}"

    def __repr__(self):
        return f"C-{self.name}"

    def aggregate_grades(self, list_of_grades: list[dict[Student,float]]):
        """
        Compute the resulting grade for this category from the given list
        :param list_of_grades: list of exam data
        :return:
        """

        # subclasses must implement this


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


class CategoryDefault(BaseCategory):
    def __init__(self, name:str, weight:float):
        """
        Subclass with weight fields for weight as well as computation_mode
        :param name: E.g. Voci
        :param weight: How much the category should weight in comparison to other categories
        """
        raise NotImplementedError

    def aggregate_grades(self, list_of_grades: list[dict[Student,float]]):
        """

        :param list_of_grades:
        :return:
        """
        raise NotImplementedError

class CategoryWithDroppedGrades(CategoryDefault):
    def __init__(self, name: str, weight: float, number_drop_grades: int=1):
        """
        Subclass to only count the best n-number_drop_grades of n exams (Streichnote, in Deutsch
        :param name:
        :param weight:
        :param number_drop_grades:
        """

        self.number_drop_grades = number_drop_grades
        super().__init__(name, weight)

        raise NotImplementedError

    def aggregate_grades(self, list_of_grades: list[dict[Student,float]]):
        """

        :param list_of_grades:
        :return:
        """

        raise NotImplementedError

class CategoryOnlyIfImproves(BaseCategory):
    def __init__(self, name: str, weight: float):
        """
        Exam results from this category should only count if it improves the grade.
        :param name:
        :param weight:
        """
        raise NotImplementedError

class CategoryBonus(BaseCategory):
    # TODO might do that as an exam without a category
    def __init__(self, bonus_weight, achieved_bonus: dict[Student, float]):
        """
        Subclass for categories that should not count towards weight, but instead be added absolutely. E.g. bonus grade of 0.25
        :param bonus_weight: How much should the absolute bonus count towards the final grade
        :param achieved_bonus: "Hardcode" the achieved bonus instead of creating a new exam
        """
        self.bonus_weight = bonus_weight
        self.achieved_bonus = achieved_bonus
        raise NotImplementedError