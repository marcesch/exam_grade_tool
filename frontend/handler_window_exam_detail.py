from PyQt6.QtWidgets import QMainWindow

from frontend.window_exam_details import Ui_WindowExamDetails
from window_class_detail import  Ui_WindowClassDetail

# TODO maybe change QMainWindow -> QApplicationWindow
class WindowExamDetail(QMainWindow, Ui_WindowExamDetails):

    def __init__(self, parent=None):

        # initialize all GUI elements based on information from .ui file (compiled to python using pyuic6)
        super().__init__(parent)


        self.setupUi(self)

