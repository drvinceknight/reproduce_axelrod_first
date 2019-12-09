import csv

import pandas as pd

import collections
import pandas as pd
import axelrod as axl


def get_players():
    """
    Return the list of strategies from Axelrod's first tournament.
    """
    first_tournament_participants_ordered_by_reported_rank = [
        s() for s in axl.axelrod_first_strategies
    ]
    return first_tournament_participants_ordered_by_reported_rank


def obtain_ranked_names(players, seed=0):
    """
    Run the tournament with the same parameters as reported in the original work
    (5 repetitions and 200 turns) and return the ranked names.
    """
    axl.seed(seed)
    tournament = axl.Tournament(
        players=players, turns=200, repetitions=5
    )
    results = tournament.play(progress_bar=False)
    return results.ranked_names


def count_matches(ranked_names, ranked_players):
    """
    Count the number of ranks that match between the reported and reproduced
    tournaments.
    """
    first_tournament_ranked_names = [str(p) for p in ranked_players]
    return sum(
        reported == reproduced
        for reported, reproduced in zip(first_tournament_ranked_names, ranked_names)
    )


def write_data(seed, number, winner, tit_for_tat_rank, filename, mode="a"):
    """
    Write the data to a csv file.
    """
    with open(filename, mode) as f:
        writer = csv.writer(f)
        writer.writerow([seed, number, tit_for_tat_rank, winner])


def check_seed(seed, players, filename):
    """
    Check a given seed and return how many ranks match.
    """
    ranked_names = obtain_ranked_names(players=players, seed=seed)
    number_of_matches = count_matches(ranked_names=ranked_names, ranked_players=players)

    write_data(
        seed=seed,
        number=number_of_matches,
        tit_for_tat_rank=ranked_names.index("Tit For Tat"),
        winner=ranked_names[0],
        filename=filename,
    )

    return number_of_matches


def main():
    """
    Run the experiments.
    """
    players = get_players()
    number_of_players = len(players)
    filename = "main.csv"

    try:
        seed = pd.read_csv("main.csv")["seed"].max() + 1
    except FileNotFoundError:
        seed = 0
        write_data(
            seed="seed",
            number="number",
            winner="winner",
            tit_for_tat_rank="tit_for_tat_rank",
            filename=filename,
            mode="w",
        )

    while check_seed(seed=seed, players=players, filename=filename) != number_of_players:
        seed += 1

def summarise():
    """
    Analyse and display the current data collection
    """

    df = pd.read_csv("main.csv")
    print(df.describe())
    print("All winners:")
    print(collections.Counter(df["winner"]))

if __name__ == "__main__":
    import sys
    if "--summarise" in sys.argv:
        summarise()
    else:
        main()
