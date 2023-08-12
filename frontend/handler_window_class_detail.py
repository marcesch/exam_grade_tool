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

        # windows that can be opened from this view
        self.window_examDetail = None
        self.prompt_add_category = None
        self.prompt_add_exam = None
        self.prompt_add_students = None
        self.prompt_add_students_now = None
        self.prompt_add_student_details = None

        _translate = QtCore.QCoreApplication.translate
        self.window().setWindowTitle(f"Class {self.class_obj.name} {self.class_obj.term.upper()} {self.class_obj.year}")
        # WindowClassDetail.setWindowTitle(_translate("WindowClassDetail", f"Class detail {self.class_obj.name} {self.class_obj.term.upper()} {self.class_obj.year}"))


    def test_function(self):
        """
        Used to connect actions etc.
        :return:
        """
        print("hi")
        return
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

        single_elements_buttons_students = []
        single_elements_buttons_exams = []
        single_elements_buttons_categories = []
        single_element_buttons = single_elements_buttons_students + single_elements_buttons_exams + single_elements_buttons_categories

        something_selected_buttons_students = []
        something_selected_buttons_exams = []
        something_selected_buttons_categories = []
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




    def show_prompt_add_category(self):
        raise NotImplementedError

    def show_prompt_add_exam(self):
        raise NotImplementedError

    def show_prompt_add_students(self):
        raise NotImplementedError

    def show_prompt_add_students_now(self):
        raise NotImplementedError

    def show_prompt_student_details(self):
        raise NotImplementedError

    def show_window_exam_detail(self):
        if self.window_examDetail is None:
            self.window_examDetail = WindowExamDetail()

        self.window_examDetail.show()


# TODO remove debug code

def main():
    app = QApplication(sys.argv)


    win = WindowClassDetail(Class(name="1a", year=2020, term="HS"))

    win.show()

    sys.exit(app.exec())

main()
