import requests
import pandas as pd
import numpy as np

_BASE_ENDPOINT = "http://data.nba.net/10s/prod/v1/"
_PLAYER_ENDPOINT = "{year}/players.json"
_PROFILE_ENDPOINT = "{year}/players/{pid}_profile.json"


def get_players_df(year: int) -> pd.DataFrame:
    """
    Gets a pandas dataframe that includes all currently active player
    Arguments:
        year: active nba season
    """
    endpoint = _BASE_ENDPOINT + _PLAYER_ENDPOINT
    r = requests.get(endpoint.format(year=year)).json()
    standard_stats = r.get("league").get("standard")
    result_dict = [{
        "FirstName": s.get("firstName"),
        "LastName": s.get("lastName"),
        "PlayerID": s.get("personId"),
        "TeamID": s.get("teamId"),
    } for s in standard_stats]
    return pd.DataFrame(result_dict)


def get_player_profile(year: int, pid: int) -> dict:
    """
    Gets a dict with provided player stats
    Arguments:
        year: active nba season
        pid: player id in nba db
    """
    endpoint = _BASE_ENDPOINT + _PROFILE_ENDPOINT
    p = requests.get(endpoint.format(year=year, pid=pid)).json()
    latest_stats = p.get("league").get("standard").get("stats").get("latest")
    result_dict = {
        "FGP":
        latest_stats.get("fgp"),
        "FTP":
        latest_stats.get("ftp"),
        "3PM":
        round(
            int(latest_stats.get("tpm")) / int(
                latest_stats.get("gamesPlayed")), 1),
        "PPG":
        latest_stats.get("ppg"),
        "APG":
        latest_stats.get("apg"),
        "RPG":
        latest_stats.get("rpg"),
        "SPG":
        latest_stats.get("spg"),
        "BPG":
        latest_stats.get("bpg"),
        "TPG":
        latest_stats.get("topg"),
        "MPG":
        round(
            int(latest_stats.get("min")) / int(
                latest_stats.get("gamesPlayed")), 1)
    }
    return result_dict


def get_players_data(pids: [int]) -> pd.DataFrame:
    """
    Gets a pandas dataframe that includes all player data
    Arguments:
        pids: list of player ids in nba db
    """
    result_list = [get_player_profile(2018, pid) for pid in pids]
    return pd.DataFrame(result_list)