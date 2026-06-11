import tkinter as tk
from tkinter import ttk
import json
import os

# File used to store history permanently
HISTORY_FILE = "history.json"

# In-memory history list
history = []


# Load history from file when app starts
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    return []


# Save history to file
def save_history():
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file)


# Core calculation logic
def calculate(num1, num2, operation):
    if operation == "Add":
        return num1 + num2
    elif operation == "Subtract":
        return num1 - num2
    elif operation == "Multiply":
        return num1 * num2
    elif operation == "Divide":
        if num2 == 0:
            return "Cannot divide by zero"
        return num1 / num2
    return "Invalid operation"


# Handle calculate button click
def perform_operation():
    try:
        # Read inputs
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()

        # Perform calculation
        result = calculate(num1, num2, operation)

        # Format output
        output = f"{num1} {operation} {num2} = {result}"

        # Update UI label
        label_result.config(text=f"Result: {result}")

        # Store in memory
        history.append(output)

        # Save to file (persistence)
        save_history()

        # Update UI list
        listbox_history.insert(tk.END, output)

    except ValueError:
        label_result.config(text="Enter valid numbers")


# Clear input fields
def clear_inputs():
    entry_num1.delete(0, tk.END)
    entry_num2.delete(0, tk.END)


# ---------------- UI SETUP ---------------- #

root = tk.Tk()
root.title("Calculator Pro")
root.geometry("500x400")

# Load saved history at startup
history = load_history()

# Input fields
entry_num1 = tk.Entry(root)
entry_num1.grid(row=0, column=1)

entry_num2 = tk.Entry(root)
entry_num2.grid(row=1, column=1)

# Operation selector
operation_var = tk.StringVar()

operation_box = ttk.Combobox(
    root,
    textvariable=operation_var,
    values=["Add", "Subtract", "Multiply", "Divide"]
)

operation_box.grid(row=2, column=1)
operation_box.set("Add")

# Buttons
tk.Button(root, text="Calculate", command=perform_operation).grid(row=3, column=1)
tk.Button(root, text="Clear", command=clear_inputs).grid(row=3, column=0)

# Result label
label_result = tk.Label(root, text="Result")
label_result.grid(row=4, column=1)

# History listbox
listbox_history = tk.Listbox(root, width=40)
listbox_history.grid(row=5, column=0, columnspan=2)

# Load history into UI
for item in history:
    listbox_history.insert(tk.END, item)

# Start app
root.mainloop()