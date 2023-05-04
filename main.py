# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from exam import Exam, Student, Cateogry
from classes import Class

"""
TODO keep list of classes to index everything -- in GUI, user can then select which class to edit
TODO add functionality to delete old classes
TODO upon startup, load everything from csv
=> sample run:
1. Load list of classes from disk (stored as csv)
2. Let user choose class to be viewed / edited
3. Load class-list, list of exams and exams themselves from stored csv
=> either just load all exams found in a folder or keep index (stored somewhere as csv), probably the latter as I also 
need to store information about the category weights / ...

=> Probably need to create new file for loading / storing stuff. Keep it minimal, loading takes quite a long time...
TODO don't always store everything on disk, only on major changes and on shutdown!

TODO add fucntionality to creat exam summary as a PDF or so (average, mean, quartils, standard deviation, ..)
"""

def test_class_management():

    """
    Not sure what to do with this stuff yet -- mainly just test some things
    :return:
    """

    print("Starting program")

    class_6a = Class("6a", "hs", 2016)

    students = [
        {"firstname": "Noe", "lastname" : "Matumona"},
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

    class_6a.initialize_new_class(students)

    class_6a.add_student("Marcel", "Schmid")
    class_6a.remove_student("Nicolas", "Zillig")

    print("Starting to store to DB")
    class_6a.store_to_database()

    class_6a.update_semester()
    print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")
    class_6a.update_semester()
    print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")



    categories = [
        {"name": "oral", "weight" : 0.3, "grading_type" : "default"},
        {"name": "redaction", "weight": 0.2},
        {"name": "voci", "weight" : 0.3},
    ]

    class_6a.initialize_categories(categories)
    class_6a.add_category({"name": "grammaire", "weight": 0.2})
    class_6a.add_category({"name": "asdf", "weight": 0.5})
    class_6a.remove_category("asdf")


    grades_noe = [25, 25, 15, 15, 15, 10, 35, 35]
    grades_nici = [15 ,15, 10, 10, 9, 10, 20, 20]
    grades_dominik = [8, 22, 12, 5, 9, 12, 14, 17]
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
    class_6a.add_exam("voci 3", "voci", 15,  achieved_points=voci3)
    class_6a.add_exam("orale", "oral", 10,  achieved_points=orale)
    class_6a.add_exam("grammaire 1", "grammaire", 35, 30, achieved_points=grammaire1)
    class_6a.add_exam("grammaire 2", "grammaire", 35, 28, achieved_points=grammaire2)

    # TODO IT DID NOT STORE THE EXAMS AS CSV!

    class_6a.create_grade_report()

    class_6a.upadte_categories([{"name": "grammaire", "weight": 0.3}, {"name": "voci", "weight" : 0.1}])
    try:
        class_6a.create_grade_report()
    except Exception as e:
        print(e)

    class_6a.update_semester()
    print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")
    class_6a.update_semester()
    print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")
    class_6a.store_to_database()

    print("Succesfull run")



def test_exam_creation():
    raise NotImplementedError



def main():
    test_class_management()



main()
