
from enum import Enum

import numpy as np
import pandas as pd


class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2


def decode_outcome(outcome):
    desc = {
        0: 'Draw!',
        1: 'Player 1 wins!',
        2: 'Player 2 wins!'
    }
    return desc[outcome]


def rps_payoff_matrix(p1_move, p2_move):
    """
    Payoff matrix.  Read off the relevant outcome for any possible
    pair of p1_move and p2_move.
    """
    payoff = pd.DataFrame([[0, 2, 1],
                           [1, 0, 2],
                           [2, 1, 0]], index=list(Move), columns=list(Move))

    outcome = payoff.loc[p1_move][p2_move]
    return decode_outcome(outcome)


def rps_one_liner(p1_move, p2_move):
    """
    The obligatory (almost) one-liner
    """
    outcome = (3 + p1_move.value - p2_move.value) % 3
    return decode_outcome(outcome)


def rps_directed_graph(p1_move, p2_move):
    """
    Game modelled as a connected, directed graph whose structure is wholly
    inferred from enum member ordering.

    If we have 'n' enum members then, for all i in the range 1 to n, assume
    member i 'beats' member i-1.

    Assume enum member 0 'beats' enum member n.

    Represent 'beat' relationship as a directed edge from one vertex to
    another; an edge in the opposing direction represents a 'lose' relationship.
    """
    arr = np.array(Move)
    idx = np.where(arr == p1_move)[0]

    outcome = 0
    outcome += 1 * (np.roll(arr, shift=1)[idx] == p2_move)
    outcome += 2 * (np.roll(arr, shift=-1)[idx] == p2_move)

    return decode_outcome(outcome.item(0))


if __name__ == '__main__':
    outcome = rps_payoff_matrix(Move.ROCK, Move.PAPER)
    print(outcome)

    outcome = rps_one_liner(Move.ROCK, Move.SCISSORS)
    print(outcome)

    outcome = rps_directed_graph(Move.ROCK, Move.ROCK)
    print(outcome)
