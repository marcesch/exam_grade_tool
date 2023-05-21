from tkinter import BOTH

import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import sys
import json

from tkintertable import TableCanvas
from tkintertable.Testing import sampledata

sys.path.append("/home/marcesch/privat/Selina/Notenuebersicht/backend/")
from backend.overview import Overview
from backend.classes import Class
from backend.exam import Exam


class App_OverviewExam(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, exam, class_obj, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__(f"Übersicht Prüfung {exam.name}", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.exam: Exam = exam
        self.class_obj = class_obj

        self.panedWindow1 = self.PanedWindow(f"")
        self.pane1 = self.panedWindow1.addWindow()
        self.pane1.label_frame = self.pane1.addLabelFrame(f"Übersicht Prüfung {exam.name}")
        text_description = "Hier können Prüfungsresultate angepasst werden. Standardmässig werden Noten basierend von Punkten berechnet, man kann die Note aber auch direkt eintragen."
        width = 800
        self.pane1.label_frame.Text(text_description, widgetkwargs={"wraplength": width})

        self.create_header_fields()
        self.create_overview_grades()

        self.run()

    def create_header_fields(self):
        """
        Prints header stuff like:
        - max points
        - grading type
        - ...
        :return:
        """

        self.pane1.button_frame = self.pane1.addLabelFrame("Allgemeine Daten")

        row = 0
        self.pane1.button_frame.Text("Prüfungsname", row=row, col=0)
        self.pane1.textinputvar = tk.StringVar(value=f"{self.exam.name}")
        self.pane1.textinputvar.trace_add('write', self.update_exam_name)
        self.pane1.button_frame.Entry(self.pane1.textinputvar, validatecommand=self.validate_exam_name, row=row, col=1)
        self.pane1.button_frame.Text("Berechnungsmodus", row=row, col=2)
        options_grade_comp = self.exam.computation_strategies
        default_option = tk.StringVar(value="linear")
        self.pane1.button_frame.OptionMenu(options_grade_comp, default_option, lambda x: print(f"Menu {x}"), row=row, col=3)

        row = 1
        self.pane1.button_frame.Text("Maximale Punktezahl", row=row, col=0)
        self.pane1.textin_punktezahl = tk.StringVar(value=f"Max. Punktezahl")
        self.pane1.textin_punktezahl.trace_add('write', self.update_max_points)
        self.pane1.button_frame.Entry(self.pane1.textin_punktezahl, validatecommand=self.validate_pts, row=row, col=1)
        self.pane1.button_frame.Text("Punkte für 6", row=row, col=2)
        self.pane1.textin_punkteFuer6 = tk.StringVar(value=f"Punkte für 6")
        self.pane1.textin_punkteFuer6.trace_add('write', self.update_pts_for_max)
        self.pane1.button_frame.Entry(self.pane1.textin_punkteFuer6, validatecommand=self.validate_pts, row=row, col=3)


    def create_overview_grades(self):
        """
        Main functionality of this window -- allows modifying exam grades, ...

        :return:
        """

        self.pane1.base_frame = self.addFrame("table-frame")
        self.pane1.table_frame = tk.Frame(self.pane1.base_frame.master)
        self.pane1.table_frame.pack(fill=BOTH, expand=1)
        table = TableCanvas(self.pane1.table_frame, data=sampledata())
        table.show()

    def update_pts_for_max(self):
        """
        Updates points needed for 6
        :return:
        """
        return

    def validate_pts(self, text):
        """
        Validates whether given input is valid point -- basically checks if ints
        :return:
        """
        try:
            num = float(text)
            if num >= 0:
                return True
            return False
        except:
            return False

    def update_max_points(self):
        """
        Updates max_points of exam
        :return:
        """

        return

    def validate_exam_name(self, text):
        """
        Here I could probably do something that checks input
        :return:
        """
        # TODO add checks on name (no weird shitty characters)
        return True

    def update_exam_name(self):
        """
        Updates examname based on entered text
        :return:
        """
        user_input = self.textinputvar.get()
        print(user_input)
        if user_input != "":
            self.exam.rename(user_input)










