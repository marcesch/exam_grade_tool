import logging
import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication

from backend.classes import Class
from frontend.handler_window_exam_detail import WindowExamDetail
from window_class_detail import  Ui_WindowClassDetail

# TODO maybe change QMainWindow -> QApplicationWindow
class WindowClassDetail(QMainWindow, Ui_WindowClassDetail):

    def __init__(self, class_obj, parent=None):

        # TODO alter things here

        # initialize all GUI elements based on information from .ui file (compiled to python using pyuic6)
        super().__init__(parent)

        self.setupUi(self)



        self.class_obj = class_obj
        print(class_obj)
        self.window().setWindowTitle(f"Class {self.class_obj.name} {self.class_obj.term.upper()} {self.class_obj.year}")

        # windows that can be opened from this view
        self.window_examDetail = None
        self.prompt_add_category = None
        self.prompt_add_exam = None
        self.prompt_add_students = None
        self.prompt_add_students_now = None
        self.prompt_add_student_details = None



    def test_function(self):
        """
        Used to connect actions etc.
        :return:
        """
        raise NotImplementedError

    def connect_signals(self):
        """
        Take care of button presses, action calls etc.
        Probably inefficient, but collect every action here and hand the calls to the respective functions (in other files etc.) from here
        => keeps code a little bit cleaner
        :return:
        """

        self.button_studentDetails.clicked.connect(self.test_function)
        self.button_addStudents.clicked.connect(self.test_function)
        self.button_removeStudent.clicked.connect(self.test_function)
        self.button_examDetails.clicked.connect(self.test_function)
        self.button_addExam.clicked.connect(self.test_function)
        self.button_generateExamReport.clicked.connect(self.test_function)
        self.button_deleteExam.clicked.connect(self.test_function)
        self.button_detailsCategory.clicked.connect(self.test_function)
        self.button_addCategory.clicked.connect(self.test_function)
        self.button_deleteCategory.clicked.connect(self.test_function)
        self.button_generateClassReport.clicked.connect(self.test_function)
        self.button_deleteClass.clicked.connect(self.test_function)

        raise NotImplementedError


    def number_students_selected(self):
        """
        :return: Number of students selected in treeview of students
        """
        raise NotImplementedError

    def number_exams_selected(self):
        """
        :return: Number of exams selected in exam treeview
        """
        raise NotImplementedError

    def number_categories_selected(self):
        """
        :return: Number of categories selected in category treeview
        """
        raise NotImplementedError

    def update_enabled_buttons(self):
        """
        Handles the enabling / disabling of buttons, based on number of items selected in the treeviews
        :return:
        """

        single_elements_buttons_students = [self.button_studentDetails]
        single_elements_buttons_exams = [self.button_examDetails, self.button_generateExamReport]
        single_elements_buttons_categories = [self.button_detailsCategory]
        single_element_buttons = single_elements_buttons_students + single_elements_buttons_exams + single_elements_buttons_categories

        something_selected_buttons_students = [self.button_removeStudent]
        something_selected_buttons_exams = [self.button_deleteExam]
        something_selected_buttons_categories = [self.button_deleteCategory]
        something_selected_buttons = something_selected_buttons_categories + something_selected_buttons_exams + something_selected_buttons_students

        for button in single_element_buttons:
            if something_selected_buttons.__contains__(button):
                raise RuntimeError(f"Button {button} must either be single or multi select, not both")

        for button in something_selected_buttons:
            if single_element_buttons.__contains__(button):
                raise RuntimeError(f"Button {button} must either be single or multi select, not both")

        for button in single_elements_buttons_students:
            if self.number_students_selected() == 1:
                button.setEnabled(True)
            else:
                button.setDisabled(True)
        for button in something_selected_buttons_students:
            if self.number_students_selected() >= 1:
                button.setEnabled(True)
            else:
                button.setDisabled(True)

        for button in single_elements_buttons_exams:
            if self.number_exams_selected() == 1:
                button.setEnabled(True)
            else:
                button.setDisabled(True)
        for button in something_selected_buttons_exams:
            if self.number_exams_selected() >= 1:
                button.setEnabled(True)
            else:
                button.setDisabled(True)

        for button in single_elements_buttons_categories:
            if self.number_categories_selected() == 1:
                button.setEnabled(True)
            else:
                button.setDisabled(True)
        for button in something_selected_buttons_categories:
            if self.number_categories_selected() >= 1:
                button.setEnabled(True)
            else:
                button.setDisabled(True)

    def handle_button_student_details(self):
        """
        Handles the click on student details
        :return:
        """
        # find student that is selected
        selected_row = self.treeview_students.selectedItems()
        if len(selected_row) != 1:
            raise RuntimeError(f"Wrong number of students selected for this action: {len(selected_row)} instead of 1")
        lastname = selected_row[0].data(0, 0)
        firstname = selected_row[0].data(1,0)
        student = self.class_obj.get_student(firstname, lastname)
        if student is None:
            raise RuntimeError(f"Could not find student {firstname} {lastname} in this class")
        self.show_prompt_student_details(student)

    def handle_button_add_students(self):
        """
        Handles click add student
        :return:
        """
        self.show_prompt_add_students()
        # TODO maybe do some stuff here, like adding received students to class

    def handle_button_remove_student(self):
        """
        Handles click remove students
        :return:
        """

        selected_rows = self.treeview_students.selectedItems()
        if len(selected_rows) <= 0:
            raise RuntimeError(f"Empty selection of students to be deleted")
        selected_students = []
        for row in selected_rows:
            last = row.data(0,0)
            first = row.data(0,0)
            student = self.class_obj.get_student(first, last)
            if student is None:
                raise RuntimeError(f"Could not find student {first} {last} in this class")
            selected_students.append(student)
        confirmation = self.show_deletion_warning("student")
        if confirmation:
            for student in selected_students:
                self.class_obj.delete_student(student)

    def handle_button_exam_details(self):
        """
       Handles the click on exam details
       :return:
       """
        # find exam that is selected
        selected_row = self.treeview_exams.selectedItems()
        if len(selected_row) != 1:
            raise RuntimeError(f"Wrong number of exams selected for this action: {len(selected_row)} instead of 1")
        exam_name = selected_row[0].data(0,0)
        try:
            exam = self.class_obj.get_exam(exam_name)
            self.show_window_exam_detail(exam)
        except Exception as e:
            raise RuntimeError(f"Got exception on buttonpress exam details: \n{e}")

    def handle_button_add_exam(self):
        """
        Handles button Add exam
        :return:
        """
        self.show_prompt_add_exam()
        # TODO maybe do some stuff here, based on infos gotten in prompt window

    def handle_button_generate_exam_report(self):
        selected_row = self.treeview_exams.selectedItems()
        if len(selected_row) != 1:
            raise RuntimeError(f"Wrong number of exams selected for this action: {len(selected_row)} instead of 1")
        exam_name = selected_row[0].data(0, 0)

        try:
            exam = self.class_obj.get_exam(exam_name)
            # TODO ask user about file path to store the thingy -> use path instead of name, optimally
            path = ""
            filename = "report.pdf"
            exam.generate_summary_report()
        except Exception as e:
            raise RuntimeError(f"Got exception on buttonpress exam details: \n{e}")

    def handle_button_delete_exam(self):
        """
        Handles button Delete exam
        :return:
        """
        selected_rows = self.treeview_exams.selectedItems()
        if len(selected_rows) <= 0:
            raise RuntimeError(f"Empty selection of exams to be deleted")

        confirmation = self.show_deletion_warning("exam")
        if not confirmation:
            return

        selected_exams = []
        for row in selected_rows:
            exam_name = row.data(0, 0)
            try:
                exam = self.class_obj.get_exam(exam_name)
                selected_exams.append(exam)
            except:
                logging.WARNING(f"Could not find exam {exam_name} in {self.class_obj}")
        if len(selected_exams) > 0:
            for exam in selected_exams:
                self.class_obj.delete_exam(exam)

    def handle_button_details_category(self):
        raise NotImplementedError

    def handle_button_add_category(self):
        raise NotImplementedError

    def handle_button_delete_category(self):
        raise NotImplementedError

    def handle_button_generate_class_report(self):
        raise NotImplementedError

    def handle_button_delete_class(self):
        raise NotImplementedError

    def show_prompt_add_category(self):
        raise NotImplementedError

    def show_prompt_add_exam(self):
        raise NotImplementedError

    def show_prompt_add_students(self):
        raise NotImplementedError

    def show_prompt_add_students_now(self):
        raise NotImplementedError

    def show_prompt_student_details(self, student):
        raise NotImplementedError

    def show_window_exam_detail(self, exam):
        # TODO also initialize exam object in new window
        if self.window_examDetail is None:
            self.window_examDetail = WindowExamDetail()

        self.window_examDetail.show()

    def show_deletion_warning(self, type: str):
        """
        Shows warning "Are you sure you want to delete xyz
        :type: Used to distinguish what will be deleted (only GUI consequences)
        :return: True iff user presses "accept
        """

        if type == "student":
            print("Are you sure you want to delete student xyz")
        return True


# TODO remove debug code

def main():
    app = QApplication(sys.argv)


    win = WindowClassDetail(Class(name="1a", year=2020, term="HS"))

    win.show()

    sys.exit(app.exec())

main()
