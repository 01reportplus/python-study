"""真实 SQLite 与 subprocess 行为测试，不需要第三方库。"""

from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from task_cli import TaskError, TaskNotFound, TaskRepository, main


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.repository = TaskRepository(":memory:")
        self.addCleanup(self.repository.close)

    def test_create_and_filter(self):
        with self.repository.transaction():
            first = self.repository.add("  学习 Python  ")
            second = self.repository.add("完成练习")
            self.repository.mark_done(first.id)
        self.assertEqual(self.repository.get(first.id).title, "学习 Python")
        self.assertEqual([t.id for t in self.repository.list_tasks("todo")], [second.id])
        self.assertEqual([t.id for t in self.repository.list_tasks("done")], [first.id])
        self.assertEqual([t.id for t in self.repository.list_tasks(limit=1, offset=1)], [second.id])

    def test_completion_is_idempotent(self):
        with self.repository.transaction():
            task = self.repository.add("A")
            once = self.repository.mark_done(task.id)
            twice = self.repository.mark_done(task.id)
        self.assertEqual(once, twice)
        self.assertTrue(twice.done)

    def test_transaction_rolls_back_all_changes(self):
        with self.assertRaises(TaskError):
            with self.repository.transaction():
                self.repository.add("先写入")
                self.repository.add("   ")
        self.assertEqual(self.repository.list_tasks(), [])

    def test_reject_invalid_title(self):
        for title in ["", "\t\n", "x" * 201]:
            with self.subTest(title=repr(title)):
                with self.assertRaises(TaskError):
                    self.repository.add(title)

    def test_missing_task(self):
        with self.assertRaises(TaskNotFound):
            self.repository.get(999)
        with self.assertRaises(TaskNotFound):
            with self.repository.transaction():
                self.repository.delete(999)

    def test_sql_is_parameterized(self):
        title = "'); DROP TABLE tasks; --"
        with self.repository.transaction():
            task = self.repository.add(title)
        self.assertEqual(self.repository.get(task.id).title, title)
        self.assertEqual(len(self.repository.list_tasks()), 1)

    def test_invalid_query_options(self):
        for kwargs in [{"status": "bad"}, {"limit": 0}, {"limit": 1001}, {"offset": -1}]:
            with self.subTest(kwargs=kwargs), self.assertRaises(TaskError):
                self.repository.list_tasks(**kwargs)

    def test_nested_transaction_rejected_and_rolled_back(self):
        with self.assertRaises(TaskError):
            with self.repository.transaction():
                self.repository.add("rollback")
                with self.repository.transaction():
                    pass
        self.assertEqual(self.repository.list_tasks(), [])

    def test_database_constraint(self):
        with self.assertRaises(sqlite3.IntegrityError):
            with self.repository.transaction():
                self.repository._connection.execute(
                    "INSERT INTO tasks(title, done, created_at) VALUES (?, ?, ?)", ("x", 2, "now")
                )


class CommandTests(unittest.TestCase):
    def test_persistence_and_json_across_processes(self):
        temporary_root = Path(__file__).resolve().parents[1] / "tmp"
        temporary_root.mkdir(exist_ok=True)
        with TemporaryDirectory(dir=temporary_root) as tmp:
            database = str(Path(tmp) / "tasks.db")
            script = str(Path(__file__).with_name("task_cli.py"))
            command = [sys.executable, "-X", "utf8", "-B", script, "--db", database, "--json"]
            created = subprocess.run(command + ["add", "中文任务"], check=True, capture_output=True, text=True, encoding="utf-8", timeout=10)
            task_id = json.loads(created.stdout)[0]["id"]
            subprocess.run(command + ["done", str(task_id)], check=True, capture_output=True, timeout=10)
            listed = subprocess.run(command + ["list", "--status", "done"], check=True, capture_output=True, text=True, encoding="utf-8", timeout=10)
            self.assertEqual(json.loads(listed.stdout)[0]["title"], "中文任务")
            self.assertIs(json.loads(listed.stdout)[0]["done"], True)
            subprocess.run(command + ["delete", str(task_id)], check=True, capture_output=True, timeout=10)
            empty = subprocess.run(command + ["list"], check=True, capture_output=True, text=True, encoding="utf-8", timeout=10)
            self.assertEqual(json.loads(empty.stdout), [])

    def test_business_error_uses_stderr(self):
        error, output = StringIO(), StringIO()
        with redirect_stderr(error), redirect_stdout(output):
            code = main(["--db", ":memory:", "done", "999"])
        self.assertEqual(code, 1)
        self.assertIn("不存在", error.getvalue())
        self.assertEqual(output.getvalue(), "")

    def test_invalid_cli_id(self):
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit) as caught:
            main(["done", "0"])
        self.assertEqual(caught.exception.code, 2)


if __name__ == "__main__":
    unittest.main()
