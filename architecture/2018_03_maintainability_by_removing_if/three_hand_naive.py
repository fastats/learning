import random


def play_game(player1, player2):
    if player1 == player2:
        return 'draw'
    if ((player1 == 'rock' and player2 == 'paper') or
        (player1 == 'paper' and player2 == 'scissors') or
        (player1 == 'scissors' and player2 == 'rock')):
        return 'player 2 wins'
    if ((player2 == 'rock' and player1 == 'paper') or
        (player2 == 'paper' and player1 == 'scissors') or
        (player2 == 'scissors' and player1 == 'rock')):
        return 'player 1 wins'


def rps_game(my_choice):
    return play_game(
        my_choice,
        random.choice(['rock', 'paper', 'scissors'])
    )
