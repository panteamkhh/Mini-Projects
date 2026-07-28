# Day 6 - Password Generator

Generates random passwords with a configurable length and character
set (uppercase, digits, symbols), plus a simple strength indicator.

## What I learned
- Using `secrets` instead of `random` for anything security-related
  (passwords, tokens) — `random` is not cryptographically safe
- Building configuration into `__init__` so the same class can generate
  many different password "policies"

## How to run
```bash
python main.py
```

## How to test
```bash
pytest test_main.py
```
