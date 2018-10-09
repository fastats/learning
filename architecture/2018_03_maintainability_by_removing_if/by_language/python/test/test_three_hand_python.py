import importlib
from unittest import TestCase

PATH = 'architecture.2018_03_maintainability_by_removing_if.by_language.python.three_hand_python'
py_examples = importlib.import_module(PATH)


class RPSTestMixin:

    @staticmethod
    def p1_win_scenarios():
        """
        Returns an iterable to 2-tuples of the form:
            ((player 1 move, player 2 move), ...)

        where player 1 beats player 2.
        """
        return (
            (py_examples.Move.ROCK, py_examples.Move.SCISSORS),
            (py_examples.Move.SCISSORS, py_examples.Move.PAPER),
            (py_examples.Move.PAPER, py_examples.Move.ROCK),
        )

    @staticmethod
    def swap_moves(scenarios):
        return (s[::-1] for s in scenarios)

    def p2_win_scenarios(self):
        """
        Returns an iterable to 2-tuples of the form:
            ((player 1 move, player 2 move), ...)

        where player 2 beats player 1.
        """
        return self.swap_moves(self.p1_win_scenarios())

    def draw_scenarios(self):
        """
        Returns an iterable to 2-tuples of the form:
            ((player 1 move, player 2 move), ...)

        where player 1 and player 2 draw.
        """
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


class RPSPayoffMatrixTestCase(RPSTestMixin, TestCase):

    def setUp(self):
        self.fn = py_examples.rps_payoff_matrix


class RPSOneLinerTestCase(RPSTestMixin, TestCase):

    def setUp(self):
        self.fn = py_examples.rps_one_liner


class RPDirectedGraphTestCase(RPSTestMixin, TestCase):

    def setUp(self):
        self.fn = py_examples.rps_directed_graph


if __name__ == '__main__':
    import pytest
    pytest.main([__file__])
