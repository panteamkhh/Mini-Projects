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