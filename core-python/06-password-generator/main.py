"""
Day 6 - Password Generator (OOP version)

Generates random passwords using cryptographically secure randomness,
with configurable length and character sets.
"""

import secrets
import string


class PasswordGenerator:
    """Generates random passwords based on configurable rules."""

    def __init__(
        self,
        length: int = 12,
        use_upper: bool = True,
        use_digits: bool = True,
        use_symbols: bool = True,
    ) -> None:
        self.length = length
        self.use_upper = use_upper
        self.use_digits = use_digits
        self.use_symbols = use_symbols

    def _build_charset(self) -> str:
        charset = string.ascii_lowercase
        if self.use_upper:
            charset += string.ascii_uppercase
        if self.use_digits:
            charset += string.digits
        if self.use_symbols:
            charset += string.punctuation
        return charset

    def generate(self) -> str:
        if self.length < 4:
            raise ValueError("Password length should be at least 4 characters.")

        charset = self._build_charset()
        return "".join(secrets.choice(charset) for _ in range(self.length))

    @staticmethod
    def strength_label(password: str) -> str:
        """Very simple strength heuristic based on length and variety."""
        score = 0
        score += len(password) >= 8
        score += len(password) >= 12
        score += any(c.isupper() for c in password)
        score += any(c.isdigit() for c in password)
        score += any(c in string.punctuation for c in password)

        if score <= 2:
            return "Weak"
        if score <= 4:
            return "Medium"
        return "Strong"


def run_cli() -> None:
    print("Password Generator")
    try:
        length = int(input("Password length (default 12): ") or 12)
    except ValueError:
        length = 12

    use_symbols = input("Include symbols? (y/n, default y): ").lower() != "n"

    generator = PasswordGenerator(length=length, use_symbols=use_symbols)
    password = generator.generate()

    print(f"\nGenerated password: {password}")
    print(f"Strength: {PasswordGenerator.strength_label(password)}")


if __name__ == "__main__":
    run_cli()
