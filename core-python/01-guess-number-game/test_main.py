"""Basic unit tests for the GuessNumberGame class."""

from main import GuessNumberGame


def test_give_hint_correct():
    game = GuessNumberGame()
    game.secret_number = 42
    assert game.give_hint(42) == "correct"


def test_give_hint_too_high():
    game = GuessNumberGame()
    game.secret_number = 42
    assert game.give_hint(50) == "too high"


def test_give_hint_too_low():
    game = GuessNumberGame()
    game.secret_number = 42
    assert game.give_hint(10) == "too low"
