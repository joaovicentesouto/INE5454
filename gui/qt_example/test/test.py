# This Python file uses the following encoding: utf-8
import sys
from PySide2.QtWidgets import QApplication, QMainWindow, QDialog
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from ui_dialog import Ui_Dialog

#class test(QMainWindow):
#    def __init__(self):
#        QMainWindow.__init__(self)

window = 0

def do_something():
    print("hello")
    window.my_label.setText("I SAY DON'T CLICK!")
    window.dialog.show()

if __name__ == "__main__":
    app = QApplication([])

    ui_file = QFile("/home/souto/code/qt/test/mainwindow.ui")
    ui_file.open(QFile.ReadOnly)

    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()

    window.dialog = Ui_Dialog()
    window.dialog.setupUi(QDialog())

    window.my_button.clicked.connect(do_something)

    window.show()

    sys.exit(app.exec_())
