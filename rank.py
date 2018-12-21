import pandas as pd
import numpy as np
from sklearn import preprocessing

default_cols = ["FGP", "FTP", "3PM", "PPG", "RPG", "APG", "SPG", "BPG", "TPG"]

def get_rankings(col_names: [str], n_results: int) -> pd.DataFrame:
    data = pd.read_csv("data.csv")
    if col_names == []:
        col_names = default_cols
    print(col_names)
    scaler = preprocessing.StandardScaler()
    scaled_league_stats = scaler.fit_transform(data[col_names])
    scaled_league_stats = pd.DataFrame(scaled_league_stats, columns=col_names)

    if "TPG" in col_names:
        scaled_league_stats["TPG"] = scaled_league_stats["TPG"] * -1

    scaled_league_stats["TOTAL"] = np.sum(scaled_league_stats.loc[:, col_names], axis = 1)
    scaled_league_stats = scaled_league_stats.round(3)
    scaled_league_stats["NAME"] = data["NAME"]
    scaled_league_stats = scaled_league_stats.sort_values("TOTAL", ascending = False).head(n_results)
   
    ## add rank
    ranks = np.arange(1,len(scaled_league_stats)+1)
    scaled_league_stats.insert(loc=0, column="RANK", value=ranks)
    return scaled_league_stats




