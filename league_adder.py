import sys
from PyQt6 import uic, QtWidgets

Ui_FirstDialog, QtBaseWindow = uic.loadUiType("add_league_window.ui")

oid = 0
name = ""

class AddLeagueWindow(QtBaseWindow, Ui_FirstDialog):
    def __init__(self, parent=None):
        global name
        global oid
        super().__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = AddLeagueWindow()
    window.show()
    sys.exit(app.exec())