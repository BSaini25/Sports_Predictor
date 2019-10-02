def main():
    # Checking which league user wants to choose
    lg = input("Which league? ")

    if lg.lower() == "nfl":
        nfl()


def nfl():
    from sportsreference.nfl.teams import Teams

    teams = Teams()
    lg_pf = 0.0
    lg_pa = 0.0
    for team in teams:
        df = team.dataframe
        lg_pf = lg_pf + (float(df["points_for"]) / float(df["games_played"]))
        lg_pa = lg_pa + (float(df["points_against"]) / float(df["games_played"]))
    lg_pf = lg_pf / 32.0
    lg_pa = lg_pa / 32.0
    print("The league average pf is %.1f and pa is %.1f" % (lg_pf, lg_pa))

    """
    away_input = input("Away team? ")
    home_input = input("Home team? ")

    for team in teams:
        if team.name.lower() == away_team.lower():
            away_df = team.dataframe
            away_pf = away_df.loc[:, "points_for"] / away_df.loc[:, "games_played"]
            away_pa = away_df.loc[:, "points_against"] / away_df.loc[:, "games_played"]
            print("%.1f %.1f" % (away_pf, away_pa))

    for team in teams:
        if team.name.lower() == home_team.lower():
            home_df = team.dataframe
            home_pf = home_df.loc[:, "points_for"] / home_df.loc[:, "games_played"]
            home_pa = home_df.loc[:, "points_against"] / home_df.loc[:, "games_played"]
            print("%.1f %.1f" % (home_pf, home_pa))
    """


main()
