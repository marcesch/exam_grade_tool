from random import random, seed, randint, uniform

import pytest as pytest
from backend.exam import *
from backend.category import *


# TODO properly assert correct results
# TODO test behavior for grades that are added manually

@pytest.fixture
def gen_students():
    students_6a = [
        Student("Noe", "Matumona"),
        Student("Nicolas", "Zillig"),
        Student("Dominik", "Sarman"),
        Student("Alina", "Kohler"),
        Student("Nina", "Matumona"),
        Student("Marlene", "asdf"),
        Student("Nina", "Kohler"),
    ]
    return students_6a

@pytest.fixture
def gen_example_points(gen_students):
    """
    Fixture providing points
    :param gen_students:
    :return:
    """
    class_6a = gen_students
    max_points = 30

    # make testing seeded for reproducability
    seed(42)
    points = {}
    for student in class_6a:
        points[student] = randint(int(max_points/3),max_points)

    return points, max_points

@pytest.fixture
def gen_example_grades(gen_students):
    """
    Fixture providing grades instead of points
    :param gen_students:
    :return:
    """
    class_6a = gen_students

    seed(17)
    grades = {}
    for student in class_6a:
        grades[student] = uniform()*3 + 3

    return grades


@pytest.mark.ExamModeLinear_test
def test_exam_points_linear_basic_initialized_points(gen_students, gen_example_points):
    class_6a = gen_students
    points, max_points = gen_example_points

    points_for_max = max_points

    base_exam = ExamModeLinear("test1", "hs20", "classX", BaseCategory("defaultCat"), max_points, points_for_max, points=points)

    base_exam.compute_grades()
    print(f"\n[TEST test_exam_points_linear_basic_initialized_points] Results: \n {base_exam.points} \n{base_exam.grades}")


@pytest.mark.ExamModeLinear_test
def test_exam_points_linear_basic_points_added_later(gen_students, gen_example_points):
    class_6a = gen_students
    points, max_points = gen_example_points

    points_for_max = max_points

    base_exam = ExamModeLinear("test1", "hs20", "classX", BaseCategory("defaultCat"), max_points, points_for_max)

    base_exam.add_points(points)

    base_exam.compute_grades()
    print(f"\n[TEST test_exam_points_linear_basic_points_added_later] Results: \n {base_exam.points} \n{base_exam.grades}")

@pytest.mark.ExamModeLinear_test
def test_exam_points_linear_lower_maxpoints(gen_students, gen_example_points):
    class_6a = gen_students
    points, max_points = gen_example_points

    points_for_max = max_points - 5

    base_exam = ExamModeLinear("test1", "hs20", "classX", BaseCategory("defaultCat"), max_points, points_for_max, points=points)

    base_exam.compute_grades()
    print(f"\n[TEST test_exam_points_linear_lower_points_for_max] Results (max grade at {points_for_max}/{max_points} points:  \n {base_exam.points} \n{base_exam.grades}")


@pytest.mark.ExamModeLinearWithPassingGrade_test
def test_exam_points_lwpg_initialized_points(gen_students, gen_example_points):
    class_6a = gen_students
    points, max_points = gen_example_points

    points_for_max = max_points
    points_for_pass = int(1/2*max_points)

    base_exam = ExamModeLinearWithPassingPoints("test1", "hs20", "classX", BaseCategory("defaultCat"), max_points, points_for_max, points_for_pass, points=points)

    base_exam.compute_grades()
    print(f"\n[TEST test_exam_points_lwpg_initialized_points] Results: \n Points for 6: {base_exam.points_for_max} Points for 4: {base_exam.points_for_pass} \n{base_exam.points} \n{base_exam.grades}")

@pytest.mark.ExamModeLinearWithPassingGrade_test
def test_exam_points_lwpg_points_added_later(gen_students, gen_example_points):
    class_6a = gen_students
    points, max_points = gen_example_points

    points_for_max = max_points
    points_for_pass = int(1/2*max_points)

    base_exam = ExamModeLinearWithPassingPoints("test1", "hs20", "classX", BaseCategory("defaultCat"), max_points, points_for_max, points_for_pass)
    base_exam.add_points(points)

    base_exam.compute_grades()
    print(f"\n[TEST test_exam_points_lwpg_initialized_points] Results:\n Points for 6: {base_exam.points_for_max} Points for 4: {base_exam.points_for_pass} \n \n {base_exam.points} \n{base_exam.grades}")


@pytest.mark.ExamModeLinearWithPassingGrade_test
def test_exam_points_lwpg_lower_maxpoints(gen_students, gen_example_points):
    class_6a = gen_students
    points, max_points = gen_example_points

    points_for_max = max_points -3
    points_for_pass = int(1/2*max_points)

    base_exam = ExamModeLinearWithPassingPoints("test1", "hs20", "classX", BaseCategory("defaultCat"), max_points, points_for_max, points_for_pass, points=points)

    base_exam.compute_grades()
    print(f"\n[TEST test_exam_points_lwpg_initialized_points]  Results: \n Points for 6: {base_exam.points_for_max} Points for 4: {base_exam.points_for_pass}  \n {base_exam.points} \n{base_exam.grades}")

