# 示例与下载

示例使用 Python 标准库，可在本机运行。GitHub Pages 提供文档和源码下载，Python 命令在你的本地终端执行。

## 源码文件

| 文件 | 用途 |
| --- | --- |
| [task_cli.py](examples/task_cli.py) | SQLite 任务管理器，包含模型、仓储、事务与 CLI |
| [test_task_cli.py](examples/test_task_cli.py) | 任务管理器的 12 个测试 |
| [verify_tutorial.py](scripts/verify_tutorial.py) | 教程代码块与本地链接检查器；完整运行请克隆仓库 |
| [build_book.py](scripts/build_book.py) | 从分章文档生成完整合订版；在仓库根目录运行 |

下载任务管理器和测试文件后，将二者放在同一个 `examples/` 目录中：

```shell
python examples/task_cli.py --db demo-tasks.db add "完成 Python 教程"
python examples/task_cli.py --db demo-tasks.db list
python examples/task_cli.py --db demo-tasks.db done 1
python -B -m unittest discover -s examples -p "test_*.py" -v
```

`demo-tasks.db` 是本地运行时创建的数据文件。

## 完整合订版

[打开 / 保存完整教程 Markdown 源文](downloads/Python完整教程.txt){ .md-button }

下载文件使用 `.txt` 扩展名以便浏览器直接查看；保存后可以改名为 `Python完整教程.md`。
合订版中的相对链接按仓库根目录组织，分章跳转需要配套仓库；在线阅读请使用本站章节导航。

合订版在每次站点构建时直接从 `docs/tutorial/` 生成，与章节正文保持一致；下载文件不会重复进入全文搜索。
在本地仓库中也可以生成根目录下的合订版：

```shell
python -B scripts/build_book.py
```
