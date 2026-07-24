# Day 2 - Calculator Pro

A GUI calculator (tkinter) supporting Add / Subtract / Multiply / Divide,
with results saved to `history.json` so history persists between runs.

## What I learned
- Building a basic GUI with tkinter (`Entry`, `Combobox`, `Listbox`, `Button`)
- Separating **logic** (`Calculator`), **persistence** (`HistoryManager`) and
  **UI** (`CalculatorApp`) into their own classes instead of one big script
- Reading/writing JSON for simple persistence

## How to run
```bash
python main.py
```

## How to test
```bash
pytest test_main.py
```
(Only the calculation logic is unit-tested; the UI is not covered by
automated tests here.)
