import sys
from PyQt5.QtWidgets import QApplication, QDialog
from mainMenu import Ui_Dialog
from userlist import Ui_UserList


def main():
    app = QApplication(sys.argv)
    window = QDialog()
    ui = Ui_Dialog()
    ui.setupUi(window)
    window.show()
    sys.exit(app.exec_())



if __name__ == "__main__":
    main()