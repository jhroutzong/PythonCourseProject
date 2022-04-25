import os
import sys
from PyQt6 import uic, QtWidgets
from PyQt6.QtWidgets import QFileDialog

from members_builder import MembersWindow
from curling_league_manager import League, Team, LeagueDatabase

Ui_TeamWindow, QtBaseWindow = uic.loadUiType("TeamsWindow.ui")

class TeamsWindow(QtBaseWindow, Ui_TeamWindow):
    def __init__(self, league, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.SecondAddButton.clicked.connect(self.AddTeam)
        self.SecondEditButton.clicked.connect(self.EditTeam)
        self.SecondDeleteButton.clicked.connect(self.DeleteTeam)
        self.ImportTeamsButton.clicked.connect(self.ImportTeams)
        self.ExportTeamsButton.clicked.connect(self.ExportTeams)
        self.league = league
        self.update_ui()

    def ImportTeams(self):
        data = LeagueDatabase()
        try:
            file = QFileDialog.getOpenFileName(self)
            data.import_league_teams(self.league, (os.path.basename(file[0])))
            self.update_ui()
        except:
            print("Wrong file or no file chosen.")


    def ExportTeams(self):
        data = LeagueDatabase()
        try:
            file = QFileDialog.getSaveFileName(self)
            data.export_league_teams(self.league, (os.path.basename(file[0])))
        except:
            print("You entered the incorrect file type.")

    def DeleteTeam(self):
        row = self.TeamList.currentRow()
        del self.league.teams[row]
        self.update_ui()

    def EditTeam(self):
        row = self.TeamList.currentRow()
        window = MembersWindow(self.league.teams[row])
        window.exec()

    def AddTeam(self):
        new_team = Team(int(self.TeamOID.text()), self.TeamName.text())
        self.league.add_team(new_team)
        self.update_ui()
        self.ClearTextBoxes()

    def ClearTextBoxes(self):
        self.TeamOID.setText("")
        self.TeamName.setText("")

    def update_ui(self):
        self.TeamList.clear()
        for team in self.league.teams:
            self.TeamList.addItem(str(team.name + " " + str(team.oid)))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TeamsWindow()
    window.show()
    sys.exit(app.exec())