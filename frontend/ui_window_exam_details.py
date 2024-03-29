# Form implementation generated from reading ui file 'ui/ui_window_exam_details.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_WindowExamDetails(object):
    def setupUi(self, WindowExamDetails):
        WindowExamDetails.setObjectName("WindowExamDetails")
        WindowExamDetails.resize(876, 768)
        self.centralwidget = QtWidgets.QWidget(parent=WindowExamDetails)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.input_examName = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.input_examName.setInputMask("")
        self.input_examName.setObjectName("input_examName")
        self.gridLayout.addWidget(self.input_examName, 0, 1, 1, 1)
        self.label_exam_cat = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_exam_cat.setObjectName("label_exam_cat")
        self.gridLayout.addWidget(self.label_exam_cat, 0, 2, 1, 1)
        self.input_examCategory = QtWidgets.QComboBox(parent=self.centralwidget)
        self.input_examCategory.setObjectName("input_examCategory")
        self.gridLayout.addWidget(self.input_examCategory, 0, 3, 1, 1)
        self.input_voluntary = QtWidgets.QComboBox(parent=self.centralwidget)
        self.input_voluntary.setObjectName("input_voluntary")
        self.gridLayout.addWidget(self.input_voluntary, 1, 3, 1, 1)
        self.label_voluntary = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_voluntary.setObjectName("label_voluntary")
        self.gridLayout.addWidget(self.label_voluntary, 1, 2, 1, 1)
        self.input_examType = QtWidgets.QComboBox(parent=self.centralwidget)
        self.input_examType.setObjectName("input_examType")
        self.gridLayout.addWidget(self.input_examType, 1, 1, 1, 1)
        self.label_exam_name = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_exam_name.setObjectName("label_exam_name")
        self.gridLayout.addWidget(self.label_exam_name, 0, 0, 1, 1)
        self.label_exam_type = QtWidgets.QLabel(parent=self.centralwidget)
        self.label_exam_type.setObjectName("label_exam_type")
        self.gridLayout.addWidget(self.label_exam_type, 1, 0, 1, 1)
        self.table_points_grades = QtWidgets.QTableWidget(parent=self.centralwidget)
        self.table_points_grades.setObjectName("table_points_grades")
        self.table_points_grades.setColumnCount(4)
        self.table_points_grades.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.table_points_grades.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_points_grades.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_points_grades.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_points_grades.setHorizontalHeaderItem(3, item)
        self.gridLayout.addWidget(self.table_points_grades, 2, 0, 1, 4)
        self.button_export_excel = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_export_excel.setObjectName("button_export_excel")
        self.gridLayout.addWidget(self.button_export_excel, 3, 0, 1, 2)
        self.button_generateReport = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_generateReport.setObjectName("button_generateReport")
        self.gridLayout.addWidget(self.button_generateReport, 3, 2, 1, 2)
        WindowExamDetails.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=WindowExamDetails)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 876, 30))
        self.menubar.setObjectName("menubar")
        WindowExamDetails.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=WindowExamDetails)
        self.statusbar.setObjectName("statusbar")
        WindowExamDetails.setStatusBar(self.statusbar)

        self.retranslateUi(WindowExamDetails)
        QtCore.QMetaObject.connectSlotsByName(WindowExamDetails)

    def retranslateUi(self, WindowExamDetails):
        _translate = QtCore.QCoreApplication.translate
        WindowExamDetails.setWindowTitle(_translate("WindowExamDetails", "Exam Details"))
        self.input_examName.setText(_translate("WindowExamDetails", "<exam_name>"))
        self.label_exam_cat.setText(_translate("WindowExamDetails", "Exam Category"))
        self.label_voluntary.setText(_translate("WindowExamDetails", "Voluntary"))
        self.label_exam_name.setText(_translate("WindowExamDetails", "Exam Name"))
        self.label_exam_type.setText(_translate("WindowExamDetails", "Computation Strategy"))
        item = self.table_points_grades.horizontalHeaderItem(0)
        item.setText(_translate("WindowExamDetails", "Lastname"))
        item = self.table_points_grades.horizontalHeaderItem(1)
        item.setText(_translate("WindowExamDetails", "Firstname"))
        item = self.table_points_grades.horizontalHeaderItem(2)
        item.setText(_translate("WindowExamDetails", "Points"))
        item = self.table_points_grades.horizontalHeaderItem(3)
        item.setText(_translate("WindowExamDetails", "Grades"))
        self.button_export_excel.setText(_translate("WindowExamDetails", "Export Exam as .xlsx"))
        self.button_generateReport.setText(_translate("WindowExamDetails", "Generate Exam Report"))
