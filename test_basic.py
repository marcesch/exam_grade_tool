import os
import shutil

import pytest as pytest

from classes import Class


# TODO do it properly with pytest


@pytest.mark.student_management
def test_student_management_basic():
    """
    Tests some basic functionality for adding, deleting and storing students to a class
    """
    class_6a = Class("6a", "hs", 2016)
    class_3b = Class("3b", "hs", 2016)

    students_6a = [
        {"firstname": "Noe", "lastname": "Matumona"},
        {"firstname": "Nicolas", "lastname": "Zillig"},
        {"firstname": "Dominik", "lastname": "Sarman"},
        {"firstname": "Alina", "lastname": "Kohler"},
    ]

    students_3b = [
        {"firstname": "Nina", "lastname": "Matumona"},
        {"firstname": "Marlene", "lastname": "asdf"},
        {"firstname": "Nina", "lastname": "Kohler"},
        {"firstname": "Noe", "lastname": "Matumona"},
    ]

    class_6a.initialize_new_class(students_6a)
    class_3b.initialize_new_class(students_3b)
    assert class_3b.contains_student("Nina", "Matumona")
    assert not class_6a.contains_student("asdf", "asdf")
    class_6a.remove_student("Noe", "Matumona")
    assert not class_6a.contains_student("Noe", "Matumona")
    with pytest.raises(RuntimeWarning):
        class_6a.remove_student("Noe", "Matumona")

    len1 = len(class_3b.students)
    class_3b.add_student("Nina", "Kohler")
    assert len(class_3b.students) == len1


@pytest.mark.file_management
def test_basic_files():
    """
    Tests whether the right files are created and deleted. Only targets class lists, not yet exams themselves
    :return:
    """
    students_6a = [
        {"firstname": "Noe", "lastname": "Matumona"},
        {"firstname": "Nicolas", "lastname": "Zillig"},
        {"firstname": "Dominik", "lastname": "Sarman"},
        {"firstname": "Alina", "lastname": "Kohler"},
        {"firstname": "Nina", "lastname": "Matumona"},
        {"firstname": "Marlene", "lastname": "asdf"},
        {"firstname": "Nina", "lastname": "Kohler"},
        {"firstname": "Noe", "lastname": "Matumona"},
    ]

    class_6a = Class("6a", "HS", 2015)
    class_6a.initialize_new_class(students_6a)

    location_6a = class_6a.filename_class
    assert os.path.isfile(location_6a)

    class_6a.update_name("NewName_6a")
    location_newName_6a = class_6a.filename_class
    class_6a.store_to_database()
    assert os.path.isfile(location_newName_6a), f"Not found; location: {location_newName_6a}"

    class_6a.update_semester()
    location_6a_new_term = class_6a.filename_class
    class_6a.store_to_database()
    assert os.path.isfile(location_6a_new_term)

    # check also that the old files were deleted
    # TODO this does not work yet -- need to move old files to trash!
    assert not os.path.isfile(location_6a)
    assert not os.path.isfile(location_newName_6a)


@pytest.mark.skip
@pytest.mark.file_management
def test_trash_functionality():
    """
    Tests whether the right files are put in the trash when needed and if I can empty it correclty etc.
    :return:
    """
    raise NotImplementedError


@pytest.mark.test_exam
def test_cateogries_exams_simple():
    """
    Tests simple functionality of exams / categories, like adding exams / cateogories, deleting them, ...

    Not yet with student's data (or at least, nothing is done with their grades
    :return:
    """

    students_6a = [
        {"firstname": "Noe", "lastname": "Matumona"},
        {"firstname": "Nicolas", "lastname": "Zillig"},
        {"firstname": "Dominik", "lastname": "Sarman"},
        {"firstname": "Alina", "lastname": "Kohler"},
        {"firstname": "Nina", "lastname": "Matumona"},
        {"firstname": "Marlene", "lastname": "asdf"},
        {"firstname": "Nina", "lastname": "Kohler"},
    ]

    class_6a = Class("6x", "HS", 2015)
    class_6a.initialize_new_class(students_6a)

    categories = [
        {"name": "oral", "weight": 0.3, "grading_type": "default"},
        {"name": "redaction", "weight": 0.2},
        {"name": "voci", "weight": 0.3},
    ]

    class_6a.initialize_categories(categories)
    class_6a.add_category({"name": "grammaire", "weight": 0.2})
    class_6a.add_category({"name": "asdf", "weight": 0.5})
    class_6a.remove_category("asdf")

    points_max = [25, 25, 15, 15, 15, 10, 35, 35]
    points_for_6 = [22, 23, 15, 15, 15, 10, 30, 28]
    grades_noe = [25, 25, 15, 15, 15, 10, 35, 35]
    grades_nici = [15, 15, 10, 10, 9, 10, 20, 20]
    grades_dominik = [8, 22, 15, 7, 9, 10, 17, 17]
    grades_alina = [0, 0, 0, 0, 0, 0, 0, 0]
    grades_nina = [23, 18, 14, 15, 14, 10, 30, 29]
    grades_marlene = [21, 16, 12, 14, 14, 7, 28, 29]
    grades_nina2 = [20, 15, 12, 13, 11, 10, 26, 26]

    noe = class_6a.get_student("Noe", "Matumona")
    nici = class_6a.get_student("Nicolas", "Zillig")
    dominik = class_6a.get_student("Dominik", "Sarman")
    alina = class_6a.get_student("Alina", "Kohler")
    nina = class_6a.get_student("Nina", "Matumona")
    marlene = class_6a.get_student("Marlene", "asdf")
    nina2 = class_6a.get_student("Nina", "Kohler")

    redaction1 = {
                    noe: grades_noe[0],
                    nici: grades_nici[0],
                    dominik: grades_dominik[0],
                    alina: grades_alina[0],
                    nina: grades_nina[0],
                    marlene: grades_marlene[0],
                    nina2: grades_nina2[0]
                  }
    redaction2 = {
                    noe: grades_noe[1],
                    nici: grades_nici[1],
                    dominik: grades_dominik[1],
                    alina: grades_alina[1],
                    nina: grades_nina[1],
                    marlene: grades_marlene[1],
                    nina2: grades_nina2[1]
                  }
    voci1 = {
                    noe: grades_noe[2],
                    nici: grades_nici[2],
                    dominik: grades_dominik[2],
                    alina: grades_alina[2],
                    nina: grades_nina[2],
                    marlene: grades_marlene[2],
                    nina2: grades_nina2[2]
                  }
    voci2 = {
                    noe: grades_noe[3],
                    nici: grades_nici[3],
                    dominik: grades_dominik[3],
                    alina: grades_alina[3],
                    nina: grades_nina[3],
                    marlene: grades_marlene[3],
                    nina2: grades_nina2[3]
                  }

    voci3 = {
                    noe: grades_noe[4],
                    nici: grades_nici[4],
                    dominik: grades_dominik[4],
                    alina: grades_alina[4],
                    nina: grades_nina[4],
                    marlene: grades_marlene[4],
                    nina2: grades_nina2[4]
                  }

    oral = {
                    noe: grades_noe[5],
                    nici: grades_nici[5],
                    dominik: grades_dominik[5],
                    alina: grades_alina[5],
                    nina: grades_nina[5],
                    marlene: grades_marlene[5],
                    nina2: grades_nina2[5]
                  }

    grammaire1 = {
                    noe: grades_noe[6],
                    nici: grades_nici[6],
                    dominik: grades_dominik[6],
                    alina: grades_alina[6],
                    nina: grades_nina[6],
                    marlene: grades_marlene[6],
                    nina2: grades_nina2[6]
                  }

    grammaire2 = {
                    noe: grades_noe[7],
                    nici: grades_nici[7],
                    dominik: grades_dominik[7],
                    alina: grades_alina[7],
                    nina: grades_nina[7],
                    marlene: grades_marlene[7],
                    nina2: grades_nina2[7]
                  }

    class_6a.add_exam("redaction 1", "redaction", points_max[0], points_needed_for_6=points_for_6[0], achieved_points=redaction1)
    class_6a.add_exam("redaction 2", "redaction", points_max[1], points_needed_for_6=points_for_6[1], achieved_points=redaction2)
    class_6a.add_exam("voci 1", "voci", points_max[2], achieved_points=voci1)
    class_6a.add_exam("voci 2", "voci", points_max[3], achieved_points=voci2)
    class_6a.add_exam("voci 3", "voci", points_max[4], achieved_points=voci3)
    class_6a.add_exam("orale", "oral", points_max[5], achieved_points=oral)
    class_6a.add_exam("grammaire 1", "grammaire", points_max[6], points_for_6[6], achieved_points=grammaire1)
    class_6a.add_exam("grammaire 2", "grammaire", points_max[7], points_for_6[7], achieved_points=grammaire2)

    class_6a.store_exams()
    class_6a.create_grade_report()

    report_location = os.path.join(class_6a.filename_class_base, f"{class_6a.name}_report{(class_6a.report_id-1):02}.xlsx")
    shutil.copy(report_location, "./results_tests/")
    with open("./results_tests/exams_testrun_exams_simple", "w") as f:
        f.write(f"Categories: {[cat.__str__() for cat in class_6a.categories]}\n\n")
        for cat in class_6a.categories:
            f.write(f"Cat {cat}: exams:\n{[ex.__str__() for ex in cat.exams]}\n")


test_cateogries_exams_simple()
exit()

@pytest.mark.test_exam
@pytest.mark.skip
def test_mixed_points_grades():
    """
    tests behavior when directly setting some of the grades (e.g. used for oral grades, ...)
    :return:
    """
    raise NotImplementedError

@pytest.mark.test_exam
@pytest.mark.skip
def test_categories_exams_grade_calculation_basic():
    """
    Test correctness of grade computation if everything works as expected. Use Selina's data as an example
    :return:
    """
    raise NotImplementedError


@pytest.mark.test_exam
@pytest.mark.skip
def test_categories_exams_grade_calculation_edge_cases():
    """
    Tests whacky shit like student not taking exam, ...
    :return:
    """
    raise NotImplementedError


@pytest.mark.test_exam
@pytest.mark.skip
def test_categories_exam_failures_in_grade_computation():
    """
    Tests behavior that should result in fails, e.g.
    1. sum of weight is not 1
    2. Generating report on empty exam-set
    3. Maybe truly whacky shit like grades that are higher than max grade.
    :return:
    """
    raise NotImplementedError


@pytest.mark.file_management
@pytest.mark.skip
def test_check_correct_storage_of_exams():
    """
    Tests whether files are created correctly

    :return:
    """
    raise NotImplementedError


@pytest.mark.multiple_classes
@pytest.mark.skip
def test_simple_multiple_classes():
    """
    Repeats the tests from above with multiple classes
    :return:

    """
    raise NotImplementedError


@pytest.mark.multiple_classes
@pytest.mark.skip
def test_multiple_classes_weird_behavior():
    """
    Tests different failure paths, like
    - updating terms / names until two classes collide (e.g. 6a-HS-2022 and 4a-HS-2020 -- update the 4a class until it clashes with 6a)
    :return:
    """
    raise NotImplementedError


@pytest.mark.skip
def test_class_management():
    """
    Not sure what to do with this stuff yet -- mainly just test some things
    :return:
    """

    print("Starting program")

    class_6a = Class("6a", "hs", 2016)
    class_3b = Class("3b", "hs", 2016)

    students = [
        {"firstname": "Noe", "lastname": "Matumona"},
        {"firstname": "Nicolas", "lastname": "Zillig"},
        {"firstname": "Dominik", "lastname": "Sarman"},
        {"firstname": "Alina", "lastname": "Kohler"},
        # {"firstname": "Renato", "lastname": "Meier"},
        # {"firstname": "Adrian", "lastname": "Pfeiffer"},
        # {"firstname": "Nina", "lastname": "Matumona"},
        # {"firstname": "Marlene", "lastname": "asdf"},
        # {"firstname": "Nina", "lastname": "Kohler"},
        # {"firstname": "Noe", "lastname": "Matumona"},
    ]

    students2 = [
        {"firstname": "Nina", "lastname": "Matumona"},
        {"firstname": "Marlene", "lastname": "asdf"},
        {"firstname": "Nina", "lastname": "Kohler"},
        {"firstname": "Noe", "lastname": "Matumona"},
    ]

    class_6a.initialize_new_class(students)
    class_3b.initialize_new_class(students2)

    class_6a.add_student("Marcel", "Schmid")
    class_6a.remove_student("Nicolas", "Zillig")

    print("Starting to store to DB")
    class_6a.store_to_database()
    class_3b.store_to_database()

    class_6a.update_semester()
    print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")
    class_6a.update_semester()
    print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")

    categories = [
        {"name": "oral", "weight": 0.3, "grading_type": "default"},
        {"name": "redaction", "weight": 0.2},
        {"name": "voci", "weight": 0.3},
    ]

    class_6a.initialize_categories(categories)
    class_6a.add_category({"name": "grammaire", "weight": 0.2})
    class_6a.add_category({"name": "asdf", "weight": 0.5})
    class_6a.remove_category("asdf")

    grades_noe = [25, 25, 15, 15, 15, 10, 35, 35]
    grades_nici = [15, 15, 10, 10, 9, 10, 20, 20]
    grades_dominik = [8, 22, 15, 7, 9, 12, 17, 17]
    grades_alina = [0, 0, 0, 0, 0, 0, 0, 0]

    noe = class_6a.get_student("Noe", "Matumona")
    nici = class_6a.get_student("Nicolas", "Zillig")
    dominik = class_6a.get_student("Dominik", "Sarman")
    alina = class_6a.get_student("Alina", "Kohler")

    redaction1 = {noe: grades_noe[0], nici: grades_nici[0], dominik: grades_dominik[0], alina: grades_alina[0]}
    redaction2 = {noe: grades_noe[1], nici: grades_nici[1], dominik: grades_dominik[1], alina: grades_alina[1]}
    voci1 = {noe: grades_noe[2], nici: grades_nici[2], dominik: grades_dominik[2], alina: grades_alina[2]}
    voci2 = {noe: grades_noe[3], nici: grades_nici[3], dominik: grades_dominik[3], alina: grades_alina[3]}
    voci3 = {noe: grades_noe[4], nici: grades_nici[4], dominik: grades_dominik[4], alina: grades_alina[4]}
    orale = {noe: grades_noe[5], nici: grades_nici[5], dominik: grades_dominik[5], alina: grades_alina[5]}
    grammaire1 = {noe: grades_noe[6], nici: grades_nici[6], dominik: grades_dominik[6], alina: grades_alina[6]}
    grammaire2 = {noe: grades_noe[7], nici: grades_nici[7], dominik: grades_dominik[7], alina: grades_alina[7]}

    class_6a.add_exam("redaction 1", "redaction", 25, points_needed_for_6=22, achieved_points=redaction1)
    class_6a.add_exam("redaction 2", "redaction", 25, points_needed_for_6=23, achieved_points=redaction2)
    class_6a.add_exam("voci 1", "voci", 15, achieved_points=voci1)
    class_6a.add_exam("voci 2", "voci", 15, achieved_points=voci2)
    class_6a.add_exam("voci 3", "voci", 15, achieved_points=voci3)
    class_6a.add_exam("orale", "oral", 10, achieved_points=orale)
    class_6a.add_exam("grammaire 1", "grammaire", 35, 30, achieved_points=grammaire1)
    class_6a.add_exam("grammaire 2", "grammaire", 35, 28, achieved_points=grammaire2)

    class_6a.store_exams()

    class_6a.store_to_database()

    # TODO IT DID NOT STORE THE EXAMS AS CSV!

    print([cat.name for cat in class_6a.categories])
    print([exam.name for exam in class_6a.categories[1].exams])
    print([exam.name for exam in class_6a.categories[0].exams])
    print([exam.name for exam in class_6a.categories[2].exams])

    class_6a.create_grade_report()

    # class_6a.upadte_categories([{"name": "grammaire", "weight": 0.3}, {"name": "voci", "weight" : 0.1}])
    # try:
    #     class_6a.create_grade_report()
    # except Exception as e:
    #     print(e)
    #
    # class_6a.update_semester()
    # print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")
    # class_6a.update_semester()
    # print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")
    # class_6a.store_to_database()

    print("Succesfull run")
