import importlib
from unittest import TestCase

import numpy as np
import pandas as pd

non_oo = importlib.import_module('architecture.2018_03_maintainability_by_removing_if.three_hand_non_oo')
oo = importlib.import_module('architecture.2018_03_maintainability_by_removing_if.three_hand_oo')


class RPSTestMixin:

    @staticmethod
    def p1_win_scenarios():
        return (
            (non_oo.Move.ROCK, non_oo.Move.SCISSORS),
            (non_oo.Move.SCISSORS, non_oo.Move.PAPER),
            (non_oo.Move.PAPER, non_oo.Move.ROCK),
        )

    def p2_win_scenarios(self):
        return (s[::-1] for s in self.p1_win_scenarios())

    def draw_scenarios(self):
        return ((s[0], s[0]) for s in self.p1_win_scenarios())

    def test_p1_wins(self):

        for move in self.p1_win_scenarios():
            outcome = self.fn(*move)
            assert outcome == 'Player 1 wins!'

    def test_p2_wins(self):

        for move in self.p2_win_scenarios():
            outcome = self.fn(*move)
            assert outcome == 'Player 2 wins!'

    def test_draw(self):

        for move in self.draw_scenarios():
            outcome = self.fn(*move)
            assert outcome == 'Draw!'

    @staticmethod
    def all_moves():
        return list(non_oo.Move)

    def test_long_run_outcomes(self):

        rng = np.random.RandomState(4)  # does not affect global state
        moves = rng.choice(self.all_moves(), 2000)
        p1_moves = moves[:1000]
        p2_moves = moves[1000:]

        outcomes = [self.fn(p1, p2) for p1, p2 in zip(p1_moves, p2_moves)]
        value_counts = pd.Series(outcomes).value_counts()

        # we should expect each possible game outcome to occur with
        # roughly the same frequency
        assert value_counts.loc['Player 1 wins!'] == 333
        assert value_counts.loc['Player 2 wins!'] == 349
        assert value_counts.loc['Draw!'] == 318


class RPSPayoffMatrixTestCase(RPSTestMixin, TestCase):

    def setUp(self):
        self.fn = non_oo.rps_payoff_matrix


class RPSOneLinerTestCase(RPSTestMixin, TestCase):

    def setUp(self):
        self.fn = non_oo.rps_one_liner


class RPBiconnectedGraphTestCase(RPSTestMixin, TestCase):

    def setUp(self):
        self.fn = non_oo.rps_biconnected_graph


class RPooTestCase(RPSTestMixin, TestCase):

    @staticmethod
    def all_moves():
        return list(oo.Move)

    @staticmethod
    def p1_win_scenarios():
        return (
            (oo.Move.ROCK, oo.Move.SCISSORS),
            (oo.Move.SCISSORS, oo.Move.PAPER),
            (oo.Move.PAPER, oo.Move.ROCK),
        )

    def setUp(self):
        self.fn = oo.rps_oo


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
