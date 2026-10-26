# 教程验证记录

## Python 基础补全（2026-10-26）

本次对照 Python 官网教程、固定 3.14 系列语言参考、HOWTO 与标准库文档扩写。仅增加 Python 语言和标准库基础内容；原有第三方框架部分不扩写。正文来源仍为 `docs/tutorial/`，合订版和网站下载从同一份正文生成。

### 内容与结构

- 保留 23 章文件名、章标题、222 个二级节及原顺序；20 章有内容补充或导读更新。
- 在 56 个原有二级节下补充专题，并更新 00 章的基础学习范围和版本表。
- 分章正文从 181,636 字符增至 228,852 字符，新增 47,216 字符（含代码、标点、表格和链接，不是纯中文字数）。
- Python 代码块从 241 个增至 287 个；实际执行从 218 个增至 264 个，新增 46 个可自动执行示例。其余 23 个仍仅编译检查。
- 19.12 节增加 82 组易混概念对照，19.13 节补充综合自测；20.1 节对照官网教程主题，20.5 节记录本次官方来源。
- 校验修改前快照，`main.py` 和 `examples/*.py` 的 SHA-256 保持一致；第 15、17、18 章正文未修改。
- 文件围栏配对、章标题/二级目录、替换字符和 Git 空白检查通过。结构检查只把 Markdown 标题计入目录，不将代码围栏内的 Python 注释误认为标题。

### 实际运行环境与检查结果

Windows / CPython **3.14.5**。教程块由 `D:\develop\env\python\python.exe` 执行；站点构建使用项目 `.venv\Scripts\python.exe`（同为 3.14.5），MkDocs 1.6.1。

```text
python -B scripts/build_book.py
chapters=23

python -B scripts/verify_tutorial.py
documents=28 python_blocks=287 executed=264 local_links=81
failures=0

python -B -m unittest discover -s examples -p 'test_*.py' -v
Ran 12 tests
OK
```

新执行示例覆盖：定义/装饰/调用时机、方法绑定、MRO 参数协作、dataclass 字段分类、Enum 别名、运算协商、特殊方法类型查找、延迟注解、异常组剩余错误、异步资源逆序清理、Future 超时后仍运行、队列关闭、协程重复等待、shield、单线程异步竞争、ContextVar 共享对象、缓存返回对象共享，以及真实文件的 `python -m` 包入口。

**新增 14.6 的 spawn 示例已真实启动子进程**，验证参数经传输后对子列表的修改不影响父进程列表。旧进程池教学块仍仅做语法检查；不能把一项新增进程实验表述为全部进程模式均已验证。

站点检查使用 `mkdocs build --strict` 和 `scripts/verify_site.py`，覆盖默认根路径与 `https://example.github.io/python-study01/` 子路径，检查 28 个 HTML 页面、23 个章节，以及站内锚点、canonical、搜索索引、下载和静态资源。构建产物中的合订版下载与本地生成文件另作字节一致性检查。Material 输出了上游 MkDocs 2.0 的提示信息，本次仍使用已有 MkDocs 1.6.1。

### 验证边界

- 标记代码块在独立 UTF-8 解释器和临时目录中执行，通过 assert 检查行为；未标记块只编译。`tmp/` 用于当前环境的临时文件，测试命令把 TMP/TEMP 指向该目录。
- 本次新增示例只使用标准库，不访问外部业务服务、不安装第三方框架。
- 没有运行 mypy/Pyright、wheel 构建安装、真实外部 HTTP/数据库服务、自由线程构建、InterpreterPoolExecutor 或实验性 JIT。
- 没有验证 Python 3.11—3.13、Linux/macOS，也没有发布站点或运行线上 GitHub Actions。版本适用范围由正文标注，实际执行结论限定为本机版本。
- 网站检查是构建和 HTML/链接检查，本次没有重新进行浏览器交互或截图验收。
- 官方来源已用于语义核对，不代表已逐页审阅全部官方站点；教程主题覆盖不等于标准库全部 API 或解释器内部实现的穷举。

下面保留 2026-10-20 的历史记录，其中运行数量和“未执行进程池”等表述属于当时状态，本次结果以上文为准。

> 以下记录保留 2026-10-20 教程内容扩写时的验证结果。GitHub Pages 整理后，章节路径为
> `docs/tutorial/`，本记录路径为 `docs/validation.md`；站点构建与检查命令见
> [构建与发布](deployment.md)。文中“原有 .gitignore 未修改”等描述指当时的内容扩写，
> 本次 Pages 整理已另外添加站点产物和 Python 临时文件的忽略规则。

验证日期：2026-10-20。环境：Windows，CPython 3.14.5（`D:\develop\env\python\python.exe`），由本轮实际执行确认。

## 内容规模

- 23 章分章文档（00—22），保留原文件名、章标题、222 个二级节编号及顺序。
- 在 73 个原有小节中扩写，形成 77 个三级讲解主题；各章增加阅读目标。
- 分章正文约 18.2 万字符，修改前约 11.9 万字符；含代码、标点与链接，不是中文纯文字字数。
- 241 个 Python 代码块，其中 218 个标记为自动执行，23 个仅检查语法。
- 修改前基线为 190 个代码块、175 个实际执行，本轮新增 43 个可自动执行示例；包章节移除了一个不完整的旧占位代码块。
- 同时提供完整合订版，内容由分章自动生成。

## 验证命令

在项目根目录执行：

```powershell
python -B scripts/build_book.py
python -B -m unittest discover -s examples -p 'test_*.py' -v
python -B scripts/verify_tutorial.py
```

## 验证范围

1. 对每个分章中的完整 Python 代码块进行编译检查。
2. 对标记为 `verify: run` 的 218 个代码块，在独立解释器和临时工作目录中运行；示例内断言验证输出语义。
3. 检查 README、分章、合订版与本记录中的本地 Markdown 文件链接。
4. 编译检查 examples 与 scripts 中的 Python 源文件。
5. 任务管理器的 12 个测试使用真实 SQLite，覆盖输入校验、分页、状态过滤、幂等、事务回滚、表约束、SQL 参数化、退出码和跨进程持久化。

本轮所执行的教程示例不安装依赖、不访问外部网络。验证器用于可信教材，不是安全沙箱；`-I` 和临时目录不会禁止任意代码访问网络或其他文件。临时数据位于当前仓库的 `tmp/` 下，以兼容当前受限环境；运行示例的临时子目录由 TemporaryDirectory 清理。

另外对照修改前本地快照，检查章节文件名、一级标题、二级编号与顺序、代码围栏配对、尾随空白及替换字符；确认原有 examples 中的任务管理器与测试内容没有改变。旧文件本轮开始时均为未跟踪状态，因此结构对照使用工作区修改前快照，而不是把 Git 未跟踪状态误认为文件是本轮新建。

新增运行验证包括：元组增强赋值的失败后状态、Decimal 非有限值拒绝、参数绑定错误、异步装饰器异常传播、一次性迭代与资源关闭、模块绑定、描述符优先级、严格 JSON、CSV 记录错误、暂存写入失败保留旧文件、线程库存不变量、TaskGroup 失败清理、SQLite 显式事务回滚、批量导入、游标分页和有界异步流水线失败退出。

## 未执行的部分

- 第三方库示例仅做语法检查，未安装 NumPy、pandas、SQLAlchemy、FastAPI、requests、Matplotlib、Pillow 等依赖。
- 第 07 章的多文件包示例仅编译各 Python 片段，未实际组装安装 wheel；TOML、SQL 和 shell 块没有由代码块验证器逐块执行。
- 未安装或运行 mypy / Pyright；故意展示静态类型错误的示例不能被描述为类型检查通过。
- 交互输入、断点、GUI、外部 HTTP / TLS、真实 PostgreSQL / MySQL、打包安装命令没有自动执行。
- 进程池教学片段需要保存成独立脚本运行，本轮只做语法检查；线程与 asyncio 标记示例已实际执行。
- 没有运行真实 Web 服务器、发送邮件、上传或发布任何内容。
- 未针对 Python 3.11—3.13、自由线程构建、PyPy、Linux / macOS 或生产环境进行兼容验证。
- 本地链接检查只验证文件目标存在，不检查 Markdown 锚点、浏览器渲染或所有外部 URL 的状态。合订版代码从分章生成，避免重复执行同一示例。

## 参考资料访问

本轮读取 Python 官方中文教程、廖雪峰 introduction 页面、W3Schools Python 首页、PythonTutorial.net 首页，并核对相关官方专题文档。菜鸟指定元组页两次返回 HTTP 530，未获取正文，没有声称已经核查该页。

用户提供的 Python `/3/` 链接当时显示 3.15.0；本机仍为 3.14.5。固定 `/3.14/` 文档对应该小版本系列的在线补丁版本，不能当作本机补丁版本实测。完整来源与使用范围见 [第 20 章](tutorial/20-知识点索引与参考资料.md)。

## 结果

最终验证通过，命令输出为：

```text
chapters=23
Ran 12 tests
OK
documents=24 python_blocks=241 executed=218 local_links=60
failures=0
```

`documents=24` 指 README 与 23 份分章；合订版和本记录也进行了链接检查，代码块只按分章验证一次，避免重复计数。

本文中的“覆盖”指教学主题覆盖，不能替代目标应用的集成测试、部署验证或生产安全审计。

原有 main.py、.gitignore、任务管理器与项目测试未修改。本轮更新原有 tutorial/ 文档、README、验证记录、合订版，以及生成器中的合订版标题和日期说明。

## GitHub Pages 整理验证（2026-10-20）

- 原 23 章迁移到 `docs/tutorial/` 后逐文件 SHA-256 与迁移前一致。
- 原有 `main.py`、任务管理器和 12 个测试的源码校验值与整理前一致。
- 完整教程验证：`documents=28 python_blocks=241 executed=218 local_links=59`，`failures=0`。
- 任务管理器：12 个 unittest 测试全部通过。
- 使用 `SITE_URL=https://example.github.io/python-study01/` 执行 `mkdocs build --strict` 成功。
- 构建产物检查：28 个 HTML 页面、23 章，站内链接与资源目标检查 `failures=0`。
- 检查范围包括本地锚点、规范地址、Pages 子路径、样式与脚本资源、搜索索引、源码下载的一致性及合订版存在性。
- 浏览器实际打开首页，搜索“事务”返回相关章节，深浅色主题切换正常。
- 构建依赖安装于项目 `.venv/`，`pip check` 通过；工作流 YAML 可解析，部署权限与构建依赖关系已检查。

以上是本地 Windows / Python 3.14.5 的结果。当前仓库没有配置远程地址，尚未在 GitHub 上运行 Actions 或验证线上 Pages；Linux 构建与部署结果以首次 Actions 执行为准。

