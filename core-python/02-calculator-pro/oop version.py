"""
Day 2 - Calculator Pro (OOP version)

A simple GUI calculator built with tkinter that supports the four
basic operations and keeps a persistent calculation history.
"""

import json
import os
import tkinter as tk
from tkinter import ttk


class HistoryManager:
    """Handles loading and saving calculation history to a JSON file."""

    def __init__(self, file_path: str = "history.json") -> None:
        self.file_path = file_path
        self.history: list[str] = self._load()

    def _load(self) -> list[str]:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return []

    def save(self) -> None:
        with open(self.file_path, "w") as file:
            json.dump(self.history, file)

    def add(self, entry: str) -> None:
        self.history.append(entry)
        self.save()


class Calculator:
    """Core arithmetic logic, decoupled from the UI."""

    OPERATIONS = ("Add", "Subtract", "Multiply", "Divide")

    @staticmethod
    def calculate(num1: float, num2: float, operation: str):
        if operation == "Add":
            return num1 + num2
        if operation == "Subtract":
            return num1 - num2
        if operation == "Multiply":
            return num1 * num2
        if operation == "Divide":
            if num2 == 0:
                return "Cannot divide by zero"
            return num1 / num2
        return "Invalid operation"


class CalculatorApp:
    """Tkinter GUI wrapper around Calculator and HistoryManager."""

    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Calculator Pro")
        self.root.geometry("500x400")

        self.history_manager = HistoryManager()
        self.calculator = Calculator()

        self._build_ui()
        self._load_history_into_ui()

    def _build_ui(self) -> None:
        self.entry_num1 = tk.Entry(self.root)
        self.entry_num1.grid(row=0, column=1)

        self.entry_num2 = tk.Entry(self.root)
        self.entry_num2.grid(row=1, column=1)

        self.operation_var = tk.StringVar(value="Add")
        operation_box = ttk.Combobox(
            self.root, textvariable=self.operation_var, values=self.calculator.OPERATIONS
        )
        operation_box.grid(row=2, column=1)

        tk.Button(self.root, text="Calculate", command=self.perform_operation).grid(row=3, column=1)
        tk.Button(self.root, text="Clear", command=self.clear_inputs).grid(row=3, column=0)

        self.label_result = tk.Label(self.root, text="Result")
        self.label_result.grid(row=4, column=1)

        self.listbox_history = tk.Listbox(self.root, width=40)
        self.listbox_history.grid(row=5, column=0, columnspan=2)

    def _load_history_into_ui(self) -> None:
        for item in self.history_manager.history:
            self.listbox_history.insert(tk.END, item)

    def perform_operation(self) -> None:
        try:
            num1 = float(self.entry_num1.get())
            num2 = float(self.entry_num2.get())
            operation = self.operation_var.get()

            result = self.calculator.calculate(num1, num2, operation)
            output = f"{num1} {operation} {num2} = {result}"

            self.label_result.config(text=f"Result: {result}")
            self.history_manager.add(output)
            self.listbox_history.insert(tk.END, output)

        except ValueError:
            self.label_result.config(text="Enter valid numbers")

    def clear_inputs(self) -> None:
        self.entry_num1.delete(0, tk.END)
        self.entry_num2.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()
