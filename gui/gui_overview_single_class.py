import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import sys
import json
sys.path.append("/home/marcesch/privat/Selina/Notenuebersicht/backend/")
from backend.overview import Overview
from backend.classes import Class
from gui_overview_single_exam import App_OverviewExam


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
        super().__init__(f"Klassenübersicht Klasse {class_obj.name}", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.label_frame = self.addLabelFrame(f"Klassenübersicht Klasse {class_obj.name}")
        self.caller_tabs = tabs
        self.theme = theme
        self.mode = mode
        self.usecommandlineargs = usecommandlineargs
        self.usethemeconfigfile = usethemeconfigfile
        self.ov: Overview = ov
        self.class_obj: Class = class_obj
        assert len(self.caller_tabs) > 0
        assert len(self.class_obj.students) > 0, f"Class {class_obj}\n"

        self.panedWindow1 = self.PanedWindow(f"")
        self.pane1 = self.panedWindow1.addWindow()
        self.pane1.Text(f"Hier ist eine Übersicht aller Attribute der Klasse {class_obj.name}. Mit den Tabs auf "
                        f"andere Semester wechseln.\n\n Speicherort für alle relevanten Daten (Prüfungserge"
                        f"bnisse usw.): \n{class_obj.filename_class_base}")

        self.create_utility_bar()

        self.notebook = self.pane1.Notebook(f"")
        self.tabs = []

        self.create_tabs()

        for tab in self.tabs:
            self.create_student_overview(tab)
            self.create_categories_overview(tab)
            self.create_exam_overview(tab)

        self.run()

    def create_utility_bar(self):
        """
        Prints utility bar on the right hand side. Potential buttons include:
        - Create grade report (check that sum of weights is 1)
        - add exam
        - add category
        - add student
        - rename class  -> maybe also handle with double click on name of class or so
        - update semester

        :return:
        """
        # TODO multipel buttons next to each other -- example for that is on github of GUI package

        self.pane1.button_frame = self.pane1.addLabelFrame("Aktionen")
        self.pane1.button_frame.Button("Klasse umbenennen", self.rename_class,  col=0)
        self.pane1.button_frame.Button("Speicherort wechseln", self.change_location, col=1)
        self.pane1.button_frame.Button("Neues semester", self.update_sem, col=2)
        self.pane1.button_frame.Button("Notenzusammenfassung erstellen", self.generate_grade_report, col=3)

    def create_exam_overview(self, tab):
        """
        Prints list of all exams for that class for that year/term
        :return:
        """

        tab.nextCol()
        # prepare exam data for treeview
        exams = []
        for cat in self.class_obj.categories:
            for exam in cat.exams:
                exams.append({"name": exam.name, "cat": cat.name})

        tab.frame_exam = tab.addLabelFrame("Prüfungen")
        tab.frame_exam.Text("Folgende Prüfungen sind eingetragen \n (Doppelklick oder \"Details\" für mehr Optionen)")

        tab.frame_exam.treeview_exam = tab.frame_exam.Treeview(["Prüfung", "Kategorie"], [120, 120], 10, exams, 'subfiles',
                                    ['name', 'cat'])
        tab.frame_exam.treeview_exam.bind("<Double-1>", self.on_click_exam)
        tab.frame_exam.treeview_exam.bind("<Button-1>")

        tab.frame_exam.Button("Details", self.selectItem_exams)
        tab.frame_exam.Button("Prüfung hinzufügen", self.add_exam)
        tab.frame_exam.Button("Prüfungszusammenfassung generieren", self.some_fun)

    def create_categories_overview(self, tab):
        """
        Prints list of all categories and their weights
        :return:
        """

        tab.nextCol()
        tab.frame_cat = tab.addLabelFrame("Kategorien")
        tab.frame_cat.Text("Folgende Prüfungskateogrien sind registriert")

        # prepare categories data for treeview
        categories = []
        for cat in self.class_obj.categories:
            categories.append({"name": cat.name, "weight": cat.weight, "type": cat.grading_type})

        tab.frame_cat.treeview_cat = tab.frame_cat.Treeview(["Kategorie", "Gewicht", "Bewertungstyp"], [120, 120, 120], 10, categories, 'subfiles',
                                    ['name', 'weight', 'type'])
        tab.frame_cat.treeview_cat.bind("<<TreeviewSelect>>", self.on_click_category)

        tab.frame_cat.Button("Details", self.selectItem_cat)
        tab.frame_cat.Button("Kategorie hinzufügen", self.add_category)

    def some_fun(self, event=None):
        """
        Test function used for debugging
        :return:
        """
        print("Invoked this function")


    def create_student_overview(self, tab):
        """
        Prints a table of all students for this class, probably to the left.

        :return:
        """

        # TODO support for other tabs -- only select those students whcih actually belong to said class

        # prepare student list for Treeview
        students = []
        for stud in self.class_obj.students:
            students.append({'lastname': stud.lastname, 'firstname': stud.firstname})

        students.sort(key=lambda stud: (stud['lastname'], stud['firstname']))

        tab.frame_class = tab.addLabelFrame("Klassenübersicht")
        tab.frame_class.Text(f"Schüler:innen Klasse {self.class_obj.name}")

        tab.frame_class.treeview = tab.frame_class.Treeview(["Nachname", "Vorname"], [120, 120], 10, students, 'subfiles', ['lastname', 'firstname'])
        tab.frame_class.treeview.bind("<Double-1>", self.on_click_student)
        # TODO can also use https://stackoverflow.com/questions/30614279/tkinter-treeview-get-selected-item-values
        # to select multiple students and edit them all at once
        tab.frame_class.treeview.bind("<Button-1>")
        tab.frame_class.Button("Schüler:in entfernen", self.selectItem_student)
        tab.frame_class.Button("Schüler:in hinzufügen", self.add_student)

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
        # TODO automatically choose the tab that was "ca    lled upon" => switch to tab that matches the year / term when class-object was being pressed
        for tab in self.caller_tabs:
            term, year = (tab.name).split(" ")[-2:]

            curr_tab = self.notebook.addTab(f"{term.upper()} {year}")
            self.tabs.append(curr_tab)

    def rename_class(self):
        """
        Invokes rename_class
        :return:
        """
        raise NotImplementedError

    def change_location(self):
        """
        Alters location of class folder stored on disk
        :return:
        """
        raise NotImplementedError

    def update_sem(self):
        """
        Invokes update_sem on class -> refresh window to include new tab!
        :return:
        """

        # refresh window
        # TODO find out how to kill old window
        # smthin like this:
        # super().destroy()
        self.__init__(self.theme, self.mode, self.class_obj, self.tabs, self.ov, self.usecommandlineargs, self.usethemeconfigfile)
        raise NotImplementedError

    def generate_grade_report(self):
        """
        Invokes class_obj.generate_grade_report
        CHECKS WHETHER sum of weights is 1!!!
        :return:
        """

        sum_weight = 0
        for cat in self.class_obj.categories:
            sum += cat.weight
        if sum_weight != 1:
            # show error promt or so
            print(f"Bad new, sum of weights is {sum_weight} instead of 1...aborting")

        # TODO include check that all cateogries have weights (e.g. if category is created by creating exam and choosing an unknown cat)
        # and raise warning if weight of category is 0

        raise NotImplementedError

    def selectItem_student(self, tab):
        curItem = tab.frame_class.treeview.focus()
        print(f"Could invoke this {curItem}")
        self.some_fun()

    def on_click_student(self, event):
        """
        Allows editing the student (change name, ..)
        :param event:
        :return:
        """
        raise NotImplementedError

    def add_student(self):
        """
        Add student object to this class
        :return:
        """
        raise NotImplementedError

    def add_category(self):
        """
        Opens new winow prompt to let the user add a new category
        Has fields name, weight, and drop-down with grading types
        :return:
        """
        raise NotImplementedError

    def selectItem_cat(self):
        """
        Invokes on_click_category for selected category. Make button unavailable if no cat is selected
        :param tab:
        :return:
        """
        # curItem = tab.frame_cat.treeview.focus()
        # self.some_fun()
        raise NotImplementedError

    def on_click_category(self, event):
        """
        In new prompt, can:
        - update weight, name, grading type
        - delete category
        :return:
        """
        raise NotImplementedError

    def add_exam(self):
        """
        Open a new prompt to let the user add a new exam.
        Can use tree.insert() instead of refreshing the window
        :return:
        """
        raise NotImplementedError

    def selectItem_exams(self):
        """
        Invokes on_click_exam() for selected exam
        Make unavailable if no exams are selected
        :return:
        """
        # TODO how can I pass state from button press (need to know current tab) -> ugly solution would be "self.current_tab"
        # curItem = tab.frame_exam.treeview.focus()
        # -> can use PARTIAL, see examples of the modern theme thingy

        raise NotImplementedError

    def on_click_exam(self, event):
        """
        Opens details on exam, allowing user to add grades etc.
        :param event:
        :return:
        """

        item = event.widget.focus()
        values = event.widget.item(item)["values"]
        text = event.widget.item(item)["text"]
        exams = self.class_obj.fetch_exams()
        exam = None
        for ex in exams:
            if ex.name == text and ex.category == values[0]:
                exam = ex
                break
        if exam == None:
            raise RuntimeError(f"Something went wrong while fetching the exam {values[0]}-{text}")

        App_OverviewExam(theme=self.theme,
                         mode=self.mode,
                         exam=exam,
                         class_obj=self.class_obj,
                         usecommandlineargs=self.usecommandlineargs,
                         usethemeconfigfile=self.usethemeconfigfile
                         )



