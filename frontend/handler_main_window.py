import logging
import random
import sys, os

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTreeWidgetItem, QTabWidget, QWidget, QGridLayout, QTreeView,
    QTreeWidget, QHeaderView, QAbstractItemView
)

from backend.classes import Class
from frontend.handler_window_exam_detail import WindowExamDetail
from ui_main_window import Ui_MainWindow
from frontend.handler_window_class_detail import WindowClassDetail
from backend.overview import Overview

DEBUG = True


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        # initialize all GUI elements based on information from .ui file (compiled to python using pyuic6)
        super().__init__(parent)

        self.window_classDetail = None

        self.startup()
        self.setupUi(self)

        self.create_tabs()
        self.connect_signals()

        # those buttons will be (dis)selected, based on whether a class is selected or not
        self.selectable_buttons = [self.button_details, self.button_deleteClass]

    def startup(self):
        """
        Here, I can handle the startup thingies, like loading config (stored on some predetermined location:
        https://softwareengineering.stackexchange.com/questions/160097/where-should-i-put-configuration-files
        https://stackoverflow.com/questions/15677388/default-location-for-configuration-files-macos
        and loading class data / previous database (location of which can be found in config file)

        might want to do this in separate file instead to keep things clean
        :return:
        """

        working_directory = os.path.join(os.path.expanduser('~'), "grades_students/", "klassen/")
        print(f"[MAIN] looking for classes in {working_directory}")

        self.ov = None
        if DEBUG:
            self.ov = Overview.load_from_json("testing_file.json")
        else:
            self.ov = Overview.load_from_json()


        no_classes_found = (len(self.ov.classes) == 0)
        if no_classes_found:
            # TODO add prompt "No classes found -> look elsewhere or create new"
            print(f"No classes found in {working_directory}")

        # TODO load exams for each class (broken as of now)
        # for class_obj in self.ov.classes:
        #     print(f"name:  {class_obj.filename_base_exam[1:]}")
        #     self.ov.load_categories_and_exams(class_obj)

        print(self.ov.classes)
        print(self.ov.get_terms())

        return

    def create_tabs(self):
        """
        Based on all found semesters, create QtWidgets.QTabWidget(parent=self.centralwidget) for all found semesters (up to 4 or so)
        Handle no semester found => Do some default thingy
        Also populate treeview with found classes
        :return:
        """

        # remove the second tab -- cannot do that in QT designer (could also alter the ui_main_window.py file, but that gets overwritten with every change in qt designer)
        self.tabWidget.removeTab(1)

        # To handle no semester found, I can use a "default tab" that I add in ui_main_window.py and remove this tab with         self.tabWidget.removeTab(0)
        # add tabs:
        # self.tab_2 = QtWidgets.QWidget()
        # self.tab_2.setObjectName("tab_2")
        # self.tabWidget.addTab(self.tab_2, "")

        if len(self.ov.get_terms()) == 0:
            logging.INFO(f"No classes found. Using default tab for gui")
        else:
            # add tabs for each found term
            self.tabWidget.removeTab(0)
            self.treeViews_classes_in_term = {}
            for term_tuple in self.ov.get_terms()[-4:]:
                print(f"term: {term_tuple[0]} {term_tuple[1]}")
                tab_clss = QWidget()
                tab_clss.setEnabled(True)
                tab_clss.setObjectName(f"tab_{term_tuple[0]}_{term_tuple[1]}")
                self.tabWidget.addTab(tab_clss, f"{term_tuple[0].upper()} {term_tuple[1]}")

                # create treeview for this term
                classes_in_term = self.ov.get_all_classes_of_period(term=term_tuple[0], year=term_tuple[1])
                grid_layout = QGridLayout(tab_clss)
                grid_layout.setObjectName(f"gridLayout_{term_tuple[0].lower()}_{term_tuple[1]}")
                treeview_clss = QTreeWidget(parent=tab_clss)
                # TODO better disselection of items (with esc, clicking somewhere else, ...)
                treeview_clss.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
                treeview_clss.setObjectName(f"treeView__{term_tuple[0].lower}_{term_tuple[1]}")
                header = treeview_clss.header()
                header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                header.setStretchLastSection(True)

                # fill treeview with list of classes
                treeview_clss.setColumnCount(3)
                treeview_clss.setHeaderLabels([f"Classes in {term_tuple[0].upper()} {term_tuple[1]}", "Number of students", "Number of exams"])

                treeview_clss.insertTopLevelItems(0, [QTreeWidgetItem([cls.name, str(len(cls.students)), str(len(cls.exams))]) for cls in classes_in_term])

                grid_layout.addWidget(treeview_clss, 0, 0, 1, 1)
                self.treeViews_classes_in_term[f"{term_tuple[0].lower()}_{term_tuple[1]}"] = treeview_clss


    def test_function(self):
        """
        Test slot function
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

        self.button_details.clicked.connect(self.handle_button_details)
        self.button_addClass.clicked.connect(self.handle_button_add)
        self.button_deleteClass.clicked.connect(self.handle_button_delete)
        self.button_saveDB.clicked.connect(self.handle_button_save)
        self.button_changeLocation.clicked.connect(self.handle_button_change_location)
        self.button_openDB.clicked.connect(self.handle_button_open_db)

        # deal with treeview signals
        for treeview_key in self.treeViews_classes_in_term:
            treeview: QTreeWidget = self.treeViews_classes_in_term[treeview_key]
            treeview.itemSelectionChanged.connect(self.handle_treeview_selection_change)
            treeview.itemDoubleClicked.connect(self.handle_treeview_doubleclick)

    def handle_treeview_selection_change(self):
        """
        Triggered when user selects different items in treeview. Handles disabling of buttons etc.
        :return:
        """

        b_items_selected, items_selected = self.treeview_items_selected()
        if b_items_selected:
            self.enable_buttons(items_selected)
        else:
            self.disable_buttons()

    @QtCore.pyqtSlot(QTreeWidgetItem, int)

    def handle_treeview_doubleclick(self, item, col):
        """

        :param item: clicked treeview item
        :param col: column which was clicked
        :return:
        """

        class_name = item.text(0)
        year, term = self.get_current_term_year()
        selected_class  = self.ov.get_class(class_name, year, term)
        self.show_class_details(selected_class)

    def handle_button_details(self):
        """
        Handler for button click details. Find selected class object, call show_class_details
        :return:
        """

        tree_widget: QTreeWidget = self.tabWidget.currentWidget().findChild(QTreeWidget)
        selected_row = tree_widget.selectedItems()
        if len(selected_row) != 1:
            raise RuntimeError(f"Wrong number of classes selected in treeview: {len(selected_row)} instead of 1")
        class_name = selected_row[0].data(0, 0)
        print(class_name)
        year, term = self.get_current_term_year()
        selected_class = self.ov.get_class(class_name, year, term)
        self.show_class_details(selected_class)


    def handle_button_delete(self):
        """
        Handler for button click delet class
        :return:
        """
        tree_widget: QTreeWidget = self.tabWidget.currentWidget().findChild(QTreeWidget)
        selected_row = tree_widget.selectedItems()
        year, term = self.get_current_term_year()
        for el in selected_row:
            class_name = el.data(0,0)
            print(class_name, year, term)
            class_obj = self.ov.get_class(class_name, year, term)
            self.ov.delete_class(class_obj)

    def handle_button_add(self):
        """
        Open new prompt (alert thingy) to get data from user and initialize new class
        :return:
        """

        # TODO open new prompt to get the required data
        name = ""
        year = 0
        term = ""
        self.ov.add_class(name, term, year)

    def handle_button_save(self):
        """
        Saves the DB to disk
        :return:
        """

        self.ov.store_to_db()


    def handle_button_open_db(self):
        """
        Handles button click change DB. Load classes, exam data, ...
        :return:
        """

        # todo folder pciker from os library
        path = ""
        self.ov.change_location(path)


    def handle_button_change_location(self):
        """
        Handler for "change location". Stores entire DB to new location / folder
        :return:
        """
        raise NotImplementedError

    def treeview_items_selected(self):
        """

        :return: True, list of selected items iff at least 1 item is selected in treeview
        """
        tab_clss = self.tabWidget.currentWidget()
        treeView_clss: QTreeWidget = tab_clss.findChild(QTreeWidget)
        selected_items = treeView_clss.selectedItems()
        if len(selected_items) <= 0:
            return False, selected_items
        else:
            return True, selected_items

    def treevie_one_item_selected(self):
        """

        :return: True iff exatly 1 item is selected in treeview
        """
        at_least_one, selected_items = self.treeview_items_selected()
        return  at_least_one and len(selected_items) == 1


    def enable_buttons(self, selected_items):
        """
        Some buttons (delete class, details, ...) should only be clickable if an item is selected
        :return:
        """
        for but in self.selectable_buttons:
            # special case for details: only one class detail should be allowed to be opened, not multiple.
            if but == self.button_details:
                if len(selected_items) != 1:
                    but.setDisabled(True)
                    continue
            but.setEnabled(True)

    def disable_buttons(self):
        """
        Once items are not clicked anymore, disable the buttons again
        :return:
        """
        for but in self.selectable_buttons:
            but.setDisabled(True)

    def show_class_details(self, class_obj):
        """
        Opens details of new class based on selected class in treeview. See
        https://www.pythonguis.com/tutorials/pyqt6-creating-multiple-windows/
        for opening multiple windows
        :return:
        """

        if self.window_classDetail is None:
            self.window_classDetail = WindowClassDetail(class_obj)

        self.window_classDetail.show()


    def populate_treeview(self):

        # Old code form online example, is example of hierarchical structure
        raise NotImplementedError

        data = {"Project A": ["file_a.py", "file_a.txt", "something.xls"],
                "Project B": ["file_b.csv", "photo.jpg"],
                "Project C": []}
        self.treeView.setColumnCount(2)
        self.treeView.setHeaderLabels(["Name", "Type"])
        items = []
        for key, values in data.items():
            item = QTreeWidgetItem([key])
            for value in values:
                ext = value.split(".")[-1].upper()
                child = QTreeWidgetItem([value, ext])
                item.addChild(child)
            items.append(item)

        self.treeView.insertTopLevelItems(0, items)

    def get_current_term_year(self):
        """
        based on currently selected tab, return year / term
        :return: year (int), term (lower str)
        """

        curr_tab_name = self.tabWidget.currentWidget().objectName()

        _, term, year = curr_tab_name.split('_')

        return year, term.lower()

def main():

    print(f"[MAIN] Starting application...")
    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())

# TODO proper calling from cli.py or so, don't hardcode the main function caller

# DEBUG CODE
from tests.interaction_test_overview import initiate_overview
overview = initiate_overview()
debug_class = overview.classes[0]

# TODO continue here

def debug_window_exam_detail():
    app = QApplication(sys.argv)
    example_exams = debug_class.exams[0]


    win = WindowExamDetail(example_exams, debug_class)
    win.show()

    sys.exit(app.exec())


def debug_window_class_detail():
    app = QApplication(sys.argv)
    win = WindowClassDetail(debug_class)
    win.show()

    sys.exit(app.exec())



# main()
# debug_window_class_detail()
debug_window_exam_detail()
