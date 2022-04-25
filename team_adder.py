import sys
from PyQt6 import uic, QtWidgets

Ui_SecondDialog, QtBaseWindow = uic.loadUiType("add_team_window.ui")

class AddTeamWindow(QtBaseWindow, Ui_SecondDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AddTeamWindow()
    window.show()
    sys.exit(app.exec())
