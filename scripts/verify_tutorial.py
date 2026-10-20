"""检查 Markdown 本地链接、Python 代码块，并隔离执行显式标记示例。

默认不安装依赖、不访问外网。每个示例在独立临时目录、独立解释器运行。
适用于本教程可信源码，不是用于执行不可信 Markdown 的安全沙箱。
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Block:
    path: Path
    line: int
    code: str
    run: bool


def blocks(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    index = 0
    while index < len(lines):
        if lines[index].strip() != "```python":
            index += 1
            continue
        start = index + 1
        run = index > 0 and lines[index - 1].strip() == "<!-- verify: run -->"
        index += 1
        body = []
        while index < len(lines) and lines[index].strip() != "```":
            body.append(lines[index])
            index += 1
        if index == len(lines):
            raise ValueError(f"{path}:{start} 代码围栏未闭合")
        yield Block(path, start + 1, "\n".join(body) + "\n", run)
        index += 1


def main():
    if sys.version_info < (3, 14):
        print("验证完整教程需要 Python 3.14+（包含新版语法示例）", file=sys.stderr)
        return 2
    documents = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
    link_documents = [*documents, ROOT / "Python完整教程.md"]
    temporary_root = ROOT / "tmp" / "tutorial-verification"
    temporary_root.mkdir(parents=True, exist_ok=True)
    failures = []
    compiled = executed = links = 0
    for source in [*sorted((ROOT / "examples").glob("*.py")), *sorted((ROOT / "scripts").glob("*.py"))]:
        try:
            compile(source.read_text(encoding="utf-8"), str(source), "exec")
        except SyntaxError as exc:
            failures.append(f"{source.name}: 语法失败 {exc}")
    for document in link_documents:
        if not document.exists():
            failures.append(f"缺少文档 {document.name}")
            continue
        text = document.read_text(encoding="utf-8")
        prose = re.sub(r"```[^\n]*\n.*?```", "", text, flags=re.DOTALL)
        prose = re.sub(r"`[^`]+`", "", prose)
        for target in re.findall(r"(?<!!)\[[^\]]+\]\(([^)]+)\)", prose):
            if "://" in target or target.startswith("#"):
                continue
            destination = target.split("#", 1)[0]
            # Material attribute lists and MkDocs-generated source downloads.
            resolved = (document.parent / destination).resolve()
            relative = resolved.relative_to(ROOT).as_posix()
            if relative.startswith(("docs/examples/", "docs/scripts/")):
                resolved = ROOT / relative.removeprefix("docs/")
            elif relative == "docs/downloads/Python完整教程.txt":
                resolved = ROOT / "Python完整教程.md"
            links += 1
            if not resolved.exists():
                failures.append(f"{document.name}: 链接不存在 {destination}")
        if document not in documents:
            continue
        for block in blocks(document):
            label = f"{document.name}:{block.line}"
            try:
                compile(block.code, label, "exec")
                compiled += 1
            except SyntaxError as exc:
                failures.append(f"{label}: 语法失败 {exc}")
                continue
            if not block.run:
                continue
            with TemporaryDirectory(prefix="example-", dir=temporary_root) as tmp:
                script = Path(tmp) / "example.py"
                script.write_text(block.code, encoding="utf-8")
                environment = dict(
                    os.environ, PYTHONUTF8="1", PYTHONDONTWRITEBYTECODE="1",
                    TMP=str(temporary_root), TEMP=str(temporary_root),
                )
                try:
                    result = subprocess.run(
                        [sys.executable, "-I", "-X", "utf8", "-B", str(script)],
                        cwd=tmp, env=environment, capture_output=True, text=True,
                        encoding="utf-8", timeout=15,
                    )
                    if result.returncode:
                        failures.append(f"{label}: 执行失败\n{result.stderr.strip()}")
                    else:
                        executed += 1
                except subprocess.TimeoutExpired:
                    failures.append(f"{label}: 执行超时")
    print(f"documents={len(documents)} python_blocks={compiled} executed={executed} local_links={links}")
    for failure in failures:
        print(failure, file=sys.stderr)
    print(f"failures={len(failures)}")
    return int(bool(failures))


if __name__ == "__main__":
    raise SystemExit(main())
