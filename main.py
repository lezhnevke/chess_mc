import numpy as np
import pandas as pd
import xlsxwriter


# general parameters of the simulation
proponent = 3300.                   # rating of the player in question
opponent = (2700., 2950.)           # ratings of the opponents
num_games = 600                     # number of games in one simulation
num_simulations = 10000             # number of simulations
thresh = [20, 30, 40, 50, 60, 70]   # series lengths in question


def exp_points(prop, opp):
    """Calculates expected amount of points in the game"""
    return 1./(1.+np.power(10., (opp-prop)/400.))


def mc1(games):
    """Monte-Carlo simulation of the specified number of games.
    Returns sorted list containing all of the series lengths."""
    proponents = proponent * np.ones(games)
    opponents = opponent[0] * np.ones(games) + (opponent[1]-opponent[0]) * np.random.rand(games)

    scores = exp_points(proponents, opponents)
    seeds = np.random.rand(games)
    results = np.abs(np.ceil(scores - seeds)).astype(int)

    series = []
    counter = 0
    for i in range(games):
        if results[i] == 1:
            counter += 1
        else:
            series.append(counter)
            counter = 0

    series.append(counter)
    series.sort()

    return series


def get_more(ser, thresholds):
    """Returns number of series that are longer than the ones in the thresholds array."""
    nums = []
    for element in thresholds:
        nums.append(sum(1 for x in ser if x >= element))
    return nums


all_series = []
all_thresh = []

for j in range(num_simulations):
    curr_series = mc1(num_games)
    curr_thresh = get_more(curr_series, thresh)
    all_series.append(curr_series)
    all_thresh.append(curr_thresh)

df_thresh = pd.DataFrame(all_thresh, columns=thresh)
df_series = pd.DataFrame(all_series)

with pd.ExcelWriter("mc_results.xlsx") as writer:
    df_thresh.to_excel(writer, sheet_name="Thresholds")
    df_series.to_excel(writer, sheet_name="Series")

