
import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import sys
import json
sys.path.append("/home/marcesch/privat/Selina/Notenuebersicht/backend/")
from backend.overview import Overview
from backend.classes import Class
from gui_overview_single_class import App_OverviewClass


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

        # TODO fix folderpaths!!! they are not correct anymore as I moved stuff to backend and gui folders
        self.ov = Overview()
        self.ov.folderpath = "/home/marcesch/noten/tmp/klassen"
        # TODO use that instead of testing init function
        self.ov.load_classes()
        # for class_obj in self.ov.classes:
        #     print(f"name:  {class_obj.filename_base_exam[1:]}")
        #     self.ov.load_categories_and_exams(class_obj)
        # self.initialize_dummy_classes()

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