from PyQt6 import QtCore
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem

from backend.classes import Class
from backend.exam import Exam
from frontend.ui_window_exam_details import Ui_WindowExamDetails
from ui_window_class_detail import  Ui_WindowClassDetail


# TODO use
#         grade = round(grade, 4)
# for rounding

class WindowExamDetail(QMainWindow, Ui_WindowExamDetails):

    # TODO dynamically add some of the buttons (based on the exam type, e.g. max points, ...)

    def __init__(self, exam: Exam, class_obj: Class, parent=None):

        # use to ignore items-changed signals
        self.setup_finished = False

        # initialize all GUI elements based on information from .ui file (compiled to python using pyuic6)
        super().__init__(parent)
        self.setupUi(self)
        self.window().setWindowTitle(f"Exam {exam.name} (class {exam.classname}, {exam.term.upper}{exam.year}")

        # fields
        self.exam = exam
        self.class_obj = class_obj
        print(f"[WINDOW EXAM DETAIL] got here with {exam} {exam.grades}")

        # windows to be opened from here

        self.populate_list_view()
        self.setup_finished = True

        # TODO show data in tableview to see how it behaves

    def populate_list_view(self):
        """
        Fills the list view with the data for the students
        :return:
        """

        # lastname, firstname, points, grades

        # TODO set selection mode, resize modes, ...
        self.table_points_grades.setColumnCount(4)
        self.table_points_grades.setHorizontalHeaderLabels([f'Lastname', f'Firstname', 'points', 'grades'])

        # fill in actual data
        for student in self.exam.grades:
            row_position = self.table_points_grades.rowCount()
            self.table_points_grades.insertRow(row_position)

            # ensure student name cannot be tampered with
            item_lastname = QTableWidgetItem(student.lastname)
            item_lastname.setFlags(item_lastname.flags() &~ QtCore.Qt.ItemFlag.ItemIsEditable)
            item_firstname = QTableWidgetItem(student.firstname)
            item_firstname.setFlags(item_firstname.flags() &~ QtCore.Qt.ItemFlag.ItemIsEditable)

            self.table_points_grades.setItem(row_position, 0, item_lastname)
            self.table_points_grades.setItem(row_position, 1, item_firstname)
            try:
                student_points = self.exam.points[student]
                if student_points < 0:
                    # means that the field was blocked in backend
                    raise
                self.table_points_grades.setItem(row_position, 2, QTableWidgetItem(str(student_points)))
            except:
                # if there are no points for this exam type or the student did not write exam
                self.table_points_grades.setItem(row_position, 2, QTableWidgetItem(""))

            try:
                student_grade = self.exam.grades[student]
                if student_grade < 0:
                    # means that the field was blocked in backend
                    raise
                self.table_points_grades.setItem(row_position, 3, QTableWidgetItem(str(student_grade)))
            except:
                self.table_points_grades.setItem(row_position, 3, QTableWidgetItem(""))

            def switcher_for_item_change(item):
                if not self.setup_finished:
                    return
                if item.column()==2:
                    self.handle_student_point_modification(item.row(), float(self.table_points_grades.item(item.row(), item.column()).text()))
                if item.column()==3:
                    self.handle_student_point_modification(item.row(), float(self.table_points_grades.item(item.row(), item.column()).text()))

            # now, add behavior on modifying field values
            self.table_points_grades.itemChanged.connect(switcher_for_item_change)

    def refresh_table_view(self):
        self.setup_finished = False
        for student in self.exam.grades:
            row_position = self.table_points_grades.rowCount()
            self.table_points_grades.insertRow(row_position)

            # ensure student name cannot be tampered with
            item_lastname = QTableWidgetItem(student.lastname)
            item_lastname.setFlags(item_lastname.flags() &~ QtCore.Qt.ItemFlag.ItemIsEditable)
            item_firstname = QTableWidgetItem(student.firstname)
            item_firstname.setFlags(item_firstname.flags() &~ QtCore.Qt.ItemFlag.ItemIsEditable)

            self.table_points_grades.setItem(row_position, 0, item_lastname)
            self.table_points_grades.setItem(row_position, 1, item_firstname)

            if hasattr(self.exam, "points"):
                print(f"Exam points: {self.exam.points}")
                raise
                # TODO fix this thing here
                # TODO Why does it not read in the user input?
                if student in self.exam.points:
                    student_points = self.exam.points[student]
                    if student_points < 0:
                        raise RuntimeError(f"[WINDOW EXAM DETAIL] Points {student_points} cannot be negative")
                    self.table_points_grades.setItem(row_position, 2, QTableWidgetItem(str(student_points)))

            if student in self.exam.grades:
                student_grade = self.exam.grades[student]
                if student_grade < 0:
                    # means that the field was blocked in backend
                    raise RuntimeError(f"[WINDOW EXAM DETAIL] Grade cannot be negative {student_grade}")
                self.table_points_grades.setItem(row_position, 3, QTableWidgetItem(str(student_grade)))

            try:
                student_grade = self.exam.grades[student]
                if student_grade < 0:
                    # means that the field was blocked in backend
                    raise
                self.table_points_grades.setItem(row_position, 3, QTableWidgetItem(str(student_grade)))
            except:
                self.table_points_grades.setItem(row_position, 3, QTableWidgetItem(""))
            self.setup_finished = True

    def handle_student_point_modification(self, row, new_points):
        print(f"[DEBUG] Got here with {new_points}")

        if new_points < 0:
            # catch this case just to be sure that nothing bad happens (the negative grades are special flags in backend)
            return

        if hasattr(self.exam, 'points'):
            firstname = self.table_points_grades.item(row, 1).text()
            lastname = self.table_points_grades.item(row, 0).text()
            student = self.class_obj.get_student(firstname, lastname)
            new_points = self.exam.enforce_point_boundaries(new_points)
            self.exam.points[student] = new_points
            # TODO maybe replace with method that computes grade just for this student
            self.exam.compute_grades()

        self.refresh_table_view()



    def handle_student_grade_modification(self, row, new_grade):
        firstname = self.table_points_grades.item(row, 1).text()
        lastname = self.table_points_grades.item(row, 0).text()
        student = self.class_obj.get_student(firstname, lastname)

        new_grade = self.exam.enforce_grade_boundaries(new_grade)
        self.exam.grades[student] = new_grade
        if hasattr(self.exam, "points"):
            if student in self.exam.points:
                # if grade is overwritten, delete points to avoid inconsitensies
                self.exam.points.pop(student)

        self.refresh_table_view()