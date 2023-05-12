import TKinterModernThemes as TKMT
import tkinter as tk
from tkinter import ttk


classes = [
    {'name': 'Mathematics', 'year': 2021, 'term': 'Spring'},
    {'name': 'Computer Science', 'year': 2020, 'term': 'Fall'},
    {'name': 'History', 'year': 2022, 'term': 'Summer'},
    {'name': 'Chemistry', 'year': 2023, 'term': 'Winter'}
]



def buttonCMD():
    print("Button clicked!")


class App(TKMT.ThemedTKinterFrame):
    def __init__(self):
        super().__init__(str("TITLE"), str("azure"), str("light"))

        root = tk.Tk()
        root.title('Overview')
        root.geometry('800x600')

        self.button_frame = self.addLabelFrame(str("Frame Label"))
        self.button_frame.Button(str("Button Text"), buttonCMD)  # the button is dropped straight into the frame
        self.run()


App()