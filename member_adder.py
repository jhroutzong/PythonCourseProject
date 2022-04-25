import sys
from PyQt6 import uic, QtWidgets

Ui_ThirdDialog, QtBaseWindow = uic.loadUiType("add_member_window.ui")

class AddMemberWindow(QtBaseWindow, Ui_ThirdDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AddMemberWindow()
    window.show()
    sys.exit(app.exec())