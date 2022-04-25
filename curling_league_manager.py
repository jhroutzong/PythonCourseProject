import csv

import yagmail
import pickle
from os.path import exists as file_exists

class IdentifiedObject:
    """Instantiates the identifier variable to be incremented by one each time an object is created."""

    @property # r/o prop
    def oid(self):
        return self._oid

    def __init__(self, oid):
        self._oid = oid

    def __eq__(self, other):
        if self.__class__ is other.__class__ and self._oid == other.oid:
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.oid)


class League(IdentifiedObject):

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def teams(self):
        return self._teams

    @property
    def competitions(self):
        return self._competitions

    def __init__(self, oid, name):
        super().__init__(oid)
        self.name = name
        self._teams = []
        self._competitions = []

    def add_team(self, team):
        for x in self._teams:
            if x.oid == team.oid:
                raise DuplicateOid
        self._teams.append(team)

    def remove_team(self, team):
        for y in self._competitions:
            if team in y:
                raise ValueError
        for x in self._teams:
            if x == team:
                self.teams.remove(team)  # check for accuracy

    def team_named(self, s):
        for team in self._teams:
            if s == team.name:
                return team
            # else
            #     return None

    def add_competition(self, competition):   # check for league.teams, not league.competitions
        for x in self._competitions:
            if x not in self._teams:
                raise ValueError("The competition you are trying to add is already in the list.")
        self._competitions.append(competition)
                  # <----- check for accuracy


    def teams_for_member(self, member):
        teams_for_member0 = []
        for x in self._teams:
            for mem in x.members:
                if str(member) == str(mem):
                    teams_for_member0.append(x)
                # if y == member:

        return teams_for_member0

    def competitions_for_team(self, team):
        _local_competitions = []
        for x in self._competitions:
            if team in x.teams_competing:
                _local_competitions.append(x)

        return _local_competitions

    def competitions_for_member(self, member):
        all_competitions = []
        for competition in self._competitions:
            for team in competition.teams_competing:
                if member in team.members:
                    all_competitions.append(competition)
        return all_competitions

    def __str__(self):

        return self._name + ": " + str(self._teams.count) + " teams, " + str(self._competitions.count) + "competitions"


class Team(IdentifiedObject):

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def members(self):
        return self._members

    def __init__(self, oid, name):
        super().__init__(oid)
        self._name = name
        self._members = []

    def add_member(self, member):
        for m in self._members:
            if member.oid == m.oid:
                raise DuplicateOid(member.oid) # missed the argument when calling the constructor
            elif str(member.email).lower() == str(m.email).lower():
                raise DuplicateEmail(member.email)
        self._members.append(member)

    def member_named(self, s):
        for member in self._members:
            if member.name == s:
                return member
        return None

    def remove_member(self, member):
        if member in self._members:
            self._members.remove(member)

    def send_email(self, emailer, subject, message):
        a = []
        for member in self._members:
            if member.email is not None:
                a.append(member.email)

        emailer.send_plain_email(a, subject, message)



    def __str__(self):
        return str(self._name + ": " + str(len(self._members)) + " members")


class TeamMember(IdentifiedObject):

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    def __init__(self, oid, name, email):
        super().__init__(oid)
        self._name = name
        self._email = email

    def send_email(self, emailer, subject, message):
        if self._email is not None:
            emailer.send_plain_email([self._email], subject, message)
        # use the emailer argument to send an email to to this member

    def __str__(self):
        return self._name + "<" + self._email + ">"


class Competition(IdentifiedObject):

    @property
    def teams_competing(self):
        return self._teams

    @property
    def date_time(self):
        return self._datetime

    @date_time.setter
    def date_time(self, value):
        self._datetime = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    def __init__(self, oid, teams, location, datetime):
        super().__init__(oid)
        self._teams = teams
        self._location = location
        self._datetime = datetime

    def send_email(self, emailer, subject, message):
        print('hello')
        a = set()
        for team in self._teams:
            for member in team.members:
                if member.email is not None:
                    a.add(member.email)
        emailer.send_plain_email(a, subject, message)  #  <---- check for correctness

    def __str__(self):
        return "Competition at " + self._location + "on " + self._datetime + "with " + str(len(self.teams)) + " teams"


class Emailer:
    _sender_address = ""
    _sole_instance = None

    @classmethod
    def configure(cls, sender_address):
        cls._sender_address = sender_address

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    def send_plain_email(self, recipients, subject, message):
        yag = yagmail.SMTP()
        for recipient in recipients:
            yag.send(recipient, subject, message)   # <----- test?
            print(f"Sending mail to: " + recipient)

class LeagueDatabase:
    _sole_instance = None
    _last_oid = 0   # <--- is being initialized correctly?

    def __init__(self):
        self._leagues = []

    @classmethod
    def instance(cls):
        if cls._sole_instance is None:
            cls._sole_instance = cls()
        return cls._sole_instance

    @classmethod
    def load(cls, file_name):
        try:
            with open(file_name, mode="rb") as f:
                cls._sole_instance = pickle.load(f)  # <--- check for correctness
                print("Found file. Storing in sole instance.")
                return cls._sole_instance
        except FileNotFoundError:
            print("File not found. ")
            my_string = file_name + ".backup"
            try:
                with open(my_string, mode="rb") as f:
                    print("Opened backup file")
                    cls._sole_instance = pickle.load(f)  # <--- check for correctness
                    return cls._sole_instance
            except FileNotFoundError:
                print("Searched for backup file -- File not found. ")


    @property
    def leagues(self):
        return self._leagues

    def add_league(self, league):
        self._leagues.append(league)

    def remove_league(self, league):
        if league in self._leagues:
            self._leagues.remove(league)
        else:
            print("League doesn't exist.")

    def league_named(self, name):
        for league in self._leagues:
            if league.name == name:
                return league
            else:
                print("League not found.")

    def next_oid(self):
        self._last_oid = self._last_oid + 1
        return self._last_oid

    def save(self, file_name):   # <----- check for correctness
        if not file_exists(file_name):
            with open(file_name, mode="wb") as f:
                pickle.dump(self, f)   #  <---- self.leagues???
        else:
            my_string = file_name + ".backup"
            with open(my_string, mode="wb") as f:
                pickle.dump(self, f)   # changes made


    def import_league_teams(self, league, file_name):
        try:
            with open(file_name, "rt", encoding="UTF8") as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    if league.team_named(row[0]) is None:
                        team = Team(self.next_oid(), row[0])
                        league.add_team(team)
                    member = TeamMember(self.next_oid(), row[1], row[2])
                    league.team_named(row[0]).add_member(member)
        except Exception as e:
            print(e)
            print("Error loading league/file. One of your parameters is incorrect.")



    def export_league_teams(self, league, file_name):
        # The method export_league_teams(league, file_name) should write the teams belonging to the league specified
        # in the first argument. But if the league does not exist in the database, it should do nothing.
        if league in self.leagues:
            with open(file_name, "w", encoding="UTF8") as f:
                try:
                    writer = csv.writer(f)
                    default_header = ["Team name", "Member name", "Member email"]
                    writer.writerow(default_header)
                    for team in league.teams:
                        for member in team.members:
                            header = [team.name, member.name, member.email]
                            writer.writerow(header)
                except Exception as e:
                    print(e)
                    print("Error occured while writing league.")





class DuplicateOid(Exception):
    pass

    def __init__(self, oid):
        self._oid = oid
        # set in super? (Identified Object?)  <------- super().__init__(oid)


class DuplicateEmail(Exception):
    pass

    def __init__(self, email):
        self._email = email
        # set in super? (Team Member?)  <-------


if __name__ == "__main__":
    b = LeagueDatabase()
    b.load("test_file_for_saving")
    a = []
    for league in b._sole_instance:
        a.append(league.name)
        print(league.name)

