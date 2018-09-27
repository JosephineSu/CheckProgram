# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    # def __init__(self,MainWindow):
    #     super(MainWindow, self).__init__()
    #     # self.setupUi()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1084, 808)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(40, 510, 301, 131))
        self.label.setText("")
        self.label.setObjectName("label")
        self.openFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.openFileButton.setGeometry(QtCore.QRect(0, 0, 112, 34))
        self.openFileButton.setObjectName("openFileButton")
        self.tableView = QtWidgets.QTableView(self.centralwidget)
        self.tableView.setGeometry(QtCore.QRect(400, 80, 371, 491))
        self.tableView.setObjectName("tableView")
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(170, 0, 211, 41))
        self.toolButton.setObjectName("toolButton")
        self.listView = QtWidgets.QListView(self.centralwidget)
        self.listView.setGeometry(QtCore.QRect(50, 270, 256, 192))
        self.listView.setObjectName("listView")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(110, 350, 112, 34))
        self.pushButton_2.setObjectName("pushButton_2")
        self.buttonBox = QtWidgets.QDialogButtonBox(self.centralwidget)
        self.buttonBox.setGeometry(QtCore.QRect(90, 160, 233, 34))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(400, 0, 99, 24))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.tableView.raise_()
        self.label.raise_()
        self.openFileButton.raise_()
        self.toolButton.raise_()
        self.listView.raise_()
        self.pushButton_2.raise_()
        self.buttonBox.raise_()
        self.comboBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        # self.pushButton.clicked.connect(self.pushButton.click)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # 按钮点击事件
        self.openFileButton.clicked.connect(self.openFile)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle("审核程序") #_translate("MainWindow", "MainWindow")
        self.openFileButton.setText(_translate("MainWindow", "导入文件"))
        self.toolButton.setText(_translate("MainWindow", "文件"))
        self.pushButton_2.setText(_translate("MainWindow", "PushButton"))
        self.comboBox.setItemText(0, _translate("MainWindow", "导入文件"))
        self.comboBox.setItemText(1, _translate("MainWindow", "导出文件"))
        self.comboBox.setItemText(2, _translate("MainWindow", "审核"))

    def openFile(self):
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          "C:/",
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔
        print(fileName1, filetype)

