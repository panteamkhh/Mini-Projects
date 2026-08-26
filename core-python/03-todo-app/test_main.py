"""
Unit tests for the todo app.

Covers the pure data/logic layer of both versions:
- todo_procedural.load_tasks / save_tasks
- todo_oop.Task / TaskManager

The interactive CLI loops (input()/print() driven) are not covered by
automated tests here, since they wrap the tested logic almost directly.
"""

import json

import pytest

import todo_procedural
from todo_oop import Task, TaskManager


# ---------------------------------------------------------------------------
# Shared fixture: point both versions at a throwaway file per test
# ---------------------------------------------------------------------------
@pytest.fixture
def tasks_file(tmp_path, monkeypatch):
    file_path = tmp_path / "tasks.json"
    monkeypatch.setattr(todo_procedural, "FILE_NAME", str(file_path))
    return file_path


# ---------------------------------------------------------------------------
# Procedural version
# ---------------------------------------------------------------------------
class TestProceduralLoadTasks:
    def test_missing_file_returns_empty_list(self, tasks_file):
        assert todo_procedural.load_tasks() == []

    def test_empty_file_returns_empty_list(self, tasks_file):
        tasks_file.write_text("")
        assert todo_procedural.load_tasks() == []

    def test_corrupted_json_returns_empty_list(self, tasks_file):
        tasks_file.write_text("{not valid json")
        assert todo_procedural.load_tasks() == []

    def test_wrong_shape_returns_empty_list(self, tasks_file):
        tasks_file.write_text(json.dumps({"not": "a list"}))
        assert todo_procedural.load_tasks() == []

    def test_valid_file_loads_correctly(self, tasks_file):
        data = [{"task": "Buy milk", "done": False}]
        tasks_file.write_text(json.dumps(data))
        assert todo_procedural.load_tasks() == data


class TestProceduralSaveTasks:
    def test_save_then_load_roundtrip(self, tasks_file):
        data = [{"task": "Walk dog", "done": True}]
        assert todo_procedural.save_tasks(data) is True
        assert todo_procedural.load_tasks() == data

    def test_save_returns_false_on_os_error(self, tasks_file, monkeypatch):
        def raise_oserror(*args, **kwargs):
            raise OSError("disk full")

        monkeypatch.setattr("builtins.open", raise_oserror)
        assert todo_procedural.save_tasks([{"task": "x", "done": False}]) is False


class TestProceduralAddTask:
    def test_add_task_appends_and_saves(self, tasks_file, monkeypatch):
        tasks = []
        monkeypatch.setattr("builtins.input", lambda _: "Buy milk")
        todo_procedural.add_task(tasks)
        assert tasks == [{"task": "Buy milk", "done": False}]
        assert todo_procedural.load_tasks() == tasks

    def test_add_empty_task_is_ignored(self, tasks_file, monkeypatch):
        tasks = []
        monkeypatch.setattr("builtins.input", lambda _: "   ")
        todo_procedural.add_task(tasks)
        assert tasks == []


# ---------------------------------------------------------------------------
# OOP version
# ---------------------------------------------------------------------------
class TestTask:
    def test_to_dict(self):
        task = Task("Buy milk", done=True)
        assert task.to_dict() == {"task": "Buy milk", "done": True}

    def test_from_dict(self):
        task = Task.from_dict({"task": "Walk dog", "done": False})
        assert task.description == "Walk dog"
        assert task.done is False

    def test_toggle(self):
        task = Task("Read book")
        assert task.done is False
        task.toggle()
        assert task.done is True
        task.toggle()
        assert task.done is False


class TestTaskManagerLoading:
    def test_missing_file_starts_empty(self, tmp_path):
        manager = TaskManager(str(tmp_path / "tasks.json"))
        assert manager.tasks == []

    def test_corrupted_file_starts_empty(self, tmp_path):
        path = tmp_path / "tasks.json"
        path.write_text("not json at all")
        manager = TaskManager(str(path))
        assert manager.tasks == []

    def test_wrong_shape_starts_empty(self, tmp_path):
        path = tmp_path / "tasks.json"
        path.write_text(json.dumps({"oops": True}))
        manager = TaskManager(str(path))
        assert manager.tasks == []

    def test_valid_file_loads_tasks(self, tmp_path):
        path = tmp_path / "tasks.json"
        path.write_text(json.dumps([{"task": "Buy milk", "done": True}]))
        manager = TaskManager(str(path))
        assert len(manager.tasks) == 1
        assert manager.tasks[0].description == "Buy milk"
        assert manager.tasks[0].done is True


class TestTaskManagerMutations:
    def test_add_appends_and_persists(self, tmp_path):
        path = tmp_path / "tasks.json"
        manager = TaskManager(str(path))
        manager.add("Buy milk")

        assert len(manager.tasks) == 1
        reloaded = TaskManager(str(path))
        assert reloaded.tasks[0].description == "Buy milk"

    def test_delete_removes_and_persists(self, tmp_path):
        path = tmp_path / "tasks.json"
        manager = TaskManager(str(path))
        manager.add("Buy milk")
        manager.add("Walk dog")

        removed = manager.delete(0)
        assert removed.description == "Buy milk"
        assert len(manager.tasks) == 1

        reloaded = TaskManager(str(path))
        assert len(reloaded.tasks) == 1
        assert reloaded.tasks[0].description == "Walk dog"

    def test_toggle_flips_done_and_persists(self, tmp_path):
        path = tmp_path / "tasks.json"
        manager = TaskManager(str(path))
        manager.add("Buy milk")

        toggled = manager.toggle(0)
        assert toggled.done is True

        reloaded = TaskManager(str(path))
        assert reloaded.tasks[0].done is True

    def test_delete_out_of_range_raises(self, tmp_path):
        manager = TaskManager(str(tmp_path / "tasks.json"))
        with pytest.raises(IndexError):
            manager.delete(0)

    def test_is_valid_index(self, tmp_path):
        manager = TaskManager(str(tmp_path / "tasks.json"))
        manager.add("Buy milk")
        assert manager.is_valid_index(0) is True
        assert manager.is_valid_index(1) is False
        assert manager.is_valid_index(-1) is False
