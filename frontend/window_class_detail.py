# Form implementation generated from reading ui file 'window_class_detail.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_WindowClassDetail(object):
    def setupUi(self, WindowClassDetail):
        WindowClassDetail.setObjectName("WindowClassDetail")
        WindowClassDetail.resize(782, 747)
        self.centralwidget = QtWidgets.QWidget(parent=WindowClassDetail)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.treeWidget = QtWidgets.QTreeWidget(parent=self.centralwidget)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.verticalLayout_4.addWidget(self.treeWidget)
        self.button_studentDetails = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_studentDetails.setEnabled(False)
        self.button_studentDetails.setObjectName("button_studentDetails")
        self.verticalLayout_4.addWidget(self.button_studentDetails)
        self.button_addStudents = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_addStudents.setEnabled(True)
        self.button_addStudents.setObjectName("button_addStudents")
        self.verticalLayout_4.addWidget(self.button_addStudents)
        self.button_removeStudent = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_removeStudent.setEnabled(False)
        self.button_removeStudent.setObjectName("button_removeStudent")
        self.verticalLayout_4.addWidget(self.button_removeStudent)
        self.verticalLayout_2.addLayout(self.verticalLayout_4)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.label_3 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_5.addWidget(self.label_3)
        self.treeWidget_2 = QtWidgets.QTreeWidget(parent=self.centralwidget)
        self.treeWidget_2.setObjectName("treeWidget_2")
        self.treeWidget_2.headerItem().setText(0, "1")
        self.verticalLayout_5.addWidget(self.treeWidget_2)
        self.button_examDetails = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_examDetails.setEnabled(False)
        self.button_examDetails.setObjectName("button_examDetails")
        self.verticalLayout_5.addWidget(self.button_examDetails)
        self.button_addExam = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_addExam.setObjectName("button_addExam")
        self.verticalLayout_5.addWidget(self.button_addExam)
        self.button_generateExamReport = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_generateExamReport.setEnabled(False)
        self.button_generateExamReport.setObjectName("button_generateExamReport")
        self.verticalLayout_5.addWidget(self.button_generateExamReport)
        self.button_deleteExam = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_deleteExam.setEnabled(False)
        self.button_deleteExam.setObjectName("button_deleteExam")
        self.verticalLayout_5.addWidget(self.button_deleteExam)
        self.horizontalLayout_4.addLayout(self.verticalLayout_5)
        self.horizontalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_4 = QtWidgets.QLabel(parent=self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_6.addWidget(self.label_4)
        self.treeWidget_3 = QtWidgets.QTreeWidget(parent=self.centralwidget)
        self.treeWidget_3.setObjectName("treeWidget_3")
        self.treeWidget_3.headerItem().setText(0, "1")
        self.verticalLayout_6.addWidget(self.treeWidget_3)
        self.button_detailsCategory = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_detailsCategory.setEnabled(False)
        self.button_detailsCategory.setObjectName("button_detailsCategory")
        self.verticalLayout_6.addWidget(self.button_detailsCategory)
        self.button_addCategory = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_addCategory.setObjectName("button_addCategory")
        self.verticalLayout_6.addWidget(self.button_addCategory)
        self.button_deleteCategory = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_deleteCategory.setEnabled(False)
        self.button_deleteCategory.setObjectName("button_deleteCategory")
        self.verticalLayout_6.addWidget(self.button_deleteCategory)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_6.addItem(spacerItem)
        self.button_generateClassReport = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_generateClassReport.setEnabled(False)
        self.button_generateClassReport.setObjectName("button_generateClassReport")
        self.verticalLayout_6.addWidget(self.button_generateClassReport)
        self.button_deleteClass = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_deleteClass.setObjectName("button_deleteClass")
        self.verticalLayout_6.addWidget(self.button_deleteClass)
        self.horizontalLayout_3.addLayout(self.verticalLayout_6)
        self.horizontalLayout.addLayout(self.horizontalLayout_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)
        WindowClassDetail.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=WindowClassDetail)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 782, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        WindowClassDetail.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=WindowClassDetail)
        self.statusbar.setObjectName("statusbar")
        WindowClassDetail.setStatusBar(self.statusbar)
        self.actionUndo = QtGui.QAction(parent=WindowClassDetail)
        self.actionUndo.setObjectName("actionUndo")
        self.actionRedo = QtGui.QAction(parent=WindowClassDetail)
        self.actionRedo.setObjectName("actionRedo")
        self.actionSave_on_Disk = QtGui.QAction(parent=WindowClassDetail)
        self.actionSave_on_Disk.setObjectName("actionSave_on_Disk")
        self.actionGenerate_Semester_Reporr = QtGui.QAction(parent=WindowClassDetail)
        self.actionGenerate_Semester_Reporr.setObjectName("actionGenerate_Semester_Reporr")
        self.actionDelete_Class = QtGui.QAction(parent=WindowClassDetail)
        self.actionDelete_Class.setObjectName("actionDelete_Class")
        self.actionOpen_Tutorial = QtGui.QAction(parent=WindowClassDetail)
        self.actionOpen_Tutorial.setObjectName("actionOpen_Tutorial")
        self.menuFile.addAction(self.actionSave_on_Disk)
        self.menuFile.addAction(self.actionGenerate_Semester_Reporr)
        self.menuFile.addAction(self.actionDelete_Class)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuHelp.addAction(self.actionOpen_Tutorial)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(WindowClassDetail)
        QtCore.QMetaObject.connectSlotsByName(WindowClassDetail)

    def retranslateUi(self, WindowClassDetail):
        _translate = QtCore.QCoreApplication.translate
        WindowClassDetail.setWindowTitle(_translate("WindowClassDetail", "MainWindow"))
        self.label_2.setText(_translate("WindowClassDetail", "Students"))
        self.button_studentDetails.setText(_translate("WindowClassDetail", "Details"))
        self.button_addStudents.setText(_translate("WindowClassDetail", "Add Students"))
        self.button_removeStudent.setText(_translate("WindowClassDetail", "Remove Student"))
        self.label_3.setText(_translate("WindowClassDetail", "Exams"))
        self.button_examDetails.setText(_translate("WindowClassDetail", "Details"))
        self.button_addExam.setText(_translate("WindowClassDetail", "Add Exam"))
        self.button_generateExamReport.setText(_translate("WindowClassDetail", "Generate Exam Report"))
        self.button_deleteExam.setText(_translate("WindowClassDetail", "Delete Exam"))
        self.label_4.setText(_translate("WindowClassDetail", "Categories"))
        self.button_detailsCategory.setText(_translate("WindowClassDetail", "Details"))
        self.button_addCategory.setText(_translate("WindowClassDetail", "Add Category"))
        self.button_deleteCategory.setText(_translate("WindowClassDetail", "Delete Category"))
        self.button_generateClassReport.setText(_translate("WindowClassDetail", "Generate Semester Report"))
        self.button_deleteClass.setText(_translate("WindowClassDetail", "Delete Class"))
        self.menuFile.setTitle(_translate("WindowClassDetail", "File"))
        self.menuEdit.setTitle(_translate("WindowClassDetail", "Edit"))
        self.menuHelp.setTitle(_translate("WindowClassDetail", "Help"))
        self.actionUndo.setText(_translate("WindowClassDetail", "Undo"))
        self.actionUndo.setShortcut(_translate("WindowClassDetail", "Ctrl+Z"))
        self.actionRedo.setText(_translate("WindowClassDetail", "Redo"))
        self.actionRedo.setShortcut(_translate("WindowClassDetail", "Ctrl+Y"))
        self.actionSave_on_Disk.setText(_translate("WindowClassDetail", "Save on Disk"))
        self.actionSave_on_Disk.setShortcut(_translate("WindowClassDetail", "Ctrl+S"))
        self.actionGenerate_Semester_Reporr.setText(_translate("WindowClassDetail", "Generate Semester Report"))
        self.actionGenerate_Semester_Reporr.setShortcut(_translate("WindowClassDetail", "Ctrl+R"))
        self.actionDelete_Class.setText(_translate("WindowClassDetail", "Delete Class"))
        self.actionOpen_Tutorial.setText(_translate("WindowClassDetail", "Open Tutorial"))
