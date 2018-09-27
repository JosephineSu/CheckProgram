# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AuditingMainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

import os,sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget,QFileDialog,QTableWidgetItem,QMainWindow
import pandas as pd


class Ui_MainWindow(QMainWindow):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")

        desktop = QtWidgets.QApplication.desktop()
        self.windowsWidth = desktop.width()
        self.windowsHeight = desktop.height()-200
        # MainWindow.resize(self.windowsWidth,self.windowsHeight -100)
        # MainWindow.resize(1366, 768)
        icon = QtGui.QIcon.fromTheme("审")
        MainWindow.setWindowIcon(icon)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tableList = QtWidgets.QListWidget(self.centralwidget)
        self.tableList.setGeometry(QtCore.QRect(10, 10, 300, 666))
        self.tableList.setObjectName("tableList")

        self.tableData = QtWidgets.QTableWidget(self.centralwidget)
        self.tableData.setGeometry(QtCore.QRect(312, 10, self.windowsWidth - 350, 666))
        self.tableData.setObjectName("tableData")
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 796, 30))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionimportFile = QtWidgets.QAction("导入文件", MainWindow,triggered=self.openFile)
        self.actionimportFile.setObjectName("actionimportFile")
        self.actionexportFile = QtWidgets.QAction(MainWindow)
        self.actionexportFile.setObjectName("actionexportFile")
        self.menu.addAction(self.actionimportFile)
        self.menu.addAction(self.actionexportFile)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())

        self.retranslateUi(MainWindow)

        screen = QDesktopWidget().screenGeometry()
        print(screen.width(), screen.height())
        # screen = QDesktopWidget.screenGeometry()
        MainWindow.resize(screen.width(), screen.height())
        MainWindow.move(0,0)
        # self.resize(800, 600)

        # self.fullScreen()
        # self.statusbar.messageChanged['QString'].connect(self.tableList.reset)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # self.connect(actionimportFile, SIGNAL("triggered()"), self.openFile)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "审核程序"))
        self.menu.setTitle(_translate("MainWindow", "文件"))
        self.menu_2.setTitle(_translate("MainWindow", "编辑"))
        self.menu_3.setTitle(_translate("MainWindow", "帮助"))
        # self.actionimportFile.setText(_translate("MainWindow", "导入文件"))
        self.actionexportFile.setText(_translate("MainWindow", "导出文件"))


    def fullScreen(self):
        screen = QDesktopWidget().screenGeometry()
        print(screen.width(), screen.height())
        # screen = QDesktopWidget.screenGeometry()
        self.resize(screen.width(), screen.height())
        self.move(0,0)


    def openFile(self):
        print("openFile")
        fileName1, filetype = QFileDialog.getOpenFileName(self,
                                                          "选取文件",
                                                          os.getcwd(),
                                                          "All Files (*);;Text Files (*.txt)")  # 设置文件扩展名过滤,注意用双分号间隔

        if fileName1 != None:
            self.tableList.addItem(fileName1)
            print(fileName1, filetype)

            try:
                df = pd.read_csv(fileName1,header=0,encoding='gbk')
                print('gbk')
                print(df.head())
                # 获取表头
                header = df.columns.values.tolist()  # [str(col) for col in df]
                print(len(header))
                print("df:", df, "type", type(df))
                print(header)
                # 获取表的行列数
                colCount = df.columns.size
                rowCount = df.iloc[:, 0].size
                # 设置表行数
                self.tableData.setRowCount(rowCount)
                # 设置表列数
                self.tableData.setColumnCount(colCount)
                self.tableData.clear()
                # 重新设置表头
                self.tableData.setHorizontalHeaderLabels(header)
                for r in range(rowCount):
                    for c in range(colCount):
                        item = df.iat[r, c]
                        print('set', r, c, "item:", item)
                        self.tableData.setItem(r, c, QTableWidgetItem(str(df.iat[r, c])))

            except:
                df = pd.read_csv(fileName1, header=0,encoding='utf-8')
                print('utf-8')


                # 获取表头
                header = df.columns.values.tolist() #[str(col) for col in df]
                print(len(header))
                print("df:",df,"type",type(df))
                print(header)
                # 获取表的行列数
                colCount = df.columns.size
                rowCount = df.iloc[:,0].size
                # 设置表行数
                self.tableData.setRowCount(rowCount)
                # 设置表列数
                self.tableData.setColumnCount(colCount)
                self.tableData.clear()
                # 重新设置表头
                self.tableData.setHorizontalHeaderLabels(header)
                for r in range(rowCount):
                    for c in range(colCount):
                        item = df.iat[r,c]
                        print('set',r,c,"item:",item)
                        self.tableData.setItem(r,c,QTableWidgetItem(str(df.iat[r,c])))


        def showTable(self):
            # 清空数据
            self.tableWidget.clear()
            # 重新设置表头
            self.tableWidget.setHorizontalHeaderLabels(
                ['编号', '姓名', '证件号', '航班号', '航班日期', '座位号', '登机口', '序号', '出发地', '目的地'])