"""Unit tests for PasswordGenerator."""

import pytest
from main import PasswordGenerator


def test_generate_correct_length():
    generator = PasswordGenerator(length=16)
    password = generator.generate()
    assert len(password) == 16


def test_generate_raises_on_short_length():
    generator = PasswordGenerator(length=2)
    with pytest.raises(ValueError):
        generator.generate()


def test_strength_label_weak():
    assert PasswordGenerator.strength_label("abc") == "Weak"


def test_strength_label_strong():
    assert PasswordGenerator.strength_label("Ab1!Ab1!Ab1!") == "Strong"
