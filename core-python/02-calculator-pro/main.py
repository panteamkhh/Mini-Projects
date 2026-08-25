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