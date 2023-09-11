import logging
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

from backend.student import Student
from backend.category import Category

"""
TODO exam modes:
- best n-1 of n
- normal
- only if it improves grade
- voluntary / make way to "delete" exam
- absolut bonus (e.g. +0.25 or so)

=> need to rewrite this, mostly (e.g., computing grade with linear vs. fixed points vs. ... requires inheritance, since different method signatures are required)

"""

class Exam:
    def __init__(self, name: str, term: str, classname: str, category: Category,
                 min_grade: float, max_grade: float, grades: dict[Student, float]):
        self.name = name
        # term = hs23 etc.
        self.term = term
        self.class_obj: str = classname
        self.category: Category = category
        if min_grade > max_grade:
            raise RuntimeError(f"Minimum grade must be smaller than maximum grade")
        self.min_grade = min_grade
        self.max_grade = max_grade

        # replaced the self.points by self.grades -- the subclasses should keep the points (e.g. for oral grades..)

        self.grades: dict[Student, float] = {}
        if grades != None:
            self.grades: dict[Student, float] = grades

        # TODO only makes sense in a setting where grades grow from 1 to 6
        if min_grade > max_grade:
            raise RuntimeError(f"Received higher min_grade than max_grade")

    def __str__(self):
        return f"{self.name} ({self.term})"

    def __repr__(self):
        return f"E-{self.name}-{self.term}"

    def number_participants(self):
        """

        :return: The number of students that have written this exam
        """
        return len(self.points.keys())


    def rename(self, new_name: str):
        """
        Renams the exam
        :param new_name:
        :return:
        """
        # TODO maybe include some checks
        self.name = new_name

    def change_category(self, new_category: Category):
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

        # TODO this function should be overwritten in subclasses
        raise NotImplementedError

    def compute_grades(self):
        """
        Computes the grades for all students, based on the compute_single_grade method implemented in subclass
        :return:
        """

        if self.points == None:
            return

        for student in self.points:
            # TODO check for point being -1 (see below), i.e. the grade was overwritten manually
            self.grades[student] = self.compute_single_grade(self.points[student])

    def add_grades_manually(self, grades: dict[Student, float]):
        """
        Wrapper that allows calling add_grade_manually for multiple students
        :param grades: Dict containing the grades of the students that should be overwritten
        :return:
        """

        for stud in grades:
            self.add_grade_manually(stud, grades[stud])


    def add_grade_manually(self, student: Student, grade: float):
        """
        Manually add grade (used to overwrite stuff). Callers job to ensure student is in class
        :param student:
        :param grade:
        :return: -1 if grade was too low, 1 if grade was too high -- will be truncated in either case
        """

        ret = 0
        if grade < self.min_grade:
            ret = -1
            grade = self.min_grade
        elif grade > self.max_grade:
            ret = 1
            grade = self.max_grade

        if student not in self.grades.keys():
            logging.info(f"Student {student} not yet part of exam, adding them...")

        self.grades[student] = grade

        # let the caller know about out of bounds
        return ret


    def add_points(self, points: dict[Student, int]):
        """
        Sets grades and computes respective grades
        :param points: dict mapping students to points
        :return:
        """

        if points is None or len(points) == 0:
            raise RuntimeError(f"Received points dictionary is none or empty")

        for student in points:
            # check if grades will be overwritten
            if self.points is not None:
                if student in self.points:
                    if points[student] != self.points[student]:
                        logging.warning(f"Overwriting old grade {self.points[student]} for {student}")
            self.points[student] = points[student]

        self.compute_grades()


    def generate_summary_report(self, filename):
        """
        Taken from chatGPT, might want to check how well that stuff works
        TODO replace filename with file path
        TODO might want to move that in subclasses -- depending on exam mode, this might be handled differently (e.g. show table with mapping points -> grades)
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
        if not filename.endswith('.pdf'):
            filename = filename + '.pdf'
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


class ExamModeLinear(Exam):
    def __init__(self, name: str, term: str, classname: str, category: Category, max_points: float, points_for_max: float,
                 min_grade: int=1, max_grade=6, points: dict[Student, float] = {}, grades: dict[Student, float] = {}):
        """
        Subclass of Exam dealing with a standard linear fitting mode (achieved_pts/max_pts * 5 + 1)
        :param name: exam name, passed to parent
        :param term: exam term, passed to parent
        :param classname: which class this exam belongs to, passed to parent
        :param category: which category this exam belongs to, passed to parent
        :param max_points: maximum achievable points
        :param points_for_max: points needed to achieve maximum grade
        :param min_grade:
        :param max_grade:
        :param points: points achieved by students
        :param grades: manually overwrite computed grades with present grades
        """

        if len(grades.keys() != 0):
            # pass the grades argument
            super().__init__(self, name, term, classname, category, min_grade, max_grade, grades)
        else:
            super().__init__(self, name, term, classname, category, min_grade, max_grade)

        # define fields specifically for this class
        self.max_points = max_points
        self.points_for_max = points_for_max
        self.points = points

        # make sure to keep the manually set grade over the one calculated by grades
        for student in grades:
            self.points[student] = -1

        if points_for_max > max_points:
            raise RuntimeError(f"Points needed for max grade ({points_for_max}) cannot be higher than maximum possible points ({max_points})")

    def compute_single_grade(self, points: float):
        """
        Computes the grade corresponding to the amount of points, based on params stored in class
        :param points:
        :return: resulting grade, based on received points
        """

        if points < -1:
            raise RuntimeError(f"[EXAM] Cannot compute grade based on negative points")

        # compute the grade
        grade = self.min_grade + (self.max_grade - self.min_grade) * points / self.points_needed_for_6
        grade = round(grade, 4)

        if grade >= self.max_grade:
            logging.warning("[EXAM] Resulting grade was too hight, capping at maximum grade")
            grade = self.max_grade

        return grade

    def add_grade_manually(self, student: Student, grade: float):
        """
        Manually add grade (used to overwrite stuff). Callers job to ensure student is in class
        :param student:
        :param grade:
        :return: -1 if grade was too low, 1 if grade was too high -- will be truncated in either case
        """

        ret = 0
        if grade < self.min_grade:
            ret = -1
            grade = self.min_grade
        elif grade > self.max_grade:
            ret = 1
            grade = self.max_grade

        if student not in self.points.keys():
            logging.info(f"Student {student} not yet part of exam, adding them...")

        # mark that the student's grade was overwritten and should not be automatically computed
        self.points[student] = -1
        self.grades[student] = grade

        # let the caller know about out of bounds
        return ret

    def compute_grades(self):
        """
        Computes the grades for all students, based on the compute_single_grade method implemented in subclass
        :return:
        """

        if self.points == None:
            return

        for student in self.points:
            # if a student's points are -1, the grade was overwritten manually
            if self.points[student] != -1:
                self.grades[student] = self.compute_single_grade(self.points[student])

class ExamModeSetGradeManually(Exam):
    def __init__(self, name: str, term: str, classname: str, category: Category,
                 min_grade: int = 1, max_grade=6, grades: dict[Student, float] = {}):
        super().__init__(self, name, term, classname, category, min_grade, max_grade, grades)

        def compute_single_grade(self, points):
            """
            Must implement this function here, else I'll get errors when Exam.compute_grades() is called from somewhere.
            Does not provide any functionality, but avoids the NotImplementedError in parent class
            :param self:
            :param points:
            :return:
            """

            return


class ExamModeCurveLinearWithPassingPoints(ExamModeLinear):
    def __init__(self, name: str,
                 term: str,
                 classname: str,
                 category: Category,
                 max_points: float,
                 points_for_max: float,
                 points_for_pass: float,
                 min_grade: float=1,
                 passing_grade: float=4,
                 max_grade: float=6,
                 points: dict[Student, float] = {},
                 grades: dict[Student, float] = {}):
        """
        Allows setting a cutoff for passing grade (allowing the teacher to adjust the resulting grades more for difficult exams)
        :param points_for_max: points for maximal grade
        :param points_for_pass: points for passing grade
        :param min_grade: minimum grade, 1 in Switzerland
        :param passing_grade: passing grade, 4 in Switzerland
        :param max_grade: max grade, 6 in Switzerland
        """

        self.passing_grade = passing_grade
        self.points_for_pass = points_for_pass
        if points_for_pass > points_for_max:
            raise RuntimeError(f"Passing points cannot be higher than points for max")

        if not (min_grade <= passing_grade <= max_grade):
            raise RuntimeError(f"Passing grade must be in between minimum possible and maximum possible")
        if points_for_max > max_points:
            raise RuntimeError(
                f"Points needed for max grade ({points_for_max}) cannot be higher than maximum possible points ({max_points})")


        super().__init__(self, name, term, classname, category, max_points, points_for_max,
                 min_grade, max_grade, points, grades)


