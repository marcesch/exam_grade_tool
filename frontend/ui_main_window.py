# Form implementation generated from reading ui file 'ui/ui_main_window.ui'
#
# Created by: PyQt6 UI code generator 6.5.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(692, 572)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        MainWindow.setMouseTracking(False)
        MainWindow.setWindowOpacity(1.0)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.default_tab = QtWidgets.QWidget()
        self.default_tab.setObjectName("default_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.default_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtWidgets.QLabel(parent=self.default_tab)
        font = QtGui.QFont()
        font.setItalic(True)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.tabWidget.addTab(self.default_tab, "")
        self.remove_tab = QtWidgets.QWidget()
        self.remove_tab.setEnabled(True)
        self.remove_tab.setObjectName("remove_tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.remove_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget = QtWidgets.QTreeWidget(parent=self.remove_tab)
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.gridLayout_2.addWidget(self.treeWidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.remove_tab, "")
        self.horizontalLayout.addWidget(self.tabWidget)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.button_details = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_details.setEnabled(False)
        self.button_details.setObjectName("button_details")
        self.verticalLayout_2.addWidget(self.button_details)
        self.button_addClass = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_addClass.setObjectName("button_addClass")
        self.verticalLayout_2.addWidget(self.button_addClass)
        self.button_deleteClass = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_deleteClass.setEnabled(False)
        self.button_deleteClass.setObjectName("button_deleteClass")
        self.verticalLayout_2.addWidget(self.button_deleteClass)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.button_saveDB = QtWidgets.QPushButton(parent=self.centralwidget)
        self.button_saveDB.setObjectName("button_saveDB")
        self.verticalLayout_2.addWidget(self.button_saveDB)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.IBeamCursor))
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(QtCore.Qt.TextInteractionFlag.LinksAccessibleByMouse|QtCore.Qt.TextInteractionFlag.TextSelectableByMouse)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 692, 30))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(parent=self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(parent=self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_newDB = QtGui.QAction(parent=MainWindow)
        self.action_newDB.setObjectName("action_newDB")
        self.action_openDB = QtGui.QAction(parent=MainWindow)
        self.action_openDB.setObjectName("action_openDB")
        self.actionOption_1 = QtGui.QAction(parent=MainWindow)
        self.actionOption_1.setObjectName("actionOption_1")
        self.action_save = QtGui.QAction(parent=MainWindow)
        self.action_save.setObjectName("action_save")
        self.action_changeLocation = QtGui.QAction(parent=MainWindow)
        self.action_changeLocation.setObjectName("action_changeLocation")
        self.action_undo = QtGui.QAction(parent=MainWindow)
        self.action_undo.setObjectName("action_undo")
        self.action_redo = QtGui.QAction(parent=MainWindow)
        self.action_redo.setObjectName("action_redo")
        self.action_openTutorial = QtGui.QAction(parent=MainWindow)
        self.action_openTutorial.setObjectName("action_openTutorial")
        self.action_restoreData = QtGui.QAction(parent=MainWindow)
        self.action_restoreData.setObjectName("action_restoreData")
        self.action_cleanTrash = QtGui.QAction(parent=MainWindow)
        self.action_cleanTrash.setObjectName("action_cleanTrash")
        self.actionImport_From_Excel = QtGui.QAction(parent=MainWindow)
        self.actionImport_From_Excel.setObjectName("actionImport_From_Excel")
        self.menuFile.addAction(self.action_save)
        self.menuFile.addAction(self.actionImport_From_Excel)
        self.menuFile.addSeparator()
        self.menuEdit.addAction(self.action_undo)
        self.menuEdit.addAction(self.action_redo)
        self.menuHelp.addAction(self.action_openTutorial)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tool for Grade Calucation"))
        self.label_2.setText(_translate("MainWindow", "(you first need to create classes, using the Add Class button to the right. If you don\'t find your previously created classes, try \"Change Location of DB\" and select the folder where you have stored the exams the last time)."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.default_tab), _translate("MainWindow", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.remove_tab), _translate("MainWindow", "Tab 2"))
        self.button_details.setText(_translate("MainWindow", "Details"))
        self.button_addClass.setText(_translate("MainWindow", "Add Class"))
        self.button_deleteClass.setText(_translate("MainWindow", "Delete Class"))
        self.button_saveDB.setText(_translate("MainWindow", "Save Database"))
        self.label.setText(_translate("MainWindow", "Some text can come here, like a description of the program or so. I\'ll have to figure out line breaks or text wrapping, because this way it looks shitty."))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.action_newDB.setText(_translate("MainWindow", "New Database"))
        self.action_newDB.setToolTip(_translate("MainWindow", "Create New Database"))
        self.action_newDB.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.action_openDB.setText(_translate("MainWindow", "Open Database"))
        self.action_openDB.setToolTip(_translate("MainWindow", "Open Existing Database"))
        self.action_openDB.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionOption_1.setText(_translate("MainWindow", "Option 1"))
        self.action_save.setText(_translate("MainWindow", "Save on Disk"))
        self.action_save.setToolTip(_translate("MainWindow", "Save DB on Disk"))
        self.action_save.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.action_changeLocation.setText(_translate("MainWindow", "Change Location"))
        self.action_undo.setText(_translate("MainWindow", "Undo"))
        self.action_undo.setShortcut(_translate("MainWindow", "Ctrl+Z"))
        self.action_redo.setText(_translate("MainWindow", "Redo"))
        self.action_redo.setShortcut(_translate("MainWindow", "Ctrl+Y"))
        self.action_openTutorial.setText(_translate("MainWindow", "Open Tutorial"))
        self.action_restoreData.setText(_translate("MainWindow", "Restore Data"))
        self.action_cleanTrash.setText(_translate("MainWindow", "Clean Trash"))
        self.actionImport_From_Excel.setText(_translate("MainWindow", "Import From Excel"))
