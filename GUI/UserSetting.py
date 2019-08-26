# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UserSetting.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from addSec import Ui_Dialog as Ui_addSec
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtWidgets
import SQLconnect


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(490, 426)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(50, 30, 81, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(40, 120, 141, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(240, 120, 104, 26))
        self.comboBox.setObjectName("comboBox")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(360, 370, 113, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(Dialog.close)

        self.textEdit_2 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_2.setGeometry(QtCore.QRect(140, 30, 104, 21))
        self.textEdit_2.setObjectName("textEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(360, 120, 61, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.popaddSec)

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(40, 170, 81, 16))
        self.label_3.setObjectName("label_3")
        self.textEdit_3 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_3.setGeometry(QtCore.QRect(240, 170, 104, 21))
        self.textEdit_3.setObjectName("textEdit_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(40, 230, 81, 16))
        self.label_4.setObjectName("label_4")
        self.textEdit_4 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_4.setGeometry(QtCore.QRect(240, 230, 104, 21))
        self.textEdit_4.setPlaceholderText("")
        self.textEdit_4.setObjectName("textEdit_4")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(220, 370, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.editSave)

        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(420, 120, 61, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(40, 290, 60, 16))
        self.label_5.setObjectName("label_5")
        self.textEdit_5 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_5.setGeometry(QtCore.QRect(240, 290, 104, 21))
        self.textEdit_5.setPlaceholderText("")
        self.textEdit_5.setObjectName("textEdit_5")
        self.textEdit_6 = QtWidgets.QTextEdit(Dialog)
        self.textEdit_6.setGeometry(QtCore.QRect(360, 30, 104, 21))
        self.textEdit_6.setObjectName("textEdit_6")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(270, 30, 81, 16))
        self.label_6.setObjectName("label_6")
        self.checkBox = QtWidgets.QCheckBox(Dialog)
        self.checkBox.setGeometry(QtCore.QRect(50, 80, 87, 20))
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(Dialog)
        self.checkBox_2.setGeometry(QtCore.QRect(140, 80, 87, 20))
        self.checkBox_2.setObjectName("checkBox_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Setting"))
        self.label.setText(_translate("Dialog", "First Name"))
        self.label_2.setText(_translate("Dialog", "Subscribed Securities"))
        self.pushButton.setText(_translate("Dialog", "Close"))
        self.pushButton_2.setText(_translate("Dialog", "Add"))
        self.label_3.setText(_translate("Dialog", "Email"))
        self.label_4.setText(_translate("Dialog", "Wechat"))
        self.pushButton_3.setText(_translate("Dialog", "Apply Change"))
        self.pushButton_4.setText(_translate("Dialog", "Edit"))
        self.label_5.setText(_translate("Dialog", "UserID"))
        self.label_6.setText(_translate("Dialog", "Last Name"))
        self.checkBox.setText(_translate("Dialog", "Male"))
        self.checkBox_2.setText(_translate("Dialog", "Female"))


    def editSave(self):
        userfirstname = self.textEdit_2.toPlainText()
        userlastname = self.textEdit_6.toPlainText()
        gender = 0
        if self.checkBox.isChecked():
            gender =1
        useremail =self.textEdit_3.toPlainText()
        userwechat = self.textEdit_4.toPlainText()
        userUserID = int(self.textEdit_5.toPlainText())
        db = SQLconnect.getdb()
        try:
            db.insert_user(userUserID, userfirstname, userlastname, gender, '', userwechat, useremail, 0)
        except:
            print("Inserst Failed")


    def popaddSec(self):
        window = QDialog()
        ui = Ui_addSec()
        ui.setupUi(window)
        window.exec_()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
