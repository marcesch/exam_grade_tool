import csv

from student import Student
from exam import Exam, Cateogry
import os
import logging
import shutil

FOLDERPATH = "./tmp/klassen/"

""""
TODO: sanitize / ... students names... what if there are sume ugly shit thigns like accents etc?
=> might have to slightly alter the contains_student function etc. (always compare sanitized version)

=> add possibility to import old examples (e.g. for categories etc., otherwise have to do that everytime again)


TODO: when should I store stuff?

"""


class Class:
    def __init__(self, name: str, term: str, year: int):
        self.students: list[Student] = []
        self.exams: list[Exam] = []
        self.categories: list[Cateogry] = {}
        self.name: str = name
        if (term.lower() == "hs"):
            self.term: str = term.upper()
        else:
            if (term.lower() == "fs"):
                self.term: str = term.upper()
            else:
                raise RuntimeError("Please choose either HS or FS")
        self.year: int = year
        self.filename_class_base = ""
        self.filename_class = ""
        self.filename_base_exam = ""
        self.update_filenames()
        self.folder_shadow = FOLDERPATH + "/.trash/"

        if not os.path.exists(self.filename_base_exam):
            os.makedirs(self.filename_base_exam)
        else:
            logging.warning(f"Directory '{self.filename_base_exam}' already exists.")

    def update_name(self, new_name: str):
        self.name = new_name

    def update_filenames(self):
        """
        after seen a change (e.g. year / term / ...), need to adjust the filename
        :return:
        """

        # TODO ask selina for her preferences regarding layout of files
        self.filename_class_base = FOLDERPATH + str(self.year) + "_" + self.term.upper() + "_" + self.name
        self.filename_class = self.filename_class_base + ".csv"
        self.filename_base_exam = self.filename_class_base + "/pruefungen/"


    def update_semester(self):
        """
        :return:

        updates the semester by one term
        creates new file for grades
        """
        oldterm = self.term
        oldyear = self.year
        if self.term == "hs":
            self.year = self.year + 1
            self.term = "fs"
        else:
            self.term = "hs"
            logging.info("Consider updating the name of the class! It has likely changed, e.g. from 3a to 4a")

        logging.info(f"Updating term for class {self.name} from {oldterm} {oldyear} to {self.term} {self.year}")
        logging.info(f"Removing old class list, updating with new classlist")
        old_filename = self.filename_class
        # TODO also make new files for class name, deleting the old ones
        self.update_filenames()
        os.remove(old_filename)
        self.store_to_database()

        # make new base folder for exams
        if not os.path.exists(self.filename_base_exam):
            os.makedirs(self.filename_base_exam)
        else:
            logging.error(f"Directory '{self.filename_base_exam}' already exists.")

    def store_to_database(self):
        """
        Stores the old class file to the trash-folder and stores an updated version
        :return:
        """
        # TODO this implementation litters the trash! Might want to do something against that

        students_old = []
        # load "old" student's database for comparison
        # Read the list of students from the CSV file
        try:
            with open(self.filename_class, "r") as csvfile:
                reader = csv.reader(csvfile)
                # Skip the header row
                next(reader)
                # Iterate over the rows in the CSV file and create a new Student object for each row
                for row in reader:
                    student = Student(row[0], row[1])
                    students_old.append(student)

            # find difference between the two files
            students_removed = []
            for student in students_old:
                b, student_diff = self.contains_student(student.firstname, student.lastname)
                if b:
                    students_removed.append(student_diff)

            if len(students_removed) == 0 and len(students_old) == len(self.students):
                print("The class has not changed. Won't store anything")
                return

            if len(students_removed) != 0:
                print(
                    f"REMOVING the following students from the database. If this was an error, you can find the old file in {self.folder_shadow}")
                for student in students_removed:
                    print(f"Removing student {student.firstname} {student.lastname}")

            # move "old" student's database to trash-folder
            logging.info("Moving old database to trash folder")
            shutil.move(self.filename_class, self.folder_shadow)
        except:
            logging.info(f"No old file found")

        # store "new" / current database under folderpath
        # Write the list of students to a CSV file
        with open(self.filename_class, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            # Write the header row to the CSV file
            writer.writerow(["Nachname", "Vorname"])
            # Write each student's first name and last name to the CSV file
            for student in self.students:
                writer.writerow([student.lastname, student.firstname])

    def contains_student(self, first: str, last: str, return_student=False):
        """
        Slow and unelegant, but hey
        Allows only searching for one of the names (surname or firstname), this is a little bit more convenient
        :param return_student:  can let the function also return the Student object (used for deletion)
        :param first:
        :param last:
        :return:
        """
        if first == None and last == None:
            raise RuntimeError("Must give at least one name")
        res = False
        res_student = None
        for students_contained in self.students:
            if students_contained.firstname == first and students_contained.lastname == last:
                res = True
                res_student = students_contained
            if first == None and students_contained.lastname == last:
                res = True
                res_student = students_contained
            if first == students_contained.firstname and last == None:
                res = True
                res_student = students_contained

        if return_student:
            return res, res_student
        return res

    def initialize_new_class(self, students: list[dict[str, str]]):
        """
        creates new class from scratch and stores the data of the students as a csv.
        :param
        :return:
        """

        for student in students:
            if self.contains_student(student["firstname"], student["lastname"]):
                print(f"Warning! Received the same student a second time! Won't add anything")
                # TODO find some reasonable way to ping that back to GUI (do you really want to do that? or so)
            else:
                self.students.append(Student(student["firstname"], student["lastname"]))

        # store the class as a csv
        # => that function checks whether old file already exists
        self.store_to_database()

    def delete_class(self):
        """
        deltes class AND ALL ITS FILES
        :return:
        """
        # TODO could also just move it to the trash folder -- need to decide that later
        logging.warning(f"Removing all the files for class {self.name} {self.term} {self.year}. This action cannot be reverted.")
        os.remove(self.filename_class_base)

        # remove the folder containing this classes exam
        for item in os.listdir(self.filename_base_exam):
            item_path = os.path.join(self.filename_base_exam, item)
            if os.path.isfile(item_path):
                # if the item is a file, delete it
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # if the item is a directory, recursively delete it and all its contents
                shutil.rmtree(item_path)

    def empty_trash(self):
        """
        removes everything from the trash folder, raising tons of warnings

        :return:
        """
        logging.warning("DELETING the entire contents of the trash folder")

        for item in os.listdir(self.folder_shadow):
            item_path = os.path.join(self.folder_shadow, item)
            if os.path.isfile(item_path):
                # if the item is a file, delete it
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # if the item is a directory, recursively delete it and all its contents
                shutil.rmtree(item_path)

    def add_student(self, first: str, last: str):
        """
        :return:
        adds new student
        """
        if self.contains_student(first, last):
            print(f"Warning! Adding the same student a second time!")
            # TODO find some reasonable way to ping that back to GUI (do you really want to do that? or so)
        self.students.append(Student(first, last))
        self.store_to_database()

    def remove_student(self, first: str, last: str):
        """
        what to do with the grades???
        :param student:
        :return:
        """
        b, student_in_db = self.contains_student(first, last, return_student=True)
        if not b or student_in_db == None:
            raise RuntimeWarning(f"Could not find student {first} {last} in my database. Did you mistype?")

        self.students.remove(student_in_db)
        self.store_to_database()

    def add_exam_category(self, exam_category: str, weight, grading_type="default"):
        """
        probably use a dictionary to keep track of exam categories
        :param exam_cateogry:
        :param weight:
        :return:
        """

        # TODO DO NOT ONLY USE EXAM CATEGORY AS ID -- USE ALSO TERM AND YEAR
        # => e.g., each term there will be a category redaction, but only the current ones should count

        if exam_category in self.categories:
            print(f"Category {exam_category} already in list. Aborting")
            return

        cat = Cateogry(exam_category, weight, grading_type)
        self.categories[exam_category] = cat

    def upadte_categories(self):
        """
        Not quite sure how exactly to do that part -- It might be reasonable to use a wrapper function that checks that
        the weight of the categories always sum to 1 (invariant regarding the correctness) instead of letting user create
        categories individually

        Downside: need to create all of them at once, always. But I think, GUI can help me here to make it reasonably nice to use

        :return:
        """

    def add_exam(self, exam_name: str, exam_category: str, max_points: int, points_needed_for_6: int, min_grade=1,
                 max_grade=6, category_weight=None):
        """

        :param exam_name: e.g. Redaction 1
        :param exam_category: e.g. redaction, orale, ...
        :param max_points: maximum possible points
        :param points_needed_for_6:
        :param min_grade:
        :param max_grade:
        :return:

        TODO make sure to support whacky characters in name
        # TODO add .csv file for that exam notes

        """

        if not exam_category in self.categories:
            if category_weight != None:
                print(f"Creating new category {exam_category}")
                cat = Cateogry(exam_category, category_weight)
                self.categories[exam_category] = cat
            else:
                print(f"Error: Don't know {exam_category}. Aborting")
                return

        cat: Cateogry = self.categories[exam_category]
        cat.add_exam(exam_name, max_points, points_needed_for_6, min_grade, max_grade)

    def update_grade(self, exam: str, student: Student):
        """

        :param exam:
        :param student:
        :return:
        """

        if student not in self.students:
            raise RuntimeWarning("Student not found in this class")
        if exam not in self.exams:
            raise RuntimeWarning("Exam not found. Make sure to first create a new exam")

        # TOD how to keep the mapping student -> grade? Dict or always load from csv?

        raise NotImplementedError

    def create_grade_report(self):
        """
        creates new report, i.e. computes average grades for each student
        :return:
        """

        """
        probably iterate over each category over each exam or so -- support students not taking exams
        """

        # TODO check that the category weights sum to 1!

        raise NotImplementedError
