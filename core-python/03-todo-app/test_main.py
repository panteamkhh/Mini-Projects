"""Unit tests for the TodoApp / Task classes (using a temp file for isolation)."""

import os
from main import Task, TodoApp


def test_task_to_dict_and_back():
    task = Task("Buy milk")
    data = task.to_dict()
    rebuilt = Task.from_dict(data)
    assert rebuilt.description == "Buy milk"
    assert rebuilt.done is False


def test_add_and_toggle_task(tmp_path):
    file_path = tmp_path / "tasks.json"
    app = TodoApp(file_name=str(file_path))

    app.add_task("Write tests")
    assert len(app.tasks) == 1
    assert app.tasks[0].done is False

    app.toggle_task(0)
    assert app.tasks[0].done is True


def test_delete_task(tmp_path):
    file_path = tmp_path / "tasks.json"
    app = TodoApp(file_name=str(file_path))
    app.add_task("Task A")
    app.add_task("Task B")

    removed = app.delete_task(0)
    assert removed.description == "Task A"
    assert len(app.tasks) == 1
