# Python 系统教程

面向已有 Go 和 Python 基础的开发者，从语言语义到工程实践的中文教程。共 23 章，配套可运行的 SQLite 任务管理器与测试，使用 **MkDocs Material + GitHub Pages** 提供在线阅读。

**[开始阅读](docs/tutorial/00-导读与学习路线.md)** · **[知识点索引](docs/tutorial/20-知识点索引与参考资料.md)** · **[构建与发布](docs/deployment.md)** · **[验证记录](docs/validation.md)**

2026-10-26 按 **Python 官方教程、语言参考和标准库文档** 补全基础主线，重点扩写对象模型与工程、并发和进阶机制。新增内容围绕规则、执行时机、共享状态、失败反例与可执行断言展开；不新增第三方框架知识。

只学习 Python 基础时，按 **01—14 → 16 → 19—22** 阅读；15 章选读标准库网络与 SQLite，17 章用于综合练习，18.9 为 Python 3.14 语言特性。原有框架和生态内容保留为可选资料。集中查阅易混点请看 [19.12 易混点总表](docs/tutorial/19-练习答案与迁移陷阱.md)，对照官网覆盖范围请看 [20.1 官方教程覆盖表](docs/tutorial/20-知识点索引与参考资料.md)。

## 本地启动

建议使用 Python 3.14，便于同时执行完整教程验证。

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-docs.txt
.\.venv\Scripts\python.exe -m mkdocs serve
```

打开 `http://127.0.0.1:8000/`。macOS / Linux 使用 `.venv/bin/python`；已有虚拟环境时直接使用，无需重复创建。

站点提供中文全文搜索、按阶段分组的章节导航、页内目录、代码高亮与复制、深浅色主题和移动端阅读布局。样式采用简洁的 GitHub 文档配色和系统字体。

## 发布到 GitHub Pages

1. 将项目提交到 GitHub 仓库的默认分支。
2. 打开仓库 **Settings → Pages → Build and deployment**，将 **Source** 设为 **GitHub Actions**。
3. 默认分支 push 后自动运行 `.github/workflows/pages.yml`；也可在 Actions 页面手动运行 **Build and deploy documentation**。
4. 完成后，在工作流的 `github-pages` 环境或 Pages 设置中查看站点地址。

工作流自动识别默认分支与 Pages 地址，适配 `/仓库名/` 子路径；PR 执行检查和构建，发布在默认分支执行。产物通过官方 Pages artifact 流程发布。

## 项目结构

```text
.
├── .github/workflows/pages.yml  # 检查、构建、发布
├── docs/                       # 网站内容
│   ├── index.md                # 阅读首页
│   ├── tutorial/               # 23 章 Markdown 教程（00—22）
│   ├── assets/stylesheets/     # GitHub 风格样式
│   ├── examples.md             # 示例与合订版下载
│   ├── deployment.md           # 本地开发与 Pages 配置
│   └── validation.md           # 教程验证记录
├── examples/                   # 可运行示例与 SQLite 测试
├── scripts/                    # 合订版生成、构建钩子、验证工具
├── main.py                     # 原有学习脚本
├── mkdocs.yml                  # 主题、导航与 Markdown 配置
├── requirements-docs.txt       # 站点构建依赖
└── README.md
```

`docs/tutorial/` 是正文的唯一来源，新增或调整章节时同步维护 `mkdocs.yml`。`site/` 和根目录 `Python完整教程.md` 由构建生成，已加入忽略规则。示例、脚本和合订版会自动加入站点下载资源，无需手动维护副本。

## 教程路线

| 阶段 | 内容 |
| --- | --- |
| [00 导读](docs/tutorial/00-导读与学习路线.md) | 读者定位、学习路线与能力验收 |
| [01—07 语言基础](docs/tutorial/01-环境安装与基本语法.md) | 环境、对象、容器、控制流、函数、迭代器、模块 |
| [08—13 对象与工程](docs/tutorial/08-面向对象与数据建模.md) | 类、协议、类型提示、异常、文件、常用标准库 |
| [14—17 并发与实战](docs/tutorial/14-线程进程与异步编程.md) | 并发、网络数据库、测试、SQLite 任务管理器 |
| [18—22 进阶与速查](docs/tutorial/18-生态专题与扩展边界.md) | 生态、练习、索引、内置函数、高级机制 |

完整章节目录见站点导航或 [知识点索引](docs/tutorial/20-知识点索引与参考资料.md)。

## 示例与验证

在仓库根目录使用虚拟环境中的 Python，或已安装构建依赖的 Python：

```shell
python examples/task_cli.py --db demo-tasks.db add "学习 Python 对象模型"
python examples/task_cli.py --db demo-tasks.db list
python -B scripts/build_book.py
python -B -m unittest discover -s examples -p "test_*.py" -v
python -B scripts/verify_tutorial.py
python -m mkdocs build --strict
python -B scripts/verify_site.py
```

`build_book.py` 生成根目录的完整合订版。站点构建也会从分章自动生成 `.txt` 格式的 Markdown 源文下载版。

主体内容面向 Python 3.11+，新版本特性单独标注；完整教程代码块验证需要 Python 3.14+。第三方框架、外部服务和其他环境的验证边界见 [验证记录](docs/validation.md)。
