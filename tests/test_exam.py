from random import random, seed, randint, uniform

import pytest as pytest

from backend.classes import Class
from backend.exam import *
from backend.category import *


# TODO properly assert correct results
# TODO test behavior for grades that are added manually



@pytest.fixture
def gen_students():
    """
    Base example of how a class might look like in practice
    :return:
    """

    students = {
        0:Student("stud", "15"),
        1:Student("stud", "16"),
        2:Student("stud", "17"),
        3:Student("stud", "18"),
        4:Student("stud", "19"),
        5:Student("stud", "20"),
        6:Student("stud", "21"),
        7:Student("stud", "22"),
        8:Student("stud", "23"),
        9:Student("stud", "24"),
        10:Student("stud", "25"),
        11:Student("stud", "26"),
        12:Student("stud", "27"),
        13:Student("stud", "28"),
        14:Student("stud", "29"),
        15:Student("stud", "30"),
        16:Student("stud", "31"),
    }

    return students

@pytest.fixture
def gen_full_example(gen_students):
    class_obj = Class("test1", "HS",  2020)

    class_obj.add_multiple_students([(stud.firstname, stud.lastname) for stud in gen_students.values()])

    # initiate categories
    cat_voci = CategoryDefault("voci", 0.2)
    cat_redaction = CategoryDefault("redaction", 0.2)
    cat_grammaire = CategoryDefault("grammaire", 0.3)
    cat_orale = CategoryDefault("orale", 0.1)
    cat_participation = CategoryDefault("participation", 0.15)
    cat_controle_lecture = CategoryDefault("controle_lecture", 0.05)

    args_voci1 = {"max_points" : 22.5,"points_for_max" : 21}
    exam_voci1 = class_obj.add_exam("voci1", cat_voci, "default", args_voci1)
    args_voci2 = {"max_points": 22,"points_for_max": 21}
    exam_voci2 = class_obj.add_exam("voci2", cat_voci, "default", args_voci2)
    args_voci3 = {"max_points": 22,"points_for_max": 22}
    exam_voci3 = class_obj.add_exam("voci3", cat_voci, "default", args_voci3)
    args_voci4 = {"max_points": 22,"points_for_max": 22}
    exam_voci4 = class_obj.add_exam("voci4", cat_voci, "default", args_voci4)
    args_voci5 = {"max_points": 20,"points_for_max": 20}
    exam_voci5 = class_obj.add_exam("voci5", cat_voci, "default", args_voci5)
    args_voci_balzac = {"max_points": 22,"points_for_max": 22}
    exam_voci_balzac = class_obj.add_exam("vociB", cat_voci, "default", args_voci_balzac)
    args_red_1 = {"max_points": 50,"points_for_max": 50}
    exam_red1 = class_obj.add_exam("red1", cat_redaction, "default", args_red_1)
    args_red_2 = {"max_points": 32,"points_for_max": 32}
    exam_red2 = class_obj.add_exam("red2", cat_redaction, "default", args_red_2)
    args_interrog_1 = {"max_points": 46,"points_for_max": 42}
    exam_interrog1 = class_obj.add_exam("interrog1", cat_grammaire, "default", args_interrog_1)
    args_interrog_2 = {"max_points": 60,"points_for_max": 57}
    exam_interrog2 = class_obj.add_exam("interrog2", cat_grammaire, "default", args_interrog_2)
    args_orale = {}
    exam_orale_grade = class_obj.add_exam("orale", cat_participation, "direct_grade", args_orale)
    args_controle_lecture = {"max_points": 10,"points_for_max": 10}
    exam_controle_lecutre = class_obj.add_exam("controle_lecture", cat_controle_lecture, "default", args_controle_lecture)
    args_exam_orale = {}
    exam_orale_exam = class_obj.add_exam("oral_exam", cat_orale, "direct_grade", args_exam_orale)

    # fill in exam points
    points_voci1 = {}
    points_voci2 = {}
    points_voci3 = {}
    points_voci4 = {}
    points_voci5 = {}
    points_vociB = {}
    points_red1 = {}
    points_red2 = {}
    points_interrog1 = {}
    points_interrog2 = {}
    grades_participation = {}
    points_controle_lecture = {}
    grades_orale_exam = {}

    list_points_voci1 = [1.5, 13.5, 16.5, 18, 19, 12, 19, 7, 8.5, 3.5, 18, 8.5, 6, 8.5, 13.5, 0, 13.5]
    list_points_voci2 = [10, 14, 17.5, 21, 16,15.5,19,12,16,14.5,21,15.5,5,12.5,5,4,17]
    list_points_voci3 = [4,15,19.5,21,18,15.5,21.5,14.5,14.5,18,19.5,3,5.5,13,16,11,14.5]
    list_points_voci4 = [3.5,16,15,19.5,18.5,15,19,10.5,4,15.5,18.5,10.5,6.5,0,13,8.5,15]
    list_points_voci5 = [0,0,0,16.5,0,0,18.5,0,0,0,0,18,0,0,0,0,0]
    list_points_vociB = [4.5,15.5,14.5,21,17.5,19.5,18.5,5.5,11.5,11,17,12,4.5,11,15,10,16]
    list_points_redaction1 = [47,38,42,37,49,47,38,41,26,13,43,13,45,47,47,37,39]
    list_point_redaction2 = [0,17,19,19,30,28,21,21,16,23,27,9,27,0,21,19,26]
    list_point_interrog1 = [10,28,35,37,36,33.5,33,22,31.5,19.5,38.5,13,18.5,27,36,30.5,36.5]
    list_point_interrog2 = [5,31.5,48,50.5,40.5,23.5,47,27.5,40.5,24.5,43,25.5,15,28.5,47.5,33,45.5]
    list_grades_participation = [2,3,5.5,5.5,4,3,5.5,3,3.5,2.5,4.5,3,2.5,2.5,4.5,5,3.5]
    list_point_controle_lecture = [2,6.5,6.5,10,4.5,8,10,1,7,2,9.5,3,2,0,7,4,4]
    list_grade_orale = [-1, 3,5 ,5.5,6,-1,5,3,5,2.5,6,3.5,1.5,-1,4,3,5.5]


    for i in range(len(list_points_voci1)):
        # fill in all exams for each student
        current_student = gen_students[i]
        points_voci1[current_student] = list_points_voci1[i]
        points_voci2[current_student] = list_points_voci2[i]
        points_voci3[current_student] = list_points_voci3[i]
        points_voci4[current_student] = list_points_voci4[i]
        points_voci5[current_student] = list_points_voci5[i]
        points_vociB[current_student] = list_points_vociB[i]
        points_red1[current_student] = list_points_redaction1[i]
        points_red2[current_student] = list_point_redaction2[i]
        points_interrog1[current_student] = list_point_interrog1[i]
        points_interrog2[current_student] = list_point_interrog2[i]
        grades_participation[current_student] = list_grades_participation[i]
        points_controle_lecture[current_student] = list_point_controle_lecture[i]

        if list_grade_orale[i] != -1:
            grades_orale_exam[current_student] = list_grade_orale[i]

    # now, add points / grades to exam objects
    exam_voci1.add_points(points_voci1)
    exam_voci2.add_points(points_voci2)
    exam_voci3.add_points(points_voci3)
    exam_voci4.add_points(points_voci4)
    exam_voci5.add_points(points_voci5)
    exam_voci_balzac.add_points(points_vociB)
    exam_red1.add_points(points_red1)
    exam_red2.add_points(points_red2)
    exam_interrog1.add_points(points_interrog1)
    exam_interrog2.add_points(points_interrog2)
    exam_controle_lecutre.add_points(points_controle_lecture)

    exam_orale_grade.add_grades_manually(grades_participation)
    exam_orale_exam.add_grades_manually(grades_orale_exam)

    return class_obj



@pytest.fixture
def gen_students_6a():
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
def gen_example_points(gen_students_61):
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


@pytest.mark.Exam
def test_full_semester_regular(gen_full_example, gen_students):
    """
    Tests with real data a normal behaving semester
    :param gen_full_example:
    :return:
    """

    class_obj = gen_full_example

    expected_grades_voc1 = [1.35714285714286, 4.21428571428571, 4.92857142857143, 5.28571428571429, 5.52380952380952, 3.85714285714286, 5.52380952380952, 2.66666666666667, 3.02380952380952, 1.83333333333333, 5.28571428571429, 3.02380952380952, 2.42857142857143, 3.02380952380952, 4.21428571428571, 1.0, 4.21428571428571]
    expected_grades_voc2 = [3.38095238095238, 4.33333333333333, 5.16666666666667, 6.0, 4.80952380952381, 4.69047619047619, 5.52380952380952, 3.85714285714286, 4.80952380952381, 4.45238095238095, 6.0, 4.69047619047619, 2.19047619047619, 3.97619047619048, 2.19047619047619, 1.95238095238095, 5.04761904761905]
    expected_grades_voc3 = [1.90909090909091, 4.40909090909091, 5.43181818181818, 5.77272727272727, 5.09090909090909, 4.52272727272727, 5.88636363636364, 4.29545454545455, 4.29545454545455, 5.09090909090909, 5.43181818181818, 1.68181818181818, 2.25, 3.95454545454545, 4.63636363636364, 3.5, 4.29545454545455]
    expected_grades_voc4 = [1.79545454545455, 4.63636363636364, 4.40909090909091, 5.43181818181818, 5.20454545454545, 4.40909090909091, 5.31818181818182, 3.38636363636364, 1.90909090909091, 4.52272727272727, 5.20454545454545, 3.38636363636364, 2.47727272727273, 1.0, 3.95454545454545, 2.93181818181818, 4.40909090909091]
    expected_grades_voc5 = [1.0, 1.0, 1.0, 5.125, 1.0, 1.0, 5.625, 1.0, 1.0, 1.0, 1.0, 5.5, 1.0, 1.0, 1.0, 1.0, 1.0]
    expected_grades_vocB = [2.02272727272727, 4.52272727272727, 4.29545454545455, 5.77272727272727, 4.97727272727273, 5.43181818181818, 5.20454545454545, 2.25, 3.61363636363636, 3.5, 4.86363636363636, 3.72727272727273, 2.02272727272727, 3.5, 4.40909090909091, 3.27272727272727, 4.63636363636364]
    expected_grades_red1 = [5.7,4.8,5.2,4.7,5.9,5.7,4.8,5.1,3.6,2.3,5.3,2.3,5.5,5.7,5.7,4.7,4.9]
    expected_grades_red2 = [1.0, 3.65625, 3.96875, 3.96875, 5.6875, 5.375, 4.28125, 4.28125, 3.5, 4.59375, 5.21875, 2.40625, 5.21875, 1.0, 4.28125, 3.96875, 5.0625]
    expected_grades_interrog1 = [2.19047619047619, 4.33333333333333, 5.16666666666667, 5.40476190476191, 5.28571428571429, 4.98809523809524, 4.92857142857143, 3.61904761904762, 4.75, 3.32142857142857, 5.58333333333333, 2.54761904761905, 3.20238095238095, 4.21428571428571, 5.28571428571429, 4.63095238095238, 5.3452380952381]
    expected_grades_interrog2 = [1.43859649122807, 3.76315789473684, 5.21052631578947, 5.42982456140351, 4.55263157894737, 3.06140350877193, 5.12280701754386, 3.41228070175439, 4.55263157894737, 3.14912280701754, 4.7719298245614, 3.23684210526316, 2.31578947368421, 3.5, 5.16666666666667, 3.89473684210526, 4.99122807017544]
    expected_grades_controle_lecture = [2.0, 4.25, 4.25, 6.0, 3.25, 5.0, 6.0, 1.5, 4.5, 2.0, 5.75, 2.5, 2.0, 1.0, 4.5, 3.0, 3.0]
    expected_grades_total = [2.0, 3.79313, 4.85201, 5.28, 4.88387, 3.81197, 5.14356, 3.39968, 3.97711, 3.06494, 5.09385, 2.99695, 2.9369, 2.80063, 4.54614, 3.80096, 4.55848]


    # define custom method for comparing results (taking rounding into account)
    def diff_eq(grade1, grade2, precision=0.001):
        return (abs(grade1-grade2) <= precision)

    # first, individually test the correctness of grades,
    print(f"[TESTING] Checking correctness of individual exams...")
    failed_exams = []
    ex_voci1 = class_obj.get_exam("voci1")
    ex_voci2 = class_obj.get_exam("voci2")
    ex_voci3 = class_obj.get_exam("voci3")
    ex_voci4 = class_obj.get_exam("voci4")
    ex_voci5 = class_obj.get_exam("voci5")
    ex_vociB = class_obj.get_exam("vociB")
    ex_red1 = class_obj.get_exam("red1")
    ex_red2 = class_obj.get_exam("red2")
    ex_interrog1 = class_obj.get_exam("interrog1")
    ex_interrog2 = class_obj.get_exam("interrog2")
    ex_participation = class_obj.get_exam("orale")
    ex_controle_lecture = class_obj.get_exam("controle_lecture")
    ex_oral_exam = class_obj.get_exam("oral_exam")
    print(f"[TESTING] Participation / Orale:\n {ex_participation.grades}\n {ex_oral_exam.grades}")


    ex_voci1.compute_grades()
    ex_voci2.compute_grades()
    ex_voci3.compute_grades()
    ex_voci4.compute_grades()
    ex_voci5.compute_grades()
    ex_vociB.compute_grades()
    ex_red1.compute_grades()
    ex_red2.compute_grades()
    ex_interrog1.compute_grades()
    ex_interrog2.compute_grades()
    ex_controle_lecture.compute_grades()

    print(f"[TESTING] Could compute all grades of the exams. Starting comparison")

    total_diffs = {}
    for i in range(len(gen_students)):
        student_errors = {}
        if  not diff_eq(ex_voci1.grades[gen_students[i]], expected_grades_voc1[i]):
            student_errors[ex_voci1] = (ex_voci1.grades[gen_students[i]], expected_grades_voc1[i], abs(ex_voci1.grades[gen_students[i]] - expected_grades_voc1[i]))
        if  not diff_eq(ex_voci2.grades[gen_students[i]], expected_grades_voc2[i]):
            student_errors[ex_voci2] = (ex_voci2.grades[gen_students[i]], expected_grades_voc2[i], abs(ex_voci2.grades[gen_students[i]]- expected_grades_voc2[i]))
        if  not diff_eq(ex_voci3.grades[gen_students[i]], expected_grades_voc3[i]):
            student_errors[ex_voci3] = (ex_voci3.grades[gen_students[i]], expected_grades_voc3[i], abs(ex_voci3.grades[gen_students[i]]- expected_grades_voc3[i]))
        if not  diff_eq(ex_voci4.grades[gen_students[i]], expected_grades_voc4[i]):
            student_errors[ex_voci4] = (ex_voci4.grades[gen_students[i]], expected_grades_voc4[i], abs(ex_voci4.grades[gen_students[i]]- expected_grades_voc4[i]))
        if not  diff_eq(ex_voci5.grades[gen_students[i]], expected_grades_voc5[i]):
            student_errors[ex_voci5] = (ex_voci5.grades[gen_students[i]], expected_grades_voc5[i], abs(ex_voci5.grades[gen_students[i]]- expected_grades_voc5[i]))
        if not diff_eq(ex_vociB.grades[gen_students[i]], expected_grades_vocB[i]):
            student_errors[ex_vociB] = (ex_vociB.grades[gen_students[i]], expected_grades_vocB[i], abs(ex_vociB.grades[gen_students[i]]- expected_grades_vocB[i]))
        if not diff_eq(ex_red1.grades[gen_students[i]], expected_grades_red1[i]):
            student_errors[ex_red1] = (ex_red1.grades[gen_students[i]], expected_grades_red1[i], abs(ex_red1.grades[gen_students[i]]- expected_grades_red1[i]))
        if not diff_eq(ex_red2.grades[gen_students[i]], expected_grades_red2[i]):
            student_errors[ex_red2] = (ex_red2.grades[gen_students[i]], expected_grades_red2[i], abs(ex_red2.grades[gen_students[i]]- expected_grades_red2[i]))
        if not  diff_eq(ex_interrog1.grades[gen_students[i]], expected_grades_interrog1[i]):
            student_errors[ex_interrog1] = (ex_interrog1.grades[gen_students[i]], expected_grades_interrog1[i], abs(ex_interrog1.grades[gen_students[i]]- expected_grades_interrog1[i]))
        if not diff_eq(ex_interrog2.grades[gen_students[i]], expected_grades_interrog2[i]):
            student_errors[ex_interrog2] = (ex_interrog2.grades[gen_students[i]], expected_grades_interrog2[i], abs(ex_interrog2.grades[gen_students[i]]-expected_grades_interrog2[i]))
        if not diff_eq(ex_controle_lecture.grades[gen_students[i]], expected_grades_controle_lecture[i]):
            student_errors[ex_controle_lecture] = (ex_controle_lecture.grades[gen_students[i]], expected_grades_controle_lecture[i], abs(ex_controle_lecture.grades[gen_students[i]]- expected_grades_controle_lecture[i]))

        if len(student_errors) != 0:
            total_diffs[gen_students[i]] = student_errors

    if len(total_diffs) > 0:
        print(f"\n[TESTING] Error on the following students:\n")
        for row in total_diffs:
            print(f"Student {row}: {total_diffs[row]}")

        assert False

    print(f"[TESTING] Comparison of single exams was successfull")

    # TODO skipped the edge case of students not writing exams (which is in ex_oral_exam) and directly setting grades

    # TODO check also weightes average grades


    print(f"[TESTING] Computing stuff automatically...")

    total_diffs_full_computation = {}
    for student_id in gen_students:
        # skip students with missing exams for now
        if student_id in [0,5, 13]:
            continue
        student = gen_students[student_id]
        computed_grade = class_obj.compute_average_grade_student(student, DEBUG=True)

        if not diff_eq(computed_grade, expected_grades_total[student_id]):
            total_diffs_full_computation[student] = (computed_grade, expected_grades_total[student_id], abs(computed_grade-expected_grades_total[student_id]))

    print(f"[TESTING] Could compute all grades at once using Class-method")

    if len(total_diffs_full_computation) > 0:
        print(f"[TESTING] Error on the following students:")
        print(f"Present exams/categories: {class_obj.exams}\n{class_obj.categories} (sum: {sum([cat.weight for cat in class_obj.categories])})")

        for student in total_diffs_full_computation:
            print(f"Student {student}: {total_diffs_full_computation[student]}")
        assert False


# TODO add testcase for students that have not written all exams











