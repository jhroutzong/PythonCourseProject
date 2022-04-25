import sys
from PyQt6 import uic, QtWidgets
from curling_league_manager import Team, TeamMember
Ui_MemberWindow, QtBaseWindow = uic.loadUiType("MemberWindow.ui")

class MembersWindow(QtBaseWindow, Ui_MemberWindow):
    def __init__(self, team=None, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.ThirdEditButton.clicked.connect(self.EditMember)
        self.ThirdAddButton.clicked.connect(self.AddMember)
        self.team = team
        self.ThirdDeleteButton.clicked.connect(self.DeleteMember)
        self.update_ui()

    def update_ui(self):
        self.MemberList.clear()
        for member in self.team.members:
            self.MemberList.addItem(str(member.name + " " + member.email + " " + str(member.oid)))

    def DeleteMember(self):
        row = self.MemberList.currentRow()
        del self.team.members[row]
        self.update_ui()

    def EditMember(self):
        row = self.MemberList.currentRow()
        updated_member = TeamMember(int(self.MemberOID.text()), self.MemberName.text(), self.MemberEmail.text())
        self.team.members[row] = updated_member
        self.ClearTextBoxes()
        self.update_ui()


    def AddMember(self):
        new_member = TeamMember(int(self.MemberOID.text()), self.MemberName.text(), self.MemberEmail.text())
        self.team.add_member(new_member)
        self.update_ui()
        self.ClearTextBoxes()

    def ClearTextBoxes(self):
        self.MemberOID.setText("")
        self.MemberName.setText("")
        self.MemberEmail.setText("")



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MembersWindow()
    window.show()
    sys.exit(app.exec())