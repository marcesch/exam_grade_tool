from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QMainWindow, QTableWidgetItem

from backend.classes import Class
from backend.exam import *
from frontend.ui_window_exam_details import Ui_WindowExamDetails
from ui_window_class_detail import  Ui_WindowClassDetail


# TODO use
#         grade = round(grade, 4)
# for rounding

class WindowExamDetail(QMainWindow, Ui_WindowExamDetails):

    # TODO dynamically add some of the buttons (based on the exam type, e.g. max points, ...)

    def __init__(self, exam_name: str, class_obj: Class, parent=None):

        # use to ignore items-changed signals
        self.setup_finished = False
        self.ignore_updates = False

        self.add_additional_fields()

        # initialize all GUI elements based on information from .ui file (compiled to python using pyuic6)
        super().__init__(parent)
        self.setupUi(self)

        # fields
        self.class_obj = class_obj
        self.exam = self.class_obj.get_exam(exam_name)

        self.window().setWindowTitle(f"Exam {self.exam.name} (class {self.exam.classname}, {self.exam.term.upper}{self.exam.year}")



        # windows to be opened from here

        self.populate_list_view()
        self.display_fields()
        self.connect_signals()
        self.setup_finished = True

        # TODO add average as a last row in treeview


    def add_additional_fields(self):
        """
        Add additional fields to ui, based on exam type
        :return:
        """

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
                self.table_points_grades.setItem(row_position, 3, QTableWidgetItem(str(round(student_grade, 2))))
            except:
                self.table_points_grades.setItem(row_position, 3, QTableWidgetItem(""))


    def display_fields_examtype(self, new_type = None):
        _translate = QtCore.QCoreApplication.translate
        exam_type = type(self.exam) if new_type == None else new_type
        print(exam_type)
        if not issubclass(exam_type, Exam):
            raise RuntimeError(f"[WINDOW EXAM DETAILS] New_type must be a valid subclass of Exam (got {new_type}")

            # display different fields based on exam type
        if exam_type == ExamModeLinearWithPassingPoints:
            print(f"[WINDOW EXAM DETAIL, DEBUG] Arrived here")
            # TODO continue here
            raise NotImplementedError
        elif exam_type == ExamModeLinear:
            number_additinal_rows = 1
            # move table view and buttons down
            # TODO quite  alot of hard coding for the position of the widgets. Could be solved more elegantly
            self.gridLayout_2.addWidget(self.table_points_grades, 3 + number_additinal_rows, 0, 1, 7)
            self.gridLayout_2.addWidget(self.button_generateReport, 4 + number_additinal_rows, 4, 1, 1)
            self.gridLayout_2.addWidget(self.button_export_excel, 4 + number_additinal_rows, 1, 1, 1)

            self.input_points_for_max = QtWidgets.QLineEdit(parent=self.centralwidget)
            self.input_points_for_max.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhFormattedNumbersOnly)
            self.input_points_for_max.setObjectName("points_for_max")
            self.gridLayout_2.addWidget(self.input_points_for_max, 3, 4, 1, 1)
            self.input_max_points = QtWidgets.QLineEdit(parent=self.centralwidget)
            self.input_max_points.setInputMethodHints(QtCore.Qt.InputMethodHint.ImhFormattedNumbersOnly)
            self.input_max_points.setObjectName("max_points")
            self.gridLayout_2.addWidget(self.input_max_points, 3, 1, 1, 1)

            self.label_max_points = QtWidgets.QLabel(parent=self.centralwidget)
            self.label_max_points.setObjectName("label_4")
            self.gridLayout_2.addWidget(self.label_max_points, 3, 0, 1, 1)
            self.label_pts_for_max = QtWidgets.QLabel(parent=self.centralwidget)
            self.label_pts_for_max.setObjectName("label_5")
            self.gridLayout_2.addWidget(self.label_pts_for_max, 3, 2, 1, 1)

            self.label_max_points.setText(_translate("WindowExamDetails", "Maximum Points"))
            self.label_pts_for_max.setText(_translate("WindowExamDetails", "Points for Max"))

            self.input_max_points.setText(_translate("WindowExamDetails", str(self.exam.max_points)))
            self.input_points_for_max.setText(_translate("WindowExamDetails", str(self.exam.points_for_max)))

            # add behavior on changes for values


        elif exam_type == ExamModeFixedPointScheme:
            raise NotImplementedError
        elif exam_type == ExamModeHeavyCurveFitting:
            raise NotImplementedError
        elif exam_type == ExamModeSetGradeManually:
            raise NotImplementedError
        else:
            raise RuntimeError(f"[WINDOW EXAM DETAIL] Unknown exam type: {type(self.exam)}")

    def display_fields(self):
        """
        Based on the type of the exam, show different fields
        :return:
        """
        _translate = QtCore.QCoreApplication.translate
        self.input_examName.setText(_translate("WindowExamDetails", self.exam.name))

        self.input_examCategory.addItems([cat.name for cat in self.class_obj.categories])
        self.input_examCategory.setCurrentText(self.exam.category.name)
        exam_types_dict = Exam.show_exam_types()
        self.input_examType.addItems(exam_types_dict.keys())
        self.input_examType.setCurrentText(self.exam.exam_type())
        self.input_voluntary.addItems(["Yes", "No"])
        self.input_voluntary.setCurrentText("Yes" if self.exam.voluntary else "No")

        self.display_fields_examtype(type(self.exam))

        # TODO show average over class (points and grades)

    def disselect_current_widget(self):
        current_widget = self.focusWidget()
        current_widget.clearFocus()

    def update_max_points(self):
        item = self.input_max_points.text()
        try:
            new_max_points = float(item)
            if new_max_points < 0:
                new_max_points = 0
            if new_max_points < self.exam.points_for_max:
                self.exam.points_for_max = new_max_points
                self.input_points_for_max.setText(str(self.exam.points_for_max))
                self.exam.compute_grades()
                self.update_table_data()
            self.exam.max_points = new_max_points
            self.input_max_points.setText(str(self.exam.max_points))
            print(f"[WINDOW EXAM DETAIL] Changed max_points value: {self.exam.max_points}, {item}")
        except:
            self.input_max_points.setText(str(self.exam.max_points))
        finally:
            self.update_student_point_warnings()


    def update_table_data(self):
        """
        Updates the values for points / grades that are displayed
        :return:
        """

        self.ignore_updates = True

        print(f"[DEBUG] {self.table_points_grades.rowCount()}")


        for row in range(self.table_points_grades.rowCount()):
            print(f"[DEBUG1] Updating table view...row {row}")


            item_lastname = self.table_points_grades.item(row, 0).text()
            item_firstname = self.table_points_grades.item(row, 1).text()
            student = self.class_obj.get_student(item_firstname, item_lastname)
            item_points = self.table_points_grades.item(row, 2)
            item_grades = self.table_points_grades.item(row, 3)
            print(f"[DEBUG2] Updating table view...row {row}, {item_grades}, {item_points}")

            try:
                if item_grades is not None:
                    if student in self.exam.grades:
                        grade_student = self.exam.grades[student]
                        if grade_student < 0:
                            item_grades.setText("")
                        self.ignore_updates = True
                        item_grades.setText(str(round(grade_student, 2)))

                    else:
                        item_grades.setText("")
            except:
                continue
            try:
                if item_points is not None:
                    if hasattr(self.exam, "points"):
                        if student in self.exam.points:
                            points_student = self.exam.points[student]

                            if points_student < 0:
                                print(points_student)
                                print(self.exam.points)
                                item_points.setText("")
                            else:
                                # make it more beautiful
                                if (points_student * 10) % 10 == 0:
                                    item_points.setText(str(int(points_student)))
                                else:
                                    item_points.setText(str(points_student))

                        else:

                            item_points.setText("")
            except:
                continue




    def update_student_point_warnings(self):
        """
        If max_points is changed, and some students now have too many points, color them red
        :return:
        """

        if not hasattr(self.exam, "max_points"):
            return

        for row in range(self.table_points_grades.rowCount()):
            item = self.table_points_grades.item(row, 2)
            if item is not None:
                value = float(item.text())
                if value > self.exam.max_points:
                    item.setForeground(QColor("red"))
                else:
                    item.setForeground(QColor("black"))


    def update_points_for_max(self):
        item = self.input_points_for_max.text()
        print(item)
        try:
            new_pts_for_max = float(item)
            if new_pts_for_max < 0:
                new_pts_for_max = 0
            if new_pts_for_max > self.exam.max_points:
                new_pts_for_max = self.exam.max_points
            self.exam.points_for_max = new_pts_for_max
            self.exam.compute_grades()
            self.input_points_for_max.setText(str(self.exam.points_for_max))
            self.update_table_data()
            print(f"[WINDOW EXAM DETAIL] Changed points_for_max value: {self.exam.points_for_max}, {item} (max: {self.exam.max_points})")
        except:
            self.input_points_for_max.setText(str(self.exam.points_for_max))
        self.ignore_updates = False

    def test_function(self):

        raise NotImplementedError


    def connect_signals(self):

        self.button_generateReport.clicked.connect(self.handle_button_generate_grade_report)

        self.input_max_points.editingFinished.connect(self.update_max_points)
        self.input_points_for_max.editingFinished.connect(self.update_points_for_max)
        self.input_max_points.returnPressed.connect(self.disselect_current_widget)
        self.input_points_for_max.returnPressed.connect(self.disselect_current_widget)
        self.input_examCategory.currentIndexChanged.connect(self.test_function)
        self.input_voluntary.currentIndexChanged.connect(self.test_function)
        self.input_examType.currentIndexChanged.connect(self.handle_exam_type_change)

        def switcher_for_item_change(item):
            if self.ignore_updates:
                return
            if not self.setup_finished:
                return
            try:
                if item.column() == 2:
                    self.handle_student_point_modification(item.row(), float(
                        self.table_points_grades.item(item.row(), item.column()).text()))
                if item.column() == 3:
                    self.handle_student_grade_modification(item.row(), float(
                        self.table_points_grades.item(item.row(), item.column()).text()))
            except Exception as e:
                # if anything weird happens (badly formatted input etc.), simply don't accept the change
                print(f"Exception here: {e}")
                self.update_table_data()

        # now, add behavior on modifying field values
        self.table_points_grades.itemChanged.connect(switcher_for_item_change)

    def handle_button_generate_grade_report(self):


        raise NotImplementedError


    def handle_student_point_modification(self, row, new_points):
        print(f"[DEBUG] Got here with {new_points}")

        if not hasattr(self.exam, 'points'):
            raise RuntimeError(f"[WINDOW EXAM DETAIL] Cannot set points for that exam (wrong type)")
        firstname = self.table_points_grades.item(row, 1).text()
        lastname = self.table_points_grades.item(row, 0).text()
        student = self.class_obj.get_student(firstname, lastname)
        new_points = self.exam.enforce_point_boundaries(new_points)
        self.exam.points[student] = new_points
        # display cleaned grade
        self.ignore_updates = True

        # TODO maybe replace with method that computes grade just for this student
        self.exam.compute_grades()
        self.update_table_data()

        # use this to signal the itemChanged thingy to not do anything
        # self.table_points_grades.setItem(row, 3, QTableWidgetItem(str(round(self.exam.grades[student], 4))))
        self.ignore_updates = False




    def handle_student_grade_modification(self, row, new_grade):
        firstname = self.table_points_grades.item(row, 1).text()
        lastname = self.table_points_grades.item(row, 0).text()
        student = self.class_obj.get_student(firstname, lastname)

        # try:
        #     float(new_grade)
        # except:
        #     raise RuntimeError(f'Type of grade must be float!')

        new_grade, _ = self.exam.enforce_grade_boundaries(float(new_grade))
        self.exam.add_grade_manually(student, new_grade)
        if hasattr(self.exam, "points"):
            if student in self.exam.points:
                # if grade is overwritten, delete points to avoid inconsitensies
                self.exam.points.pop(student)


        self.ignore_updates = True
        self.update_table_data()
        # self.table_points_grades.setItem(row, 2, QTableWidgetItem(""))
        self.table_points_grades.setItem(row, 3, QTableWidgetItem(str(self.exam.grades[student])))
        self.ignore_updates = False

    def handle_exam_type_change(self):
        """
        Changes type of self.exam, invokes display_fields
        :return:
        """

        new_text = self.input_examType.currentText()
        new_type = Exam.exam_types[new_text]
        print(f"new_type: {new_type}; new_type.name: {new_type.name}; new_text: {new_text}")

        # TODO display new fields, fetch data from them -- do something like while try, except until the user put in correct data to initiate new exam type
        self.display_fields_examtype(new_type)

        # TODO hardcoded for now
        additional_args = {"points_for_pass": 12}


        self.exam = self.class_obj.change_exam_type(self.exam, new_type.name, additional_args)


