import csv
from datetime import datetime
import math

def main():
    # Checking which league user wants to choose
    lg = input("Which league? ")
    if lg.lower() == "mlb":
        file1 = open("./Data/MLB/mlb_bat.csv")
        file2 = open("./Data/MLB/mlb_pitch.csv")
        bat = list(csv.reader(file1))
        pitch = list(csv.reader(file2))
        two_csv(bat, pitch, "mlb")
    elif lg.lower() == "nba":
        file1 = open("./Data/NBA/nba_team.csv")
        file2 = open("./Data/NBA/nba_opp.csv")
        team = list(csv.reader(file1))
        opp = list(csv.reader(file2))
        two_csv(team, opp, "nba")
    elif lg.lower() =="nfl":
        file1 = open("./Data/NFL/nfl_team.csv")
        file2 = open("./Data/NFL/nfl_opp.csv")
        team = list(csv.reader(file1))
        opp = list(csv.reader(file2))
        two_csv(team, opp, "nfl")
    elif lg.lower() == "nhl":
        file = open("./Data/NHL/nhl.csv")
        data = list(csv.reader(file))
        one_csv(data, "nhl")


def row_containing_team(team, data):
    """
    Returns row of team in data
    :type team: str
    :type data: list
    :rtype: int
    """
    # Looping through rows in data and checking which one matches the team selected
    row_num = 0
    for row in data:
        # Checking at both indices since MLB CSV has team at index 1
        if team.lower() in row[0].lower() or team.lower() in row[1].lower():
            break
        else:
            row_num += 1
    return row_num


def one_csv(data, lg):
    """
    Predicts final score of league with one CSV
    :type data: list
    :type lg: str
    :rtype: None
    """
    filename = f"{lg.lower()}_{datetime.now().strftime('%m-%d-%Y')}.txt"
    file = open(filename, "a")

    # Getting league averages based on which league user wants
    if lg.lower() == "nhl":
        lg_ppg = float(data[32][9]) / float(data[32][3])

    while True:
    # Getting team stats from CSV
        away = input("Away team? ")
        if away.lower() == "exit":
            break

        away_row = row_containing_team(away, data)
        if lg.lower() == "nhl":
            away = data[away_row][1]
            away_ppg = float(data[away_row][9]) / float(data[away_row][3])
            away_ppga = float(data[away_row][10]) / float(data[away_row][3])

        home = input("Home team? ")
        if home.lower() == "exit":
            break

        home_row = row_containing_team(home, data)
        if lg.lower() == "nhl":
            home = data[home_row][1]
            home_ppg = float(data[home_row][9]) / float(data[home_row][3])
            home_ppga = float(data[home_row][10]) / float(data[home_row][3])

        # Making predictions using stats
        away_score = (away_ppg / lg_ppg) * (home_ppga / lg_ppg) * lg_ppg
        home_score = (home_ppg / lg_ppg) * (away_ppga / lg_ppg) * lg_ppg
        spread = math.fabs(away_score - home_score)
        total = away_score + home_score

        print(f"{away}: {away_score:.1f} - {home}: {home_score:.1f}\nSpread: {spread:.1f}, Total: {total:.1f}\n\n")
        file.write(f"{away}: {away_score:.1f} - {home}: {home_score:.1f}\nSpread: {spread:.1f}, Total: {total:.1f}\n\n")


def two_csv(data1, data2, lg):
    """
    Predicts final score of league with two CSVs
    :type data1: list
    :type data2: list
    :type lg: str
    :rtype: None
    """
    filename = f"{lg.lower()}_{datetime.now().strftime('%m-%d-%Y')}.txt"
    file = open(filename, "a")

    # Getting league averages based on which league user wants
    if lg.lower() == "mlb":
        lg_ppg = float(data1[31][3])
    elif lg.lower() == "nba":
        lg_ppg = float(data1[31][24])
    elif lg.lower() == "nfl":
        lg_ppg = float(data1[35][3])

    while True:
        # Getting team stats from CSV
        away = input("Away team? ")
        if away.lower() == "exit":
            break

        away_row_off = row_containing_team(away, data1)
        away_row_def = row_containing_team(away, data2)
        if lg.lower() == "mlb":
            away = data1[away_row_off][0]
            away_ppg = float(data1[away_row_off][3])
            away_ppga = float(data2[away_row_def][3])
        elif lg.lower() == "nba":
            away = data1[away_row_off][1]
            away_ppg = float(data1[away_row_off][24])
            away_ppga = float(data2[away_row_def][24])
        elif lg.lower() == "nfl":
            away = data1[away_row_off][1]
            away_ppg = float(data1[away_row_off][3]) / float(data1[away_row_off][2])
            away_ppga = float(data2[away_row_def][3]) / float(data2[away_row_def][2])

        home = input("Home team? ")
        if home.lower() == "exit":
            break

        home_row_off = row_containing_team(home, data1)
        home_row_def = row_containing_team(home, data2)
        if lg.lower() == "mlb":
            home = data1[home_row_off][0]
            home_ppg = float(data1[home_row_off][3])
            home_ppga = float(data2[home_row_def][3])
        elif lg.lower() == "nba":
            home = data1[home_row_off][1]
            home_ppg = float(data1[home_row_off][24])
            home_ppga = float(data2[home_row_def][24])
        elif lg.lower() == "nfl":
            home = data1[home_row_off][1]
            home_ppg = float(data1[home_row_off][3]) / float(data1[home_row_off][2])
            home_ppga = float(data2[home_row_def][3]) / float(data2[home_row_def][2])

        # Making predictions using stats
        away_score = (away_ppg / lg_ppg) * (home_ppga / lg_ppg) * lg_ppg
        home_score = (home_ppg / lg_ppg) * (away_ppga / lg_ppg) * lg_ppg
        spread = math.fabs(away_score - home_score)
        total = away_score + home_score

        print(f"{away}: {away_score:.1f} - {home}: {home_score:.1f}\nSpread: {spread:.1f}, Total: {total:.1f}\n\n")
        file.write(f"{away}: {away_score:.1f} - {home}: {home_score:.1f}\nSpread: {spread:.1f}, Total: {total:.1f}\n\n")


main()
