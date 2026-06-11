import tkinter as tk
from tkinter import ttk

# In-memory storage for calculation history
history = []

# Core function to perform arithmetic operations
def calculate(num1, num2, operation):
    # Addition
    if operation == "Add":
        return num1 + num2

    # Subtraction
    elif operation == "Subtract":
        return num1 - num2

    # Multiplication
    elif operation == "Multiply":
        return num1 * num2

    # Division with zero check
    elif operation == "Divide":
        if num2 == 0:
            return "Cannot divide by zero"
        return num1 / num2

    # Invalid operation fallback
    return "Invalid operation"


# Function triggered when user clicks Calculate button
def perform_operation():
    try:
        # Read inputs from UI and convert to float
        num1 = float(entry_num1.get())
        num2 = float(entry_num2.get())

        # Get selected operation from dropdown
        operation = operation_var.get()

        # Perform calculation
        result = calculate(num1, num2, operation)

        # Format output string for history
        output = f"{num1} {operation} {num2} = {result}"

        # Update result label
        label_result.config(text=f"Result: {result}")

        # Save result in memory history
        history.append(output)

        # Display result in listbox
        listbox_history.insert(tk.END, output)

    except ValueError:
        # Handle invalid numeric input
        label_result.config(text="Enter valid numbers")


# Clear input fields
def clear_inputs():
    entry_num1.delete(0, tk.END)
    entry_num2.delete(0, tk.END)


# ---------------- UI SETUP ---------------- #

# Create main application window
root = tk.Tk()
root.title("Calculator Pro")
root.geometry("500x400")

# Input field for first number
entry_num1 = tk.Entry(root)
entry_num1.grid(row=0, column=1)

# Input field for second number
entry_num2 = tk.Entry(root)
entry_num2.grid(row=1, column=1)

# Variable to store selected operation
operation_var = tk.StringVar()

# Dropdown menu for selecting operation
operation_box = ttk.Combobox(
    root,
    textvariable=operation_var,
    values=["Add", "Subtract", "Multiply", "Divide"]
)

operation_box.grid(row=2, column=1)
operation_box.set("Add")

# Button to perform calculation
tk.Button(root, text="Calculate", command=perform_operation).grid(row=3, column=1)

# Button to clear inputs
tk.Button(root, text="Clear", command=clear_inputs).grid(row=3, column=0)

# Label to display result
label_result = tk.Label(root, text="Result")
label_result.grid(row=4, column=1)

# Listbox to show calculation history
listbox_history = tk.Listbox(root, width=40)
listbox_history.grid(row=5, column=0, columnspan=2)

# Start Tkinter event loop
root.mainloop()