import logging
import sys, os

from PyQt6 import QtGui, QtCore
from PyQt6.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QTreeWidgetItem, QTabWidget, QWidget, QGridLayout, QTreeView,
    QTreeWidget, QHeaderView, QAbstractItemView
)

from PyQt6.uic import loadUi

from frontend.class_window_handler import WindowClassDetail
from main_window import Ui_MainWindow
from backend.overview import Overview


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

        # self.populate_treeview()
        # self.connectSignalsSlots()

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
        print(working_directory)

        self.ov = Overview()
        self.ov.folderpath = working_directory
        self.ov.load_classes()

        # TODO load exams for each class (broken as of now)
        # for class_obj in self.ov.classes:
        #     print(f"name:  {class_obj.filename_base_exam[1:]}")
        #     self.ov.load_categories_and_exams(class_obj)

        print(self.ov.classes)
        print(self.ov.terms)

        return

    def create_tabs(self):
        """
        Based on all found semesters, create QtWidgets.QTabWidget(parent=self.centralwidget) for all found semesters (up to 4 or so)
        Handle no semester found => Do some default thingy
        Also populate treeview with found classes
        :return:
        """
        # self.populate_treeview()

        # remove the second tab -- cannot do that in QT designer (could also alter the main_window.py file, but that gets overwritten with every change in qt designer)
        self.tabWidget.removeTab(1)

        # To handle no semester found, I can use a "default tab" that I add in main_window.py and remove this tab with         self.tabWidget.removeTab(0)
        # add tabs:
        # self.tab_2 = QtWidgets.QWidget()
        # self.tab_2.setObjectName("tab_2")
        # self.tabWidget.addTab(self.tab_2, "")

        if len(self.ov.terms) == 0:
            logging.INFO(f"No classes found at location {self.ov.folderpath}. Using default tab for gui")
        else:
            # add tabs for each found term
            self.tabWidget.removeTab(0)
            self.treeViews_classes_in_term = {}
            for term in self.ov.terms[-4:]:
                print(f"term: {term}")
                tab_clss = QWidget()
                tab_clss.setEnabled(True)
                tab_clss.setObjectName(f"tab_{term[0]}_{term[1]}")
                self.tabWidget.addTab(tab_clss, f"{term[0]} {term[1].upper()}")

                # create treeview for this term
                classes_in_term = self.ov.fetch_classes(term=term[1], year=term[0])
                print(classes_in_term)
                grid_layout = QGridLayout(tab_clss)
                grid_layout.setObjectName(f"gridLayout_{term[0]}_{term[1].lower()}")
                treeview_clss = QTreeWidget(parent=tab_clss)
                # TODO better disselection of items (with esc, clicking somewhere else, ...)
                treeview_clss.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
                treeview_clss.setObjectName(f"treeView__{term[0]}_{term[1].lower()}")
                # TODO maybe do this thing a little bit nicer (dynamic resizing of column widths)
                header = treeview_clss.header()
                header.setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
                header.setStretchLastSection(False)


                # fill treeview with list of classes
                treeview_clss.setColumnCount(3)
                treeview_clss.setHeaderLabels([f"Classes in {term[1].upper()} {term[0]}", "Number of students", "Number of exams"])

                treeview_clss.insertTopLevelItems(0, [QTreeWidgetItem([cls.name, str(len(cls.students)), str(len(cls.fetch_exams()))]) for cls in classes_in_term])

                grid_layout.addWidget(treeview_clss, 0, 0, 1, 1)
                self.treeViews_classes_in_term[f"{term[0]}_{term[1].lower()}"] = treeview_clss

        return

    def test_function(self):
        raise NotImplementedError

    def connect_signals(self):
        """
        Take care of button presses, action calls etc.
        Probably inefficient, but collect every action here and hand the calls to the respective functions (in other files etc.) from here
        => keeps code a little bit cleaner
        :return:
        """

        """
        Find way to disable certain buttons (delete class, details) if nothing in treeview is selected
        """
        self.button_details.clicked.connect(self.handle_button_details)
        self.button_addClass.clicked.connect(self.test_function)
        self.button_deleteClass.clicked.connect(self.handle_button_delete)
        self.button_saveDB.clicked.connect(self.test_function)
        self.button_changeLocation.clicked.connect(self.test_function)
        self.button_openDB.clicked.connect(self.test_function)


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

        print("here")
        tab_clss = self.tabWidget.currentWidget()
        treeView_clss: QTreeWidget = tab_clss.findChild(QTreeWidget)
        selected_items = treeView_clss.selectedItems()
        if len(selected_items) == 0:
            self.disable_buttons()
        if len(selected_items) > 0:
            self.enable_buttons(selected_items)

    @QtCore.pyqtSlot(QTreeWidgetItem, int)

    def handle_treeview_doubleclick(self, item, col):
        """

        :param item: clicked treeview item
        :param col: column which was clicked
        :return:
        """

        class_name = item.text(0)
        year, term = self.get_current_term_year()
        print(self.ov.classes)
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


    def enable_buttons(self, selected_items):
        """
        Some buttons (delete class, details, ...) should only be clickable if an item is selected
        :return:
        """
        for but in self.selectable_buttons:
            # special case for details: only one class detail should be allowed to be opened, not multiple.
            if but == self.button_details:
                print("here2")
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
        # self.treeView
        exams = ["orale 1", "orale 2", "grammaire"]
        students = ["Peter", "Hans", "Frieda"]
        grades = {}
        grades["orale 1"] = {"Peter": 4.5, "Hans": 5.3, "Frieda": 4.2}
        grades["orale 2"] = {"Peter": 3.5, "Hans": 4.7, "Frieda": 5.6}
        grades["grammaire"] = {"Peter": 5.5, "Hans": 4.3, "Frieda": 5}

        self.treeView.setColumnCount(1 + len(grades))
        self.treeView.setHeaderLabels(["Students"] + list(grades.keys()))
        items = []
        for student in students:
            # get layout [student, grade 1, grade 2, grade 3, ...]
            list_tmp = [student]
            for exam in grades:
                list_tmp.append(str((grades[exam])[student]))
            item = QTreeWidgetItem(list_tmp)
            items.append(item)
        self.treeView.insertTopLevelItems(0, items)
        return

        # Old code form online example, is example of hierarchical structure
        # data = {"Project A": ["file_a.py", "file_a.txt", "something.xls"],
        #         "Project B": ["file_b.csv", "photo.jpg"],
        #         "Project C": []}
        # self.treeView.setColumnCount(2)
        # self.treeView.setHeaderLabels(["Name", "Type"])
        # items = []
        # for key, values in data.items():
        #     item = QTreeWidgetItem([key])
        #     for value in values:
        #         ext = value.split(".")[-1].upper()
        #         child = QTreeWidgetItem([value, ext])
        #         item.addChild(child)
        #     items.append(item)
        #
        # self.treeView.insertTopLevelItems(0, items)

    def some_action2(self):
        print("hello world")

    def connectSignalsSlots(self):

        self.button1.clicked.connect(self.some_action2)
        self.action_Some_option2.triggered.connect(self.some_action2)

    #
    #     self.action_Find_Replace.triggered.connect(self.findAndReplace)
    #
    #     self.action_About.triggered.connect(self.about)


    def about(self):

        QMessageBox.about(

            self,

            "About Sample Editor",

            "<p>A sample text editor app built with:</p>"

            "<p>- PyQt</p>"

            "<p>- Qt Designer</p>"

            "<p>- Python</p>",

        )

    ### HELPER FUNCTIONS

    def get_current_term_year(self):
        """
        based on currently selected tab, return year / term
        :return: year (int), term (lower str)
        """

        curr_tab_name = self.tabWidget.currentWidget().objectName()

        _, year, term = curr_tab_name.split('_')

        return year, term.lower()




def main():


    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())

# TODO proper calling from cli.py or so, don't hardcode the main function caller
main()

