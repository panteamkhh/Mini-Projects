import tkinter as tk
from tkinter import ttk
import json
import os


# File used to store history permanently
HISTORY_FILE = "history.json"


def load_history():
    """Load calculation history from disk. Returns an empty list if the
    file doesn't exist or contains invalid/corrupted data."""
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
            return []
    except (OSError, json.JSONDecodeError):
        return []


def save_history(history):
    """Persist calculation history to disk."""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as file:
            json.dump(history, file, ensure_ascii=False, indent=2)
    except OSError:
        raise


def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


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


def format_calculation(num1, num2, operation, result):
    """Create a human-readable history entry."""
    return f"{num1:g} {operation} {num2:g} = {result:g}"


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator Pro")
        self.root.geometry("500x400")

        # Keep application state in memory while the app is running.
        self.history = load_history()

        self._build_ui()
        self._load_history_into_ui()

    def _build_ui(self):
        # Create input fields.
        self.entry_num1 = tk.Entry(self.root)
        self.entry_num1.grid(row=0, column=1, padx=5, pady=5)

        self.entry_num2 = tk.Entry(self.root)
        self.entry_num2.grid(row=1, column=1, padx=5, pady=5)

        # Create the operation selector.
        self.operation_var = tk.StringVar(value="Add")
        self.operation_box = ttk.Combobox(
            self.root,
            textvariable=self.operation_var,
            values=list(OPERATIONS.keys()),
            state="readonly",
        )
        self.operation_box.grid(row=2, column=1, padx=5, pady=5)

        # Create action buttons.
        tk.Button(
            self.root,
            text="Calculate",
            command=self.perform_operation,
        ).grid(row=3, column=1, padx=5, pady=5)

        tk.Button(
            self.root,
            text="Clear",
            command=self.clear_inputs,
        ).grid(row=3, column=0, padx=5, pady=5)

        # Create the result display.
        self.label_result = tk.Label(self.root, text="Result")
        self.label_result.grid(row=4, column=1, padx=5, pady=5)

        # Create the calculation history list.
        self.listbox_history = tk.Listbox(self.root, width=40)
        self.listbox_history.grid(
            row=5,
            column=0,
            columnspan=2,
            padx=5,
            pady=5,
        )

    def _load_history_into_ui(self):
        # Display persisted history in the listbox.
        for item in self.history:
            self.listbox_history.insert(tk.END, self._history_to_text(item))

    @staticmethod
    def _history_to_text(item):
        """Convert structured history data into display text."""
        return format_calculation(
            item["num1"],
            item["num2"],
            item["operation"],
            item["result"],
        )

    def perform_operation(self):
        """Read input, calculate, persist, and update the UI."""
        try:
            num1 = float(self.entry_num1.get())
            num2 = float(self.entry_num2.get())
            operation = self.operation_var.get()

            result = calculate(num1, num2, operation)

            history_item = {
                "num1": num1,
                "num2": num2,
                "operation": operation,
                "result": result,
            }

            self.history.append(history_item)
            save_history(self.history)

            output = self._history_to_text(history_item)
            self.label_result.config(text=f"Result: {result:g}")
            self.listbox_history.insert(tk.END, output)

        except ValueError:
            self.label_result.config(text="Enter valid numbers or select a valid operation")
        except ZeroDivisionError as error:
            self.label_result.config(text=str(error))
        except OSError:
            self.label_result.config(text="Could not save history")

    def clear_inputs(self):
        """Clear both input fields."""
        self.entry_num1.delete(0, tk.END)
        self.entry_num2.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()