# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainMenu.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!
from userlist import Ui_UserList
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtWidgets
import SQLconnect
class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(254, 300)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 221, 16))
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(60, 140, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.popUserlist)

        self.retranslateUi(Dialog)
        self
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Manager"))
        self.label.setText(_translate("Dialog", "Shanghai Stock Exchange"))
        self.pushButton.setText(_translate("Dialog", "User Database"))

    def popUserlist(self):
        window = QDialog()
        ui = Ui_UserList()
        ui.setupUi(window)
        list = SQLconnect.getdb().get_user_name()
        for x in range(0,len(list)):
            ui.listWidget.addItem(str(list[x][0])+ " " + list[x][1] + " " + list[x][2])
        window.exec_()







