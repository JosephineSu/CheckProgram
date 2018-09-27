import sys
import widgetsLayout
from PyQt5.QtWidgets import QApplication, QMainWindow

if __name__ == '__main__':
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = widgetsLayout.Ui_Form()
    ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
    # sys.exit()
