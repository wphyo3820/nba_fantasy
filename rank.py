import pandas as pd
import numpy as np
from sklearn import preprocessing

default_cols = ["FGP", "FTP", "3PM", "PPG", "RPG", "APG", "SPG", "BPG", "TPG"]


def get_rankings(data: pd.DataFrame, col_names: [str],
                 n_results: int) -> pd.DataFrame:
    """
	Creates scaled rankings based on data.csv
	Arguments:
		col_names: names of columns to use for calculating rank 
		n_results: number of results to display
	"""
    if col_names == []:
        col_names = default_cols

    scaler = preprocessing.StandardScaler()
    scaled_league_stats = scaler.fit_transform(data[col_names])
    scaled_league_stats = pd.DataFrame(scaled_league_stats, columns=col_names)

    if "TPG" in col_names:
        scaled_league_stats["TPG"] = scaled_league_stats["TPG"] * -1

    scaled_league_stats["TOTAL"] = np.sum(
        scaled_league_stats.loc[:, col_names], axis=1)
    scaled_league_stats = scaled_league_stats.round(3)
    scaled_league_stats["NAME"] = data["NAME"]
    scaled_league_stats = scaled_league_stats.sort_values(
        "TOTAL", ascending=False).head(n_results)

    ranks = np.arange(1, len(scaled_league_stats) + 1)
    scaled_league_stats.insert(loc=0, column="RANK", value=ranks)
    return scaled_league_stats
