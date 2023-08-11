from PyQt6.QtWidgets import QMainWindow
from window_class_detail import  Ui_WindowClassDetail

# TODO maybe change QMainWindow -> QApplicationWindow
class WindowClassDetail(QMainWindow, Ui_WindowClassDetail):

    def __init__(self, class_obj, parent=None):

        # TODO alter things here

        # initialize all GUI elements based on information from .ui file (compiled to python using pyuic6)
        super().__init__(parent)

        self.class_obj = class_obj
        print(class_obj)

        self.window_classDetail = None

        self.setupUi(self)

