import tkinter as tk
from tkinter import ttk

# Create main window
root = tk.Tk()
root.title("Calculator Pro")
root.geometry("500x400")

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
tk.Button(root, text="Calculate").grid(row=3, column=1)
tk.Button(root, text="Clear").grid(row=3, column=0)

# Result label
label_result = tk.Label(root, text="Result")
label_result.grid(row=4, column=1)

# History list
listbox_history = tk.Listbox(root, width=40)
listbox_history.grid(row=5, column=0, columnspan=2)

root.mainloop()