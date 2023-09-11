from PyQt6.QtWidgets import QMainWindow

from backend.exam import Exam
from frontend.ui_window_exam_details import Ui_WindowExamDetails
from ui_window_class_detail import  Ui_WindowClassDetail

class WindowExamDetail(QMainWindow, Ui_WindowExamDetails):

    # TODO dynamically add some of the buttons (based on the exam type, e.g. max points, ...)

    def __init__(self, exam: Exam, parent=None):

        # initialize all GUI elements based on information from .ui file (compiled to python using pyuic6)
        super().__init__(parent)

        print(f"[WINDOW EXAM DETAIL] got here with {exam} {exam.grades}")

        self.setupUi(self)

        # TODO show data in tableview to see how it behaves

