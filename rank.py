import pandas as pd
import numpy as np
from nba_api.stats.endpoints import leaguedashplayerstats
from sklearn import preprocessing

def get_league_stats(last_n = 0):
    params = {} if last_n == 0 else {"last_n_games": last_n}
    league_stats = leaguedashplayerstats.LeagueDashPlayerStats(**params).get_data_frames()[0]
    per_cols = ["REB", "AST", "TOV", "STL", "BLK", "PTS"]
    league_stats[per_cols] = league_stats[per_cols].div(league_stats["GP"].values, axis = 0)
    return league_stats

def get_rankings(league_stats, col_names: [str], n_results = 100):
    scaler = preprocessing.StandardScaler()

    scaled_league_stats = scaler.fit_transform(league_stats[col_names])
    scaled_league_stats = pd.DataFrame(scaled_league_stats, columns=col_names)

    if "TOV" in col_names:
        scaled_league_stats["TOV"] = scaled_league_stats["TOV"] * -1

    scaled_league_stats["TOTAL"] = np.sum(scaled_league_stats.loc[:, col_names], axis = 1)
    scaled_league_stats = scaled_league_stats.round(3)
    scaled_league_stats["PLAYER_NAME"] = league_stats["PLAYER_NAME"]
    scaled_league_stats = scaled_league_stats.sort_values("TOTAL", ascending = False).head(n_results)
   
    ## add rank
    ranks = np.arange(1,len(scaled_league_stats)+1)
    scaled_league_stats.insert(loc=0, column="RANK", value=ranks)
    return scaled_league_stats




