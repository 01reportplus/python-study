"""SQLite 任务管理器。仅依赖标准库，面向 Python 3.11+。"""

from __future__ import annotations

import argparse
from contextlib import contextmanager
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import sqlite3
import sys
from collections.abc import Iterator, Sequence


class TaskError(Exception):
    """可向命令行用户直接解释的业务错误。"""


class TaskNotFound(TaskError):
    """指定任务不存在。"""


@dataclass(frozen=True, slots=True)
class Task:
    id: int
    title: str
    done: bool
    created_at: str


class TaskRepository:
    """持有一个连接；通过上下文管理显式释放，不跨线程共享。"""

    def __init__(self, database: str | Path):
        self._connection = sqlite3.connect(str(database), timeout=5)
        try:
            self._connection.row_factory = sqlite3.Row
            self._connection.execute("PRAGMA foreign_keys = ON")
            self._connection.execute(
                """CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY,
                    title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 200),
                    done INTEGER NOT NULL DEFAULT 0 CHECK(done IN (0, 1)),
                    created_at TEXT NOT NULL
                )"""
            )
            self._connection.commit()
        except BaseException:
            self._connection.close()
            raise

    def __enter__(self) -> TaskRepository:
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        self.close()
        return False

    def close(self) -> None:
        self._connection.close()

    @contextmanager
    def transaction(self) -> Iterator[TaskRepository]:
        """一个业务工作单元，不支持嵌套事务。"""
        if self._connection.in_transaction:
            raise TaskError("不支持嵌套事务")
        try:
            self._connection.execute("BEGIN")
            yield self
            self._connection.commit()
        except BaseException:
            self._connection.rollback()
            raise

    @staticmethod
    def _task(row: sqlite3.Row) -> Task:
        return Task(row["id"], row["title"], bool(row["done"]), row["created_at"])

    def add(self, title: str) -> Task:
        title = title.strip()
        if not 1 <= len(title) <= 200:
            raise TaskError("标题去除首尾空白后必须为 1..200 个字符")
        created_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
        cursor = self._connection.execute(
            "INSERT INTO tasks(title, created_at) VALUES (?, ?)", (title, created_at)
        )
        task_id = cursor.lastrowid
        if task_id is None:
            raise RuntimeError("数据库未返回任务 ID")
        return self.get(task_id)

    def get(self, task_id: int) -> Task:
        row = self._connection.execute(
            "SELECT id, title, done, created_at FROM tasks WHERE id = ?", (task_id,)
        ).fetchone()
        if row is None:
            raise TaskNotFound(f"任务 {task_id} 不存在")
        return self._task(row)

    def list_tasks(self, status: str = "all", limit: int = 100, offset: int = 0) -> list[Task]:
        if status not in {"all", "todo", "done"}:
            raise TaskError("status 必须为 all / todo / done")
        if not 1 <= limit <= 1000 or offset < 0:
            raise TaskError("limit 必须为 1..1000，offset 不能为负")
        sql = "SELECT id, title, done, created_at FROM tasks"
        parameters: list[int] = []
        if status != "all":
            sql += " WHERE done = ?"
            parameters.append(int(status == "done"))
        sql += " ORDER BY id LIMIT ? OFFSET ?"
        parameters.extend([limit, offset])
        return [self._task(row) for row in self._connection.execute(sql, parameters)]

    def mark_done(self, task_id: int) -> Task:
        # 同一任务重复完成仍成功，体现幂等行为。
        self.get(task_id)
        self._connection.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
        return self.get(task_id)

    def delete(self, task_id: int) -> None:
        cursor = self._connection.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        if cursor.rowcount == 0:
            raise TaskNotFound(f"任务 {task_id} 不存在")


def positive_int(raw: str) -> int:
    value = int(raw)
    if value <= 0:
        raise argparse.ArgumentTypeError("必须为正整数")
    return value


def nonnegative_int(raw: str) -> int:
    value = int(raw)
    if value < 0:
        raise argparse.ArgumentTypeError("不能为负数")
    return value


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="SQLite 任务管理器")
    parser.add_argument("--db", default="tasks.db", help="数据库文件（默认 tasks.db）")
    parser.add_argument("--json", action="store_true", help="以 JSON 输出")
    commands = parser.add_subparsers(dest="command", required=True)
    add = commands.add_parser("add", help="新增任务")
    add.add_argument("title")
    listing = commands.add_parser("list", help="查询任务")
    listing.add_argument("--status", choices=["all", "todo", "done"], default="all")
    listing.add_argument("--limit", type=positive_int, default=100)
    listing.add_argument("--offset", type=nonnegative_int, default=0)
    for command, description in [("done", "完成任务"), ("delete", "删除任务")]:
        subparser = commands.add_parser(command, help=description)
        subparser.add_argument("id", type=positive_int)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        with TaskRepository(args.db) as repository:
            match args.command:
                case "add":
                    with repository.transaction():
                        tasks = [repository.add(args.title)]
                case "list":
                    tasks = repository.list_tasks(args.status, args.limit, args.offset)
                case "done":
                    with repository.transaction():
                        tasks = [repository.mark_done(args.id)]
                case "delete":
                    with repository.transaction():
                        repository.delete(args.id)
                    tasks = []
                case _:
                    raise TaskError("未知命令")
        if args.json:
            print(json.dumps([asdict(task) for task in tasks], ensure_ascii=False))
        elif args.command == "delete":
            print(f"已删除任务 {args.id}")
        else:
            for task in tasks:
                marker = "x" if task.done else " "
                print(f"{task.id}\t[{marker}] {task.title}\t{task.created_at}")
        return 0
    except (TaskError, sqlite3.Error, OSError) as exc:
        print(f"错误：{exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
