"""
Demo of all widgets
"""

import TKinterModernThemes as TKMT
from functools import partial
import tkinter as tk
import json




def fun_print_hello():
    print("hello")

def fun_print_ciao():
    print("ciao")

def fun_action(first, last):
    print(f"some action {first} {last}")

class App_OverviewExam(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, student_first, student_last, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.label_frame = self.addLabelFrame("Class 2")
        self.label_frame.Label("This is some text for new class window")

        self.Label(f"Here I could put some more text, boxes, buttons etc.\n"
                   f"This maybe even works for texts containing the args given: {student_first} {student_last}")
        self.run()

class App(TKMT.ThemedTKinterFrame):
    def __init__(self, theme, mode, usecommandlineargs=True, usethemeconfigfile=True):
        super().__init__("TKinter Custom Themes Demo", theme, mode,
                         usecommandlineargs=usecommandlineargs, useconfigfile=usethemeconfigfile)

        self.label_frame = self.addLabelFrame("Section 1")
        self.label_frame.Label("This is some text")


        self.panedWindow1 = self.PanedWindow("Should be middle paned window")
        self.pane1 = self.panedWindow1.addWindow()
        self.panedWindow = self.PanedWindow("asdfasdf", rowspan=4)

        student_data = [
            {"firstname": "Nina", "lastname": "Matumona"},
            {"firstname": "Marlene", "lastname": "asdf"},
            {"firstname": "Nina", "lastname": "Kohler"},
            {"firstname": "Noe", "lastname": "Matumona"},
        ]
        self.pane1.treeview = self.pane1.Treeview(['Last name', 'First name'], [120,120], 10, student_data, 'subfiles', ['lastname', 'firstname'], openkey='open')
        self.pane1.treeview.bind("<<TreeviewSelect>>", self.on_treeview_select)

        self.nextCol()
        self.button_frame = self.addLabelFrame("Buttons")
        self.button_frame.Button("Some Button", fun_print_hello)
        self.button_frame.Button("Ohter Button", fun_print_ciao)

        self.pane3 = self.panedWindow.addWindow()
        self.pane3.Label(self.theme.capitalize() + " theme: " + self.mode)

        self.debugPrint()
        self.run()


    def on_treeview_select(self, event):
        item = self.pane1.treeview.focus()
        values = self.pane1.treeview.item(item)["values"]
        firstname = values[0]
        lastname = self.pane1.treeview.item(item)['text']
        fun_action(firstname, lastname)
        if item:
            # create a new themed frame with a label
            App_OverviewExam(self.theme, self.mode, firstname, lastname, usecommandlineargs=True, usethemeconfigfile=True)

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

if __name__ == '__main__':
    app = App("azure", "light")
    # app = App(input("Theme (azure / park / sun-valley): ").lower(), input("dark / light: ").lower())