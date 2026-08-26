# Todo CLI App

A simple command-line to-do list manager with persistent storage in
`tasks.json`. Includes two implementations of the same app:

- **`todo_procedural.py`** — function-based version
- **`todo_oop.py`** — object-oriented version (`Task`, `TaskManager`, `TodoCLI`)

Both support the same menu: add, view, delete, and toggle (done/undone)
tasks, plus exit.

## Bug fix

The original version only caught `FileNotFoundError` when loading
`tasks.json`. If that file existed but was empty or corrupted (e.g. from
an interrupted previous run), `json.load` raised an uncaught
`JSONDecodeError` and crashed the program **before the menu even
appeared** — which looked like "View tasks doesn't work" but was really
the whole app failing at startup. Both versions now:

- Fall back to an empty task list if the file is missing, empty,
  corrupted, or not shaped as a list.
- Use explicit `utf-8` encoding on read/write (avoids issues with the
  ✔/❌ symbols on some systems).
- Replace bare `except:` with `except ValueError:` so real errors
  aren't silently swallowed.
- Report a clear message instead of crashing if saving to disk fails.

## What I learned

- Why only catching one exception type during file I/O isn't enough,
  and how a startup crash can masquerade as an unrelated feature bug
- Separating **logic** (`TaskManager`) from **UI** (`TodoCLI`) in the
  OOP version, versus keeping everything in top-level functions in the
  procedural version
- Writing tests for logic that touches the filesystem, using pytest's
  `tmp_path` and `monkeypatch` fixtures instead of touching the real
  `tasks.json`

## How to run

```bash
python todo_procedural.py
# or
python todo_oop.py
```

## How to test

```bash
pytest test_main.py
```

Tests cover the data/logic layer of both versions (`load_tasks`/
`save_tasks`, `Task`, `TaskManager`) using temporary files, so your
real `tasks.json` is never touched. The interactive menu loop itself
(`input()`/`print()`) is not covered by automated tests here.
