import math

def main():
    # Checking which league user wants to choose
    lg = input("Which league? ")

    # Calling calculate based on chosen league
    if lg.lower() == "nfl":
        from sportsipy.nfl.teams import Teams
        teams = Teams()
        calculate("nfl", teams)
    elif lg.lower() == "mlb":
        from sportsipy.mlb.teams import Teams
        teams = Teams()
        calculate("mlb", teams)
    elif lg.lower() == "nhl":
        from sportsipy.nhl.teams import Teams
        teams = Teams()
        calculate("nhl", teams)
    elif lg.lower() == "nba":
        from sportsipy.nba.teams import Teams
        teams = Teams()
        calculate("nba", teams)

def calculate(lg, teams):
    """
    Calculates game score and probability of win
    :type lg: string
    :type teams: Teams
    :rtype: None
    """
    lg_pf = get_league_average(lg, teams)

    # Getting ppg tuples for away and home teams
    away_input = input("Away team? ")
    away_team = get_team(teams, away_input)
    away_ppg = get_ppg_tuple(lg.lower(), away_team)

    home_input = input("Home team? ")
    home_team = get_team(teams, home_input)
    home_ppg = get_ppg_tuple(lg.lower(), home_team)

    # Calculating score based on team performances against the league average
    away_score = (away_ppg[0] / lg_pf) * (home_ppg[1] / lg_pf) * lg_pf
    home_score = (home_ppg[0] / lg_pf) * (away_ppg[1] / lg_pf) * lg_pf
    spread = math.fabs(away_score - home_score)
    total = away_score + home_score

    print(f"\n{away_team.name}: {away_score:.1f} - {home_team.name}: {home_score:.1f}\nSpread: {spread:.1f}, Total: {total:.1f}\n")


def get_league_average(lg, teams):
    """
    Get league average points per game
    :type lg: string
    :type teams: Teams
    :rtype: float
    """
    lg_gp = 0
    lg_pf = 0.0
    lg_pa = 0.0

    # Finding league average ppg for and ppg against
    if lg.lower() == "nfl":
        for team in teams:
            lg_gp = lg_gp + team.games_played
            lg_pf = lg_pf + team.points_for
        lg_gp = lg_gp / 32
        lg_pf = lg_pf / 32
    elif lg.lower() == "mlb":
        for team in teams:
            lg_gp = lg_gp + team.games_played
            lg_pf = lg_pf + team.runs
        lg_gp = lg_gp / 30
        lg_pf = lg_pf / 30
    elif lg.lower() == "nhl":
        for team in teams:
            lg_gp = lg_gp + team.games_played
            lg_pf = lg_pf + team.goals_for
        lg_gp = lg_gp / 31
        lg_pf = lg_pf / 31
    elif lg.lower() == "nba":
        for team in teams:
            lg_gp = lg_gp + team.games_played
            lg_pf = lg_pf + team.points
        lg_gp = lg_gp / 30
        lg_pf = lg_pf / 30

    return lg_pf / lg_gp


def get_team(teams, team_input):
    """
    Returns desired Team from Teams
    :type teams: Teams
    :type team: string
    :rtype: Team
    """
    # Looping through teams until desired team is found
    for team in teams:
        if team_input.lower() in team.name.lower():
            return team


def get_ppg_tuple(lg, team):
    """
    Returns a tuple of team's ppg for and ppg against.
    :type lg: string
    :type team: string
    :rtype: float tuple
    """
    if lg.lower() == "nfl":
        gp = team.games_played
        pf = team.points_for
        pf = pf / gp
        pa = team.points_against
        pa = pa / gp
        tup = (pf, pa)
        return tup
    elif lg.lower() == "mlb":
        rf = team.runs_for
        ra = team.runs_against
        tup = (rf, ra)
        return tup
    elif lg.lower() == "nhl":
        gp = team.games_played
        gf = team.goals_for
        gf = gf / gp
        ga = team.goals_against
        ga = ga / gp
        tup = (gf, ga)
        return tup
    elif lg.lower() == "nba":
        gp = team.games_played
        pf = team.points
        pf = pf / gp
        pa = team.opp_points
        pa = pa / gp
        tup = (pf, pa)
        return tup


main()
