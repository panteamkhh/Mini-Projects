import tkinter as tk
from tkinter import ttk
import json
import os


# File used to store history permanently
HISTORY_FILE = "history.json"


def load_history():
    """Load calculation history from disk."""
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []



# Map operation names to calculation functions.
OPERATIONS = {
    "Add": add,
    "Subtract": subtract,
    "Multiply": multiply,
    "Divide": divide,
}


def calculate(num1, num2, operation):
    """Validate the operation and execute the matching function."""
    try:
        operation_function = OPERATIONS[operation]
    except KeyError:
        raise ValueError("Invalid operation")

    return operation_function(num1, num2)

load_history()
save_history()

def format_calculation(num1, num2, operation, result):
    return f"{num1:g} {operation} {num2:g} = {result:g}"

def _load_history_into_ui(self):
    for item in self.history:
        self.listbox_history.insert(tk.END, self._history_to_text(item))


@staticmethod
def _history_to_text(item):
    return format_calculation(
        item["num1"],
        item["num2"],
        item["operation"],
        item["result"],
    )        

self._load_history_into_ui()


def _load_history_into_ui(self):
    for item in self.history:
        self.listbox_history.insert(tk.END, self._history_to_text(item))


@staticmethod
def _history_to_text(item):
    return format_calculation(
        item["num1"],
        item["num2"],
        item["operation"],
        item["result"],
    )

