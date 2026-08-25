# Day 9 - Banking System

A command-line banking system with account creation, deposits,
withdrawals, transfers between accounts, and per-account transaction
history, persisted to `accounts.json`.

## What I learned
- Modeling a real-world domain with two classes: `Account` (data +
  behaviour) and `Bank` (a collection of accounts + persistence)
- Using a **custom exception** (`InsufficientFundsError`) instead of
  returning error strings, and catching it cleanly in the CLI layer
- Keeping the CLI (`BankCLI`) completely separate from the business
  logic, so the logic can be tested without any `input()` calls

## How to run
```bash
python main.py
```

## How to test
```bash
pytest test_main.py
```
