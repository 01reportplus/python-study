"""把分章教程汇总为单文件 Markdown，不依赖第三方包。"""

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def render_book():
    chapters = sorted((ROOT / "docs" / "tutorial").glob("[0-9][0-9]-*.md"))
    if not chapters:
        raise RuntimeError("docs/tutorial/ 下没有教程章节")
    parts = [
        "# Python 系统教程：面向已有 Go 和 Python 基础的开发者（完整合订版）\n",
        "> 修订日期：2026-10-20。实际验证环境与范围见 docs/validation.md。\n"
        "> 本文由分章文档自动汇总；修改请优先编辑 docs/tutorial/ 下的章节，再运行 scripts/build_book.py。\n",
        "本文覆盖语言核心、主要运行机制、常见标准库和工程路径；第三方生态提供入门示例和深入方向，"
        "不宣称逐项覆盖全部第三方 API 或解释器内部实现。\n",
        "[分章目录](README.md) · [验证记录](docs/validation.md)\n",
        "## 阅读目录\n",
    ]
    for chapter in chapters:
        title = chapter.read_text(encoding="utf-8").splitlines()[0].removeprefix("# ")
        parts.append(f"- [{title}](docs/tutorial/{chapter.name})")
    for chapter in chapters:
        content = chapter.read_text(encoding="utf-8")
        # 分章内部链接按合订版所在目录重新定位。
        content = content.replace("](" + "../examples/", "](examples/")
        content = content.replace("](" + "../scripts/", "](scripts/")
        content = re.sub(r"\]\((\d{2}-[^)]+\.md)\)", r"](docs/tutorial/\1)", content)
        parts.append("\n---\n\n" + content)
    return "\n".join(parts) + "\n"


def main():
    output = ROOT / "Python完整教程.md"
    output.write_text(render_book(), encoding="utf-8")
    chapters = list((ROOT / "docs" / "tutorial").glob("[0-9][0-9]-*.md"))
    print(f"chapters={len(chapters)} output={output}")


if __name__ == "__main__":
    main()
