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



class App_OverviewExam(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, exam, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__(f"Übersicht Prüfung {exam.name}", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.exam: Exam = exam
        self.label_frame = self.addLabelFrame(f"Übersicht Prüfung {exam.name}")
        self.label_frame.Text("Some text here")

        self.run()

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
        Has fields name
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

        raise NotImplementedError

    def on_click_exam(self, event):
        """
        Opens details on exam, allowing user to add grades etc.
        => How to change cat?? -- need to:
        1. remove exam from old_cat.exams()
        2. add exam to new_cat.exams()
        3. change category-field of exam
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
                         usecommandlineargs=self.usecommandlineargs,
                         usethemeconfigfile=self.usethemeconfigfile
                         )






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

        self.label_frame = self.addLabelFrame("Tool zur Notenberechnung")
        text1 = f"Mit dieser Anwendung lassen sich Noten von verschiedenen Klassen automatisch berechnen. Im Grunde ist das Ganze ein glorifiziertes Excel-Dokument, welches auch ohne hohe Technikkenntnisse verwendbar sein sollte."
        text2 = f"Unten aufgeführt sind alle Klassen, die die Anwendung am Speicherort gefunden hat.\nWICHTIG: Falls eine Klasse nicht erscheint, wurde sie vermutlich manuell als File erstellt oder man hat die Dateinamen der Dokumente geändert. In dem Fall kann der gleiche Stand wie beim letzten Ausführen wiederhergestellt werden durch Drücken des Knopfes \"Hard Reset\""
        text3 = f"Alle Dokumente sind gespeichert in {self.ov.folderpath}"

        width = 800
        self.label_frame.Text(text1, widgetkwargs={"wraplength": width})
        self.label_frame.Text(text2, widgetkwargs={"wraplength": width})
        self.label_frame.Text(text3, widgetkwargs={"wraplength": width})

        self.panedWindow1 = self.PanedWindow("")
        self.pane1 = self.panedWindow1.addWindow()

        self.create_tabs()
        self.create_utility_bar()

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
        class6a.add_category({"name": "voci", "weight": 0.5})
        for i, cat in enumerate(class6a.categories):
            if i == 0:
                class6a.add_exam("orale", cat.name, 6)
            if i == 1:
                class6a.add_exam("grammaire1", cat.name, 23, 20)
                class6a.add_exam("grammaire2", cat.name, 25)
            if i == 2:
                class6a.add_exam("voci1", cat.name, 15)
                class6a.add_exam("voci2", cat.name, 15)
                class6a.add_exam("voci2", cat.name, 15)



        self.ov.classes.append(Class("3b", "FS", 2021))
        self.ov.classes.append(Class("4b", "HS", 2021))
        self.ov.classes.append(Class("4x", "HS", 2021))
        self.ov.classes.append(Class("1s", "HS", 2021))
        self.ov.classes.append(Class("2s", "FS", 2022))
        self.ov.classes.append(Class("5b", "FS", 2022))
        self.ov.classes.append(Class("3b", "FS", 2015))

    def create_utility_bar(self):
        """
        Shows some buttons to the right
        :return:
        """

        self.pane1.nextCol()
        self.button_frame = self.pane1.addLabelFrame("Aktionen")
        self.button_frame.Button("Speicherort ändern", self.change_base_location)
        self.button_frame.Button("Elemente wiederherstellen", self.restore_elements)
        self.button_frame.Button("Mülleimer permanent löschen", self.free_storage)
        self.button_frame.Button("Hard Reset", self.hard_reset)

    def create_tabs(self):
        """
        Creates the tabs for the last 4 semesters, if possible.
        :return:
        """
        self.notebook = self.pane1.Notebook("")
        newest_semesters = self.ov.return_newest_classes(4)
        self.tabs = []

        for sem in newest_semesters:
            tabs_curr_sem = self.notebook.addTab(f"{sem[0]} {sem[1]}")
            tabs_curr_sem.Label(f"{sem[0]}-{sem[1]}")
            self.tabs.append(tabs_curr_sem)

        for tab in self.tabs:
            self.create_classes_window(tab)

    def create_classes_window(self, tab):
        """
        Prints details of all classes for the current tab
        :return:
        """
        term, year = (tab.name).split(" ")[-2:]
        classes = self.ov.fetch_classes(term, year)
        class_data = []

        for class_obj in classes:
            class_data.append({"name": class_obj.name, 'year': class_obj.term, 'term': class_obj.year})

        tab.treeview = tab.Treeview(['Klassenname', 'Semester', 'Jahr'], [120, 120, 120], 10, class_data, 'subfiles',
                                    ['name', 'term', 'year'], openkey='open')
        tab.treeview.bind("<Double-1>", self.on_treeview_select)

        tab.Button("Details", self.selectItem_class_details)
        tab.Button("Klasse hinzufügen", self.add_class)
        tab.Button("Klasse löschen", self.selectItem_class_deletion)

    def selectItem_class_details(self):
        """
        Handles click on details for selected exam
        :return:
        """
        raise NotImplementedError

    def selectItem_class_deletion(self):
        """
        Handles click on Klasse löschen for selected class
        :return:
        """
        raise NotImplementedError

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

    def hard_reset(self):
        """
        panic mode if no files are found -> takes files from hidden storage location instead if user screwed with the names of files etc.

        :return:
        """
        raise NotImplementedError

    def change_base_location(self):
        """
        Handles press on change location -> moves all files to new location
        :return:
        """
        raise NotImplementedError

    def restore_elements(self):
        """
        Searches through the trash folder and allows moving deleted stuff back to user-space
        :return:
        """
        raise NotImplementedError

    def free_storage(self):
        """
        Deletes all files from the trash folder to free space
        :return:
        """
        raise NotImplementedError

def startup_process():
    print("Somewhere here I could start initializing all classes, .. loaded from disk => use that in memory (presumably reasonably small amount of data) and load from disk only once ")

def load_config():
    """
    Loads config info from files, most notably the theme
    :return:
    """

    theme = "azure"
    mode = "light"
    return theme, mode


if __name__ == '__main__':
    theme, mode = load_config()
    startup_process()
    app = App_OverviewClasses(theme, mode)
    # app = App(input("Theme (azure / park / sun-valley): ").lower(), input("dark / light: ").lower())