
from enum import Enum

import numpy as np


class Move(Enum):
    ROCK = 0
    PAPER = 1
    SCISSORS = 2

    @staticmethod
    def decode_outcome(outcome):
        desc = {
            0: 'Draw!',
            1: 'Player 1 wins!',
            2: 'Player 2 wins!'
        }
        return desc[outcome]

    def __gt__(self, other):
        diff = self.value - other.value
        return diff and diff == 1 or diff == 1 - len(Move)

    def play(self, other):
        cmp = (self > other) - (self < other)
        outcome = np.where(cmp < 0, 2, cmp).item(0)
        return self.decode_outcome(outcome)


def rps_oo(p1_move, p2_move):
    return p1_move.play(p2_move)


if __name__ == '__main__':

    outcome = rps_oo(Move.ROCK, Move.ROCK)
    print(outcome)
