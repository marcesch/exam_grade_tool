"""
Demo of all widgets
"""

import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import sys
import json
sys.path.append("/home/marcesch/privat/Selina/Notenuebersicht/backend/")
from backend.overview import Overview
from backend.classes import Class
from backend.exam import Exam
from backend.student import Student


def fun_print_hello():
    print("hello")

def fun_print_ciao():
    print("ciao")

def fun_action(first, last):
    print(f"some action {first} {last}")

class App_OverviewClass(TKMT.ThemedTKinterFrame):

    """
    Window containing details on one single class, roughly:

    |------------------------------------------------------------|
    |  some text here                                            |
    |                                                            |
    |  |---------------|   |------------------|   |-----------|  |
    |  | student a     |   | cat1 weight mode |   | stuff     |  |
    |  | student b     |   | cat2 weight mode |   |           |  |
    |  | student c     |   | ...              |   |-----------|  |
    |  | ...           |   |------------------|                  |
    |  |---------------|                                         |
    |                      |------------------|                  |
    |                      | exam1            |                  |
    |                      | ...              |                  |
    |                      |------------------|                  |
    |                                                            |
    |------------------------------------------------------------|

    """

    def __init__(self, theme, mode, class_obj, tabs, ov, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.label_frame = self.addLabelFrame("Class 2")
        self.label_frame.Label("This is some text for new class window")
        self.caller_tabs = tabs
        self.ov: Overview = ov
        self.class_obj: Class = class_obj
        assert len(self.caller_tabs) > 0
        assert len(self.class_obj.students) > 0, f"Class {class_obj}\n"

        self.panedWindow1 = self.PanedWindow(f"Overview Class {self.class_obj.name}")
        self.pane1 = self.panedWindow1.addWindow()

        self.notebook = self.pane1.Notebook("Notebook Exam overview")
        self.tabs = []
        self.create_tabs()


        for tab in self.tabs:
            students = []
            for stud in self.class_obj.students:
                students.append({'lastname': stud.lastname, 'firstname': stud.firstname})

            students.sort(key=lambda stud: (stud['lastname'], stud['firstname']))

            tab.frame_class = tab.addLabelFrame("Klassenübersicht")
            tab.frame_class.Label("Text zur Klassenübersicht")
            tab.treeview_classlist = tab.frame_class.Treeview(["Nachname", "Vorname"], [120, 120], 10, students, 'subfiles',
                                        ['lastname', 'firstname'])
            tab.treeview_classlist.bind("<<TreeviewSelect>>", self.on_click_student)

            tab.nextCol()
            tab.frame_cat = tab.addLabelFrame("Here is some text")
            tab.frame_cat.Label("With some more text here")

            categories = []
            for cat in self.class_obj.categories:
                categories.append({"name": cat.name, "weight": cat.weight, "type": cat.grading_type})

            tab.treeview_categories = tab.frame_cat.Treeview(["Kategorie", "Gewicht", "Bewertungstyp"], [120, 120, 120], 10,
                                                   categories, 'subfiles',
                                                   ['name', 'weight', 'type'])
            tab.treeview_categories.bind("<<TreeviewSelect>>", self.on_click_category)

        self.run()



    def create_tabs(self):
        """
        Using tabs-list form main window, add tabs to this view. User should be able to switch between different years for this class smoothly
        Need to add some predecessor list as a field to class to keep track of old instances of this class
        :return:
        """
        curr_tab = self.notebook.addTab(f"{self.class_obj.term.upper()} {self.class_obj.year}")
        self.tabs.append(curr_tab)
        return

        # TODO this part will be a little bit fiddly -- I'll ignore it for now
        # TODO in order to work properly, I need to keep a dictionary of (year, term) of previous exams -> otherwise, switching tabs won't work
        # => ignoring for now
        # TODO automatically choose the tab that was "called upon" => switch to tab that matches the year / term when class-object was being pressed
        for tab in self.caller_tabs:
            term, year = (tab.name).split(" ")[-2:]

            curr_tab = self.notebook.addTab(f"{term.upper()} {year}")
            self.tabs.append(curr_tab)

    def on_click_student(self, event):
        """
        Maybe add functionality (renaming / ...) when double clicking student
        :return:
        """
        raise NotImplementedError

    def on_click_category(self, event):
        raise NotImplementedError








class App_OverviewClasses(TKMT.ThemedTKinterFrame):

    """
    Window containing overview over all classes, roughly:

    |------------------------------------------------------------|
    |  some text here                                            |
    |                                                            |
    |                                                            |
    |  | tab1 | tab2 | tab3 | tab 4|                             |
    |                                                            |
    |  |------------------------------|                          |
    |  | student a                    |                          |
    |  | student b                    |                          |
    |  | student c                    |                          |
    |  | ...                          |                          |
    |  |------------------------------|                          |
    |                                                            |
    |------------------------------------------------------------|

    """

    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("Overview over all classes", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.ov = Overview()

        # TODO use that instead of testing init function
        # self.ov.load_classes()
        # for class_obj in self.ov.classes:
        #     self.ov.load_categories_and_exams(class_obj)
        self.initialize_dummy_classes()

        self.label_frame = self.addLabelFrame("Section 1")
        self.label_frame.Label("This is some text")

        self.panedWindow1 = self.PanedWindow("Should be middle paned window")
        self.pane1 = self.panedWindow1.addWindow()

        self.create_tabs()

        self.nextCol()
        self.button_frame = self.addLabelFrame("Buttons")
        self.button_frame.Button("Add Class", self.add_class)
        self.button_frame.Button("Delete Class", self.remove_class)

        # self.debugPrint()
        self.run()

    def initialize_dummy_classes(self):
        """
        Only for testing purposes -- initialize some class objects in an overview instance
        :return:
        """
        self.ov.classes.append(Class("6a", "HS", 2020))
        class6a: Class = (self.ov.classes[0])
        class6a.initialize_new_class([{'firstname': "alex", 'lastname': "hansson"}])
        class6a.add_category({"name": "orale", "weight": 0.3})
        class6a.add_category({"name": "grammaire", "weight": 0.2})
        class6a.add_category({"name": "essaie", "weight": 0.5})


        self.ov.classes.append(Class("3b", "FS", 2021))
        self.ov.classes.append(Class("4b", "HS", 2021))
        self.ov.classes.append(Class("4x", "HS", 2021))
        self.ov.classes.append(Class("1s", "HS", 2021))
        self.ov.classes.append(Class("2s", "FS", 2022))
        self.ov.classes.append(Class("5b", "FS", 2022))
        self.ov.classes.append(Class("3b", "FS", 2015))

    def add_class(self):
        """
        Handler for button press "add class"
        TBD should open new window that takes some prompts etc.
        :return:
        """
        raise NotImplementedError

    def remove_class(self):
        """
        Handler for button press "remove class"
        TBD should open new window that takes some prompts etc.
        :return:
        """
        raise NotImplementedError

    def create_tabs(self):
        """
        Creates the tabs for the last 4 semesters, if possible.
        :return:
        """
        self.notebook = self.pane1.Notebook("Test Name is where no idea")
        newest_semesters = self.ov.return_newest_classes(4)
        self.tabs = []

        for sem in newest_semesters:
            tabs_curr_sem = self.notebook.addTab(f"{sem[0]} {sem[1]}")
            tabs_curr_sem.Label(f"{sem[0]}-{sem[1]}")
            self.tabs.append(tabs_curr_sem)

        for tab in self.tabs:
            term, year = (tab.name).split(" ")[-2:]
            classes = self.ov.fetch_classes(term, year)
            class_data = []

            for class_obj in classes:
                class_data.append({"name": class_obj.name, 'year': class_obj.term, 'term': class_obj.year})

            tab.treeview = tab.Treeview(['Klassenname', 'Semester', 'Jahr'], [120, 120, 120], 10, class_data, 'subfiles', ['name', 'term', 'year'], openkey='open')
            tab.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

    def on_treeview_select(self, event):
        item = event.widget.focus()
        values = event.widget.item(item)["values"]
        year = values[0]
        term = values[1]
        assert term.lower() == "hs" or "fs"
        name = event.widget.item(item)['text']
        # fun_action(firstname, lastname)
        if item:
            # create a new themed frame with a label
            class_obj = self.ov.get_class(name, year, term)
            App_OverviewClass(theme=self.theme,
                             mode=self.mode,
                             class_obj=class_obj,
                             tabs=self.tabs,
                             ov=self.ov,
                             usecommandlineargs=True,
                             usethemeconfigfile=True)

    def printcheckboxvars(self, number):
        print("Checkbox number:", number, "was pressed")
        print("Checkboxes: ", self.checkbox1.get(), self.checkbox2.get())

    def printradiobuttons(self, _var, _indx, _mode):
        print("Radio button: ", self.radiobuttonvar.get(), "pressed.")

    def handleButtonClick(self):
        print("Button clicked. Current toggle button state: ", self.togglebuttonvar.get())

    def textupdate(self, _var, _indx, _mode):
        print("Current text status:", self.textinputvar.get())

    def menuprint(self, item):
        if self == self:
            pass
        print("Menu item chosen: ", item)

    def validateText(self, text):
        if self == self:
            pass
        if 'q' not in text:
            return True
        print("The letter q is not allowed.")
        return False

def startup_process():
    print("Somewhere here I could start initializing all classes, .. loaded from disk => use that in memory (presumably reasonably small amount of data) and load from disk only once ")

if __name__ == '__main__':
    startup_process()
    app = App_OverviewClasses("azure", "light")
    # app = App(input("Theme (azure / park / sun-valley): ").lower(), input("dark / light: ").lower())