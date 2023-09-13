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

        # ensure that subclasses implement this
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


class CategoryBonus(BaseCategory):
    # TODO might do that as an exam without a category
    def __init__(self, name,  max_bonus_amount):
        """
        Subclass for categories that should not count towards weight, but instead be added absolutely. E.g. bonus grade of 0.25
        :param bonus_weight: How much should the absolute bonus count towards the final grade
        """
        self.bonus_weight = max_bonus_amount
        self.achieved_bonus = dict[Student, float]= {}

        raise NotImplementedError