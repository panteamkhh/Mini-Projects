"""Unit tests for RockPaperScissorsGame winner logic."""

from main import RockPaperScissorsGame


def test_draw():
    game = RockPaperScissorsGame()
    assert game.get_winner("rock", "rock") == "draw"


def test_user_wins():
    game = RockPaperScissorsGame()
    assert game.get_winner("rock", "scissors") == "user"
    assert game.get_winner("paper", "rock") == "user"
    assert game.get_winner("scissors", "paper") == "user"


def test_pc_wins():
    game = RockPaperScissorsGame()
    assert game.get_winner("rock", "paper") == "pc"
    assert game.get_winner("paper", "scissors") == "pc"
    assert game.get_winner("scissors", "rock") == "pc"
