import csv
import math

def main():
    lg = input("Which league? ")
    if lg.lower() == "mlb":
        file1 = open("./Data/mlb_bat.csv")
        file2 = open("./Data/mlb_pitch.csv")
        bat = list(csv.reader(file1))
        pitch = list(csv.reader(file2))
        two_csv(bat, pitch, "mlb")
    elif lg.lower() == "nba":
        file1 = open("./Data/nba_team.csv")
        file2 = open("./Data/nba_opp.csv")
        team = list(csv.reader(file1))
        opp = list(csv.reader(file2))
        two_csv(team, opp, "nba")
    elif lg.lower() =="nfl":
        file1 = open("./Data/nfl_team.csv")
        file2 = open("./Data/nfl_opp.csv")
        team = list(csv.reader(file1))
        opp = list(csv.reader(file2))
        two_csv(team, opp, "nfl")
    elif lg.lower() == "nhl":
        file = open("./Data/nhl.csv")
        data = list(csv.reader(file))
        one_csv(data, "nhl")


def row_containing_team(team, data):
    """
    Returns row of team in data

    :type team: str
    :type data: list
    :rtype: int
    """
    row_num = 0
    for row in data:
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
    if lg.lower() == "nhl":
        file = open("nhl", "a")
        lg_ppg = float(data[32][9]) / float(data[32][3])

    away = input("Away team? ")
    away_row = row_containing_team(away, data)
    if lg.lower() == "nhl":
        away = data[away_row][1]
        away_ppg = float(data[away_row][9]) / float(data[away_row][3])
        away_ppga = float(data[away_row][10]) / float(data[away_row][3])

    home = input("Home team? ")
    home_row = row_containing_team(home, data)
    if lg.lower() == "nhl":
        home = data[home_row][1]
        home_ppg = float(data[home_row][9]) / float(data[home_row][3])
        home_ppga = float(data[home_row][10]) / float(data[home_row][3])

    away_score = (away_ppg / lg_ppg) * (home_ppga / lg_ppg) * lg_ppg
    home_score = (home_ppg / lg_ppg) * (away_ppga / lg_ppg) * lg_ppg
    spread = math.fabs(away_score - home_score)
    total = away_score + home_score

    print("\n%s: %.1f - %s: %.1f\nSpread: %.1f, Total: %.1f\n" % (away, away_score, home, home_score, spread, total))
    file.write("%s: %.1f - %s: %.1f\nSpread: %.1f, Total: %.1f\n" % (away, away_score, home, home_score, spread, total))

    away_win = 0.0
    home_win = 0.0
    tie = 0.0

    if lg.lower() == "nhl":
        for i in range(9):
            for j in range(9):
                prob = poisson(i, away_score) * poisson(j, home_score)
                if i < j:
                    home_win += prob
                elif i > j:
                    away_win += prob
                else:
                    tie += prob
    print("%s: %.3f" % (away, away_win / (away_win + home_win + tie)))
    file.write("%s: %.3f\n" % (away, away_win / (away_win + home_win + tie)))
    print("%s: %.3f" % (home, home_win / (away_win + home_win + tie)))
    file.write("%s: %.3f\n" % (home, home_win / (away_win + home_win + tie)))
    print("Tie: %.3f" % (tie / (away_win + home_win + tie)))
    file.write("Tie: %.3f\n" % (tie / (away_win + home_win + tie)))
    print("SU: %.3f\n" % (max(away_win, home_win) / (away_win + home_win)))
    file.write("SU: %.3f\n\n" % (max(away_win, home_win) / (away_win + home_win)))
    file.close()


def two_csv(data1, data2, lg):
    """
    Predicts final score of league with two CSVs

    :type data1: list
    :type data2: list
    :type lg: str
    :rtype: None
    """
    if lg.lower() == "mlb":
        file = open("mlb", "a")
        lg_ppg = float(data1[31][3])
    elif lg.lower() == "nba":
        file = open("nba", "a")
        lg_ppg = float(data1[31][24])
    elif lg.lower() == "nfl":
        file = open("nfl", "a")
        lg_ppg = float(data1[35][3])

    away = input("Away team? ")
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

    away_score = (away_ppg / lg_ppg) * (home_ppga / lg_ppg) * lg_ppg
    home_score = (home_ppg / lg_ppg) * (away_ppga / lg_ppg) * lg_ppg
    spread = math.fabs(away_score - home_score)
    total = away_score + home_score

    print("\n%s: %.1f - %s: %.1f\nSpread: %.1f, Total: %.1f\n" % (away, away_score, home, home_score, spread, total))
    file.write("%s: %.1f - %s: %.1f\nSpread: %.1f, Total: %.1f\n" % (away, away_score, home, home_score, spread, total))

    away_win = 0.0
    home_win = 0.0
    tie = 0.0

    if lg.lower() == "mlb":
        for i in range(9):
            for j in range(9):
                prob = poisson(i, away_score) * poisson(j, home_score)
                if i < j:
                    home_win += prob
                elif i > j:
                    away_win += prob
                else:
                    tie += prob
    elif lg.lower() == "nba":
        for i in range(80, 150, 5):
            for j in range(80, 150, 5):
                prob = poisson(i, away_score) * poisson(j, home_score)
                if i < j:
                    home_win += prob
                elif i > j:
                    away_win += prob
                else:
                    tie += prob
    elif lg.lower() == "nfl":
        for i in range(0, 50, 5):
            for j in range(0, 50, 5):
                prob = poisson(i, away_score) * poisson(j, home_score)
                if i < j:
                    home_win += prob
                elif i > j:
                    away_win += prob
                else:
                    tie += prob
    print("%s: %.3f" % (away, away_win / (away_win + home_win + tie)))
    file.write("%s: %.3f\n" % (away, away_win / (away_win + home_win + tie)))
    print("%s: %.3f" % (home, home_win / (away_win + home_win + tie)))
    file.write("%s: %.3f\n" % (home, home_win / (away_win + home_win + tie)))
    print("Tie: %.3f" % (tie / (away_win + home_win + tie)))
    file.write("Tie: %.3f\n" % (tie / (away_win + home_win + tie)))
    print("SU: %.3f\n" % (max(away_win, home_win) / (away_win + home_win)))
    file.write("SU: %.3f\n\n" % (max(away_win, home_win) / (away_win + home_win)))
    file.close()


def poisson(actual, mean):
    """
    Returns a Poisson probability

    :type actual: float
    :type mean: float
    :rtype: float
    """
    return math.pow(mean, actual) * math.exp(-mean) / math.factorial(actual)


main()
