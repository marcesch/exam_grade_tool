import logging
import sys

from PyQt6 import QtCore
from PyQt6.QtWidgets import QMainWindow, QApplication, QTreeWidget, QHeaderView, QTreeWidgetItem, QAbstractItemView

from backend.category import *
from backend.classes import Class
from backend.student import Student
from frontend.handler_window_exam_detail import WindowExamDetail
from ui_window_class_detail import  Ui_WindowClassDetail

# TODO maybe change QMainWindow -> QApplicationWindow
class WindowClassDetail(QMainWindow, Ui_WindowClassDetail):

    def __init__(self, class_obj, parent=None):

        self.DEBUG = True
        # initialize all GUI elements based on information from .ui file (compiled to python using pyuic6)
        super().__init__(parent)

        self.setupUi(self)
        self.class_obj = class_obj
        if self.DEBUG:
            print(f"[CLASS DETAIL] Showing class details for {class_obj}")
            print(f"[CLASS DETAIL] Registered students {class_obj.students}")
        self.window().setWindowTitle(f"Class {self.class_obj.name} {self.class_obj.term.upper()} {self.class_obj.year}")

        # windows that can be opened from this view
        self.window_examDetail = None
        self.prompt_add_category = None
        self.prompt_add_exam = None
        self.prompt_add_students = None
        self.prompt_add_students_now = None
        self.prompt_add_student_details = None

        # gui functions that take care of displaying stuff
        self.populate_treeviews()

        # take care of signals
        self.connect_signals()


    def populate_treeviews(self):
        """
        Fills the treeviews with data
        :return:
        """

        # set treeview properties
        for treeview in [self.treeview_students, self.treeview_exams, self.treeview_categories]:
            treeview.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)

            # dynamically adjust width of headers
            header = treeview.header()
            header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
            header.setStretchLastSection(True)



        # fill with contents
        self.treeview_students.setColumnCount(3) # first, last, average grade
        self.treeview_exams.setColumnCount((3)) # name, category, number of students that have written exam
        self.treeview_categories.setColumnCount(4) # name, number of exams, weight, strategy

        self.treeview_students.setHeaderLabels([f"Lastname", f"Firstname", f"Average Grade"])
        self.treeview_exams.setHeaderLabels([f"Exam Name", f"Number of participants", f"Category"])
        self.treeview_categories.setHeaderLabels(([f"Category Name", f"Weight", f"Mode", f"Number of exams"]))

        # TODO use real functions once they are implemented
        # self.treeview_students.insertTopLevelItems(0, [QTreeWidgetItem([stud.firstname, stud.lastname, str(self.class_obj.number_exams_taken(stud)), str(self.class_obj.average_grade(stud))]) for stud in self.class_obj.students])
        self.treeview_students.insertTopLevelItems(0, [QTreeWidgetItem([stud.lastname, stud.firstname, str(4)]) for stud in self.class_obj.students])
        # TODO keep exams in list, not in categories
        # self.treeview_exams.insertTopLevelItems(0, [QTreeWidgetItem([exam.name, exam.category, exam.number_participants()]) for exam in self.class_obj.exams])

        for exam in self.class_obj.exams:
            print(f"[DEBUG] Exam {exam} has category {exam.category} ({type(exam.category)}) with name {exam.category.name} ({type(exam.category.name)})")
        print(f"[WINDOW CLASS DETAIL] exam.category.name: {[[exam.name, str(0), exam.category.name] for exam in self.class_obj.exams]}")
        self.treeview_exams.insertTopLevelItems(0, [QTreeWidgetItem([exam.name, str(0), exam.category.name]) for exam in self.class_obj.exams])

        def return_category_type(category):
            if type(category) == BaseCategory:
                return "(no category assigned))"
            if type(category == CategoryBonus):
                return "Bonus"
            if type(category == CategoryDefault):
                return "Standard"
            if type(category == CategoryWithDroppedGrades):
                return "Drop Grades"
            else:
                raise NotImplementedError

        # self.treeview_categories.insertTopLevelItems(0, [QTreeWidgetItem([cat.name, str(cat.weight), cat.grading_type, self.class_obj.number_exams_in_category(cat)]) for cat in self.class_obj.categories])
        self.treeview_categories.insertTopLevelItems(0, [QTreeWidgetItem([cat.name, str(cat.weight), return_category_type(cat), str(len(self.class_obj.get_exams_of_category(cat)))]) for cat in self.class_obj.categories])

    def update_treeviews(self):
        """
        Updates all treeviews after alteration (addition / deletion / ...)
        :return:
        """
        self.update_treeview_student()
        self.update_treeview_exam()
        self.update_treeview_category()

    def update_treeview_student(self):
        """
        Update student treeview after alteration (addition / deletion / ...)
        :return:
        """
        self.treeview_students.clear()
        self.treeview_students.insertTopLevelItems(0, [QTreeWidgetItem([stud.lastname, stud.firstname, str(4)]) for stud in self.class_obj.students])


    def update_treeview_exam(self):
        """
        Update student treeview after alteration (addition / deletion / ...)
        :return:
        """
        self.treeview_exams.clear()
        self.treeview_exams.insertTopLevelItems(0, [QTreeWidgetItem([exam.name, str(0), exam.category]) for exam in self.class_obj.exams])


    def update_treeview_category(self):
        """
        Update student treeview after alteration (addition / deletion / ...)
        :return:
        """
        self.treeview_categories.clear()
        self.treeview_categories.insertTopLevelItems(0, [QTreeWidgetItem([cat.name, str(cat.weight), cat.grading_type, str(1)]) for cat in self.class_obj.categories])


    def connect_signals(self):
        """
        Take care of button presses, action calls etc.
        Probably inefficient, but collect every action here and hand the calls to the respective functions (in other files etc.) from here
        => keeps code a little bit cleaner
        :return:
        """

        self.button_studentDetails.clicked.connect(self.handle_button_details_student)
        self.button_addStudents.clicked.connect(self.handle_button_add_students)
        self.button_removeStudent.clicked.connect(self.handle_button_remove_student)
        self.button_examDetails.clicked.connect(self.handle_button_details_exam)
        self.button_addExam.clicked.connect(self.handle_button_add_exam)
        self.button_generateExamReport.clicked.connect(self.handle_button_generate_exam_report)
        self.button_deleteExam.clicked.connect(self.handle_button_delete_exam)
        self.button_detailsCategory.clicked.connect(self.handle_button_details_category)
        self.button_addCategory.clicked.connect(self.handle_button_add_category)
        self.button_deleteCategory.clicked.connect(self.handle_button_delete_category)
        self.button_generateClassReport.clicked.connect(self.handle_button_export_excel)
        self.button_deleteClass.clicked.connect(self.handle_button_delete_class)

        # deal with treeview signals
        for treeview in [self.treeview_students, self.treeview_exams, self.treeview_categories]:
            treeview.itemSelectionChanged.connect(self.update_enabled_buttons)

        self.treeview_students.itemSelectionChanged.connect(self.update_enabled_buttons)

        self.treeview_students.itemDoubleClicked.connect(self.handle_treeview_student_double)
        self.treeview_exams.itemDoubleClicked.connect(self.handle_treeview_exam_double)
        self.treeview_categories.itemDoubleClicked.connect(self.handle_treeview_cat_double)


    def handle_treeview_student_double(self, item, col):
        """
        Handles double click on student item
        :param item: item in treeview that was clicked
        :param col: column where it was clicked
        :return:
        """

        student_last, student_first = item.text(0), item.text(1)
        student_obj = self.class_obj.get_student(student_first, student_last)
        self.show_prompt_student_details(student_obj)

    def handle_treeview_exam_double(self, item, col):
        """
        Handles double click on exam item
        :param item: item in treeview that was clicked
        :param col: column where it was clicked
        :return:
        """

        exam_name = item.text(0)
        exam_obj = self.class_obj.get_exam(exam_name)
        self.show_window_exam_detail(exam_obj)

    def handle_treeview_cat_double(self, item, col):
        """
        Handles double click on category item
        :param item: item in treeview that was clicked
        :param col: column where it was clicked
        :return:
        """

        category_name = item.text(0)
        category_obj = self.class_obj.get_category(category_name)
        self.show_prompt_category_details(category_obj)

    def number_students_selected(self):
        """
        :return: Number of students selected in treeview of students
        """

        selected_student_rows = self.treeview_students.selectedItems()
        return len(selected_student_rows)

    def number_exams_selected(self):
        """
        :return: Number of exams selected in exam treeview
        """

        selected_exam_rows = self.treeview_exams.selectedItems()
        return len(selected_exam_rows)

    def number_categories_selected(self):
        """
        :return: Number of categories selected in category treeview
        """

        selected_cat_rows = self.treeview_categories.selectedItems()
        return len(selected_cat_rows)

    def update_enabled_buttons(self):
        """
        Handles the enabling / disabling of buttons, based on number of items selected in the treeviews
        :return:
        """

        if self.DEBUG:
            print(f"[WINDOW CLASS DETAILS] Got here")

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

    def handle_button_details_student(self):
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
            first = row.data(1,0)
            student = self.class_obj.get_student(first, last)
            if student is None:
                # TODO don't raise errors in GUI...
                print(f"[ERROR] Could not find student {first} {last} in this class")
            selected_students.append(student)
        confirmation = self.show_deletion_warning("student")
        if confirmation:
            for student in selected_students:
                self.class_obj.delete_student(student)
                # update treeview to remove the deleted item
                self.update_treeview_student()

    def handle_button_details_exam(self):
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
            print(f"[ERROR] Got exception on buttonpress exam details: \n{e}")

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
            print(f"[ERROR] Empty selection of exams to be deleted")

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
            self.update_treeview_exam()

    def handle_button_details_category(self):
        """
        Handles button details category
        :return:
        """

        selected_categories = self.treeview_categories.selectedItems()
        if len(selected_categories) != 1:
            print(f"[ERROR] Wrong number of categories selected")
            return

        selected_cat = selected_categories[0]
        self.show_prompt_category_details(self.class_obj.get_category(selected_cat.data(0,0)))

    def handle_button_add_category(self):
        """
        Handles button add category
        :return:
        """
        self.show_prompt_add_category()
        # TODO maybe add stuff here

    def handle_button_delete_category(self):
        """
        Handles button Delete category
        :return:
        """
        selected_rows = self.treeview_categories.selectedItems()
        if len(selected_rows) <= 0:
            print(f"[ERROR] Empty selection of categories to be deleted")
            return

        confirmation = self.show_deletion_warning("category")
        if not confirmation:
            return

        selected_categories = []
        for row in selected_rows:
            cat_name = row.data(0,0)
            try:
                cat_obj = self.class_obj.get_category(cat_name)
                selected_categories.append(cat_obj)
            except:
                logging.WARNING(f"Could not find cateogry {cat_name} in {self.class_obj.categories}")
        if len(selected_categories) > 0:
            for cat in selected_categories:
                self.class_obj.delete_category(cat)
            self.update_treeview_category()

    def handle_button_export_excel(self):
        raise NotImplementedError

    def handle_button_delete_class(self):

        confirmation = self.show_deletion_warning("class")
        if not confirmation:
            logging.info(f"User did not confirm deletion of class, skipping ...")
            return

        raise NotImplementedError

    def show_prompt_add_category(self):

        raise NotImplementedError

    def show_prompt_add_exam(self):
        raise NotImplementedError

    def show_prompt_add_students(self):
        raise NotImplementedError

    def show_prompt_add_students_now(self):
        raise NotImplementedError

    def show_prompt_student_details(self, student: Student):
        raise NotImplementedError

    def show_prompt_category_details(self, category: BaseCategory):
        # TODO need to create the window prompt
        print(f"Got to show_prompt_cat_details")
        raise NotImplementedError

    def show_window_exam_detail(self, exam):
        # TODO also initialize exam object in new window
        if self.window_examDetail is None:
            self.window_examDetail = WindowExamDetail(exam, self.class_obj)

        self.window_examDetail.show()

    def show_deletion_warning(self, type: str):
        """
        Shows warning "Are you sure you want to delete xyz
        :type: Used to distinguish what will be deleted (only GUI consequences)
        :return: True iff user presses "accept"
        """

        if type == "student":
            print(f"Skipped check for student deletion")
            return True
        if type == "category":
            print(f"Skipped check for category deletion")
            return True
        if type == "exam":
            print(f"Skipped check for category deletion")
            return True
        if type == "class":
            # TODO here I do need to show a prompt
            return False
        return True




