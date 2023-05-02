import logging
from student import Student


class Exam:
    def __init__(self, name: str, term: str, classname: str, category: str, max_points: int, points_needed_for_6: int, min_grade: int = 1,
                 max_grade=6):
        self.name = name
        # term = hs23 etc.
        self.term = term
        self.classname = classname
        self.category = category
        self.max_points = max_points
        self.points_needed_for_6 = points_needed_for_6
        if min_grade != 1:
            logging.info(f"Exa: changing default for min_grade")
        self.min_grade = min_grade
        self.max_grade = max_grade
        self.grades: dict[Student, float] = {}

        if max_points < points_needed_for_6:
            raise RuntimeWarning("Maximum amount of points should be smaller than points needed for 6")

        if min_grade < 1:
            min_grade = 1
            logging.warning("Setting minimum grade to 1. Lower values don't make sense")

        if min_grade > max_grade:
            logging.error("Received higher min_grade than max_grade")

    def add_grade_manually(self, student: Student, grade: float):
        """
        Manually add grade (used to overwrite stuff). Callers job to ensure student is in class
        :param student:
        :param grade:
        :return:
        """

        # TODO boundary checks on grade

        self.grades[student] = grade
        raise NotImplementedError

    def add_grade_from_points(self, student: Student, points: int):
        """
        calls compute_grade to set the grade
        :param student:
        :param points:
        :return:
        """
        self.grades[student] = self.compute_grade(points)
        raise NotImplementedError

    def add_grades_mass_import(self):
        """
        Used to import entire table from frontend, I guess?
        :return:
        """

    def compute_grade(self, points_reached, modus="default") -> float:
        """
        :param points_reached: points a student reached.
        :param modus: could potentially be used to use different grading scheme than linear
        :return: grade based on points_needed_for_6

        The convoluted formula is just a generalization of 1 + 5 * points_reached / points_for_6
        retunrs unrounded float for precision reasons
        """

        if points_reached > self.max_points:
            logging.warning("Student received more points than possible")

        res = -1
        if modus == "default":
            res = self.min_grade + (self.max_grade - self.min_grade) * points_reached / self.points_needed_for_6
        else:
            raise RuntimeError("Don't know that modus... Aborting")

        return res


class Cateogry:
    def __init__(self, name: str, term: str, classname: str, weight: float, grading_type: str = "default"):
        """

        I use terms for correctness -- only exams

        :param name:  name of the category, e.g redaction
        :param weight: weight in float of entire cateogry
        :param grading_type: e.g. best 4 of 5 or so
        """
        self.name = name
        # e.g. hs23
        self.term = term
        # e.g. 4a
        self.classname = classname
        self.term = term
        self.weight = weight
        self.grading_type = grading_type
        self.exams = []
        raise NotImplementedError

    def add_exam(self, exam_name: str, max_points: int, points_needed_for_6: int, min_grade: int=1, max_grade=6):
        """

        :param exam:
        :return:
        """
        exam = Exam(exam_name, self.name, max_points, points_needed_for_6, min_grade, max_grade)
        self.exams.append(exam)

    def update_grading_type(self):
        raise NotImplementedError

