"""
Day 9 - Banking System (OOP version)

A simple command-line banking system supporting account creation,
deposits, withdrawals, transfers, and transaction history, persisted
to a JSON file.
"""

import json
import os
from datetime import datetime


class InsufficientFundsError(Exception):
    """Raised when a withdrawal/transfer exceeds the available balance."""


class Account:
    """A single bank account with a transaction history."""

    def __init__(self, account_id: str, owner: str, balance: float = 0.0, transactions: list = None) -> None:
        self.account_id = account_id
        self.owner = owner
        self.balance = balance
        self.transactions = transactions or []

    def _log(self, description: str) -> None:
        self.transactions.append(
            {"time": datetime.now().isoformat(timespec="seconds"), "description": description}
        )

    def deposit(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.balance += amount
        self._log(f"Deposited {amount}")

    def withdraw(self, amount: float) -> None:
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > self.balance:
            raise InsufficientFundsError(f"Insufficient funds: balance is {self.balance}")
        self.balance -= amount
        self._log(f"Withdrew {amount}")

    def to_dict(self) -> dict:
        return {
            "account_id": self.account_id,
            "owner": self.owner,
            "balance": self.balance,
            "transactions": self.transactions,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Account":
        return cls(data["account_id"], data["owner"], data["balance"], data["transactions"])


class Bank:
    """Manages a collection of accounts with JSON persistence."""

    def __init__(self, file_name: str = "accounts.json") -> None:
        self.file_name = file_name
        self.accounts: dict[str, Account] = self._load()

    def _load(self) -> dict[str, Account]:
        if os.path.exists(self.file_name):
            with open(self.file_name, "r") as file:
                data = json.load(file)
            return {acc_id: Account.from_dict(acc) for acc_id, acc in data.items()}
        return {}

    def save(self) -> None:
        with open(self.file_name, "w") as file:
            json.dump({acc_id: acc.to_dict() for acc_id, acc in self.accounts.items()}, file)

    def create_account(self, account_id: str, owner: str) -> Account:
        if account_id in self.accounts:
            raise ValueError("Account ID already exists.")
        account = Account(account_id, owner)
        self.accounts[account_id] = account
        self.save()
        return account

    def get_account(self, account_id: str) -> Account:
        if account_id not in self.accounts:
            raise KeyError("Account not found.")
        return self.accounts[account_id]

    def transfer(self, from_id: str, to_id: str, amount: float) -> None:
        from_account = self.get_account(from_id)
        to_account = self.get_account(to_id)
        from_account.withdraw(amount)
        to_account.deposit(amount)
        self.save()


class BankCLI:
    """Command-line interface for interacting with a Bank."""

    def __init__(self, bank: Bank) -> None:
        self.bank = bank

    def run(self) -> None:
        while True:
            print("\n1) Create account")
            print("2) Deposit")
            print("3) Withdraw")
            print("4) Transfer")
            print("5) View account")
            print("6) Exit")

            choice = input("Enter your choice: ")

            try:
                if choice == "1":
                    account_id = input("New account ID: ")
                    owner = input("Owner name: ")
                    self.bank.create_account(account_id, owner)
                    print("Account created ✔")

                elif choice == "2":
                    account_id = input("Account ID: ")
                    amount = float(input("Amount: "))
                    self.bank.get_account(account_id).deposit(amount)
                    self.bank.save()
                    print("Deposit successful ✔")

                elif choice == "3":
                    account_id = input("Account ID: ")
                    amount = float(input("Amount: "))
                    self.bank.get_account(account_id).withdraw(amount)
                    self.bank.save()
                    print("Withdrawal successful ✔")

                elif choice == "4":
                    from_id = input("From account ID: ")
                    to_id = input("To account ID: ")
                    amount = float(input("Amount: "))
                    self.bank.transfer(from_id, to_id, amount)
                    print("Transfer successful ✔")

                elif choice == "5":
                    account_id = input("Account ID: ")
                    account = self.bank.get_account(account_id)
                    print(f"Owner: {account.owner} | Balance: {account.balance}")
                    for tx in account.transactions:
                        print(f"  {tx['time']} - {tx['description']}")

                elif choice == "6":
                    print("Goodbye 👋")
                    break

                else:
                    print("Invalid choice ❌")

            except (ValueError, KeyError, InsufficientFundsError) as error:
                print(f"Error: {error}")


if __name__ == "__main__":
    bank = Bank()
    cli = BankCLI(bank)
    cli.run()
