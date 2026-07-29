"""Unit tests for HangmanGame."""

from main import HangmanGame


def test_correct_guess_does_not_count_as_wrong():
    game = HangmanGame(word_list=["python"])
    assert game.guess("p") is True
    assert game.wrong_guesses == 0


def test_incorrect_guess_counts_as_wrong():
    game = HangmanGame(word_list=["python"])
    assert game.guess("z") is False
    assert game.wrong_guesses == 1


def test_is_won_when_all_letters_guessed():
    game = HangmanGame(word_list=["hi"])
    game.guess("h")
    game.guess("i")
    assert game.is_won is True


def test_is_lost_after_max_attempts():
    game = HangmanGame(word_list=["python"], max_attempts=2)
    game.guess("z")
    game.guess("x")
    assert game.is_lost is True
