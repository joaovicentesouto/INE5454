# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui',
# licensing of 'dialog.ui' applies.
#
# Created: Mon Nov 18 08:36:41 2019
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCore import QObject, Signal, Slot

class Ui_Dialog(QObject):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self._buttons = QtWidgets.QDialogButtonBox(Dialog)
        self._buttons.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self._buttons.setOrientation(QtCore.Qt.Horizontal)
        self._buttons.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self._buttons.setObjectName("_buttons")
        self._label = QtWidgets.QLabel(Dialog)
        self._label.setGeometry(QtCore.QRect(150, 110, 54, 17))
        self._label.setObjectName("_label")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self._buttons, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self._buttons, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self._buttons.accepted.connect(self.acc)
        self._buttons.rejected.connect(self.rej)

        self.dialog = Dialog

        self.test = 0

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self._label.setText(QtWidgets.QApplication.translate("Dialog", "Testando", None, -1))

    def acc(self):
        self._label.setText("Acertou")

    def rej(self):
        self._label.setText("Errou")

    def show(self):
        self.dialog.show()

