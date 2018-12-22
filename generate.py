import asyncio
import requests
import pandas as pd
import json
from aiohttp import ClientSession

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


def get_player_data(responses) -> pd.DataFrame:
    result = []
    for p in responses:
        data = p.decode("utf8").replace("'", '"')
        data = json.loads(data)
        latest_stats = data.get("league").get("standard").get("stats").get(
            "latest")
        stats_dict = {
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
        result.append(stats_dict)
    return pd.DataFrame(result)


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.read()


async def run(year: int, pids: [int]):
    url = _BASE_ENDPOINT + _PROFILE_ENDPOINT
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for i in range(len(pids)):
            task = asyncio.ensure_future(
                fetch(url.format(year=year, pid=pids[i]), session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        return responses


def construct(year, pids):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    future = asyncio.ensure_future(run(year, pids))
    responses = loop.run_until_complete(future)
    return get_player_data(responses)


def generate_data():
    player_df = get_players_df(2018)
    stats_df = construct(2018, player_df["PlayerID"])
    stats_df['NAME'] = player_df['FirstName'] + " " + player_df['LastName']
    stats_df["MPG"] = pd.to_numeric(stats_df["MPG"])
    stats_df.drop(stats_df[stats_df["MPG"] < 15].index, inplace=True)
    stats_df.to_csv("data.csv", index=False)
