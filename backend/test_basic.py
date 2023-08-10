import os
import shutil

import pytest as pytest

from classes import Class
from classes import FOLDERPATH
from overview import Overview



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


def print_exam_results(class_6a):
    print("=================")
    student = class_6a.get_student("Nicolas", "Zillig")
    for cat in class_6a.categories:
        for exam in cat.exams:
            print(f"Student{student} got points {exam.points[student]}/{exam.max_points}, grade {exam.grades[student]} for exam {exam}")


@pytest.fixture
def gen_class_cat_examdata_simple():
    """
    Generates "Simple" example where everything works fine
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
    grades_nici = [0, 23, 0, 15, 0, 10, 0, 25]
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

    class_6a.add_exam("redaction 1", "redaction", points_max[0], points_needed_for_6=points_for_6[0],
                      achieved_points=redaction1)
    class_6a.add_exam("redaction 2", "redaction", points_max[1], points_needed_for_6=points_for_6[1],
                      achieved_points=redaction2)
    class_6a.add_exam("voci 1", "voci", points_max[2], achieved_points=voci1)
    class_6a.add_exam("voci 2", "voci", points_max[3], achieved_points=voci2)
    class_6a.add_exam("voci 3", "voci", points_max[4], achieved_points=voci3)
    class_6a.add_exam("orale", "oral", points_max[5], achieved_points=oral)
    class_6a.add_exam("grammaire 1", "grammaire", points_max[6], points_for_6[6], achieved_points=grammaire1)
    class_6a.add_exam("grammaire 2", "grammaire", points_max[7], points_for_6[7], achieved_points=grammaire2)

    return class_6a


@pytest.mark.test_exam
def test_cateogries_exams_simple(gen_class_cat_examdata_simple):
    """
    Tests simple functionality of exams / categories, like adding exams / cateogories, deleting them, ...

    Not yet with student's data (or at least, nothing is done with their grades
    :return:
    """

    class_6a = gen_class_cat_examdata_simple

    class_6a.create_grade_report()
    class_6a.store_exams()
    # for cat in class_6a.categories:
    #     for exam in cat.exams:
    #         exam.generate_summary_report(f"tmp/{cat}-{exam}_report.pdf")

    report_location = os.path.join(class_6a.filename_class_base, f"{class_6a.name}_report{(class_6a.report_id-1):02}.xlsx")
    shutil.copy(report_location, "../results_tests/")
    with open("../results_tests/exams_testrun_exams_simple", "w") as f:
        f.write(f"Categories: {[cat.__str__() for cat in class_6a.categories]}\n\n")
        for cat in class_6a.categories:
            f.write(f"Cat {cat}: exams:\n{[ex.__str__() for ex in cat.exams]}\n")
@pytest.mark.file_management
def test_import_class_data_normal():
    """
    Tests importing different classes based on the csv file found in /tmp/class. Not yet with tedious cases (wrong files, weird names, ..)
    :return:
    """

    directory_path = FOLDERPATH
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)



    # create some classes w/o exams
    classes = [
        Class("Test_storage_1", "HS", 2017),
        Class("Test_storage_2", "HS", 2013),
        Class("Test_storage_3", "FS", 2017),
        Class("Test_storage_4", "FS", 2015),
        Class("Test_storage_5", "HS", 2020),
    ]

    # TODO maybe include renaming / updating semester shenanigang -- do that later on

    # add students
    students1 = [
        {"firstname": "peter", "lastname": "meier"},
        {"firstname": "peter1", "lastname": "meier2"},
        {"firstname": "peter2", "lastname": "meier3"},
        {"firstname": "peter3", "lastname": "meier4"},
        {"firstname": "peter4", "lastname": "meier5"},
        {"firstname": "peter5", "lastname": "meier6"},
    ]

    students2 = [
        {"firstname": "hans1", "lastname": "mueller1"},
        {"firstname": "hans2", "lastname": "mueller2"},
        {"firstname": "hans3", "lastname": "mueller3"},
        {"firstname": "hans4", "lastname": "mueller4"},
        {"firstname": "hans5", "lastname": "mueller5"},
        {"firstname": "hans6", "lastname": "mueller6"},
        {"firstname": "hans7", "lastname": "mueller7"},
        {"firstname": "hans8", "lastname": "mueller8"},
    ]

    students3 = [
        {"firstname": "jolie1", "lastname": "schmid1"},
        {"firstname": "jolie2", "lastname": "schmid2"},
        {"firstname": "jolie4", "lastname": "schmid4"},
        {"firstname": "jolie3", "lastname": "schmid3"},
        {"firstname": "jolie5", "lastname": "schmid5"},
    ]

    students4 = [
        {"firstname": "four1", "lastname": "vier1"},
        {"firstname": "four2", "lastname": "vier2"},
        {"firstname": "four3", "lastname": "vier3"},
    ]

    students5 = [
        {"firstname": "five1", "lastname": "fire1"},
        {"firstname": "five2", "lastname": "fire2"},
        {"firstname": "five3", "lastname": "fire3"},
        {"firstname": "five4", "lastname": "fire4"},
        {"firstname": "five5", "lastname": "fire5"},
        {"firstname": "five6", "lastname": "fire6"},
    ]

    classes[0].initialize_new_class(students1)
    classes[1].initialize_new_class(students2)
    classes[2].initialize_new_class(students3)
    classes[3].initialize_new_class(students4)
    classes[4].initialize_new_class(students5)

    # store on disk
    for class_obj in classes:
        class_obj.store_to_database()

    # read in classes from disk
    overview = Overview()
    overview.load_classes()

    # assert equality
    for class_obj in classes:
        res = False
        for class_comp in overview.classes:
            if class_obj.name == class_comp.name:
                res = True
        assert res, f"Could not find {class_obj.name} in {overview.classes}"

    print(f"Loaded classes from mem:\n{overview.classes}")
    print(f"Containing students:")
    for class_obj in overview.classes:
        assert len(class_obj.students) != 0, f"Class {class_obj}; studs {class_obj.students}"

    # delete stuff again and store it again -- I can then manually check whether the lists are correct
    directory_path = FOLDERPATH
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    for class_obj in overview.classes:
        class_obj.store_to_database()

@pytest.mark.file_management
def test_import_exam_data(gen_class_cat_examdata_simple):
    """
    Tests importing exams from Excel files stored on disk. Not yet with stupid cases how ppl can screw around with files they should not touch

    :param gen_class_cat_examdata_simple:
    :return:
    """

    directory_path = FOLDERPATH
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    class_6a = gen_class_cat_examdata_simple
    class_6a.store_exams()

    class_copy = Class(class_6a.name, class_6a.term, class_6a.year)
    class_6a.update_name("OLD_6a")
    ov = Overview()
    class_copy.students = class_6a.students.copy()
    ov.load_categories_and_exams(class_copy)

    for student in class_copy.students:
        for i, cat in enumerate(class_copy.categories):
            for j, exam in enumerate(cat.exams):
                assert exam.points[student] == ((class_6a.categories[i]).exams[j]).points[student]
                assert exam.grades[student] == ((class_6a.categories[i]).exams[j]).grades[student]

@pytest.mark.skip
@pytest.mark.file_management
def test_import_data_specialCases():
    """
    Include things that can go wrong -- wrong names in students columns,

    :return:
    """
    raise NotImplementedError

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


@pytest.mark.generate_example_data
def test_gen_example_exams(gen_class_cat_examdata_simple):
    """
    I use this test to generate a few dummy classes and exams and store them locally.
    :return:
    """

    # delete the old files to ensure proper testing
    directory_path = FOLDERPATH
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    class_6a = gen_class_cat_examdata_simple
    class_6a.store_to_database()
    class_6a.store_exams()

    assert True


