import tkinter as tk
from tkinter import ttk

# ---------------- LOGIC ---------------- #

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


def perform_operation():
    try:
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())
        operation = operation_var.get()

        result = calculate(num1, num2, operation)

        label_result.config(text=f"Result: {result}")

    except ValueError:
        label_result.config(text="Enter valid numbers")


# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Calculator Pro")
root.geometry("500x400")

entry_num1 = tk.Entry(root)
entry_num1.grid(row=0, column=1)

entry_num2 = tk.Entry(root)
entry_num2.grid(row=1, column=1)

operation_var = tk.StringVar()

operation_box = ttk.Combobox(
    root,
    textvariable=operation_var,
    values=["Add", "Subtract", "Multiply", "Divide"]
)
operation_box.grid(row=2, column=1)
operation_box.set("Add")

# ✅ IMPORTANT: command is set here correctly
tk.Button(root, text="Calculate", command=perform_operation).grid(row=3, column=1)

tk.Button(root, text="Clear").grid(row=3, column=0)

label_result = tk.Label(root, text="Result")
label_result.grid(row=4, column=1)

listbox_history = tk.Listbox(root, width=40)
listbox_history.grid(row=5, column=0, columnspan=2)

root.mainloop()