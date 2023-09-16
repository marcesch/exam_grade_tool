"""
This test-"suite" is for interaction with the program without using the GUI. I won't write unit-tests here, but instead
simulate the behaviour of methods that will be called from the frontend to backend. Mainly so I won't have to enter data
manually every time.
"""
from backend.category import CategoryDefault
from backend.classes import Class
from backend.overview import Overview
from backend.student import Student


def gen_example_realistic():
    """
    Base example of how a class might look like in practice
    :return:
    """

    students = [('stud', '15'), ('stud', '16'), ('stud', '17'), ('stud', '18'), ('stud', '19'), ('stud', '20'), ('stud', '21'), ('stud', '22'), ('stud', '23'), ('stud', '24'), ('stud', '25'), ('stud', '26'), ('stud', '27'), ('stud', '28'), ('stud', '29'), ('stud', '30'), ('stud', '31')]

    class_obj = Class("test1", "HS", 2020)

    class_obj.add_multiple_students(students)

    # initiate categories
    cat_voci = CategoryDefault("voci", 0.2)
    cat_redaction = CategoryDefault("redaction", 0.2)
    cat_grammaire = CategoryDefault("grammaire", 0.3)
    cat_orale = CategoryDefault("orale", 0.1)
    cat_participation = CategoryDefault("participation", 0.15)
    cat_controle_lecture = CategoryDefault("controle_lecture", 0.05)

    if not isinstance(cat_voci.name, str):
        raise RuntimeError(f"category.name must be of type str, not {type(cat_voci.name)}")

    args_voci1 = {"max_points": 22.5, "points_for_max": 21}
    exam_voci1 = class_obj.add_exam("voci1", cat_voci, "default", args_voci1)
    args_voci2 = {"max_points": 22, "points_for_max": 21}
    exam_voci2 = class_obj.add_exam("voci2", cat_voci, "default", args_voci2)
    args_voci3 = {"max_points": 22, "points_for_max": 22}
    exam_voci3 = class_obj.add_exam("voci3", cat_voci, "default", args_voci3)
    args_voci4 = {"max_points": 22, "points_for_max": 22}
    exam_voci4 = class_obj.add_exam("voci4", cat_voci, "default", args_voci4)
    args_voci5 = {"max_points": 20, "points_for_max": 20}
    exam_voci5 = class_obj.add_exam("voci5", cat_voci, "default", args_voci5)
    args_voci_balzac = {"max_points": 22, "points_for_max": 22}
    exam_voci_balzac = class_obj.add_exam("vociB", cat_voci, "default", args_voci_balzac)
    args_red_1 = {"max_points": 50, "points_for_max": 50}
    exam_red1 = class_obj.add_exam("red1", cat_redaction, "default", args_red_1)
    args_red_2 = {"max_points": 32, "points_for_max": 32}
    exam_red2 = class_obj.add_exam("red2", cat_redaction, "default", args_red_2)
    args_interrog_1 = {"max_points": 46, "points_for_max": 42}
    exam_interrog1 = class_obj.add_exam("interrog1", cat_grammaire, "default", args_interrog_1)
    args_interrog_2 = {"max_points": 60, "points_for_max": 57}
    exam_interrog2 = class_obj.add_exam("interrog2", cat_grammaire, "default", args_interrog_2)
    args_orale = {}
    exam_orale_grade = class_obj.add_exam("orale", cat_participation, "direct_grade", args_orale)
    args_controle_lecture = {"max_points": 10, "points_for_max": 10}
    exam_controle_lecutre = class_obj.add_exam("controle_lecture", cat_controle_lecture, "default",
                                               args_controle_lecture)
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
    grades_orale_exam= {}

    list_points_voci1 = [1.5, 13.5, 16.5, 18, 19, 12, 19, 7, 8.5, 3.5, 18, 8.5, 6, 8.5, 13.5, 0, 13.5]
    list_points_voci2 = [10, 14, 17.5, 21, 16, 15.5, 19, 12, 16, 14.5, 21, 15.5, 5, 12.5, 5, 4, 17]
    list_points_voci3 = [4, 15, 19.5, 21, 18, 15.5, 21.5, 14.5, 14.5, 18, 19.5, 3, 5.5, 13, 16, 11, 14.5]
    list_points_voci4 = [3.5, 16, 15, 19.5, 18.5, 15, 19, 10.5, 4, 15.5, 18.5, 10.5, 6.5, 0, 13, 8.5, 15]
    list_points_voci5 = [0, 0, 0, 16.5, 0, 0, 18.5, 0, 0, 0, 0, 18, 0, 0, 0, 0, 0]
    list_points_vociB = [4.5, 15.5, 14.5, 21, 17.5, 19.5, 18.5, 5.5, 11.5, 11, 17, 12, 4.5, 11, 15, 10, 16]
    list_points_redaction1 = [47, 38, 42, 37, 49, 47, 38, 41, 26, 13, 43, 13, 45, 47, 47, 37, 39]
    list_point_redaction2 = [0, 17, 19, 19, 30, 28, 21, 21, 16, 23, 27, 9, 27, 0, 21, 19, 26]
    list_point_interrog1 = [10, 28, 35, 37, 36, 33.5, 33, 22, 31.5, 19.5, 38.5, 13, 18.5, 27, 36, 30.5, 36.5]
    list_point_interrog2 = [5, 31.5, 48, 50.5, 40.5, 23.5, 47, 27.5, 40.5, 24.5, 43, 25.5, 15, 28.5, 47.5, 33, 45.5]
    list_grades_participation = [2, 3, 5.5, 5.5, 4, 3, 5.5, 3, 3.5, 2.5, 4.5, 3, 2.5, 2.5, 4.5, 5, 3.5]
    list_point_controle_lecture = [2, 6.5, 6.5, 10, 4.5, 8, 10, 1, 7, 2, 9.5, 3, 2, 0, 7, 4, 4]
    list_grade_orale = [-1, 3, 5, 5.5, 6, -1, 5, 3, 5, 2.5, 6, 3.5, 1.5, -1, 4, 3, 5.5]

    for i in range(len(list_points_voci1)):
        # fill in all exams for each student

        current_student = class_obj.get_student(students[i][0], students[i][1])
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

    for exam in class_obj.exams:
        if exam.grades == {}:
            exam.compute_grades()

    return class_obj

def gen_example_dummies():
    """
    Simply add some more classes to the overview, without any exams and points etc.
    :return:
    """

    class_dummies = []
    class_dummies.append(("dummy1", "HS", 2020))
    class_dummies.append(("dummy2", "HS", 2020))
    class_dummies.append(("dummy3", "HS", 2020))
    class_dummies.append(("dummy4", "HS", 2020))
    class_dummies.append(("dummy5", "HS", 2020))
    class_dummies.append(("dummy6", "HS", 2020))
    class_dummies.append(("dummy7", "HS", 2020))
    class_dummies.append(("dummy1", "FS", 2020))
    class_dummies.append(("dummy2", "FS", 2020))
    class_dummies.append(("dummy3", "FS", 2020))
    class_dummies.append(("dummy4", "FS", 2020))
    class_dummies.append(("dummy1", "HS", 2019))
    class_dummies.append(("dummy2", "HS", 2019))
    class_dummies.append(("dummy1", "FS", 2019))
    class_dummies.append(("dummy2", "FS", 2019))

    return class_dummies

def initiate_overview():
    """
    Initiates overview object, containing all the classes
    :return:
    """
    overview = Overview()

    # add the large class example manually
    overview.classes.append(gen_example_realistic())

    print(f"Created class {overview.classes[0]} with students\n {overview.classes[0].students}")
    print(f"Points for exam {overview.classes[0].exams[0]}: {overview.classes[0].exams[0].points}")
    print(f"Grades for exam {overview.classes[0].exams[0]}: {overview.classes[0].exams[0].grades}")

    # for the rest, use intended method instead
    for class_description in gen_example_dummies():
        overview.add_class(class_description[0], class_description[1], class_description[2])

    print(f"[TEST, OVERVIEW] Created the following classes: \n {overview.classes}")
    print(f"[TEST, OVERVIEW] With the following categories: {[[exam.name, str(0), exam.category.name] for exam in overview.classes[0].exams]}")
    print(f"[TEST OVERVIEW] Storing the user data in {overview.application_folder},,, ")
    overview.save_to_json("testing_file.json")
    print(f"[TEST OVERVIEW] Done storing the user data")

    return overview

def load_from_application_folder():
    print(f"\n =============\n [TESTING OVERVIEW] Starting to load data from files")

    overview = Overview.load_from_json("testing_file.json")

    print(f"[TEST OVERVIEW] Could load the following data:")
    print(f"Classes: \n {overview.classes}")
    print(f"Created class {overview.classes[0]} with students\n {overview.classes[0].students}")
    print(f"Points for exam {overview.classes[0].exams[0]}: {overview.classes[0].exams[0].points}")
    print(f"Grades for exam {overview.classes[0].exams[0]}: {overview.classes[0].exams[0].grades}")

initiate_overview()
# load_from_application_folder()