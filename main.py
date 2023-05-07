# This is a sample Python script.
import csv
import logging
import os

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

TODO add fucntionality to create exam summary as a PDF or so (average, mean, quartils, standard deviation, ..)
"""


FOLDERPATH = "./tmp/klassen/"

class Overview:
    """
    keep list of classes, ...

    """
    def __init__(self):
        self.classes = []

        def load_categories(curr_class: Class):
            """
            Loads all categories for a class object and stores it in the curr_class.categories list.

            => Does it also load exams themselves?

            :return:
            """


        def load_classes():
            """
            loads list of classes from memory
            => how to deal with multiple intstances of classes? => mb load all of them, let user decide which to pick.
            :return:
            """

            # Loop through all files in the directory
            for filename in os.listdir(FOLDERPATH):
                # Check if the file has a .csv extension
                if filename.endswith(".csv"):
                    year, term, name = filename.split("_")
                    try:
                        curr_class = Class(name, term, int(year))
                        self.classes.append(curr_class)
                        with open('filename.csv', newline='') as csvfile:
                            reader = csv.reader(csvfile)
                            first_row = next(reader)
                            if "Nachname" not in first_row:
                                raise RuntimeError("Expect the first row to contain the word Nachname")
                            for row in reader:
                                last = row[0]
                                first = row[1]
                                curr_class.add_student(first=first, last=last)

                        # get report_id (to make sure not to create reports multiple times)
                        max_report_no = 0
                        for file in os.path.join(FOLDERPATH, filename[:-4]):
                            # TODO test this functionality
                            if "report" in file:
                                try:
                                    if int(file[file.find("report"):file.find("report")+2]) > max_report_no:
                                        max_report_no = int(file[file.find("report"):file.find("report")+2])

                                except:
                                    logging.warning(f"Could not extract report number from filename {file}")
                        curr_class.report_id = max_report_no

                    except:
                        logging.error(f"Could not create class from {filename}. \n"
                              f"Make sure that the file is named correctly (YEAR_TERM_NAME) and does contain a list of students.\n"
                              f"Make sure, the first row of the Row contains a field Nachname")

            raise NotImplementedError




def test_exam_creation():
    raise NotImplementedError



def main():
    raise NotImplementedError


main()
