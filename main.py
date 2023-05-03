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
        {"firstname": "Renato", "lastname": "Meier"},
        {"firstname": "Adrian", "lastname": "Pfeiffer"},
        {"firstname": "Nina", "lastname": "Matumona"},
        {"firstname": "Marlene", "lastname": "asdf"},
        {"firstname": "Nina", "lastname": "Kohler"},
        {"firstname": "Noe", "lastname": "Matumona"},
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
    class_6a.update_semester()
    print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")
    class_6a.update_semester()
    print(f"Semester: {class_6a.term}, year: {class_6a.year}\n {class_6a.filename_class}")
    class_6a.store_to_database()

def test_exam_creation():
    raise NotImplementedError



def main():
    test_class_management()



main()
