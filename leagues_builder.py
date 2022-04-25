import os
import sys

from PyQt6.QtWidgets import QFileDialog

from curling_league_manager import LeagueDatabase, League

from PyQt6 import uic, QtWidgets

from teams_builder import TeamsWindow

Ui_MainWindow, QtBaseWindow = uic.loadUiType("leagueWindow1.ui")

class LeaguesWindow(QtBaseWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.FirstEditButton.clicked.connect(self.editLeague)
        self.FirstAddButton.clicked.connect(self.AddLeague)
        self.FirstDeleteButton.clicked.connect(self.DeleteLeague)
        self.data = LeagueDatabase()
        self.LoadDB.clicked.connect(self.LoadLeagues)
        self.SaveDB.clicked.connect(self.SaveLeagues)

    def SaveLeagues(self):
        try:
            file = QFileDialog.getSaveFileName(self)
            self.data.save(os.path.basename(file[0]))
        except:
            print("You entered the incorrect file type.")

    def LoadLeagues(self):
        try:
            file = QFileDialog.getOpenFileName(self)
            self.data.load(os.path.basename(file[0]))
            leagues = self.data.instance().leagues
            for league in leagues:
                self.data.add_league(league)
            self.update_ui()
        except:
            "You selected the wrong file type."

    def DeleteLeague(self):
        row = self.LeagueList.currentRow()
        del self.data.leagues[row]
        self.update_ui()

    def AddLeague(self):
        new_league = League(int(self.LeagueOID.text()), self.LeagueName.text())
        self.data.add_league(new_league)
        self.update_ui()
        self.ClearTextBoxes()

    def ClearTextBoxes(self):
        self.LeagueOID.setText("")
        self.LeagueName.setText("")

    def update_ui(self):
        self.LeagueList.clear()
        for league in self.data.leagues:
            self.LeagueList.addItem(str(league.name + " " + str(league.oid)))

    def editLeague(self):
        row = self.LeagueList.currentRow()
        window = TeamsWindow(self.data.leagues[row])
        window.exec()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = LeaguesWindow()
    window.show()
    sys.exit(app.exec())
