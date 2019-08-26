# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'userlist.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from UserSetting import Ui_Dialog as Ui_Setting
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore, QtWidgets
import SQLconnect


class Ui_UserList(object):
    def setupUi(self, UserList):
        UserList.setObjectName("UserList")
        UserList.resize(400, 300)
        self.listWidget = QtWidgets.QListWidget(UserList)
        self.listWidget.setGeometry(QtCore.QRect(60, 90, 256, 192))
        self.listWidget.setObjectName("listWidget")

        self.listWidget.itemDoubleClicked.connect(self.itempicked)
        self.splitter = QtWidgets.QSplitter(UserList)
        self.splitter.setGeometry(QtCore.QRect(50, 20, 341, 21))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.pushButton = QtWidgets.QPushButton(self.splitter)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.searchUser)
        self.textEdit = QtWidgets.QTextEdit(self.splitter)
        self.textEdit.setObjectName("textEdit")
        self.pushButton_2 = QtWidgets.QPushButton(UserList)
        self.pushButton_2.setGeometry(QtCore.QRect(50, 50, 85, 21))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.popEdit)
        self.pushButton_3 = QtWidgets.QPushButton(UserList)
        self.pushButton_3.setGeometry(QtCore.QRect(240, 50, 113, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.updateWidget)
        self.pushButton_4 = QtWidgets.QPushButton(UserList)
        self.pushButton_4.setGeometry(QtCore.QRect(140, 50, 85, 21))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.deleteUser)

        self.retranslateUi(UserList)
        QtCore.QMetaObject.connectSlotsByName(UserList)

    def deleteUser(self):
        x = self.listWidget.currentItem()
        if x != None:
            userId = int(x.text().split(" ")[0])
            try:
                db = SQLconnect.getdb().delete_user(user_id=userId)
            except:
                print("Unknown Error")
            self.updateWidget()


    def searchUser(self):
        userid = self.textEdit.toPlainText()
        db = SQLconnect.getdb()
        result = db.search_user(user_id=int(userid))
        if len(result) != 0:
            window = GISDialog()
            ui = Ui_Setting()
            ui.setupUi(window)
            data = result[0]
            ui.textEdit_2.setText(data[1])
            ui.textEdit_6.setText(data[3])
            ui.textEdit_3.setText(data[6])
            ui.textEdit_4.setText(data[5])
            ui.textEdit_5.setText(str(data[0]))
            sub = db.get_user_stock(int(userid))
            for i in range(0, len(sub)):
                ui.comboBox.addItem(str(sub[i][0]) + "-" + str(sub[i][1]))
            gender = data[4]
            if gender == 1:
                ui.checkBox.setChecked(True)
                ui.checkBox_2.setChecked(False)
            else:
                ui.checkBox.setChecked(False)
                ui.checkBox_2.setChecked(True)
            window.exec_()


    def retranslateUi(self, UserList):
        _translate = QtCore.QCoreApplication.translate
        UserList.setWindowTitle(_translate("UserList", "User List"))
        self.pushButton.setText(_translate("UserList", "Search"))
        self.pushButton_2.setText(_translate("UserList", "Add New"))
        self.pushButton_3.setText(_translate("UserList", "Refresh"))
        self.pushButton_4.setText(_translate("UserList", "Delete"))

    def updateWidget(self):
        self.listWidget.clear()
        list = SQLconnect.getdb().get_user_name()
        for x in range(0, len(list)):
            self.listWidget.addItem(str(list[x][0]) + " " + list[x][1] + " " + list[x][2])

    def popEdit(self, item = None):
        window = GISDialog()
        ui = Ui_Setting()
        if item == False:
            ui.setupUi(window)
        else:
            list = item.text().split()
            ui.setupUi(window)
            db = SQLconnect.getdb()
            data = db.search_user(int(list[0]),list[1],list[2])[0]
            ui.textEdit_2.setText(data[1])
            ui.textEdit_6.setText(data[3])
            ui.textEdit_3.setText(data[6])
            ui.textEdit_4.setText(data[5])
            ui.textEdit_5.setText(str(data[0]))
            sub = db.get_user_stock(int(list[0]))
            for i in range(0, len(sub)):
                ui.comboBox.addItem(str(sub[i][0]) + "-" + str(sub[i][1]))
            gender = data[4]
            if gender == 1:
                ui.checkBox.setChecked(True)
                ui.checkBox_2.setChecked(False)
            else:
                ui.checkBox.setChecked(False)
                ui.checkBox_2.setChecked(True)

        window.exec_()

    def itempicked(self,item):
        self.popEdit(item)


##This is for closeEvent
class GISDialog(QDialog):
    def closeEvent(self, event):
        print("close!!")

        event.accept()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    UserList = QtWidgets.QDialog()
    ui = Ui_UserList()
    ui.setupUi(UserList)
    UserList.show()
    sys.exit(app.exec_())
