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


def obtain_ranks(players, seed=0):
    """
    Run the tournament with the same parameters as reported in the original work
    (5 repetitions and 200 turns) and return the ranks.
    """
    axl.seed(seed)
    tournament = axl.Tournament(players=players, turns=200, repetitions=5)
    ranking = tournament.play(progress_bar=False).ranking
    return [ranking.index(i) for i, _ in enumerate(ranking)]


def count_matches(ranks):
    """
    Count the number of ranks that match between the reported and reproduced
    tournaments.
    """
    return sum(reported == reproduced for reported, reproduced in enumerate(ranks))


def write_data(seed, number, ranks, filename, mode="a"):
    """
    Write the data to a csv file.
    """
    with open(filename, mode) as f:
        writer = csv.writer(f)
        writer.writerow([seed, number] + ranks)


def check_seed(seed, players, filename):
    """
    Check a given seed and return how many ranks match.
    """
    ranks = obtain_ranks(players=players, seed=seed)

    # Check reproducibility
    assert ranks == obtain_ranks(
        players=players, seed=seed
    ), f"Failed to reproduce for seed={seed}"

    number_of_matches = count_matches(ranks=ranks)
    write_data(seed=seed, number=number_of_matches, ranks=ranks, filename=filename)

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
        player_names = [p.name for p in players]
        seed = 0
        write_data(
            seed="seed",
            number="number",
            ranks=player_names,
            filename=filename,
            mode="w",
        )

    while (
        check_seed(seed=seed, players=players, filename=filename) != number_of_players
    ):
        seed += 1


def summarise():
    """
    Analyse and display the current data collection
    """
    players = get_players()
    player_names = [p.name for p in players]

    df = pd.read_csv("main.csv")

    print(df[["seed", "number"]].describe())

    print("Number of wins:")
    print((df[player_names] == 0).sum(axis=0))


if __name__ == "__main__":
    import sys

    if "-s" in sys.argv:
        summarise()
    else:
        main()
