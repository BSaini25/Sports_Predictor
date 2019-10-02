import math

def main():
    # Checking which league user wants to choose
    lg = input("Which league? ")

    # Calling calculate based on chosen league
    if lg.lower() == "nfl":
        from sportsreference.nfl.teams import Teams
        teams = Teams()
        calculate("nfl", teams)
    elif lg.lower() == "mlb":
        from sportsreference.mlb.teams import Teams
        teams = Teams()
        calculate("mlb", teams)

def calculate(lg, teams):
    """
    Calculates game score and probability of win
    :type lg: string
    :type teams: Teams
    :rtype: None
    """
    lg_pf = 0.0
    lg_pa = 0.0

    # Finding league average ppg for and ppg against
    if lg.lower() == "nfl":
        for team in teams:
            df = team.dataframe
            lg_pf = lg_pf + (float(df["points_for"]) / float(df["games_played"]))
            lg_pa = lg_pa + (float(df["points_against"]) / float(df["games_played"]))
        lg_pf = lg_pf / 32
        lg_pa = lg_pa / 32
    elif lg.lower() == "mlb":
        for team in teams:
            df = team.dataframe
            lg_pf = lg_pf + float(df["runs"])
            lg_pa = lg_pa + float(df["runs_against"])
        lg_pf = lg_pf / 30
        lg_pa = lg_pa / 30

    # Getting ppg tuples for away and home teams
    away_input = input("Away team? ")
    home_input = input("Home team? ")
    if lg.lower() == "nfl":
        away_ppg = get_ppg_tuple("nfl", teams, away_input)
        home_ppg = get_ppg_tuple("nfl", teams, home_input)
    elif lg.lower() == "mlb":
        away_ppg = get_ppg_tuple("mlb", teams, away_input)
        home_ppg = get_ppg_tuple("mlb", teams, home_input)

    # Calculating score based on team performances against the league average
    away_score = (away_ppg[0] / lg_pf) * (home_ppg[1] / lg_pa) * lg_pf
    home_score = (home_ppg[0] / lg_pf) * (away_ppg[1] / lg_pa) * lg_pf
    spread = math.fabs(away_score - home_score)
    total = away_score + home_score
    print("\n%s: %.1f - %s: %.1f\nSpread: %.1f, Total: %.1f\n" % (away_input, away_score, home_input, home_score, spread, total))

    # Using a Poisson distribution to calculate likelihood of favourite winning
    away_win = 0.0
    home_win = 0.0
    tie = 0.0
    max_pts = 0

    if lg.lower() == "nfl":
        for i in range(0, 50, 5):
            for j in range(0, 50, 5):
                prob = poisson(i, away_score) * poisson(j, home_score)
                if i < j:
                    home_win += prob
                elif i > j:
                    away_win += prob
                else:
                    tie += prob
    elif lg.lower() == "mlb":
        for i in range(9):
            for j in range(9):
                prob = poisson(i, away_score) * poisson(j, home_score)
                if i < j:
                    home_win += prob
                elif i > j:
                    away_win += prob
                else:
                    tie += prob

    print("%s: %.3f" % (away_input, away_win / (away_win + home_win + tie)))
    print("%s: %.3f" % (home_input, home_win / (away_win + home_win + tie)))
    print("Tie: %.3f" % (tie / (away_win + home_win + tie)))
    print("SU: %.3f\n" % (max(away_win, home_win) / (away_win + home_win)))


def get_stat(teams, team_name, stat):
    """
    Returns desired statistic from dataframe
    :type teams: Teams
    :type team_name: string
    :type stat: string
    :rtype: dataframe
    """
    # Looping through teams until desired team is found
    for team in teams:
        if (team.name.lower() == team_name.lower()) or (team.abbreviation.lower() == team_name.lower()):
            df = team.dataframe
            return df.loc[:, stat]


def get_ppg_tuple(lg, teams, team_name):
    """
    Returns a tuple of team's ppg for and ppg against.
    :type lg: string
    :type teams: Teams
    :type team_name: string
    :rtype: float tuple
    """
    if lg.lower() == "nfl":
        gp = int(get_stat(teams, team_name, "games_played"))
        pf = int(get_stat(teams, team_name, "points_for"))
        pf = pf / gp
        pa = int(get_stat(teams, team_name, "points_against"))
        pa = pa / gp
        tup = (pf, pa)
        return tup
    elif lg.lower() == "mlb":
        rf = float(get_stat(teams, team_name, "runs"))
        ra = float(get_stat(teams, team_name, "runs_against"))
        tup = (rf, ra)
        return tup


def poisson(actual, mean):
    """
    Returns a Poisson probability.
    :type actual: float
    :type mean: float
    :rtype: float
    """
    # Using the Poisson distribution
    return math.pow(mean, actual) * math.exp(-mean) / math.factorial(actual)


main()
