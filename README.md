# 20 Days of Python — Mini Projects

A daily-practice repo: small, self-contained Python projects, from core
language fundamentals to basic data work. Each day lives in its own
folder with its own code, README, and (where it makes sense) tests.

## Goal

Build hands-on, practical experience with Python — one small project
at a time — moving from console programs and OOP fundamentals
(`core-python/`) into working with real data (`data-basics/`).


## Repo structure

```
mini-projects/
├── README.md
├── requirements.txt
│
├── core-python/
│   ├── 01-guess-number-game/
│   │   ├── main.py
│   │   ├── test_main.py
│   │   └── README.md
│   ├── 02-calculator-pro/
│   │   ├── main.py
│   │   ├── test_main.py
│   │   └── README.md
│   ├── 03-todo-app/
│   │   ├── main.py
│   │   ├── test_main.py
│   │   └── README.md
│   ├── 04-rock-paper-scissors/
│   │   ├── main.py
│   │   ├── test_main.py
│   │   └── README.md
│   ├── 05-treasure-island/
│   │   ├── main.py
│   │   └── README.md
│   ├── 06-password-generator/
│   │   ├── main.py
│   │   ├── test_main.py
│   │   └── README.md
│   ├── 07-hangman-game/
│   │   ├── main.py
│   │   ├── test_main.py
│   │   └── README.md
│   ├── 08-quiz-app/
│   │   ├── main.py
│   │   ├── questions.json
│   │   ├── test_main.py
│   │   └── README.md
│   ├── 09-banking-system/
│   │   ├── main.py
│   │   ├── test_main.py
│   │   └── README.md
│   └── 10-refactor-week/
│       ├── utils/
│       │   ├── __init__.py
│       │   └── validators.py
│       ├── test_validators.py
│       └── README.md
│
└── data-basics/          # Days 11-20 (in progress)
```

## Design conventions used across the repo

- Every project is written as one or more **classes** — game/business
  logic separated from CLI or GUI code — instead of one flat script.
- Public methods use **type hints** and short **docstrings**.
- Anywhere the original day used a bare `except:`, it was replaced with
  a specific exception (`ValueError`, `KeyError`, a custom exception, etc.).
- Projects that don't depend on `input()`/GUI event loops have a
  `test_main.py` written with `pytest`.
- JSON is used for lightweight persistence (history, tasks, accounts)
  instead of anything database-related, since that's out of scope for
  Days 1-10.

## How to run any project

```bash
cd core-python/01-guess-number-game
python main.py
```

## How to run tests

```bash
pip install -r requirements.txt
cd core-python/01-guess-number-game   # or any other day with tests
pytest
```

