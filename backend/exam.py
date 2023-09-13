import logging
import numpy as np
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt

from backend.student import Student
from backend.category import BaseCategory



class Exam:
    def __init__(self,
                 name: str,
                 term: str,
                 year: int,
                 classname: str,
                 category: BaseCategory,
                 min_grade: float,
                 max_grade: float,
                 voluntary: bool,
                 grades: dict[Student, float]):
        self.name = name
        self.term = term.lower()
        self.year = year
        self.class_obj: str = classname
        self.category: BaseCategory = category
        if min_grade > max_grade:
            raise RuntimeError(f"Minimum grade must be smaller than maximum grade")
        self.min_grade = min_grade
        self.max_grade = max_grade

        self.voluntary = voluntary
        if self.voluntary:
            # TODO need to implement this funcionality in classes.py; raise error here to make sure that I'm not confused later on why it does not work
            raise NotImplementedError

        self.grades: dict[Student, float] = grades

        # TODO only makes sense in a setting where grades grow from 1 to 6
        if min_grade > max_grade:
            raise RuntimeError(f"Received higher min_grade than max_grade")

    def __str__(self):
        return f"{self.name.capitalize()} ({self.term.upper()})"

    def __repr__(self):
        return f"E-{self.name.capitalize()}-{self.term.upper()}"


    ####################### FIELD MANIPULATIONS INTERFACE #######################

    def rename(self, new_name: str):
        """
        Renams the exam
        :param new_name:
        :return:
        """
        # TODO maybe include some checks
        self.name = new_name.lower()

    def change_category(self, new_category: BaseCategory):
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

        grade, boundary_check_status = self.enforce_grade_boundaries(grade)

        if student not in self.grades.keys():
            logging.info(f"Student {student} not yet part of exam, adding them...")

        self.grades[student] = grade

        # let the caller know about out of bounds
        return boundary_check_status


    ################# SMALL UTILITY ##################

    def number_participants(self):
        """
        :return: The number of students that have written this exam
        """
        return len(self.grades.keys())

    def enforce_grade_boundaries(self, grade: float):
        """
        Performs boundary checks on grade, caps grades at max/min possible value
        :param grade:
        :return: cleaned_grade, status where status indicates whether grade was too high or too low
        """

        ret = 0
        if grade < self.min_grade:
            ret = -1
            grade = self.min_grade
        elif grade > self.max_grade:
            ret = 1
            grade = self.max_grade

        return grade, ret

    ################## IMPORTANT FUNCTIONALITY #####################

    def compute_grades(self):
        """
        Computes the grades for all students, based on the compute_single_grade method implemented in subclass
        must be overwritten by subclasses
        :return:
        """
        # Ensures that subclass implements this (since looping over self.points is necessary for this, cannot implement it here)
        raise NotImplementedError

    def compute_single_grade(self, points):
        """
        this function should be overwritten in subclasses
        If the subclass does not implement this function, catch a call to the exam object and throw a runtime error
        :param points:
        :return:
        """
        raise NotImplementedError


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
    def __init__(self,
                 name: str,
                 term: str,
                 year: int,
                 classname: str,
                 category: BaseCategory,
                 max_points: float,
                 points_for_max: float,
                 additional_args: dict = {}
                 # min_grade: int=1,
                 # max_grade: int=6,
                 # voluntary: bool = False,
                 # points: dict[Student, float] = {},
                 # grades: dict[Student, float] = {}
                 ):
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

        min_grade = additional_args["min_grade"] if "min_grade" in additional_args else 1
        max_grade = additional_args["max_grade"] if "max_grade" in additional_args else 6
        passing_grade = additional_args["passing_grade"] if "passing_grade" in additional_args else 4
        voluntary = additional_args["voluntary"] if "voluntary" in additional_args else False
        points = additional_args["points"] if "points" in additional_args else {}
        grades = additional_args["grades"] if "grades" in additional_args else {}


        super().__init__(name, term, year, classname, category, min_grade, max_grade, voluntary, grades)

        # define fields specifically for this class
        self.max_points = max_points
        self.points_for_max = points_for_max

        # points entered by user take precedence over manually entered grades -- hence dropping keys form grades where points are available
        self.grades = grades
        self.points = points
        for student in self.points:
            if student in self.grades:
                del self.grades[student]

        if points_for_max > max_points:
            raise RuntimeError(f"Points needed for max grade ({points_for_max}) cannot be higher than maximum possible points ({max_points})")

    ####################### FIELD MANIPULATIONS INTERFACE #######################

    def add_points(self, points: dict[Student, int]):
        """
        Add points after initialization. Points entered take precendece over manually entered grades.
        :param points:
        :return: list of students whose grade was overwritten (CALLERS JOB TO CHECK)
        """

        students_with_overwritten_grades = []
        for student in points:
            if student in self.points:
                if self.points[student] == -1:
                    students_with_overwritten_grades.append(student)
            self.points[student] = points[student]

        return students_with_overwritten_grades

    def add_grade_manually(self, student: Student, grade: float):
        """
        Manually add grade (used to overwrite stuff). Callers job to ensure student is in class
        :param student:
        :param grade:
        :return: -1 if grade was too low, 1 if grade was too high -- will be truncated in either case
        """

        grade, boundary_check_status = self.enforce_grade_boundaries(grade)

        if student not in self.points.keys():
            logging.info(f"Student {student} not yet part of exam, adding them...")

        # mark that the student's grade was overwritten and should not be automatically computed
        self.points[student] = -1
        self.grades[student] = grade

        # let the caller know about out of bounds
        return boundary_check_status

    ################# SMALL UTILITY ##################

    ################## IMPORTANT FUNCTIONALITY #####################

    def compute_single_grade(self, points: float):
        """
        Computes the grade corresponding to the amount of points, based on params stored in class
        :param points:
        :return: resulting grade, based on received points
        """

        if points < -1:
            raise RuntimeError(f"[EXAM] Cannot compute grade based on negative points")

        # compute the grade
        grade = self.min_grade + (self.max_grade - self.min_grade) * points / self.points_for_max
        grade = round(grade, 4)

        if grade >= self.max_grade:
            logging.warning("[EXAM] Resulting grade was too high, capping at maximum grade")
            grade = self.max_grade

        return grade

    def compute_grades(self):
        """
        Computes the grades for all students, based on the compute_single_grade method implemented in subclass
        :return:
        """

        if self.points == None:
            return

        for student in self.points:
            # if a student's points are -1, the grade was overwritten manually
            self.grades[student] = self.compute_single_grade(self.points[student])

class ExamModeSetGradeManually(Exam):
    def __init__(self,
                 name: str,
                 term: str,
                 year: int,
                 classname: str,
                 category: BaseCategory,
                 additional_args = {}
                 # min_grade: int = 1,
                 # max_grade=6,
                 # voluntary=False,
                 # grades: dict[Student, float] = {}
    ):


        min_grade = additional_args["min_grade"] if "min_grade" in additional_args else 1
        max_grade = additional_args["max_grade"] if "max_grade" in additional_args else 6
        voluntary = additional_args["voluntary"] if "voluntary" in additional_args else False
        grades = additional_args["grades"] if "grades" in additional_args else {}



        super().__init__(self, name, term, year, classname, category, min_grade, max_grade, voluntary, grades)

    ####################### FIELD MANIPULATIONS INTERFACE #######################

    ################# SMALL UTILITY ##################

    ################## IMPORTANT FUNCTIONALITY #####################

    def compute_single_grade(self, points):
        """
        Must implement this function here, else I'll get errors when Exam.compute_grades() is called from somewhere.
        Does not provide any functionality, but avoids the NotImplementedError in parent class
        :param self:
        :param points:
        :return:
        """

        return

    def compute_grades(self):
        """
        Compute grades of all students
        :return:
        """
        for student in self.points:
            # TODO check for point being -1 (see below), i.e. the grade was overwritten manually
            self.grades[student] = self.compute_single_grade(self.points[student])


class ExamModeLinearWithPassingPoints(ExamModeLinear):
    def __init__(self,
                 name: str,
                 term: str,
                 year: int,
                 classname: str,
                 category: BaseCategory,
                 max_points: float,
                 points_for_max: float,
                 points_for_pass: float,
                 additional_args: dict = {},
                 # min_grade: float=1,
                 # passing_grade: float=4,
                 # max_grade: float=6,
                 # volutary: bool=False,
                 # points: dict[Student, float] = {},
                 # grades: dict[Student, float] = {}
                 ):
        """
        Allows setting a cutoff for passing grade (allowing the teacher to adjust the resulting grades more for difficult exams)
        :param points_for_max: points for maximal grade
        :param points_for_pass: points for passing grade
        :param min_grade: minimum grade, 1 in Switzerland
        :param passing_grade: passing grade, 4 in Switzerland
        :param max_grade: max grade, 6 in Switzerland
        :param additional_args: dictionary with the additional arguments for this function (used by caller for more elegant code)
        """

        self.points_for_pass = points_for_pass
        if points_for_pass > points_for_max:
            raise RuntimeError(f"Passing points cannot be higher than points for max")


        # unpack additional arguments
        min_grade = additional_args["min_grade"] if "min_grade" in additional_args else 1
        max_grade = additional_args["max_grade"] if "max_grade" in additional_args else 6
        passing_grade = additional_args["passing_grade"] if "passing_grade" in additional_args else 4
        voluntary = additional_args["voluntary"] if "voluntary" in additional_args else False
        points = additional_args["points"] if "points" in additional_args else {}
        grades = additional_args["grades"] if "grades" in additional_args else {}


        if not (min_grade <= passing_grade <= max_grade):
            raise RuntimeError(f"Passing grade must be in between minimum possible and maximum possible")
        if points_for_max > max_points:
            raise RuntimeError(
                f"Points needed for max grade ({points_for_max}) cannot be higher than maximum possible points ({max_points})")

        self.passing_grade = passing_grade
        super().__init__(name, term, year, classname, category, max_points, points_for_max,
                 min_grade, max_grade, voluntary, points, grades)


    ####################### FIELD MANIPULATIONS INTERFACE #######################

    ################# SMALL UTILITY ##################

    ################## IMPORTANT FUNCTIONALITY #####################

    def compute_single_grade(self, points: float):
        """
        Computes grade based on 2 linear fits: from min to passing, from passing to max
        :param self:
        :param points:
        :return:
        """

        if points > self.max_points:
            logging.info(f"[EXAM] Received more points than maximally possible, truncating it...")
            points = self.max_points

        if points < 0:
            raise RuntimeError(f"[EXAM] Can't compute grade for negative points")
        elif points < self.points_for_pass:
            return self.min_grade + (self.passing_grade - self.min_grade) * points / self.points_for_pass
        elif points > self.points_for_pass:
            grade =  self.passing_grade + (self.max_grade - self.passing_grade) * points / self.points_for_max
            return min(self.max_grade, grade)
        else:
            raise RuntimeError(f"[EXAM] Unexpected error while computing grade for {points}")

    def compute_grades(self):
        """
        Compute grades of all students
        :return:
        """
        for student in self.points:
            # TODO check for point being -1 (see below), i.e. the grade was overwritten manually
            self.grades[student] = self.compute_single_grade(self.points[student])


class ExamModeHeavyCurveFitting(Exam):
    def __init__(self):
        """
        Use this mode to enforce a Gaussian curve fit, just for fun I guess
        """
        raise NotImplementedError

    ####################### FIELD MANIPULATIONS INTERFACE #######################

    ################# SMALL UTILITY ##################

    ################## IMPORTANT FUNCTIONALITY #####################

    def compute_single_grade(self, points):
        raise NotImplementedError

    def compute_grades(self):
        raise NotImplementedError

class ExamModeFixedPointScheme(Exam):
    def __init__(self,
                name: str,
                term: str,
                year: int,
                classname: str,
                category: BaseCategory,
                mapping_points_grades: dict[float, float],
                additional_args: dict = {}
                # min_grade: float = 1,
                # max_grade: float = 6,
                # voluntary: bool = False,
                # points: dict[Student, float] = {},
                # grades: dict[Student, float] = {}
                 ):
        """
        Allows to set a fixed point-to-grade mapping (with x points, you get grade y)
        :param mapping_points_grades: dictionary with table point x gets grade y
        :param points:
        :param grades:
        """

        min_grade = additional_args["min_grade"] if "min_grade" in additional_args else 1
        max_grade = additional_args["max_grade"] if "max_grade" in additional_args else 6
        voluntary = additional_args["voluntary"] if "voluntary" in additional_args else False
        points = additional_args["points"] if "points" in additional_args else {}
        grades = additional_args["grades"] if "grades" in additional_args else {}


        self.mapping_points_grades = mapping_points_grades
        self.points = points

        # make sure to keep the manually set grade over the one calculated by grades
        for student in grades:
            self.points[student] = -1


        super().__init__(name, term, year, classname, category, min_grade, max_grade, voluntary, grades)

        # TODO complete
        raise NotImplementedError

    ####################### FIELD MANIPULATIONS INTERFACE #######################


    def add_grade_manually(self, student: Student, grade: float):
        """
        Manually add grade (used to overwrite stuff). Callers job to ensure student is in class
        :param student:
        :param grade:
        :return: -1 if grade was too low, 1 if grade was too high -- will be truncated in either case
        """

        grade, boundary_check_status = self.enforce_grade_boundaries(grade)

        if student not in self.points.keys():
            logging.info(f"Student {student} not yet part of exam, adding them...")

        # mark that the student's grade was overwritten and should not be automatically computed
        self.points[student] = -1
        self.grades[student] = grade

        # let the caller know about out of bounds
        return boundary_check_status

    ################# SMALL UTILITY ##################

    ################## IMPORTANT FUNCTIONALITY #####################


    def compute_single_grade(self, points):
        """

        :param points:
        :return:
        """

        # get the next smaller key in dict and return the grade stored there
        return self.mapping_points_grades[points] if points in self.mapping_points_grades else self.mapping_points_grades[min(self.mapping_points_grades.keys(), key=lambda k: (points - k) if k < points else 1000)]



    # TODO Should be inherited from parent class -- check
    # def compute_grades(self):
    #     """
    #     Computes the grades for all students, based on the compute_single_grade method implemented in subclass
    #     :return:
    #     """
    #
    #     if self.points == None:
    #         return
    #
    #     for student in self.points:
    #         # if a student's points are -1, the grade was overwritten manually
    #         if self.points[student] != -1:
    #             self.grades[student] = self.compute_single_grade(self.points[student])
