# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


from exam import Exam, Student, Cateogry
from classes import Class


def main():

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
    class_6a.store_to_database()

main()
