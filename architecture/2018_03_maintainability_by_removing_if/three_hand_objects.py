
from enum import Enum


class Hand:
    def __init__(self):
        self._beats_hand = None

    def set_beats(self, other):
        self._beats_hand = other


class Rock(Hand):
    pass


class Paper(Hand):
    pass


class Scissors(Hand):
    pass


class RPS(Enum):
    rock = Rock()
    paper = Paper()
    scissors = Scissors()


def initialise():
    RPS.rock.set_beats(RPS.scissors)
    RPS.paper.set_beats(RPS.rock)
    RPS.scissors.set_beats(RPS.paper)
