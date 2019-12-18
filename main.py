import collections
import csv

import numpy as np
import pandas as pd
import scipy.stats

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

    In Axelrod's original tournament self interactions where included. This is
    not the default in the Axelrod library so has to be handled differently.

    scipy.stats.rankdata returns a numpy array of type floats. We here convert
    that to int to match with the ranks from the paper (there were no ties)
    """
    axl.seed(seed)
    tournament = axl.Tournament(players=players, turns=200, repetitions=5)

    payoff_matrix = np.array(tournament.play(progress_bar=False).payoff_matrix)
    mean_payoffs = payoff_matrix.mean(axis=1)
    self_interaction_ranks = scipy.stats.rankdata(-payoff_matrix.mean(axis=1)).astype(
        int
    )

    ranking = tournament.play(progress_bar=False).ranking
    no_self_interaction_ranks = [ranking.index(i) + 1 for i, _ in enumerate(ranking)]

    return self_interaction_ranks, no_self_interaction_ranks


def count_matches(ranks):
    """
    Count the number of ranks that match between the reported and reproduced
    tournaments.
    """
    return sum(reported + 1 == reproduced for reported, reproduced in enumerate(ranks))


def write_data(seed, number, self_interaction, ranks, filename, mode="a"):
    """
    Write the data to a csv file.
    """
    with open(filename, mode) as f:
        writer = csv.writer(f)
        writer.writerow([seed, number, self_interaction] + list(ranks))


def check_seed(seed, players, filename):
    """
    Check a given seed and return how many ranks match.
    """
    rankings = obtain_ranks(players=players, seed=seed)

    # Check reproducibility
    assert np.array_equal(
        rankings, obtain_ranks(players=players, seed=seed)
    ), f"Failed to reproduce for seed={seed}"

    for ranks, self_interaction in zip(rankings, (True, False)):
        number_of_matches = count_matches(ranks=ranks)
        write_data(
            seed=seed,
            number=number_of_matches,
            ranks=ranks,
            self_interaction=self_interaction,
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
        player_names = [p.name for p in players]
        seed = 0
        write_data(
            seed="seed",
            number="number",
            self_interaction="self_interaction",
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

    print(
        df[["seed", "number", "self_interaction"]]
        .groupby("self_interaction")
        .describe()
    )

    print("Number of wins:")
    for self_interaction in (False, True):
        print(f"self_interaction: {self_interaction}")
        print(
            (df[df["self_interaction"] == self_interaction][player_names] == 1).sum(
                axis=0
            )
        )


if __name__ == "__main__":
    import sys

    if "-s" in sys.argv:
        summarise()
    else:
        main()
