# Python 系统教程：面向已有 Go 和 Python 基础的开发者（完整合订版）

> 修订日期：2026-10-26。实际验证环境与范围见 docs/validation.md。
> 本文由分章文档自动汇总；修改请优先编辑 docs/tutorial/ 下的章节，再运行 scripts/build_book.py。

本次补全以 Python 官方教程、语言参考和标准库为依据，聚焦语言基础、对象协议、工程组织与并发。已有第三方生态内容保留为可选扩展，不属于本次学习主线；不宣称逐项覆盖全部标准库 API 或解释器内部实现。

[分章目录](README.md) · [验证记录](docs/validation.md)

## 阅读目录

- [00｜导读与学习路线](docs/tutorial/00-导读与学习路线.md)
- [01｜环境安装与基本语法](docs/tutorial/01-环境安装与基本语法.md)
- [02｜对象模型与基础类型](docs/tutorial/02-对象模型与基础类型.md)
- [03｜列表、元组、字典与集合](docs/tutorial/03-列表元组字典与集合.md)
- [04｜控制流与模式匹配](docs/tutorial/04-控制流与模式匹配.md)
- [05｜函数、作用域与装饰器](docs/tutorial/05-函数作用域与装饰器.md)
- [06｜迭代器、生成器与函数式工具](docs/tutorial/06-迭代器生成器与函数式工具.md)
- [07｜模块、包与依赖管理](docs/tutorial/07-模块包与依赖管理.md)
- [08｜面向对象与数据建模](docs/tutorial/08-面向对象与数据建模.md)
- [09｜协议、描述符与元编程](docs/tutorial/09-协议描述符与元编程.md)
- [10｜类型提示与泛型](docs/tutorial/10-类型提示与泛型.md)
- [11｜异常与上下文管理](docs/tutorial/11-异常与上下文管理.md)
- [12｜文件、编码与数据交换](docs/tutorial/12-文件编码与数据交换.md)
- [13｜常用标准库详解](docs/tutorial/13-常用标准库详解.md)
- [14｜线程、进程与异步编程](docs/tutorial/14-线程进程与异步编程.md)
- [15｜网络、数据库与 Web 开发](docs/tutorial/15-网络数据库与Web开发.md)
- [16｜测试、调试、性能与安全](docs/tutorial/16-测试调试性能与安全.md)
- [17｜综合实战：SQLite 任务管理器](docs/tutorial/17-综合实战任务管理器.md)
- [18｜生态专题与扩展边界](docs/tutorial/18-生态专题与扩展边界.md)
- [19｜练习、参考答案与迁移陷阱](docs/tutorial/19-练习答案与迁移陷阱.md)
- [20｜知识点索引与参考资料](docs/tutorial/20-知识点索引与参考资料.md)
- [21｜内置函数与标准库补充示例](docs/tutorial/21-内置函数与标准库补充示例.md)
- [22｜高级运行机制与设计案例](docs/tutorial/22-高级运行机制与设计案例.md)

---

# 00｜导读与学习路线

> 本章目标：读者定位、修订问题清单和学习路线。
>
> 阅读重点：已有 Go 与 Python 基础；先预测对象共享例子，再选择需要深入的章节。

## 0.1 你需要重建哪些认识

如果你已经用 Go 写过 API，也用 Python 编写过脚本，Python 的难点通常不是 `if` 怎么写，而是同一段看起来熟悉的代码为什么会产生不同结果。

| 主题 | Go 的已有经验 | Python 应建立的认识 |
|---|---|---|
| 变量 | 声明约束类型 | 名称绑定对象；对象有类型 |
| 参数 | Go 按值传递；slice / map 的复制不等于复制其数据 | 传递对象引用，重新绑定与修改对象要区分 |
| 容器 | slice、map、struct | 内置容器可以混合类型；类型提示不自动校验 |
| 接口 | Go 隐式实现接口 | 运行时鸭子类型；静态约束可用 Protocol |
| 错误 | error 返回值与显式处理 | 异常沿调用栈传播，调用方按边界处理 |
| 包 | Go package 与编译期依赖 | 模块导入会执行顶层语句，并有缓存 |
| 并发 | goroutine / channel、context | 线程、进程、asyncio 各有边界 |
| 清理 | defer 与显式 Close | `with` / `finally`；没有通用 `defer` 语句 |
| 泛型 | 编译器约束 | 大多数类型提示由外部检查器解释 |
| 访问控制 | 导出名称与包边界 | 约定与名称改写，不是强制安全边界 |

看下面的代码，先预测，再执行：

<!-- verify: run -->
```python
def change(items, count):
    items.append("新增")
    count += 1
    items = ["函数内重新绑定"]
    return count

values = ["原有"]
number = 10
result = change(values, number)
assert values == ["原有", "新增"]
assert number == 10
assert result == 11
```

函数里 `items` 和调用者的 `values` 最初指向同一个列表；`append` 改变这个列表。随后对 `items` 赋值只是改变局部名称绑定，不会替换调用者名称。整数不可变，`count += 1` 在这里会绑定到计算结果。把它简单背成“可变类型按引用、不可变类型按值”会误导你。

### 本轮审阅：原教程的问题与修改依据

审阅基线为本仓库 2026-10-20 修改前的 23 章、222 个二级主题。结论是：覆盖面较好，已有可运行示例和 SQLite 项目，但整体更接近速查笔记；对已经会写 Go 和 Python 的开发者，尚不足以形成独立设计、排错和交付能力。以下判断来自原文，而不是仅凭目录推测。

| 问题 | 原教程中的具体证据 | 对学习的影响 | 本轮修订方式 |
|---|---|---|---|
| 读者定位过时 | README 标题及本节仍面向 Go / Java；第 17 章用 Spring 工程作类比 | 不符合本次 Go / Python 基础读者，花篇幅解释不必要的入门类比 | 以 Go 经验校准已有 Python 直觉，增加跳读与能力验收 |
| 个别对照有事实错误 | 原 4.1 把 `?:` 写成“Go / Java”的表达形式 | 容易误以为 Go 也有三元运算符 | 明确 Go 无 `?:`，Python 使用条件表达式 |
| 核心规则有示例但推导不足 | 3.5 已讲元组不可变与可哈希，正文仅一个短例子；5.10 标题含异步装饰器而代码只演示同步包装 | 会复述结论，遇到部分副作用、异步错误捕获就不会解释 | 增加对象关系、执行步骤、失败反例、同步与异步完整对照 |
| 工程教程存在衔接缺口 | 7.2 的 service 导入被注释；7.6 指向 `billing.cli:main`，目录中没有 cli.py | 读者不能直接按图建包完成运行 | 给出配套文件、入口、安装与干净环境验收步骤 |
| 并发失败路径较少 | 14.8 主要演示 TaskGroup 成功；22.6 虽说明结果列表无界，未演示失败时生产者退出 | 容易把并发成功当成取消、背压和退出都正确 | 增加失败注入、清理断言和容量推导 |
| 类型章节缺少使用闭环 | 10.9 简述方差，10.10 只有一条 mypy 命令；没有完整外部数据到内部模型的示例 | 容易把注解误当校验，或用 Any 消除错误 | 分开静态契约、运行时解析、业务约束，给出检查预期 |
| 事务依赖默认配置 | 15.7 提醒事务配置差异，但没有展开 autocommit 模式；项目使用显式 BEGIN 配合默认连接配置 | 迁移版本或改连接选项后，可能错误照搬事务代码 | 增加模式对照、3.12+ 显式配置示例和项目约束说明 |
| 练习与工程验收不充分 | 19.11 列出扩展任务但只有设计概述；多处异常示例只有 except，没有 else 验证“必须抛错” | 读者容易把“没失败”当成已验证异常路径 | 加分层练习、输入矩阵、失败断言及批量事务完整答案 |
| 导航与验证边界不够具体 | 20 章主要按章号索引；旧验证器只查本地文件，不核对锚点或网络链接有效性 | 难以按症状定位；容易高估验证覆盖 | 增加症状索引、逐章验收和明确的验证说明 |

原教程已经正确涉及浅拷贝、默认参数、闭包、GIL、连接关闭、外部输入等重要边界，因此本次采用保留主线、加深原节的方式，不把已有正确内容重写成另一套目录。

### 参考站点各自承担什么角色

2026-10-20 实际读取了四个可访问站点的首页或目录。官方教程明确面向已有编程经验者；廖雪峰教程提供从语言到应用的学习路线；W3Schools 将容器操作拆成小主题并提供练习入口；PythonTutorial.net 区分基础、OOP、进阶、并发等路径。这里只参考组织方式，具体语义使用官方语言参考和标准库文档核对，不据首页推断整站所有文章均已审阅。

菜鸟教程指定的元组页面本轮两次读取均返回 HTTP 530，未获得正文，不能声称已逐项核查该页。元组语义改由官方内置类型资料和本地反例确认。来源链接与访问情况统一见第 20.4 节。

### 已有 Python 基础，应该跳过什么

你可以快速浏览打印、普通循环和单个容器方法；应重点完成三类题：预测共享对象的副作用，解释导入、装饰器、生成器的实际执行时机，以及证明异常后资源和事务状态正确。知道语法名词不算完成，能从一个失败现象定位到机制才算。

本书把“详细”落实为规则、对象或状态变化、可执行例子、失败边界、选择理由和练习验收。没有必要把每一个标准库函数都复制一遍；维护项目时更有价值的是知道何时查哪份文档、如何构造反例验证自己的理解。

## 0.2 版本策略

### 本次基础补全范围（2026-10-26）

本次以 Python 官网教程为主线，以固定 3.14 系列的语言参考和标准库文档核对细节，重点补充对象关系、属性协议、工程组织、类型提示、异常与资源、线程/进程/asyncio 及运行机制。新增内容不引入框架，现有章节文件名、章标题和二级目录保持不变。

只学 Python 基础时，主线为 **01—14、16、19—22**，第 17 章作为标准库综合实战；15 章选读 urllib/socket/sqlite3，18 章选读 18.9 的语言特性。其余已有第三方内容是可选历史扩展，不作为掌握对象模型和并发的前提。

“补全”按教学主题衡量：既能找到规则，也能解释反例、执行时机和失败后的状态。官网教程本身不是标准库逐 API 全集，本书也不把所有函数签名堆成百科；[第 20 章](docs/tutorial/20-知识点索引与参考资料.md) 提供官方主题覆盖表和进一步查阅入口，[第 19 章](docs/tutorial/19-练习答案与迁移陷阱.md) 提供易混点对照与自测。

本教程以本机实际可运行的 Python 3.14.5 验证示例，不把 `/3/` 在线文档所指版本当成你机器上的版本。在线文档会随 Python 发布变化；学习时优先选择与你解释器一致的版本。

| 能力 | 起始版本 | 本教程位置 |
|---|---|---|
| f-string、变量注解 | 3.6 | 01、02、10 |
| dict 插入顺序成为语言保证 | 3.7 | 03 |
| 海象表达式、仅位置参数 `/` | 3.8 | 04、05 |
| `list[int]`、字典 `\|` 合并 | 3.9 | 03、10 |
| `match`、`X \| None` | 3.10 | 04、10 |
| `TaskGroup`、`except*`、`tomllib` | 3.11 | 11、12、14 |
| `type Alias = ...`、类型参数语法 | 3.12 | 10 |
| 可选自由线程构建、TypeIs、队列 shutdown | 3.13 起 | 10、14 |
| 注解延迟求值、模板字符串 | 3.14 | 10、18 |
| Executor.map 的 buffersize、InterpreterPoolExecutor | 3.14 | 14、22 |

版本说明参考 [Python 3.14 新特性](https://docs.python.org/3/whatsnew/3.14.html)。不要把自由线程构建推断成“所有 Python 都没有 GIL”。

## 0.3 如何阅读代码块

绝大多数 Python 代码块可以独立复制到一个 `.py` 文件执行。输出用行内注释或紧接代码的文字解释；`assert` 同时给出预期结果。

带 `<!-- verify: run -->` 标记的块会被验证器实际执行。没有标记的块可能是多文件结构、需要参数 / GUI / 网络 / 第三方包，或适合手动探索的示例，正文会解释条件。shell、TOML、SQL 块按各自语言执行，不能直接当 Python 粘贴。

从仓库根目录运行命令。文件之间的相对导入必须从包入口启动，不能把其中一段截出来当普通脚本运行。

## 0.4 学习路线与验收

1. **语法和容器：01—04。** 能把 Go 的 slice / map 操作改写成清晰 Python，并解释浅拷贝。
2. **Python 编程方式：05—11。** 能写装饰器、生成器、上下文管理器，能选择 dataclass、Protocol 与普通类。
3. **工作中的 Python：12—16。** 能处理文件、日志、HTTP、SQLite，解释线程池和 asyncio 的选择。
4. **完整交付：17—19。** 跑通 CLI，增加查询条件，补上失败路径测试，并能打包和定位性能问题。

每天只读一个章节时，建议“预测输出 → 执行 → 改一处条件 → 解释结果 → 完成练习”。已有语言经验可以提高阅读速度，但不能代替亲自验证 Python 的对象语义。

### 面向 Go / Python 开发者的分层路线

| 阶段 | 先读 | 必须交付的练习结果 | 自测问题 |
|---|---|---|---|
| 校准语义 | 02、03、05、06 | 画清嵌套容器共享关系；写一次性流处理 | 函数何时运行？副作用发生在谁拥有的对象上？ |
| 建立模块边界 | 07—11 | 一个可安装包；可替换的仓储接口；失败时释放的资源 | 类型检查能证明什么？谁负责关闭连接？ |
| 处理真实输入 | 12、13、15 | CSV/JSON 输入解析；参数化 SQL；结构化错误 | 数据格式合法是否等于业务合法？ |
| 管理并发 | 14、22.6 | 有界队列；一个 worker 失败后全体退出 | 限制的是请求数、任务数、队列长度还是输出内存？ |
| 形成交付闭环 | 16、17、19 | 事务失败测试；独立进程 CLI；安装后入口检查 | 换目录、换进程、异常退出后还正确吗？ |
| 按需专攻 | 18、20—22 | 根据业务选择一个第三方方向 | 引入库解决什么问题？增加了什么运行前提？ |

每章开头说明本章目标，原有二级目录保持不变，详细内容放在对应节下。先读正文，再运行 `assert` 示例；故意修改一个输入触发异常，最后完成本章验收。需要网络或第三方环境的例子会单独说明，不把语法通过说成依赖和部署已验证。

建议建立自己的实验记录，每次只回答四项：输入是什么、预期状态是什么、实际状态是什么、偏差来自哪条规则。错误也要分类：SyntaxError 是语法阶段，导入失败是环境或组织问题，TypeError 常是对象协议不匹配，业务 ValueError 则需要查看领域约束。

## 0.5 参考资料如何使用

本教程参考了你提供的五个网站的主题组织；以 [Python 官方教程](https://docs.python.org/zh-cn/3/tutorial/index.html)、[语言参考](https://docs.python.org/3/reference/index.html) 和 [标准库参考](https://docs.python.org/3.14/library/index.html) 核对规则。第三方教程适合辅助学习，遇到语义冲突、旧版本语法、依赖安装变化时回到官方文档。

完整来源和专题导航见 [20 资料与知识索引](docs/tutorial/20-知识点索引与参考资料.md)。


---

# 01｜环境安装与基本语法

> 本章目标：定位解释器并建立可靠运行入口。
>
> 阅读重点：重点读环境证据、参数转换与退出码；熟悉的基本语法可以快速浏览。

## 1.1 解释器、语言与执行过程

Python 是语言；CPython 是常见的实现。执行 `.py` 时，CPython 会把源码编译为字节码并执行；导入模块时可能缓存 `.pyc`。它不等价于“逐行文本翻译”，也不等价于 Go 那样通常交付一个原生可执行文件。PyPy、嵌入式 Python 等实现有不同运行特点。

先确认命令实际指向哪里：

```powershell
Get-Command python, py
python --version
python -c "import sys; print(sys.executable); print(sys.version)"
python -m pip --version
```

`python -m pip` 使用当前解释器加载 pip，能减少“包安装到另一个 Python”的问题。Windows 的 `py` 启动器是否存在取决于安装方式，不要假定每台机器都有。

## 1.2 项目独立环境

`venv` 为项目提供独立的包安装位置，类似按项目隔离依赖，但不会像容器那样隔离操作系统，也不会替你锁定所有依赖版本。

已有 `.venv` 就直接使用，不必重建。新项目可以执行：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip --version
.\.venv\Scripts\Activate.ps1
python -c "import sys; print(sys.prefix); print(sys.base_prefix)"
deactivate
```

激活只是修改当前 shell 的命令解析环境。执行策略不允许激活脚本时，直接使用 `.venv\Scripts\python.exe`，无需修改全局执行策略。Linux / macOS 通常是 `python3 -m venv .venv` 与 `source .venv/bin/activate`。

### 把“解释器正确”变成可验证的证据

排查 IDE 能运行而终端不能运行时，按下面顺序确认：启动的可执行文件、包安装目录、工作目录、导入到的具体文件。虚拟环境名称相同并不能证明是同一个环境。

```powershell
Get-Command python -All
where.exe python
.\.venv\Scripts\python.exe -c "import sys,os; print(sys.executable); print(sys.prefix); print(sys.base_prefix); print(os.getcwd())"
.\.venv\Scripts\python.exe -m pip --version
```

预期：`sys.executable` 指向项目 `.venv`，`sys.prefix` 是虚拟环境，`sys.base_prefix` 是基础解释器目录，pip 路径也属于选定环境。IDE 要把解释器设置为同一个绝对路径。不要为了让一条命令成功同时修改系统 PATH、重装 Python 和复制依赖，否则会失去可定位的原因链。

venv 不复制整套操作系统，也不使项目脱离基础解释器永久存在。移动 `.venv` 目录通常不是可靠的部署方式；应记录依赖，在目标位置重建环境。Git 保存源码和依赖声明，不保存虚拟环境生成的可执行文件。

本仓库的完整代码块检查器要求 3.14+，因为它要编译 3.14 专题语法；普通主线示例以 3.11+ 为目标。选择 3.11 阅读时跳过带 3.12+、3.14 标记的代码块，不要把全书复制进同一个文件运行。

## 1.3 脚本、模块、交互式运行

```powershell
python main.py
python -m json.tool --help
python -c "print(sum(range(5)))"
python
```

`-m` 按模块搜索规则启动模块；脚本路径启动与模块启动的 `sys.path[0]`、包上下文可能不同。REPL 适合探索，正式业务代码保存为模块并写测试。

## 1.4 缩进、语句与命名

Python 用缩进表示代码块，通常每级四个空格。不混用 Tab 和空格。冒号开启复合语句块；普通语句不需要分号。

<!-- verify: run -->
```python
MAX_RETRIES = 3  # 常量是命名约定，不会阻止重新赋值
user_name = "jackie"

def greet(name):
    """返回面向用户的问候。"""
    if name:
        return f"你好，{name}"
    return "你好，访客"

assert greet(user_name) == "你好，jackie"
```

变量与函数用 `snake_case`，类名用 `PascalCase`，常量用 `UPPER_CASE`。不要把变量命名为 `list`、`str`、`id`，否则会遮蔽内置名称。

## 1.5 注释、文档字符串与多行表达式

`#` 是注释；函数 / 类 / 模块开头的字符串是文档字符串。三引号字符串本身仍然是表达式，不应把所有三引号都叫“多行注释”。

<!-- verify: run -->
```python
def total():
    """计算固定费用。

    返回值为整数元；这里只演示 docstring。
    """
    return (
        100
        + 20
        + 5
    )

assert total() == 125
assert "整数元" in total.__doc__
```

优先利用括号换行，避免行末反斜杠续行。`help(total)` 可以显示文档。

### 词法边界：源码编码、字符串前缀和软关键字

源码文件默认 UTF-8，与 `open()` 读取另一个数据文件时采用什么编码是两件事。标识符大小写敏感，可包含允许的 Unicode 字符；项目公共名称仍宜保持一致、避免视觉近似字符。`match`、`case`、`type` 等在指定语法位置才是软关键字，不必像 `if` 一样在所有地方禁止作为名称。

<!-- verify: run -->
```python
import keyword
assert keyword.iskeyword('class')
assert keyword.issoftkeyword('match')
assert 'ab' 'cd' == 'abcd'      # 相邻字面量拼接
assert r'\n' == '\\n'           # 原始字符串保留反斜杠
assert len('\n') == 1
assert len(r'\n') == 2
assert b'A'[0] == 65
```

`r` 改变字面量反斜杠处理，`b` 创建 bytes，`f` 执行插值并生成 str；组合前缀也必须符合语法。原始字符串不能以奇数个反斜杠结束；f-string 的表达式仍是 Python 表达式。3.14 的 `t` 模板字符串产生 Template 对象，保留插值信息，不是自动安全转义的 str，详见原有 18.9 节。缩进错误、未闭合字符串在解析阶段就失败，不能靠同一个尚未解析成功的源码块内部 try 修复。

## 1.6 赋值、解包与删除名称

<!-- verify: run -->
```python
x, y = 10, 20
x, y = y, x
assert (x, y) == (20, 10)
first, *middle, last = [1, 2, 3, 4]
assert (first, middle, last) == (1, [2, 3], 4)
a = b = []
a.append(1)
assert b == [1]  # 两个名称绑定同一个对象
del a           # 解除 a 的绑定，b 仍存在
assert b == [1]
```

解包数量不符会抛 `ValueError`。`del` 作用于名称、容器元素或属性，不意味着立即销毁对象。

## 1.7 输入输出与转换

交互示例需要人在终端输入：

```python
name = input("姓名：")  # 返回 str，不会自动变成数字
age = int(input("年龄："))
print("用户", name, "年龄", age, sep=" | ", end="\n")
```

不要使用 `eval(input())` 解析输入。`int("18")` 合法，`int("18.5")` 会抛 `ValueError`。参数、HTTP 请求和配置同样需要显式解析与校验。

## 1.8 运算符与优先级

<!-- verify: run -->
```python
assert 7 / 2 == 3.5       # 真除法
assert 7 // 2 == 3        # 向下取整
assert -7 // 2 == -4      # 与 Go 的整数截断不同
assert -7 % 2 == 1        # a == (a // b) * b + a % b
assert 2 ** 3 == 8        # 幂；^ 是按位异或
assert (5 ^ 3) == 6
assert (5 & 3) == 1
assert (1 << 3) == 8
assert -2 ** 2 == -4      # -(2 ** 2)
assert (-2) ** 2 == 4
assert 1 < 2 < 3          # 比较链，中间表达式只求值一次
```

常见优先级从高到低可记为：括号 / 调用 / 索引、幂、正负号、乘除取余、加减、位移、位运算、比较、`not`、`and`、`or`、条件表达式。复杂表达式加括号，比背完整表更可靠。

### 先确定类型，再判断运算含义

相同运算符可能调用不同对象协议：数字 `+` 是加法，字符串 `+` 是拼接，列表 `+` 构造新列表。`"2" + 3` 不自动转换为 `"23"`，而是 TypeError。Go 中很多类型冲突由编译器发现，Python 常在真正执行该表达式时才发现；测试必须覆盖会进入该表达式的路径。

<!-- verify: run -->
```python
def probe():
    events.append("called")
    return 5

events = []
assert 0 < probe() < 10
assert events == ["called"]  # 比较链只计算一次中间表达式

assert (-7 // 3, -7 % 3) == (-3, 2)
assert 7 == (7 // -3) * -3 + (7 % -3)
try:
    "2" + 3
except TypeError:
    pass
else:
    raise AssertionError("字符串和整数不能直接相加")
```

整除向下取整会影响分页、桶编号和时间区间。需要“向零截断”的业务算法应明确实现；不要用 `int(a / b)` 处理任意巨大整数，因为 `/` 转成浮点可能丢失精度。正数分页通常写 `(count + size - 1) // size`，并先验证 `size > 0`。

优先级表中的一处细节是：幂对右侧一元负号的结合方式和左侧不同，`2 ** -2` 是 `0.25`，而 `-2 ** 2` 是 `-4`。业务公式直接加括号，比依赖同事记住规则稳妥。

## 1.9 真值、短路与 None

<!-- verify: run -->
```python
assert not None
assert not 0
assert not ""
assert not []
assert bool("False") is True  # 非空字符串就是真
assert ("" or "默认") == "默认"
assert (3 and "继续") == "继续"

timeout = 0
effective = 30 if timeout is None else timeout
assert effective == 0
```

`and` / `or` 返回参与运算的对象，不强制返回布尔值。`value or default` 会把 `0`、空字符串等合法值也替换掉。表示“没有值”时用 `is None`。Python 没有 `null`、`nil`、`&&`、`||`、`++` 运算符。

## 1.10 最小入口

<!-- verify: run -->
```python
def main():
    print("Python 学习开始")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
```

入口保护让模块被导入时不自动执行主流程；`SystemExit(0)` 表示成功退出。进程池示例尤其需要入口保护。

练习：读取两个整数，打印真除法与整除结果；处理除数为零的情况。答案见第 19 章。

### 入口函数应与可测试逻辑分开

`main` 负责解析输入、调用逻辑和返回退出码。计算函数接收普通参数，不直接读取 `input()` 或全局 `sys.argv`，因此测试不需要模拟整个终端。

<!-- verify: run -->
```python
def ratio(left: str, right: str) -> tuple[float, int]:
    a, b = int(left), int(right)
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b, a // b

assert ratio("9", "2") == (4.5, 4)
for left, right in [("x", "2"), ("9", "0")]:
    try:
        ratio(left, right)
    except ValueError:
        pass
    else:
        raise AssertionError((left, right))
```

验收：能说明 `python file.py`、`python -m package` 和导入模块的差别；能证明运行解释器与 pip 一致；能解释 `0 or 10` 为什么会破坏“0 为合法配置”的语义。不要用代码长度评价是否学会了本章。

延伸：[官方解释器教程](https://docs.python.org/3.14/tutorial/interpreter.html)、[venv](https://docs.python.org/3.14/library/venv.html)。


---

# 02｜对象模型与基础类型

> 本章目标：从对象关系解释副作用与数据表示。
>
> 阅读重点：重点追踪名称、引用、可变性、数值精度和编码，不靠语法记忆猜结果。

## 2.1 名称、对象、身份和值

Python 中名称是访问对象的入口。每个对象有身份、类型和值。`type()` 看类型；`==` 询问相等性；`is` 询问是否同一对象。不要根据小整数或字符串驻留的偶然现象使用 `is` 比值。

<!-- verify: run -->
```python
a = [1, 2]
b = [1, 2]
c = a
assert a == b and a is not b
assert a is c
assert type(a) is list
assert isinstance(True, int)  # bool 是 int 的子类
```

`isinstance` 考虑继承关系；`type(x) is T` 只接受精确类型。外部输入要不要接受 `bool` 作为整数，需要显式决定。

### 赋值、传参、删除：始终追踪对象关系

`a = b` 使两个名称引用同一个对象；函数参数也绑定到传入对象。函数内部重新绑定参数，不会替换调用者的名称；修改共享对象会被调用者看见。“传值还是传引用”容易把不同语言的术语混在一起，这里直接区分重新绑定与原地修改。

<!-- verify: run -->
```python
def change(values):
    values.append(2)
    values = [99]
    return values

original = [1]
returned = change(original)
assert original == [1, 2] and returned == [99]
alias = original
del original
assert alias == [1, 2]
```

`del name` 删除名称绑定，`del items[i]` 则请求容器删除元素；二者都不是直接调用对象析构函数。对象仍被其他名称、容器、闭包或缓存引用时，删除一个名称不会令它消失。`id()` 只在对象存活期间区分身份，不适合持久化 ID；两个先后创建且互不存活的对象可能复用标识。

## 2.2 可变对象、不可变对象与增强赋值

整数、浮点数、字符串、元组不可变；列表、字典、集合、bytearray 可变。不可变容器仍然可以引用可变对象。

<!-- verify: run -->
```python
a = [1]
b = a
a += [2]
assert b == [1, 2]        # list 的 += 通常原地扩展
a = a + [3]
assert a == [1, 2, 3] and b == [1, 2]

t = ([1], "标签")
t[0].append(2)
assert t == ([1, 2], "标签")
```

增强赋值可能调用原地协议；不同类型行为不同。不要把所有 `x += y` 机械理解为 `x = x + y`。

### 增强赋值失败，副作用也可能已经发生

观察 `tuple` 内嵌 `list` 时，不能只说“元组不可变所以操作没有发生”。表达式可能分步骤执行，前一步已经修改内层对象，后一步才失败。

<!-- verify: run -->
```python
record = ([1], "fixed")
try:
    record[0] += [2]
except TypeError:
    pass
else:
    raise AssertionError("元组不支持元素重新赋值")
assert record == ([1, 2], "fixed")
```

这里先取出 `record[0]` 的列表，再执行列表原地扩展，最后试图把结果写回元组的第 0 个位置。写回失败不撤销列表扩展。这解释了一个重要工程规则：异常只表示操作未正常完成，不表示整个过程没有副作用，也不自动具有数据库事务语义。

如果你要求失败后状态不变，应先构造新结果、完成校验，再提交替换；如果操作跨多个对象，则需要明确事务、快照或补偿方案。对文件、HTTP 和数据库，不能因为最后一行抛异常就盲目重试整段业务。

## 2.3 整数与进制

`int` 精度由可用内存约束，普通算术不会按 int64 溢出；这不表示任意巨大运算都廉价，也不表示网络协议 / 数据库字段没有范围限制。

<!-- verify: run -->
```python
assert 2 ** 100 > 2 ** 63
assert 0b1010 == 0o12 == 0xA == 10
assert int("ff", 16) == 255
assert bin(10) == "0b1010"
assert hex(255) == "0xff"
assert divmod(17, 5) == (3, 2)
assert pow(2, 10, 1000) == 24  # 模幂，避免先构造完整大整数
```

把整数编码成固定字节时，明确长度、大小端与有无符号：`(255).to_bytes(2, "big") == b"\x00\xff"`。

### 除法、余数和布尔值：跨语言迁移的三个反例

<!-- verify: run -->
```python
assert 7 / 2 == 3.5
assert -7 // 2 == -4      # 向负无穷取整，不是向零截断
assert -7 % 2 == 1
assert 7 % -2 == -1
for a, b in [(-7, 2), (7, -2), (-7, -2)]:
    assert a == (a // b) * b + a % b
assert int(-3.5) == -3
assert True + True == 2
assert {True: 'first', 1: 'second'} == {True: 'second'}
```

非零整数余数与除数同号。`bool` 是 `int` 子类，数值相等的键会合并；这会影响集合去重和字典键。字段要求“整数且不能是布尔值”时使用 `type(value) is int` 或显式排除 bool。`~`、`&`、`|` 是位运算，`not`、`and`、`or` 是逻辑运算；不能凭符号类似互换。

## 2.4 float、Decimal、Fraction、complex

<!-- verify: run -->
```python
import math
from decimal import Decimal, ROUND_HALF_UP, localcontext
from fractions import Fraction

assert 0.1 + 0.2 != 0.3
assert math.isclose(0.1 + 0.2, 0.3)
assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")
with localcontext() as ctx:
    ctx.prec = 10
    price = Decimal("12.345").quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
assert price == Decimal("12.35")
assert Fraction(1, 3) + Fraction(1, 6) == Fraction(1, 2)
assert (1 + 2j).imag == 2
assert math.isnan(float("nan"))
```

金额通常从十进制字符串构造 `Decimal`，而不是先构造不精确的 float 再转换。`round(2.5)` 为 2，默认并非业务常见的简单“四舍五入”。业务舍入、币种精度与计算顺序应独立约定。

### 数值类型的选择首先是业务契约

| 场景 | 建议表示 | 必须额外规定 |
|---|---|---|
| 数量、计数、ID | int | 外部系统位宽、最大值、是否允许 bool |
| 金额 | 整数最小货币单位，或 Decimal | 币种精度、舍入时机、负数退款规则 |
| 传感器读数、数值算法 | float 或数值库 dtype | 容差、NaN、Infinity、误差传播 |
| 精确比例 | Fraction | 分母增长与计算成本 |

`math.isclose` 判断接近，而不是消除浮点误差。接近零时仅设置相对误差可能不够，需要明确绝对容差。Decimal 也受上下文精度约束，并不意味着任意复杂十进制运算无限精确。输入 `"NaN"` 能构造 Decimal；业务金额必须另查 `is_finite()`。

<!-- verify: run -->
```python
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP

def parse_price(raw: str) -> Decimal:
    if not isinstance(raw, str) or len(raw) > 32:
        raise ValueError("金额必须是长度不超过 32 的文本")
    try:
        value = Decimal(raw)
        if not value.is_finite() or not Decimal("0") <= value <= Decimal("1000000"):
            raise ValueError("金额越界或不是有限数")
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    except InvalidOperation as exc:
        raise ValueError("金额格式错误") from exc

assert parse_price("12.345") == Decimal("12.35")
for raw in ["NaN", "Infinity", "-1", "bad", "1000001"]:
    try:
        parse_price(raw)
    except ValueError:
        pass
    else:
        raise AssertionError(raw)
```

本例允许 Decimal 能解析的数字文本，包括科学计数法；若接口只允许固定小数形式，应增加词法约束。这里采取输入即舍入的策略，实际计费可能要求先累计再舍入，两者结果不一定相同。

### NaN、无穷、近零容差与字面值转换

<!-- verify: run -->
```python
from decimal import Decimal
from fractions import Fraction
import math
nan = float('nan')
assert nan != nan
assert not (nan < 1) and not (nan >= 1)
assert math.isnan(nan) and not math.isfinite(nan)
assert not math.isclose(1e-12, 0.0)
assert math.isclose(1e-12, 0.0, abs_tol=1e-9)
assert Decimal(0.1) != Decimal('0.1')
assert Fraction(0.1) != Fraction('0.1')
```

从 float 转 Decimal/Fraction 会保留原二进制浮点值的影响，不能补回已丢失的十进制意图。NaN 不满足通常的相等与排序直觉，排序或聚合前需定义处理策略；容器查找还可能使用身份快速路径，不要用 `nan in values` 代替逐项 isnan。对外部数值先验证有限性、范围和单位，再参与运算，比事后格式化显示位数可靠。

## 2.5 字符串、Unicode 与编码

`str` 表示 Unicode 文本；`bytes` 表示字节序列。Go 的 string 是字节序列，按下标访问得到字节，range 则解码 UTF-8；Python str 下标访问得到一个码点组成的字符串，不能直接迁移索引直觉。

<!-- verify: run -->
```python
text = "中文🙂"
raw = text.encode("utf-8")
assert len(text) == 3
assert len(raw) == 10
assert raw.decode("utf-8") == text
assert ord("中") == 20013
assert chr(20013) == "中"
assert "e\u0301" != "é"  # 视觉相似，码点序列不同
import unicodedata
assert unicodedata.normalize("NFC", "e\u0301") == "é"
```

`len(str)` 计算码点数量，不保证等于屏幕字符数量；组合字符和复杂 emoji 可能由多个码点组成。编码错误不要随意 `errors="ignore"`，否则可能静默丢失数据。

## 2.6 字符串字面量与常用方法

<!-- verify: run -->
```python
path = r"C:\data\report.txt"  # 原始字符串；不能以奇数个反斜杠结尾
message = "第一行\n第二行"
assert "\n" in message
assert "  Python  ".strip() == "Python"
assert "a,b,c".split(",") == ["a", "b", "c"]
assert "-".join(["a", "b"]) == "a-b"
assert "hello".replace("l", "L", 1) == "heLlo"
assert "api/users".startswith("api/")
assert "report.csv".removesuffix(".csv") == "report"
assert "Straße".casefold() == "strasse"
assert "abc".find("x") == -1
```

`str.index` 找不到会抛异常；`find` 返回 -1。`strip("ab")` 删除两端属于字符集合 `{a, b}` 的字符，不是删除子串 `"ab"`。字符串方法返回新字符串。

## 2.7 格式化、repr 与转义

<!-- verify: run -->
```python
name, amount = "张三", 12345.678
assert f"{amount:,.2f}" == "12,345.68"
assert f"{7:04d}" == "0007"
assert f"{0.125:.1%}" == "12.5%"
assert f"{name=}" == "name='张三'"
assert "{name}:{n}".format(name=name, n=3) == "张三:3"
assert repr("a\nb") == "'a\\nb'"
```

`str` 倾向给用户看，`repr` 倾向供开发调试。f-string 计算 Python 表达式，不会替你做 SQL、HTML、shell 转义；格式化与安全编码是不同任务。

## 2.8 bytes、bytearray 与 memoryview

<!-- verify: run -->
```python
data = b"ABC"
assert data[0] == 65
buffer = bytearray(data)
view = memoryview(buffer)
view[0] = 97
assert buffer == bytearray(b"aBC")
view.release()
assert bytes(buffer) == b"aBC"
```

`memoryview` 提供缓冲区视图，可减少某些拷贝；生命周期与底层缓冲区关联。它不是让所有处理自动零拷贝的开关。

## 2.9 浅拷贝、深拷贝与共享

<!-- verify: run -->
```python
from copy import copy, deepcopy
original = {"tags": ["python"]}
shallow = copy(original)
deep = deepcopy(original)
original["tags"].append("go")
assert shallow["tags"] == ["python", "go"]
assert deep["tags"] == ["python"]
assert shallow is not original
```

浅拷贝新建最外层容器，仍共享嵌套对象。深拷贝会递归复制，并通过 memo 处理重复引用和循环；文件句柄、连接、线程锁不适合盲目复制。业务上显式构造新对象通常更容易控制。

### 共享关系比“浅或深”两个词更重要

设 `original["tags"]` 指向列表 L。`original.copy()` 创建新字典 D2，但 D2 的 `"tags"` 仍指向 L。对 L 执行 append，两个字典都看到变化；把 D2 的 `"tags"` 重新绑定到新列表，原字典不受影响。分析时先画名称到对象的箭头，再决定复制哪一层。

深拷贝通常保留原图内部的共享关系，不是把每条引用都变成不同对象：

<!-- verify: run -->
```python
from copy import deepcopy
shared = []
source = [shared, shared]
cloned = deepcopy(source)
assert cloned is not source
assert cloned[0] is cloned[1]  # memo 保留内部别名
assert cloned[0] is not shared

recursive = []
recursive.append(recursive)
copied = deepcopy(recursive)
assert copied[0] is copied
```

在函数 API 上注明是否会保存或修改输入，比无条件 deepcopy 更有效。例如“接收订单列表，只读取字段，不保存引用”；或者“构造配置对象时把列表转换为 tuple，后续外部修改不影响配置”。连接、锁、生成器和外部资源没有通用的深拷贝语义。

验收：解释 `is` 与 `==`，预测元组增强赋值的失败后状态，给出金额非有限值反例，区分字符串码点长度与 UTF-8 字节长度。

## 2.10 可哈希性与特殊值

<!-- verify: run -->
```python
assert {("tenant", 7): "ok"}[("tenant", 7)] == "ok"
try:
    hash(([1], 2))
except TypeError:
    print("包含 list 的 tuple 不可哈希")
assert len({True, 1, 1.0}) == 1
assert ... is Ellipsis
```

dict 键和 set 元素要求可哈希。不可变与可哈希相关但不等价：包含列表的元组不可哈希；某些按身份比较的可变自定义对象仍可哈希。`None` 表示缺失；`Ellipsis` 常见于占位或多维索引；`NotImplemented` 用于运算协议协商，不能当异常抛出。

延伸：[官方数据模型](https://docs.python.org/3/reference/datamodel.html)、[浮点算术限制](https://docs.python.org/3.14/tutorial/floatingpoint.html)。


---

# 03｜列表、元组、字典与集合

> 本章目标：按顺序、成本与共享语义选择容器。
>
> 阅读重点：用订单分组、稳定排序和缺失值处理检验已有 list/dict 使用经验。

## 3.1 选择容器

| 类型 | 有序 / 索引 | 是否可变 | 常见用途 | Go 类比 |
|---|---|---|---|---|
| list | 保留顺序，可索引 | 是 | 动态序列 | slice，复制与扩容语义不同 |
| tuple | 保留顺序，可索引 | 否 | 一组固定位置的数据 | 多返回值打包、轻量记录 |
| dict | 插入顺序，按键访问 | 是 | 索引、计数、关联 | map，但 Python dict 保留插入顺序 |
| set | 不提供顺序语义 | 是 | 去重、成员判断 | map[T]struct{} |
| frozenset | 不提供顺序语义 | 否 | 可哈希集合 | 不可变集合 |
| range | 等差序列，可索引 | 否 | 整数区间 | 无需构造整份数组 |

顺序和排序不同：dict 保留插入顺序，不会自动按键排序。set 没有可依赖的遍历顺序。

### 用操作成本选择容器

以下是常见 CPython 实现下的典型复杂度，用于选型，不是实时延迟保证。元素比较、哈希、自定义方法也可能有自己的成本。

| 操作 | 典型成本 | 设计提示 |
|---|---|---|
| list 按整数下标访问 | O(1) | 适合随机访问 |
| list 尾部 append | 摊还 O(1) | 扩容时个别操作更贵 |
| list 头部删除 / 中间插入 | O(n) | 队列优先 deque |
| list 长度为 k 的切片 | O(k) 时间及外层空间 | 切片不是免费视图 |
| dict / set 查找 | 平均 O(1)，最坏可退化 | 要求可哈希，考虑内存 |
| 排序 | 通常按 O(n log n) 估算 | 已排序程度会影响实际表现 |

如果只有 3 个选项，线性判断通常足够清楚；若每条订单都在百万用户列表中查找，先建 set 或 dict 会改变整体算法成本。不要只比较单次调用耗时，要乘上循环次数，计算是否反复构造索引。

Go 的 nil slice、空 slice 在某些操作中表现相近，但 Python 的 `None` 和 `[]` 是不同契约：`len(None)` 会失败，`len([])` 是 0。接口若约定列表，返回空列表通常比“有时 None、有时 list”更易组合。

## 3.2 list 的增删改查

<!-- verify: run -->
```python
items = ["Go", "Java"]
items.append("Python")
items.extend(["SQL", "Shell"])
items.insert(1, "Rust")
assert items[0] == "Go" and items[-1] == "Shell"
items[1] = "C"
assert items.pop() == "Shell"
items.remove("C")              # 删除首个相等元素；找不到抛 ValueError
del items[1]                    # 删除 Java
assert items == ["Go", "Python", "SQL"]
assert items.count("Go") == 1
assert items.index("Python") == 1
items.clear()
assert items == []
```

`append` 加一个对象，`extend` 遍历参数并逐个添加。`append([1, 2])` 得到嵌套列表，`extend([1, 2])` 得到两个元素。多数原地修改方法返回 `None`；不要写 `items = items.append(x)`。

## 3.3 切片和 Go slice 的区别

<!-- verify: run -->
```python
values = [0, 1, 2, 3, 4, 5]
assert values[1:4] == [1, 2, 3]
assert values[::2] == [0, 2, 4]
assert values[::-1] == [5, 4, 3, 2, 1, 0]
assert values[100:200] == []
part = values[1:3]
part[0] = 99
assert values[1] == 1  # 普通 list 切片复制外层，不共享 Go slice 式底层数组
values[1:3] = [8, 9, 10]
assert values == [0, 8, 9, 10, 3, 4, 5]
```

切片左闭右开；索引越界抛 `IndexError`，切片边界通常会被截取到有效范围。负步长需理解默认边界；`a[::-1]` 与 `a[len(a)-1:-1:-1]` 并不等价。嵌套元素仍然共享，因为切片是浅拷贝。

### 切片边界会截断，扩展切片赋值要求长度匹配

<!-- verify: run -->
```python
values = [0, 1, 2, 3, 4]
assert values[-99:99] == values
assert values[::-1] == [4, 3, 2, 1, 0]
values[1:3] = [9]
assert values == [0, 9, 3, 4]
values[::2] = [7, 8]
assert values == [7, 9, 8, 4]
try:
    values[::2] = [1]
except ValueError:
    pass
else:
    raise AssertionError('非单位步长切片不能随意改变所选槽位数量')
assert slice(None, None, -1).indices(4) == (3, -1, -1)
```

单索引越界抛 IndexError；切片通常把边界截到合法范围，步长 0 则非法。普通 list 切片产生新外层列表，但内层元素仍共享；切片赋值修改原列表，普通步长可改变长度，非单位步长要求替换项数相同。切片省略终点与显式 `-1` 在反向遍历时含义不同，不要用一套正向边界直觉硬推反向结果。

## 3.4 二维列表与重复引用

<!-- verify: run -->
```python
bad = [[0] * 2] * 3
bad[0][0] = 7
assert bad == [[7, 0], [7, 0], [7, 0]]
good = [[0] * 2 for _ in range(3)]
good[0][0] = 7
assert good == [[7, 0], [0, 0], [0, 0]]
```

`*` 复制元素引用，不会递归复制元素。构造独立行时在推导式中每次创建新列表。

## 3.5 tuple：逗号、不可变与解包

<!-- verify: run -->
```python
empty = ()
single = (42,)
assert isinstance(single, tuple)
assert isinstance((42), int)
record = 101, "张三", True
uid, name, active = record
assert uid == 101 and name == "张三" and active
assert record.count(True) == 1
assert record.index("张三") == 1
assert record[:2] == (101, "张三")
```

tuple 的固定性指不能替换其元素引用，不保证引用的对象不可变。`tuple([1, 2])` 做转换；已有合适元组时可能返回同一个对象，不应依赖“转换必定复制”。业务字段多时用 dataclass 或 NamedTuple，避免到处使用 `[0]`、`[1]`。

### 元组的操作边界与选择依据

元组不是“更快的列表”这一句可以概括的。固定位置表达不同含义时，例如 `(host, port)`，元组很自然；订单集合的元素数量会增长，就用 list；字段持续演进、调用者按字段名读取，就用 dataclass 或 NamedTuple。

<!-- verify: run -->
```python
endpoint = ("localhost", 8080)
assert endpoint + ("https",) == ("localhost", 8080, "https")
assert endpoint == ("localhost", 8080)
assert endpoint != ["localhost", 8080]
first, *remaining = (10, 20, 30)
assert first == 10 and remaining == [20, 30]  # 星号目标始终收集为列表

index = {("tenant-A", 7): "task"}
assert index[("tenant-A", 7)] == "task"
for operation in [lambda: hash(([1], 2)), lambda: (1, 2).index(9)]:
    try:
        operation()
    except (TypeError, ValueError):
        pass
    else:
        raise AssertionError("应验证不可哈希或查找失败")
```

连接和重复会构造结果，不能原地修改原元组；是否复用已有不可变对象属于另一问题，不应拿 `id` 推导业务正确性。元组比较按元素逐个进行，遇到第一个不同元素决定结果；异构元素不保证能比较大小。`(1, "x") < (1, 3)` 会因字符串与整数比较而失败。

元组可作为复合键时，它表达的是字段组合，不需要先把字段拼成容易产生歧义的字符串。只有所有组成元素都可哈希，整个元组才能哈希；“外层不可变”不充分。

## 3.6 dict：查找、默认值与视图

<!-- verify: run -->
```python
user = {"id": 101, "name": "jackie"}
assert user["id"] == 101
assert user.get("age", 18) == 18
assert "age" not in user  # get 默认值不会插入
user.setdefault("tags", []).append("python")
keys = user.keys()
user["active"] = True
assert "active" in keys  # keys / values / items 是动态视图
assert user.pop("missing", None) is None
patch = {"name": "Jackie", "age": 20}
merged = user | patch  # 右侧同名键优先，生成新 dict
user |= {"active": False}
assert merged["name"] == "Jackie"
assert user["active"] is False
```

`d[k]` 对不存在的键抛 `KeyError`；`get` 区分不了“不存在”和“存在且值为 None”，需要时用哨兵。`setdefault` 的默认参数在调用前就会求值，已有键也不会阻止昂贵表达式的计算。

<!-- verify: run -->
```python
missing = object()
data = {"value": None}
assert data.get("value", missing) is None
assert data.get("absent", missing) is missing
assert list({"a": 1, "b": 2}) == ["a", "b"]
assert dict.fromkeys(["x", "y"], 0) == {"x": 0, "y": 0}
```

`dict.fromkeys(keys, [])` 的所有键会共享同一个列表；独立列表用 `{k: [] for k in keys}`。

### 缺失、空值、覆盖和动态视图必须分开

Python 字典访问与 Go `value, ok := m[key]` 不同。`d[key]` 表示必须存在，缺失时抛 KeyError；`d.get(key)` 适合缺失与 None 可合并的情况；否则用唯一哨兵。不要写 `if d.get("enabled")` 判断键是否存在，因为 False 是合法值。

更新已有键的值通常不会把它移动到最后；删除后重新插入才改变插入位置。迭代视图不是快照，传给稍后执行的代码时会看到后续变化；需要快照可用 `list(d.items())`，但其中可变值依然共享。

<!-- verify: run -->
```python
data = {"first": 1, "second": 2}
view = data.items()
snapshot = list(view)
data["first"] = 9
assert list(data) == ["first", "second"]
assert ("first", 9) in view
assert snapshot == [("first", 1), ("second", 2)]
del data["first"]
data["first"] = 10
assert list(data) == ["second", "first"]
```

`d.setdefault(k, expensive())` 不是惰性工厂；函数调用前参数表达式已经执行。按需创建集合使用 `defaultdict(list)`，或者显式检查缺失再构造。并发读改写还需要锁，单个字典方法的实现细节不能保护多个步骤之间的不变量。

### 默认值是否共享、是否提前执行、是否真的插入

<!-- verify: run -->
```python
from collections import defaultdict
from types import MappingProxyType

calls = []
def make_default():
    calls.append('made')
    return []

data = {'a': [1]}
assert data.get('a', make_default()) == [1]
assert calls == ['made']             # 先求实参，再调用 get
data.setdefault('a', make_default())
assert len(calls) == 2               # 已有键也先求默认表达式
groups = defaultdict(list)
assert groups.get('x') is None and 'x' not in groups
groups['x'].append(1)                # [] 查找缺失才调用工厂并插入
assert groups['x'] == [1]
shared = dict.fromkeys(['a', 'b'], [])
shared['a'].append(3)
assert shared['b'] == [3]
view = MappingProxyType(data)
data['b'] = [2]
assert view['b'] == [2]              # 只读视图不是冻结快照
```

`get` 不插入，`setdefault` 可插入，`defaultdict` 的下标读取可能插入。要避免昂贵默认计算，可先捕获 `KeyError` 再构造，涉及并发时另外同步。`keys/items/values` 反映底层字典变化；遍历时增删键可能报错，应遍历 `list(data)` 等快照后再修改。快照中的嵌套值仍可能共享。

## 3.7 set 与 frozenset

<!-- verify: run -->
```python
a, b = {1, 2, 3}, {3, 4}
assert a | b == {1, 2, 3, 4}
assert a & b == {3}
assert a - b == {1, 2}
assert a ^ b == {1, 2, 4}
assert {1, 2} <= a
assert {9}.isdisjoint(a)
a.add(5)
a.discard(999)  # 不存在也不报错；remove 会报错
assert frozenset({1, 2}) in {frozenset({1, 2})}
assert isinstance({}, dict) and isinstance(set(), set)
```

成员判断对 list 一般需线性扫描，set / dict 平均常数级查找但有额外内存与哈希成本。复杂度是常见实现与正常散列条件下的分析，不保证所有输入都恒定耗时。

## 3.8 推导式：过滤和变换

<!-- verify: run -->
```python
scores = {"张三": 85, "李四": 60, "王五": 95}
passed = {name: score for name, score in scores.items() if score > 80}
assert passed == {"张三": 85, "王五": 95}
squares = [x * x for x in range(6) if x % 2 == 0]
assert squares == [0, 4, 16]
labels = ["偶" if n % 2 == 0 else "奇" for n in range(3)]
assert labels == ["偶", "奇", "偶"]
assert {s.lower() for s in ["GO", "Go", "JAVA"]} == {"go", "java"}
assert [x for row in [[1, 2], [3]] for x in row] == [1, 2, 3]
```

末尾 `if` 是过滤，前部 `A if condition else B` 是表达式。嵌套推导式的 `for` 顺序与普通嵌套循环一致。过多层、复杂副作用、异常处理更适合普通循环。

## 3.9 排序、稳定性与 key

<!-- verify: run -->
```python
rows = [{"name": "B", "score": 90}, {"name": "A", "score": 90}, {"name": "C", "score": 80}]
ranked = sorted(rows, key=lambda r: (-r["score"], r["name"]))
assert [r["name"] for r in ranked] == ["A", "B", "C"]
values = [3, 1, 2]
assert sorted(values) == [1, 2, 3] and values == [3, 1, 2]
assert values.sort(reverse=True) is None
assert values == [3, 2, 1]
assert sorted([("a", 2), ("b", 2)], key=lambda x: x[1]) == [("a", 2), ("b", 2)]
```

`sorted` 接收任意可迭代对象并生成列表；`list.sort` 原地排序。排序稳定，key 相等时保留原相对顺序。不要把 `None`、字符串和数字混排后期待自动转换。

### 排序键就是业务规则

想要“金额降序、同金额用户升序”，应构造 `(-amount, user)`；给整个排序设置 `reverse=True` 会同时反转全部维度，用户名称也变成降序。缺失值需要先分类，避免直接比较 None 和数字。

<!-- verify: run -->
```python
rows = [
    {"name": "C", "score": None},
    {"name": "B", "score": 90},
    {"name": "A", "score": 90},
]
ranked = sorted(rows, key=lambda r: (
    r["score"] is None,
    -r["score"] if r["score"] is not None else 0,
    r["name"],
))
assert [r["name"] for r in ranked] == ["A", "B", "C"]
assert rows[0]["name"] == "C"  # 外层顺序未改
ranked[0]["name"] = "changed"
assert rows[2]["name"] == "changed"  # 元素对象仍共享
```

验收：既能说明排序输出，又能说明源列表哪些状态没改、哪些状态仍可能共享；能为保序去重、FIFO、分组和查询分别选容器。

### 排序的返回值、稳定性与比较能力

<!-- verify: run -->
```python
rows = [('b', 2), ('a', 2), ('c', 1)]
assert sorted(rows, key=lambda row: row[1]) == [('c', 1), ('b', 2), ('a', 2)]
copy = rows[:]
assert copy.sort(key=lambda row: row[1]) is None
assert rows[0] == ('b', 2)
assert sorted([None, 3, 1], key=lambda x: (x is None, x or 0)) == [1, 3, None]
```

这里稳定性指 key 相同的元素保持输入相对顺序，不意味着原容器不变。`sorted` 返回新列表，`list.sort` 原地修改并返回 None；`append`、`extend` 等也不要赋回列表变量。混合 `str`、`int`、None 通常没有可用的全序，应先规范化类型或提供明确 key。集合比较 `<` 表示真子集，不是字典序大小；不要把任何支持 `<` 的对象都当成有全序。

## 3.10 常见容器操作组合

<!-- verify: run -->
```python
assert list(dict.fromkeys(["a", "b", "a"])) == ["a", "b"]  # 保序去重，可哈希元素
assert list(enumerate(["a", "b"], start=1)) == [(1, "a"), (2, "b")]
assert list(zip([1, 2], ["a", "b"], strict=True)) == [(1, "a"), (2, "b")]
assert list(reversed([1, 2])) == [2, 1]
assert all(x > 0 for x in [1, 2])
assert any(x < 0 for x in [1, -1])
assert sum([1, 2, 3]) == 6
assert min([], default=0) == 0
```

`zip` 默认截断到最短输入，业务要求长度一致时使用 `strict=True`。避免遍历 dict 时改变其大小；可以遍历 `list(d)` 再删除，或用推导式构造结果。大量队头出队使用 `deque`，不要反复 `list.pop(0)`。

练习：把订单按用户分组、汇总金额、按金额降序输出。不要依赖 set 顺序。

延伸：[官方数据结构教程](https://docs.python.org/3.14/tutorial/datastructures.html)。


---

# 04｜控制流与模式匹配

> 本章目标：把条件和结构匹配写成明确的输入契约。
>
> 阅读重点：重点区分真值、缺失、模式匹配与完整校验；Go 没有三元运算符。

## 4.1 if、elif、else 与条件表达式

<!-- verify: run -->
```python
def grade(score):
    if not 0 <= score <= 100:
        raise ValueError("分数超出范围")
    if score >= 90:
        return "A"
    elif score >= 60:
        return "B"
    else:
        return "C"

assert grade(95) == "A"
assert ("通过" if grade(70) != "C" else "未通过") == "通过"
```

条件不强制为 bool，而是执行真值判断。三元表达式写成 `值 if 条件 else 另一个值`，Go 没有 `?:` 三元运算符，通常使用 if/else 赋值。

### 真值不是接口规范

“没有值”至少有三种情形：键不存在、键存在且值为 None、键存在且值为零或空容器。业务规则决定它们是否等价。条件判断应表达这一规则，而不是为了缩短代码把它们都写成 `if not value`。

<!-- verify: run -->
```python
def normalize_limit(value):
    if value is None:
        return 100
    if type(value) is not int or not 0 <= value <= 1000:
        raise ValueError("limit 必须为 0..1000 的整数")
    return value

assert normalize_limit(None) == 100
assert normalize_limit(0) == 0
try:
    normalize_limit(False)
except ValueError:
    pass
else:
    raise AssertionError("False 不是此业务允许的数量")
```

Python 的 `if`、`for` 块不创建普通局部变量作用域，循环结束后目标名称通常仍存在；推导式的循环目标则有隔离规则。不要把 Go 的块作用域直觉直接迁移过来。函数局部变量与 `global` / `nonlocal` 见 5.6。

### 真值、缺失和比较链必须分开判断

<!-- verify: run -->
```python
assert (0 or 10) == 10
assert ([] and 'unused') == []
value = 0
assert (10 if value is None else value) == 0
assert bool('False') is True
calls = []
def middle():
    calls.append('called')
    return 2
assert 1 < middle() < 3
assert calls == ['called']
assert (1 in [1] == [1]) is True
```

`and/or` 短路并返回操作数，不强制返回 bool；`x or default` 会替换 0、空字符串和空容器，而不只替换 None。环境变量文本 `"False"` 非空，不能用 `bool()` 解析开关。链式比较共享中间表达式，`1 in [1] == [1]` 表示两个比较的合取，不是先得到 True 再与列表比较。优先级不清楚时加括号，尤其是 `not`、位运算、比较、海象表达式混用时。

## 4.2 for 迭代对象

<!-- verify: run -->
```python
total = 0
for n in range(1, 6):
    total += n
assert total == 15
assert list(range(5, 0, -2)) == [5, 3, 1]
for name, score in {"张三": 85, "李四": 60}.items():
    assert isinstance(name, str) and isinstance(score, int)
```

`for` 消费迭代协议，而不是带初始化 / 条件 / 自增的 C 风格循环。`range` 是可重复迭代的惰性整数序列，不是一次性生成器，也不提前创建所有整数对象。

## 4.3 while、break、continue、pass

<!-- verify: run -->
```python
remaining, accepted = 5, []
while remaining > 0:
    remaining -= 1
    if remaining == 3:
        continue
    if remaining == 0:
        break
    accepted.append(remaining)
assert accepted == [4, 2, 1]

def planned_feature():
    pass  # 仅占位，调用返回 None

assert planned_feature() is None
```

`break` 只退出最近一层循环。占位但必须禁止调用的接口应抛 `NotImplementedError`，不要用 `pass` 假装功能完成。

## 4.4 循环的 else

<!-- verify: run -->
```python
def contains_negative(values):
    for value in values:
        if value < 0:
            break
    else:
        return False
    return True

assert contains_negative([1, -2])
assert not contains_negative([])
assert not contains_negative([1, 2])
```

循环正常耗尽或 while 条件变假会进入 else；执行 break、return 或异常中断就不进入。读者不熟悉时可改为 `any(v < 0 for v in values)`，选择更易懂的表达。

### 三种 else 的触发条件

| 结构 | else 什么时候执行 | 不应理解成 |
|---|---|---|
| if / else | if 条件为假 | 任何异常后的备用处理 |
| for / while / else | 循环正常结束，没有用 break 跳出 | 循环一次都没运行才执行 |
| try / except / else | try 正常走到末尾 | finally 的同义写法 |

空 iterable 的 for 也会正常执行 else；continue 不取消最终 else，return 和传播出的异常会直接离开该控制流。嵌套循环的 break 只影响最近一层循环。if、for、while 和 with 通常不创建新的函数式局部作用域，语句块结束后名称可能仍然存在；但可能因为分支没执行而从未绑定，不能直接假定可读。

## 4.5 海象表达式 `:=`

<!-- verify: run -->
```python
records = ["", "  go ", " python "]
cleaned = [value for raw in records if (value := raw.strip())]
assert cleaned == ["go", "python"]
```

海象在表达式中绑定名称，适合“计算一次，再判断 / 使用”。读取流常写 `while chunk := file.read(8192): ...`。不要在复杂表达式里大量赋值；推导式里的海象绑定规则与循环变量不同，避免依赖它在外层留下的名称。

## 4.6 match 的字面量、OR 与守卫（3.10+）

<!-- verify: run -->
```python
def describe(code):
    match code:
        case 200 | 201:
            return "成功"
        case n if 400 <= n < 500:
            return "请求问题"
        case _:
            return "其他"

assert describe(201) == "成功"
assert describe(404) == "请求问题"
```

只执行首个匹配分支，不需要 break。`case SOME_NAME` 通常是捕获变量，不是引用你提前定义的常量。枚举或常量对象用限定名，例如 `case Status.DONE`。

## 4.7 序列、映射与类模式

<!-- verify: run -->
```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

def parse(value):
    match value:
        case {"op": "add", "values": [int(a), int(b)]}:
            return a + b
        case ["move", x, y]:
            return Point(x, y)
        case Point(x=0, y=y):
            return f"y轴:{y}"
        case _:
            return None

assert parse({"op": "add", "values": [2, 3], "trace": True}) == 5
assert parse(["move", 1, 2]) == Point(1, 2)
assert parse(Point(0, 7)) == "y轴:7"
```

映射模式允许额外键；要捕获其余键用 `**rest`。序列模式不会把普通字符串当成可拆字符序列匹配。类模式按类型与属性匹配，位置模式取决于 `__match_args__`。模式不是完整输入校验系统，例如 `int()` 模式仍会接受 bool 子类。

### match 做结构分派，解析器建立可信模型

一个映射模式成功，只说明符合模式写出的结构条件。它不会自动拒绝额外键，也不会把字符串数字转成整数。类模式 `int(n)` 不是 `int(value)` 转换调用；它匹配整数实例并绑定值，bool 也是 int 子类。

<!-- verify: run -->
```python
def parse_command(raw):
    match raw:
        case {"op": "close", "id": int(task_id), **extra} if type(task_id) is int and task_id > 0 and not extra:
            return ("close", task_id)
        case {"op": "list", **extra} if not extra:
            return ("list", None)
        case _:
            raise ValueError("不支持的命令结构")

assert parse_command({"op": "close", "id": 3}) == ("close", 3)
for raw in [
    {"op": "close", "id": True},
    {"op": "close", "id": "3"},
    {"op": "list", "admin": True},
]:
    try:
        parse_command(raw)
    except ValueError:
        pass
    else:
        raise AssertionError(raw)
```

本例选择严格拒绝多余字段，版本演进时也可以选择允许并忽略未知字段，但必须明确。模式复杂到需要很多守卫时，应拆成小解析函数；match 的价值是清晰表达有限协议，不是替代一切 if。

验收：空循环也可能执行 else；`break` 只影响最近循环；模式捕获名称与常量比较不同；类型和范围校验应在业务入口显式执行。

### match 中裸名称是捕获，不是已有变量常量

<!-- verify: run -->
```python
from enum import Enum
class Kind(Enum):
    TEXT = 'text'

def classify(value):
    match value:
        case {'kind': Kind.TEXT, 'body': str(body)}:
            return body
        case [first, *rest] if rest:
            return first, rest
        case _:
            return None

assert classify({'kind': Kind.TEXT, 'body': 'hi', 'extra': 1}) == 'hi'
assert classify([1, 2, 3]) == (1, [2, 3])
assert classify('abc') is None
```

值模式用 `Kind.TEXT` 这类带点名称；`case TEXT:` 会绑定名称，不能表达“等于外部 TEXT”。映射模式默认允许多余键；字符串和 bytes 不按普通序列模式拆开。类模式检查类型和属性，不调用构造器；位置模式通过 `__match_args__` 解释。守卫在模式成功绑定后执行，所以不要依赖失败分支完全没有副作用，也不要依赖失败模式留下哪些变量。需要严格输入校验时仍应检查未知字段、类型与范围。

## 4.8 as 模式与星号捕获

<!-- verify: run -->
```python
def inspect_command(value):
    match value:
        case ["batch", *commands] as whole:
            return len(commands), whole[0]
        case _:
            return 0, None

assert inspect_command(["batch", "a", "b"]) == (2, "batch")
```

嵌套匹配适合有限形状的事件 / 命令协议。规则过多时，字典分发、普通函数或显式解析器往往更便于维护。

## 4.9 assert 的边界

<!-- verify: run -->
```python
def positive_square(value):
    if value <= 0:
        raise ValueError("value 必须大于 0")
    result = value * value
    assert result > 0  # 内部不变量，外部校验已由 if 完成
    return result

assert positive_square(3) == 9
```

运行 `python -O` 可以移除 assert。它适合测试和内部调试，不能作为权限、请求参数或资金约束的唯一检查。示例中的 assert 是可执行的预期结果，验证器不使用优化模式。

延伸：[官方控制流](https://docs.python.org/3.14/tutorial/controlflow.html)。


---

# 05｜函数、作用域与装饰器

> 本章目标：设计参数、状态和装饰器的执行边界。
>
> 阅读重点：需要掌握定义时、调用时、await 时三种时机，以及它们对副作用的影响。

## 5.1 def、返回值与函数对象

<!-- verify: run -->
```python
def divide(a, b):
    """返回商和余数。"""
    return a // b, a % b

operation = divide
assert operation(17, 5) == (3, 2)
q, r = divide(17, 5)
assert q == 3 and r == 2
```

多返回值实际是返回一个对象，常见是 tuple。没有 return 或裸 return 都返回 None。函数是一等对象，可以保存到容器、传入函数、作为结果返回。

## 5.2 位置参数、关键字参数与默认值

<!-- verify: run -->
```python
def connect(host, port=5432, *, timeout=3):
    return host, port, timeout

assert connect("localhost") == ("localhost", 5432, 3)
assert connect(port=5433, host="db", timeout=5) == ("db", 5433, 5)
```

关键字让业务含义明确；同一参数不能重复提供。默认参数在定义函数时求值，不在每次调用时重新求值。这也意味着 `time.time()`、配置对象等默认值可能被提前固定。

## 5.3 可变默认参数陷阱

<!-- verify: run -->
```python
def bad_add(value, bucket=[]):
    bucket.append(value)
    return bucket

assert bad_add(1) == [1]
assert bad_add(2) == [1, 2]

def add(value, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(value)
    return bucket

assert add(1) == [1]
assert add(2) == [2]
```

不要写 `bucket = bucket or []` 替代 None 检查，因为调用者传入的空列表也会被换掉。需要区分“没传”和“明确传 None”时使用私有哨兵对象。

### 用哨兵区分“未提供”和“显式传入 None”

<!-- verify: run -->
```python
MISSING = object()
def update(value=MISSING):
    if value is MISSING:
        return '保持原值'
    if value is None:
        return '清空'
    return value

assert update() == '保持原值'
assert update(None) == '清空'
assert update(0) == 0
```

默认参数表达式在执行 `def` 时求值，不是在每次调用时求值；时间戳、随机值和函数调用同样受这个规则影响。哨兵用身份判断，避免触发用户自定义相等方法；这个普通 object 哨兵只用于当前进程的调用协议，不要假定序列化后仍保持身份。

## 5.4 `/`、`*`、`*args`、`**kwargs`

<!-- verify: run -->
```python
def request(path, /, method="GET", *, timeout=3, **headers):
    return path, method, timeout, headers

result = request("/users", "POST", timeout=5, token="demo")
assert result == ("/users", "POST", 5, {"token": "demo"})

def total(*values, scale=1):
    return sum(values) * scale

assert total(1, 2, 3, scale=2) == 12
assert total(*[1, 2], **{"scale": 3}) == 9
```

`/` 前只能按位置传；单独 `*` 后只能按关键字传。`args` 是 tuple，`kwargs` 是 dict，名称可换但习惯如此。定义处的 `*` 收集实参，调用处的 `*` 展开实参。乱用 `**kwargs` 会隐藏契约，稳定业务接口应显式列参数。

### 参数设计就是调用方契约

`/` 左边只能按位置传，`*` 右边只能按关键字传。前者允许实现将来重命名参数而不破坏关键字调用，后者让多个布尔值或超时参数更易读。`*args` 收集剩余位置参数为 tuple，`**kwargs` 收集剩余关键字参数为 dict；它们不代表函数天然接受所有输入。

<!-- verify: run -->
```python
import inspect

def fetch(resource, /, retries=2, *, timeout=3):
    return resource, retries, timeout

signature = inspect.signature(fetch)
bound = signature.bind("/tasks", timeout=5)
bound.apply_defaults()
assert bound.arguments == {"resource": "/tasks", "retries": 2, "timeout": 5}
assert fetch("/tasks", timeout=5) == ("/tasks", 2, 5)
for invoke in [
    lambda: fetch(resource="/tasks"),
    lambda: fetch("/tasks", 2, 5),
    lambda: fetch("/tasks", 2, retries=3),
]:
    try:
        invoke()
    except TypeError:
        pass
    else:
        raise AssertionError("参数绑定必须失败")
```

调用前先求值实参表达式，再进行参数绑定，进入函数体之前就可能抛 TypeError。调用方写 `f(**mapping)` 时，键必须符合关键字参数规则；不能通过多个映射向同一个参数重复传值。公共 API 尽量使用明确参数，保留 `**kwargs` 给确有需要的转发边界。

## 5.5 调用绑定与副作用

<!-- verify: run -->
```python
def normalize(values):
    return [v.strip() for v in values]

source = [" go ", " java "]
assert normalize(source) == ["go", "java"]
assert source == [" go ", " java "]
```

需要修改调用者对象的函数，要通过命名与文档表达，例如 `sort_in_place`；提供新结果的函数尽量保持输入不变。这比把可变性留给调用者猜测更容易维护。

## 5.6 LEGB、global、nonlocal

名称查找通常按 Local → Enclosing → Global → Builtins。函数内部只要存在对某名字的赋值，该名称通常就被视为局部，除非声明 global / nonlocal。

<!-- verify: run -->
```python
tax_rate = 0.1

def make_counter():
    count = 0
    def increment():
        nonlocal count
        count += 1
        return count
    return increment

counter = make_counter()
assert counter() == 1 and counter() == 2

def set_rate(value):
    global tax_rate
    tax_rate = value

set_rate(0.2)
assert tax_rate == 0.2
```

global 指当前模块命名空间，不是跨所有模块的魔法全局。nonlocal 指向外层函数作用域中已有绑定。类体并不是方法查找局部名称时的普通 enclosing 函数作用域；方法访问类属性应使用 `self` 或类名。

### UnboundLocalError 为什么发生在赋值之前

Python 在编译函数体时判断某个名称是否为局部名称。只要函数内有赋值且没有 global / nonlocal 声明，该名称通常就被作为局部处理，不会在赋值之前自动回退到全局。

<!-- verify: run -->
```python
count = 10
def broken():
    before = count
    count = 20
    return before

try:
    broken()
except UnboundLocalError:
    pass
else:
    raise AssertionError("函数中的 count 已被判定为局部名称")
assert count == 10

def make_counter():
    value = 0
    def increment():
        nonlocal value
        value += 1
        return value
    return increment

a, b = make_counter(), make_counter()
assert (a(), a(), b()) == (1, 2, 1)
```

`nonlocal` 修改最近外层函数的已有绑定，不创建任意模块变量；`global` 指当前模块的全局命名空间，不是全进程唯一配置仓库。相比修改全局状态，把依赖和状态通过参数或小对象传入，通常更容易测试和并发使用。

闭包捕获绑定而非自动复制对象。`lambda value=value: ...` 固定的是当时对象的引用，如果该对象本身可变，后续修改仍会被观察到。工厂函数能创建独立绑定，但同样不会替你深拷贝输入。

### LEGB 的适用边界：局部判定、类体和推导式

<!-- verify: run -->
```python
count = 10
def broken():
    count += 1
try:
    broken()
except UnboundLocalError:
    pass
else:
    raise AssertionError('赋值使 count 在整个函数块中被判为局部名称')

label = 'module'
class Demo:
    label = 'class'
    def read(self):
        return label, self.label

assert Demo().read() == ('module', 'class')
i = 'outside'
assert [i * 2 for i in range(3)] == [0, 2, 4]
assert i == 'outside'
for i in range(2):
    pass
assert i == 1
```

函数块中存在名称赋值，通常足以让编译器把它判为局部名称，不要求那条分支真的运行。`global` 指当前模块命名空间，不是全程序统一全局；`nonlocal` 重新绑定最近的外层函数已有名称，不能凭空创建外层变量。

普通方法的裸名称查找不把类字典当作闭包环境，读类属性应写 `self.attr` 或 `type(self).attr`。普通列表推导式中的循环目标不泄漏到外层，普通 for 会；推导式内 `:=` 的绑定又有专门规则，不能从前一条类推。3.12+ 类型参数和类型别名、3.14 注解使用注解作用域，允许的名称访问与普通函数体不同，见第 10.10 节。[官方执行模型](https://docs.python.org/3.14/reference/executionmodel.html)

## 5.7 闭包晚绑定

<!-- verify: run -->
```python
bad = [lambda: i for i in range(3)]
assert [f() for f in bad] == [2, 2, 2]
good = [lambda i=i: i for i in range(3)]
assert [f() for f in good] == [0, 1, 2]
```

闭包引用变量绑定，不自动保存每次循环的值。默认参数会在创建函数时求值，可以冻结当次对象引用；另一个方案是写工厂函数。它冻结的仍是对象引用，不会自动深拷贝。

## 5.8 lambda、高阶函数与 partial

<!-- verify: run -->
```python
from functools import partial, reduce
assert list(map(lambda n: n * 2, [1, 2])) == [2, 4]
assert list(filter(lambda n: n > 0, [-1, 0, 2])) == [2]
assert reduce(lambda a, b: a * b, [2, 3, 4], 1) == 24
parse_binary = partial(int, base=2)
assert parse_binary("101") == 5
```

lambda 只包含一个表达式，适合短 key 函数。多数 map / filter 可以用推导式表达；不要把简单逻辑写成难以阅读的多层函数嵌套。

## 5.9 装饰器：函数替换与 wraps

<!-- verify: run -->
```python
from functools import wraps

def traced(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        print(f"{fn.__name__} -> {result}")
        return result
    return wrapper

@traced
def add(a, b):
    """把两个数相加。"""
    return a + b

assert add(2, 3) == 5
assert add.__name__ == "add"
assert add.__wrapped__(2, 3) == 5
```

`@traced` 等价于函数定义完成后执行 `add = traced(add)`。装饰器会参与运行时对象构造并替换名称绑定，不只是附加一段供工具读取的元数据。`wraps` 保留常用元数据并暴露 `__wrapped__`，帮助调试和反射。

## 5.10 带参数、叠加顺序与异步装饰器

<!-- verify: run -->
```python
from functools import wraps

def multiply_result(factor):
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            return fn(*args, **kwargs) * factor
        return wrapper
    return decorate

@multiply_result(3)
@multiply_result(2)
def value():
    return 5

assert value() == 30
```

叠加相当于 `outer(inner(fn))`：装饰应用自下而上，调用入口通常先进入外层 wrapper。包装 async 函数时，wrapper 通常也要 `async def` 并 `await fn(...)`；同步包装器不会自动正确处理异步生命周期。

### 为什么同步装饰器抓不到异步函数内部异常

调用 async 函数先获得 coroutine 对象，真正执行函数体是在 await 或调度之后。同步 wrapper 中的 try 如果只包住 `fn(...)`，它包住的只是“创建协程”这个动作。计时、重试、事务装饰器若放错层次，可能在真实工作开始前就宣布成功。

<!-- verify: run -->
```python
import asyncio
from functools import wraps

events = []
def audited_async(fn):
    @wraps(fn)
    async def wrapper(*args, **kwargs):
        events.append("start")
        try:
            result = await fn(*args, **kwargs)
        except Exception:
            events.append("failure")
            raise
        else:
            events.append("success")
            return result
        finally:
            events.append("finish")
    return wrapper

@audited_async
async def work(fail=False):
    await asyncio.sleep(0)
    if fail:
        raise ValueError("bad input")
    return 42

async def check():
    assert await work() == 42
    try:
        await work(True)
    except ValueError:
        pass
    else:
        raise AssertionError("异常必须继续传播")

asyncio.run(check())
assert events == ["start", "success", "finish", "start", "failure", "finish"]
assert work.__name__ == "work"
```

这里的 Exception 不会捕获 asyncio.CancelledError；取消仍经过 finally 清理并向外传播。不能把取消当普通可重试业务错误。装饰器保持元数据与保持静态类型签名是两件事，后者见第 10 章 ParamSpec。

多个装饰器 `@outer`、`@inner` 自上而下写，相当于 `outer(inner(fn))`。装饰动作发生在定义阶段；调用时先进入 outer wrapper，再进入 inner wrapper，返回时反向退出。缓存包住权限检查，还是权限检查包住缓存，会改变每次调用是否执行鉴权。

### 四个时刻：装饰器表达式、应用装饰器、调用包装器、执行原函数

<!-- verify: run -->
```python
from functools import wraps
events = []
def decorate(name):
    events.append('evaluate ' + name)
    def apply(fn):
        events.append('apply ' + name)
        @wraps(fn)
        def wrapper():
            events.append('call ' + name)
            return fn()
        return wrapper
    return apply

@decorate('outer')
@decorate('inner')
def work():
    events.append('body')

assert events == ['evaluate outer', 'evaluate inner', 'apply inner', 'apply outer']
work()
assert events[-3:] == ['call outer', 'call inner', 'body']
assert work.__wrapped__.__wrapped__.__name__ == 'work'
```

装饰器表达式从上到下求值，应用从内到外；调用时先进入最外层包装器。`wraps` 复制常用元数据并设置 `__wrapped__`，不自动修复错误的参数转发、异步等待、生成器迭代或异常处理。包装器只返回一个生成器对象时，函数体后续执行的异常不会被包在“创建生成器”的 try 中。

## 5.11 缓存与 singledispatch

<!-- verify: run -->
```python
from functools import lru_cache, singledispatch

@lru_cache(maxsize=128)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

assert fib(10) == 55
assert fib.cache_info().hits > 0
fib.cache_clear()

@singledispatch
def render(value):
    return str(value)

@render.register
def _(value: list):
    return ",".join(map(str, value))

assert render([1, 2]) == "1,2"
```

缓存参数一般需可哈希；缓存持有参数和结果引用，可能增加内存；不要缓存含用户权限上下文但未把上下文计入键的结果。递归有深度限制，Python 不保证尾递归优化；大量递归状态优先考虑迭代。

### 缓存保存的是对象，不是每次复制出的结果

<!-- verify: run -->
```python
from functools import lru_cache

@lru_cache(maxsize=8)
def labels(key):
    return [key]

first = labels("a")
first.append("modified")
assert labels("a") == ["a", "modified"]
assert labels.cache_info().hits == 1
labels.cache_clear()
```

不要把可变缓存返回值暴露给不受约束的调用方；可返回 tuple，或在边界显式复制。缓存键需可哈希；参数等价、调用方式、用户权限、版本和有效期都可能影响键的正确性。`lru_cache` 没有自动 TTL，也不会因为数据库变化主动失效。

验收：说明默认参数在何时求值，解释闭包保存的是哪个绑定，写出保留异常和资源清理的 async wrapper，并证明缓存不会向不同调用者泄漏可变结果。

延伸：[官方函数定义](https://docs.python.org/3.14/tutorial/controlflow.html#defining-functions)、[functools](https://docs.python.org/3.14/library/functools.html)。


---

# 06｜迭代器、生成器与函数式工具

> 本章目标：用惰性迭代处理数据，同时管理资源。
>
> 阅读重点：重点验证一次性输入、消费时异常、提前退出以及内存增长来源。

## 6.1 Iterable 与 Iterator

可迭代对象可以交给 `iter()`；迭代器可以交给 `next()`，耗尽时抛 `StopIteration`。列表每次 `iter(list)` 通常返回新的迭代器；迭代器本身通常是一次性的，`iter(iterator) is iterator`。

<!-- verify: run -->
```python
values = [10, 20]
it = iter(values)
assert next(it) == 10
assert next(it) == 20
assert next(it, "结束") == "结束"
assert list(it) == []
assert list(values) == [10, 20]
assert iter(it) is it
```

这里通过 `next` / StopIteration 协议推进并识别耗尽，不提供统一的 hasNext 预探测接口。for 会负责正常处理耗尽异常。

## 6.2 自定义迭代器

<!-- verify: run -->
```python
class Countdown:
    def __init__(self, start):
        self.current = start
    def __iter__(self):
        return self
    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

counter = Countdown(3)
assert list(counter) == [3, 2, 1]
assert list(counter) == []
```

如果对象需要反复遍历，让 `__iter__` 创建独立迭代器，或在其中用 yield。不要把游标状态共享给不相关的遍历。

## 6.3 yield 与生成器函数

<!-- verify: run -->
```python
def countdown(start):
    while start > 0:
        yield start
        start -= 1

g = countdown(3)   # 此时函数体尚未执行
assert next(g) == 3
assert list(g) == [2, 1]
assert list(g) == []
```

yield 暂停函数并保存局部状态；再次 next 从暂停处继续。生成器适合处理大文件、分页、转换流。惰性只表示按需计算，不意味着每一步都低内存：若某一步调用 `list`、`sorted` 或保留所有结果，仍会物化数据。

### 把生成器看成可暂停的执行过程

普通函数在调用时执行，生成器函数在调用时创建生成器对象，遇到 next 才开始执行。每次 yield 返回一个元素并保存局部状态；return 结束，不再产生元素。输入校验放在生成器函数体里，也会被延迟。

<!-- verify: run -->
```python
events = []
def values(size):
    events.append("entered")
    if size < 0:
        raise ValueError("size 不能为负")
    for value in range(size):
        events.append(value)
        yield value

stream = values(2)
assert events == []
assert next(stream) == 0 and events == ["entered", 0]
assert list(stream) == [1]
assert list(stream) == []

bad = values(-1)  # 尚未抛错
try:
    next(bad)
except ValueError:
    pass
else:
    raise AssertionError("消费时才校验")
```

如果 API 必须在调用时立即拒绝参数，用外层普通函数校验，再返回内层生成器。不要只是把 `yield` 代码前移，因为只要函数体中存在 yield，它仍是生成器函数。

## 6.4 生成器表达式与执行时机

<!-- verify: run -->
```python
numbers = (n * n for n in range(4))
assert sum(numbers) == 14
assert sum(numbers) == 0
assert sum(n * n for n in range(4)) == 14
```

圆括号表达式通常创建生成器，方括号创建列表。生成器表达式最外层可迭代部分在创建时求值，元素计算通常发生在消费时；如果闭包依赖后来改变的状态，要留意执行时机。

### 生成器表达式只有部分工作延迟

<!-- verify: run -->
```python
events = []
def source():
    events.append('source')
    return [1, 2]
def transform(n):
    events.append(n)
    return n * 10

stream = (transform(n) for n in source())
assert events == ['source']
assert next(stream) == 10
assert events == ['source', 1]
assert list(stream) == [20]
assert list(stream) == []
```

最左侧 for 的可迭代表达式及迭代器建立发生在创建生成器表达式时，其余处理在消费时推进。“惰性”不等于整行没有任何立即执行的部分。生成器函数调用则先返回生成器，函数体要等推进才开始；列表推导式立即构造列表。这三者必须分别判断。

## 6.5 yield from、return 与 StopIteration.value

<!-- verify: run -->
```python
def child():
    yield 1
    return "子任务结束"

def parent():
    result = yield from child()
    yield result

assert list(parent()) == [1, "子任务结束"]
```

`yield from` 委托迭代并能接收子生成器返回值，不只是 `for x in child(): yield x` 的文字缩写。不要在生成器中主动抛 StopIteration 表示结束；用 return，否则可能被转成 RuntimeError。

## 6.6 send、throw、close 与清理

<!-- verify: run -->
```python
def accumulator():
    total = 0
    try:
        while True:
            value = yield total
            total += value
    finally:
        print("生成器已清理")

g = accumulator()
assert next(g) == 0    # 先启动到首个 yield
assert g.send(3) == 3
assert g.send(4) == 7
g.close()
```

`send(value)` 把值作为上次 yield 表达式的结果；未启动的生成器只能先 send(None) 或 next。`throw` 在暂停点注入异常；`close` 请求结束。实际异步业务优先用 async / await，不要用手写 send 协议代替 asyncio。

### send 交付给哪个 yield，return 交付给谁

<!-- verify: run -->
```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            return total
        total += value

stream = accumulator()
assert next(stream) == 0
assert stream.send(4) == 4
assert stream.send(5) == 9
try:
    stream.send(None)
except StopIteration as stop:
    assert stop.value == 9
else:
    raise AssertionError('应已结束')
```

第一次先 `next(g)` 或 `g.send(None)`，让它暂停在 yield；之后 send 的值成为该 yield 表达式的结果，再运行到下一次 yield。`throw` 在暂停点注入异常；`close` 请求以 GeneratorExit 结束，清理时不能继续 yield 普通值。生成器内部用 `return` 结束，手动抛出逃逸的 StopIteration 会被转换成 RuntimeError。`yield from` 不仅转发元素，还代理 send/throw/close 等协议并接收子生成器 return 值；普通 `for/yield` 不完整等价。

## 6.7 itertools 的惰性组合

<!-- verify: run -->
```python
from itertools import chain, islice, count, pairwise, product, combinations, permutations, accumulate
assert list(chain([1, 2], [3])) == [1, 2, 3]
assert list(islice(count(10, 2), 3)) == [10, 12, 14]
assert list(pairwise([1, 4, 9])) == [(1, 4), (4, 9)]
assert list(product(["a", "b"], [1, 2])) == [("a", 1), ("a", 2), ("b", 1), ("b", 2)]
assert list(combinations([1, 2, 3], 2)) == [(1, 2), (1, 3), (2, 3)]
assert len(list(permutations([1, 2, 3], 2))) == 6
assert list(accumulate([1, 2, 3])) == [1, 3, 6]
```

`count`、`cycle`、`repeat` 可能无限；必须限制消费。`tee` 用缓存支持多个游标，游标进度差很大时会吃内存。排列组合的数据量可能指数级增长，惰性不消除结果总量。

## 6.8 groupby 是相邻分组

<!-- verify: run -->
```python
from itertools import groupby
records = [("B", 2), ("A", 1), ("B", 3)]
ordered = sorted(records, key=lambda x: x[0])
groups = {key: [row[1] for row in rows] for key, rows in groupby(ordered, key=lambda x: x[0])}
assert groups == {"A": [1], "B": [2, 3]}
```

`groupby` 不等同 SQL GROUP BY：相同键必须先相邻。每个组共享底层输入，通常应及时消费，不能把所有组迭代器存起来再逐一读取。

### 多次遍历需求会改变 API 的类型与内存契约

函数接收 Iterable 不等于可以遍历两遍。下面先求总和再求数量的写法，对 list 成功，对一次性迭代器失败。需要一次消费同时维护累计量，或明确要求 Sequence，或接受物化成本。

<!-- verify: run -->
```python
def mean_once(values):
    total = count = 0
    for value in values:
        total += value
        count += 1
    if not count:
        raise ValueError("不能对空输入求均值")
    return total / count

assert mean_once(iter([2, 4, 6])) == 4
assert mean_once([2, 4, 6]) == 4
```

`tee` 让多个消费者看到相同输入，但慢消费者会使缓存累积；它没有消除“保存还未消费数据”的成本。`groupby` 的子迭代器与主迭代器共享游标，必须先消费当前组，或物化当前组后再前进。

### groupby 的组和 tee 的分支仍受原迭代器约束

<!-- verify: run -->
```python
from itertools import groupby, tee, islice
groups = groupby('AABBA')
key, first = next(groups)
assert key == 'A' and next(first) == 'A'
key, second = next(groups)
assert key == 'B' and list(first) == []
assert list(second) == ['B', 'B']
left, right = tee(iter([1, 2, 3]))
assert list(islice(left, 2)) == [1, 2]
assert list(right) == [1, 2, 3]
assert list(left) == [3]
```

`groupby` 的组共享底层输入，外层推进后旧组可能不能再读，需保存时及时转成 list。`tee` 通过缓存照顾较慢分支，不是免费复制数据源；分支进度差很大时缓存也很大。`islice` 会消费输入，`takewhile` 会消耗第一个不满足条件的元素。设计流水线时把“谁已经读走了数据”与“内存里还留着什么”一起分析。[itertools 参考](https://docs.python.org/3.14/library/itertools.html)

## 6.9 流水线示例

<!-- verify: run -->
```python
from io import StringIO

def valid_amounts(lines):
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        yield int(line)

with StringIO("10\n#备注\n20\n\n30\n") as source:
    total = sum(n for n in valid_amounts(source) if n >= 20)
assert total == 50
```

这里文件逐行读取、过滤逐个进行，sum 不保存所有元素。若在 with 内创建生成器却在 with 外消费文件，文件可能已关闭；资源生命周期必须覆盖实际迭代过程。

### 提前退出时谁负责关闭生成器里的文件

`break` 退出 for 不等于对任意迭代器调用 close。资源位于生成器内部时，应让使用方显式拥有整个迭代生命周期。

<!-- verify: run -->
```python
from contextlib import closing
from io import StringIO

events = []
def rows():
    with StringIO("A\nB\n") as source:
        try:
            for line in source:
                yield line.strip()
        finally:
            events.append("closed")

with closing(rows()) as stream:
    for row in stream:
        assert row == "A"
        break
assert events == ["closed"]
```

本例没有依赖 CPython 引用计数碰巧及时回收生成器。真正大文件可把 StringIO 换成 open，但仍应让 with 覆盖实际消费。一个更简单的设计是由调用方打开文件，把文件迭代器交给纯转换函数，后者不负责关闭它。

验收：使用包含空输入、单项、非法中间行和提前退出的测试；指出哪一步分配了整份列表；给出额外空间与输入规模之间的关系。只说“使用 yield 所以内存 O(1)”不够，结果收集和聚合表也占内存。

延伸：[迭代器与生成器](https://docs.python.org/3.14/tutorial/classes.html#iterators)、[itertools](https://docs.python.org/3.14/library/itertools.html)。


---

# 07｜模块、包与依赖管理

> 本章目标：从模块组织走到可安装的发行包。
>
> 阅读重点：按配套文件完成一个独立练习包，区分源码可运行与安装后可运行。

## 7.1 模块就是命名空间

一个 `.py` 文件通常是一个模块。import 寻找模块、创建模块对象、执行顶层代码，并绑定名称。重复导入通常使用 `sys.modules` 缓存，而不是重复执行所有代码。它与 Go 的包初始化有可比之处，但运行时导入、名称绑定和缓存规则不同。

<!-- verify: run -->
```python
import math
from math import sqrt as square_root
assert math.sqrt(81) == square_root(81) == 9
import sys
assert sys.modules["math"] is math
```

`from m import x` 把当时的对象绑定到当前名称；以后模块重新赋值 `m.x` 不会自动更新这个绑定。如果需要读取模块的动态状态，使用 `import m; m.x`。

### 导入绑定不是动态别名

理解 `import module` 与 `from module import name` 的区别，会直接影响配置刷新、测试 patch 和循环依赖。下例只在内存中建立模块，不改真实环境：

<!-- verify: run -->
```python
import sys
from types import ModuleType

module = ModuleType("_tutorial_settings")
module.limit = 10
module.tags = []
sys.modules[module.__name__] = module
try:
    import _tutorial_settings as settings
    from _tutorial_settings import limit, tags
    settings.limit = 20
    settings.tags.append("new")
    assert limit == 10
    assert settings.limit == 20
    assert tags == ["new"]
finally:
    del sys.modules[module.__name__]
```

`limit` 绑定原整数对象，模块重新绑定不会同步修改它；`tags` 与模块属性最初指向同一列表，所以能看到原地修改。如果模块也重新绑定 tags，那么已导入的局部 tags 仍指向旧列表。这个规则与第 02 章的名称绑定完全一致，不需要再发明一套“导入特殊复制规则”。

循环导入的关键不只是存在环，而是在模块尚未执行到定义某对象的位置时，另一个模块就尝试读取它。把共享协议或模型提取到不依赖业务实现的模块，通常比在各处挪动 import 更可靠。

## 7.2 包结构与 __init__.py

```text
demo_project/
  pyproject.toml
  src/
    billing/
      __init__.py
      __main__.py
      cli.py
      money.py
      service.py
  tests/
    test_money.py
```

普通包有 `__init__.py`；命名空间包允许某些没有它的目录组合成一个包，不意味着任何缺少文件的目录都能在所有启动方式下正确导入。`__init__.py` 可以暴露公共 API，但应避免连接数据库或发网络请求等副作用。

相对导入从包上下文解释。不要直接执行 `python src/billing/service.py` 再临时插入 sys.path 补救；安装项目后从 `python -m billing` 或 console script 入口启动。

### 配套文件：可以照着建立的完整包

按上面的 `demo_project/` 目录分别保存以下文件；这些片段需要同一个包上下文，验证器只编译，不单独运行。`pyproject.toml` 使用 7.6 的配置。

文件 `src/billing/__init__.py`：

```python
"""账单演示包；导入时不运行命令行。"""
from .money import cents

__all__ = ["cents"]
```

文件 `src/billing/money.py`：

```python
def cents(yuan: int) -> int:
    if type(yuan) is not int or yuan < 0:
        raise ValueError("本例只接受非负整数元")
    return yuan * 100
```

文件 `src/billing/service.py`：

```python
from .money import cents

def total(yuan: int, count: int) -> int:
    if type(count) is not int or count < 0:
        raise ValueError("数量必须为非负整数")
    return cents(yuan) * count
```

文件 `src/billing/cli.py`：

```python
import argparse
from .service import total

def main() -> int:
    parser = argparse.ArgumentParser(description="计算整数元商品的合计分值")
    parser.add_argument("yuan", type=int)
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    try:
        amount = total(args.yuan, args.count)
    except ValueError as exc:
        parser.error(str(exc))
    print(amount)
    return 0
```

文件 `src/billing/__main__.py`：

```python
from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
```

文件 `tests/test_money.py`：

```python
import unittest
from billing.service import total

class BillingTests(unittest.TestCase):
    def test_total_in_cents(self):
        self.assertEqual(total(5, 3), 1500)

    def test_reject_negative_count(self):
        with self.assertRaises(ValueError):
            total(5, -1)
```

本例使用整数元避免让包管理教学混入小数舍入规则。包的内部相对导入保留了所属关系；`src` 布局要求先安装包，避免项目根目录碰巧可导入掩盖分发问题。

## 7.3 __main__、__all__ 与循环导入

`__main__.py` 定义 `python -m package` 的入口；`if __name__ == "__main__"` 保护普通模块的脚本入口。`__all__` 影响 `from module import *` 导入哪些名字，不强制访问权限。

<!-- verify: run -->
```python
import importlib
module = importlib.import_module("json")
assert module.loads('{"ok": true}') == {"ok": True}
```

循环导入常见于 A 顶层导入 B，B 又读取尚未初始化完成的 A。优先提取共享模型、降低模块耦合；只在确有必要时采用函数内延迟导入。不要用 reload 作为生产依赖管理机制。

### 真实文件实验：导入缓存与模块入口

<!-- verify: run -->
```python
from pathlib import Path
from tempfile import TemporaryDirectory
import subprocess, sys

with TemporaryDirectory() as directory:
    root = Path(directory)
    package = root / 'lesson_package'
    package.mkdir()
    (package / '__init__.py').write_text("print('init')\n", encoding='utf-8')
    (package / 'value.py').write_text('answer = 42\n', encoding='utf-8')
    (package / '__main__.py').write_text(
        "from .value import answer\nprint(answer)\n", encoding='utf-8',
    )
    # 子进程有意不使用 -I，让临时 cwd 中的练习包可被导入。
    imported = subprocess.run(
        [sys.executable, '-B', '-c', 'import lesson_package; import lesson_package'],
        cwd=root, capture_output=True, text=True, encoding='utf-8',
        check=True, timeout=5,
    )
    launched = subprocess.run(
        [sys.executable, '-B', '-m', 'lesson_package'],
        cwd=root, capture_output=True, text=True, encoding='utf-8',
        check=True, timeout=5,
    )
    assert imported.stdout.splitlines() == ['init']
    assert launched.stdout.splitlines() == ['init', '42']
```

同一解释器重复 import 通常只初始化一次；另一个子进程有独立模块缓存，会重新初始化。`-m package` 执行包入口且保留相对导入上下文。这个实验验证模块执行，不代表已验证 wheel 的构建、安装和包数据分发。

## 7.4 sys.path、同名遮蔽与缓存

<!-- verify: run -->
```python
import sys, json
assert isinstance(sys.path, list)
print(json.__file__)
```

不要给业务文件起名 `json.py`、`typing.py`、`requests.py`，它们可能遮蔽标准库或依赖。遇到 `partially initialized module`，先检查文件名、导入链和启动目录。`__pycache__` 是字节码缓存；删缓存不能修复真实导入循环或缺失源码。

### 启动方式、当前目录和导入位置是三件事

| 情况 | 应先检查 | 常见误判 |
|---|---|---|
| `python path/to/tool.py` | 脚本目录通常进入搜索路径；模块名是 `__main__` | 认为当前工作目录自动变成脚本目录 |
| `python -m package.module` | 包必须可导入，按模块上下文执行入口 | 把它当作文件路径命令 |
| 交互式或 `-c` | 当前目录通常参与模块搜索 | 只在仓库根目录测试就认定安装成功 |
| `python -I` | 隔离模式排除部分路径和环境影响 | 认为隔离模式限制了文件系统权限 |

`open('config.toml')` 按当前工作目录解释，不按源码目录解释。包随附资源用 `importlib.resources`；用户输入文件路径由 CLI 明确解释。导入问题先打印解释器、模块来源、包上下文，再考虑修改路径：

<!-- verify: run -->
```python
import sys
import json
import importlib.util
assert sys.executable
spec = importlib.util.find_spec('json')
assert spec is not None and spec.origin == json.__file__
assert json.__package__ == 'json'
print(sys.executable, json.__file__)
```

模块对象在顶层代码执行完成之前就进入 `sys.modules`，这让循环导入能看到“部分初始化”的模块。`reload` 重新执行模块代码，不会替换其他地方保存的旧函数/旧类实例，也不保证清空旧字典。`.pyc` 是解释器相关的缓存，不是通用独立可执行文件。[导入系统参考](https://docs.python.org/3.14/reference/import.html)

## 7.5 pip、发行包与导入包名

```powershell
python -m pip install requests
python -m pip show requests
python -m pip list
python -m pip check
python -m pip freeze > requirements.txt
python -m pip install -r requirements.txt
```

命令示意会安装第三方依赖，本教程未自动执行。发行包名与 import 名不一定相同，例如某些库的安装名与模块名不同。只安装可信来源包，警惕拼写相近的仿冒包。

`freeze` 记录已安装版本，是环境快照，不等于完整跨平台锁文件；系统库、Python 小版本、平台专用 wheel、间接依赖解析也影响可复现性。团队应固定工具链、保存锁定结果，并在目标平台验证。

## 7.6 pyproject.toml：构建与项目元数据

示例项目配置，放到一个新项目使用；本教程不会改动你的当前项目依赖：

```toml
[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[project]
name = "billing-learning-demo"
version = "0.1.0"
description = "Python packaging exercise"
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
dev = ["pytest", "ruff", "mypy"]

[project.scripts]
billing-demo = "billing.cli:main"

[tool.setuptools.packages.find]
where = ["src"]
```

`build-system` 声明构建后端；`project.dependencies` 声明运行依赖；`optional-dependencies` 声明可选依赖组；`tool.*` 是工具配置。`project.scripts` 指向可导入函数，不是文件路径。你必须真的提供 `billing/cli.py` 的 `main`。

## 7.7 安装、构建、检查分发物

```powershell
python -m pip install -e '.[dev]'
python -m pip install build
python -m build
python -m pip install dist/billing_learning_demo-0.1.0-py3-none-any.whl
```

editable 安装适合开发，源码修改通常可直接被导入；它不代替验证 wheel。wheel 是构建后的分发包，sdist 是源码分发。原生扩展 wheel 还带有解释器 ABI 与平台约束。

对发布项目，另建干净虚拟环境安装生成的 wheel，运行最小入口与测试，防止仅源码目录存在时可用、安装后缺文件。发布到公共仓库属于独立操作，本教程只说明流程。

### 安装后验证与源码目录验证是两件事

在你另建的 demo_project 根目录，先用开发环境执行：

```powershell
python -m pip install -e .
python -m billing 5 --count 3
python -m unittest discover -s tests -v
```

预期第一条业务命令输出 `1500`，测试覆盖合计与非法数量。构建 wheel 后，使用独立环境安装该 wheel，并从项目外的工作目录运行入口。应看到相同输出，且 `billing.__file__` 来自安装环境，而不是意外拾取源码目录。

| 层次 | 证明的内容 | 不能证明的内容 |
|---|---|---|
| 源码编译 | 当前解释器接受语法 | 导入依赖存在、运行逻辑正确 |
| editable 安装 | 开发环境能定位源码 | wheel 包含了必要文件 |
| wheel 安装 | 构建产物可以安装 | 所有平台 ABI 都兼容 |
| 项目外运行入口 | 没有依赖当前目录偶然导入 | 生产网络和数据库可用 |

依赖管理也要区分库与应用：库通常声明允许的依赖范围，让使用方能共同解析；应用应记录实际部署解析结果。直接依赖是你主动选用的 API，传递依赖是这些库依赖的库。`pip freeze` 把两者都列出，不表达为什么需要某个包，也不自动约束 Python 版本或操作系统库。

本节安装、构建命令供手动练习，本轮未执行包安装和发布。验收时应保存解释器版本、构建工具版本、wheel 文件名和项目外运行结果，而不是只截一张 IDE 运行成功的图。

## 7.8 配置与资源文件

<!-- verify: run -->
```python
import os
from importlib.metadata import PackageNotFoundError, version
timeout = int(os.environ.get("APP_TIMEOUT", "3"))
assert isinstance(timeout, int)
try:
    print(version("pip"))
except PackageNotFoundError:
    print("当前解释器没有安装 pip 发行包")
```

读取包内数据优先用 `importlib.resources`，不要假定运行时 cwd 就是源码目录。环境变量全是文本，也需要解析、范围校验、默认值策略；机密不写入仓库。

延伸：[官方模块教程](https://docs.python.org/3.14/tutorial/modules.html)、[PyPA 打包指南](https://packaging.python.org/en/latest/tutorials/packaging-projects/)。

### 工程基础的最小责任划分

| 对象 | 负责什么 | 不负责什么 |
|---|---|---|
| Python 解释器 | 执行语法与对象协议 | 自动安装项目依赖 |
| venv | 隔离一组安装位置和入口 | 隔离操作系统、网络与任意文件访问 |
| 模块 / 导入包 | 组织运行时名称与代码 | 与安装发行包名一一对应 |
| 发行包元数据 | 声明版本、依赖、入口 | 保证源目录测试覆盖安装后行为 |
| CLI 入口 | 读取参数、配置输出与退出码 | 导入时就执行整套程序 |

激活 venv 主要调整命令解析；直接调用 `.venv/Scripts/python.exe` 也能使用环境。`sys.prefix != sys.base_prefix` 可识别常规 venv，别只看提示符。库模块在 import 时定义函数和类，入口在调用时加载配置、分配资源、执行工作。可复用函数返回结果或抛异常，由 CLI 决定 stdout、stderr 和退出码；不要在深层工具函数中随意 `sys.exit()`。

包数据不保证对应一个长期存在的普通路径。`importlib.resources.files(package)` 返回资源访问对象；外部 API 必须要真实路径时，用 `as_file()` 的上下文，并在上下文内消费路径。不要把资源临时路径保存到退出上下文后的全局变量。


---

# 08｜面向对象与数据建模

> 本章目标：为业务数据选择清晰的模型与行为边界。
>
> 阅读重点：比较普通类、dataclass、NamedTuple 和组合；明确不变量、相等性与可变性。

## 8.1 类、实例与 self

<!-- verify: run -->
```python
class Account:
    currency = "CNY"

    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("充值金额必须大于 0")
        self.balance += amount
        return self.balance

account = Account("jackie", 100)
assert account.deposit(20) == 120
assert Account.deposit(account, 5) == 125
```

`self` 是显式接收实例的参数，名称是约定。`__init__` 初始化已创建的对象，不能返回业务值；创建对象主要由 `__new__` 负责。`obj.method(...)` 通过方法绑定自动提供实例；`Class.method(obj, ...)` 可以显式提供。它与 Go 的接收者都表达“对哪个对象操作”，具体绑定机制见第 09 章。

## 8.2 实例属性与类属性

<!-- verify: run -->
```python
class User:
    role = "reader"
    def __init__(self, name):
        self.name = name
        self.tags = []

a, b = User("A"), User("B")
a.tags.append("python")
assert b.tags == []
a.role = "admin"
assert a.role == "admin" and b.role == "reader"
assert User.role == "reader"
```

把 `tags=[]` 放在类体会变成共享类属性。给实例赋 `a.role` 一般会遮蔽类属性，但描述符可能改变这个规则，第 09 章继续解释。

## 8.3 访问约定与名称改写

<!-- verify: run -->
```python
class Vault:
    def __init__(self):
        self._cache = {}
        self.__token = "example"

v = Vault()
assert v._Vault__token == "example"
```

`_name` 表示内部使用约定；`__name` 触发类内名称改写，主要避免子类意外冲突，不是安全访问控制。`__name__` 这类双边下划线名称通常留给语言协议，不随意自创。

## 8.4 property 与输入约束

<!-- verify: run -->
```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("低于绝对零度")
        self._celsius = value

t = Temperature(20)
t.celsius = 25
assert t.celsius == 25
```

property 能保留属性访问语法，同时加入校验或计算。不要把会执行远程请求、非常昂贵或频繁失败的操作藏成看起来廉价的属性。

## 8.5 实例方法、classmethod、staticmethod

<!-- verify: run -->
```python
class User:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_mapping(cls, data):
        return cls(data["name"])

    @staticmethod
    def valid_name(name):
        return bool(name.strip())

assert User.from_mapping({"name": "jackie"}).name == "jackie"
assert User.valid_name("A")
```

classmethod 接收实际调用类，适合替代构造器并支持继承；staticmethod 不接收隐式实例 / 类，适合逻辑上相关的纯函数。但很多静态方法直接做成模块函数就足够。

### 为什么赋给实例的函数不会自动得到 self

<!-- verify: run -->
```python
from types import MethodType
class Item:
    def name(self):
        return type(self).__name__
    @classmethod
    def make(cls):
        return cls()

class Child(Item):
    pass

obj = Item()
assert obj.name.__self__ is obj
assert obj.name.__func__ is Item.name
obj.plain = lambda: 'plain'
assert obj.plain() == 'plain'
obj.bound = MethodType(lambda self: self.name(), obj)
assert obj.bound() == 'Item'
assert type(Child.make()) is Child
```

类字典中的函数经描述符协议绑定，实例字典中的普通函数直接取出，不会自动插入 self。classmethod 绑定实际调用类，所以替代构造器写 `cls(...)` 才能保留子类；写死 `Item(...)` 就失去这个性质。staticmethod 不参与实例或类的隐式传参。

## 8.6 继承、重写与 super

<!-- verify: run -->
```python
class Animal:
    def speak(self):
        return "声音"

class Dog(Animal):
    def speak(self):
        return super().speak() + ":汪"

assert Dog().speak() == "声音:汪"
assert isinstance(Dog(), Animal)
assert issubclass(Dog, Animal)
```

方法默认支持动态分派；不会按参数签名保存多个同名方法实现。定义同名方法两次，后一个覆盖前一个。使用默认参数、不同方法名或 singledispatch 表达不同情况。

## 8.7 鸭子类型、抽象基类与组合

<!-- verify: run -->
```python
from abc import ABC, abstractmethod

class Sender(ABC):
    @abstractmethod
    def send(self, message):
        raise NotImplementedError

class MemorySender(Sender):
    def __init__(self):
        self.messages = []
    def send(self, message):
        self.messages.append(message)

class NotificationService:
    def __init__(self, sender):
        self.sender = sender
    def notify(self, user):
        self.sender.send(f"你好，{user}")

sender = MemorySender()
NotificationService(sender).notify("张三")
assert sender.messages == ["你好，张三"]
```

运行时只要对象提供所需行为，通常就可参与协作。ABC 在实例化阶段约束抽象方法是否实现；静态结构约束可以用 Protocol。组合便于替换实现与测试，通常比深层继承树更易维护。

## 8.8 dataclass 与默认工厂

<!-- verify: run -->
```python
from dataclasses import dataclass, field, asdict, replace

@dataclass(slots=True)
class Order:
    id: int
    tags: list[str] = field(default_factory=list)
    amount: int = 0

    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("金额不能为负")

a, b = Order(1), Order(2)
a.tags.append("new")
assert b.tags == []
assert asdict(b) == {"id": 2, "tags": [], "amount": 0}
assert replace(b, amount=50) == Order(2, amount=50)
```

dataclass 自动生成初始化、repr、相等比较等方法，不自动校验注解类型。`default_factory` 每次创建实例时生成新容器。`asdict` 会递归转换并复制部分值，复杂大对象别当作无成本序列化。

### 数据模型应该保护哪些不变量

dataclass 减少样板代码，但不会替你决定单位、合法范围、状态迁移或所有权。一个金额对象至少应说明币种、整数分值及允许的运算；不要仅有 `amount: int` 就认为模型完整。

<!-- verify: run -->
```python
from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Money:
    cents: int
    currency: str = "CNY"

    def __post_init__(self):
        if type(self.cents) is not int:
            raise TypeError("cents 必须是整数分")
        if self.currency not in {"CNY", "USD"}:
            raise ValueError("示例只支持 CNY / USD")

    def __add__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        if self.currency != other.currency:
            raise ValueError("不同币种不能直接相加")
        return Money(self.cents + other.cents, self.currency)

assert Money(120) + Money(30) == Money(150)
assert len({Money(120), Money(120)}) == 1
try:
    Money(100, "CNY") + Money(100, "USD")
except ValueError:
    pass
else:
    raise AssertionError("必须明确换汇规则")
```

该对象允许负数，便于表达退款或余额变化；如果领域规定禁止负数，应在构造或具体操作中增加限制。关键是明确约定，不能把“货币通常非负”的直觉偷偷嵌入通用模型。

dataclass 默认相等比较关注同类字段值，适合值对象；数据库实体可能按身份或业务主键定义相等性，不应不加判断地使用所有字段比较。`repr` 自动包含字段，密码或令牌字段应使用 `field(repr=False)`，并另外检查日志和序列化输出。

### dataclass 的字段、构造参数和相等规则

<!-- verify: run -->
```python
from dataclasses import dataclass, field, InitVar, fields
from typing import ClassVar

@dataclass(kw_only=True)
class Record:
    category: ClassVar[str] = 'record'
    raw: InitVar[str]
    name: str = field(init=False)
    trace: str = field(default='', compare=False, repr=False)
    def __post_init__(self, raw):
        self.name = raw.strip()

a = Record(raw=' a ', trace='one')
b = Record(raw='a', trace='two')
assert a == b
assert [f.name for f in fields(Record)] == ['name', 'trace']
assert 'trace=' not in repr(a)
```

ClassVar 不作为实例字段；InitVar 只送入初始化流程，生成器不会把它存成实例字段；`init=False` 字段需自行建立。`compare=False` 明确排除非身份信息。生成的 `__init__` 不会自动调用普通基类的 `__init__`，需要时在 `__post_init__` 显式协调。

默认 `eq=True, frozen=False` 的 dataclass 通常不可哈希；`eq=True, frozen=True` 通常生成 hash，但字段仍须可哈希。`unsafe_hash=True` 不能让可变键安全。位置字段中无默认值项不能跟在有默认值项后面，继承字段也会影响顺序；`kw_only` 可减少演进时的位置参数歧义。[dataclasses 参考](https://docs.python.org/3.14/library/dataclasses.html)

## 8.9 frozen、slots、NamedTuple 与 Enum

<!-- verify: run -->
```python
from dataclasses import dataclass
from typing import NamedTuple
from enum import Enum, auto

@dataclass(frozen=True)
class Coordinate:
    x: int
    y: int

class Pair(NamedTuple):
    key: str
    value: int

class Status(Enum):
    TODO = auto()
    DONE = auto()

assert Coordinate(1, 2) == Coordinate(1, 2)
assert Pair("x", 1).key == "x"
assert tuple(Pair("x", 1)) == ("x", 1)
assert Status.TODO.name == "TODO"
assert Status.TODO is not Status.DONE
```

`frozen=True` 阻止普通字段重新赋值，不会递归冻结内部列表，也不是安全沙箱。slots 限制通常的动态实例属性并可节省空间，但继承类可能仍有 `__dict__`。NamedTuple 有元组语义；dataclass 更适合演进的业务模型。Enum 用来表达有限状态，外部持久化时应规划稳定值，不能随意依赖 auto 编号。

### frozen、slots 与深不可变不是一回事

<!-- verify: run -->
```python
from dataclasses import dataclass, field, FrozenInstanceError, replace

@dataclass(frozen=True)
class Settings:
    tags: list[str] = field(default_factory=list)

original = Settings(["a"])
original.tags.append("b")
assert original.tags == ["a", "b"]
derived = replace(original)
assert derived.tags is original.tags
try:
    original.tags = []
except FrozenInstanceError:
    pass
else:
    raise AssertionError("普通字段赋值应被阻止")
```

这里 frozen 保护字段重新绑定；replace 创建新实例但未显式替换的列表仍共享。需要配置快照可以选择 `tuple[str, ...]`、frozenset 以及同样不可变的嵌套值。不要把 `asdict` 当作通用 JSON 序列化器，Decimal、datetime 和自定义值仍需要协议。

| 需求 | 优先选择 | 原因 |
|---|---|---|
| 临时索引或灵活数据 | dict | 构造简单，但字段约束需另做 |
| 返回少量固定位置值 | tuple / NamedTuple | 易解包，固定位置 |
| 演进中的业务记录 | dataclass | 字段名清楚，可加不变量 |
| 行为与生命周期为主 | 普通类 | 显式控制状态、资源、方法 |
| 可替换能力 | Protocol + 组合 | 调用方依赖所需行为 |

验收：能解释一个类型为何需要类、字段是否可变、调用方是否能持有内部列表，以及相等性如何定义。不要因为 Go 常用 struct，就把任何 Python 字典都强制包装成类。

### Enum 成员、名称、值、别名与 Flag

<!-- verify: run -->
```python
from enum import Enum, IntEnum, Flag, auto, unique
class State(Enum):
    READY = 'ready'
    ALIAS = 'ready'
assert State('ready') is State.READY
assert State['READY'] is State.READY
assert State.ALIAS is State.READY
assert list(State) == [State.READY]
assert State.READY != 'ready'

@unique
class Code(IntEnum):
    OK = 1
assert Code.OK == 1

class Permission(Flag):
    READ = auto()
    WRITE = auto()
both = Permission.READ | Permission.WRITE
assert Permission.READ in both
```

普通 Enum 把成员与外部标量区分；IntEnum 和 StrEnum 为兼容整数/字符串接口而允许更多跨类型行为。重复值默认形成别名，禁止时加 `unique`。Flag 表达可组合位标志，不适合互斥状态。外部值解析用 `State(value)`，按名字查询用 `State[name]`，二者错误分别是 ValueError 和 KeyError。[enum 参考](https://docs.python.org/3.14/library/enum.html)

## 8.10 多重继承与 Mixin

<!-- verify: run -->
```python
class A:
    def run(self):
        return ["A"]
class B(A):
    def run(self):
        return ["B"] + super().run()
class C(A):
    def run(self):
        return ["C"] + super().run()
class D(B, C):
    pass

assert D().run() == ["B", "C", "A"]
assert [cls.__name__ for cls in D.__mro__] == ["D", "B", "C", "A", "object"]
```

super 沿 MRO 找下一个实现，并不固定指“直接父类”。协作多继承要求调用链和参数约定一致；Mixin 尽量小而无状态。业务模型优先组合，不为了复用一两个方法制造菱形继承。

延伸：[官方类教程](https://docs.python.org/3.14/tutorial/classes.html)。

### 协作式 super：每层消费自己的参数并继续传递

<!-- verify: run -->
```python
class Root:
    def __init__(self, **kwargs):
        if kwargs:
            raise TypeError(f'未知参数: {sorted(kwargs)}')
        super().__init__()

class Named(Root):
    def __init__(self, *, name, **kwargs):
        self.name = name
        super().__init__(**kwargs)

class Tagged(Root):
    def __init__(self, *, tag, **kwargs):
        self.tag = tag
        super().__init__(**kwargs)

class Item(Named, Tagged):
    pass

obj = Item(name='book', tag='python')
assert (obj.name, obj.tag) == ('book', 'python')
assert Item.__mro__ == (Item, Named, Tagged, Root, object)
```

MRO 使用 C3 线性化，同时保持局部基类顺序和继承关系；矛盾的顺序会在建类时抛 TypeError，不会任意选一条。这里 Named 中的 super 对 Item 实例继续到 Tagged。每一层必须恰好合作调用下一层，并约定参数转发；夹杂 `Root.__init__(self)` 之类固定父类调用可能跳过或重复初始化。普通子类若覆盖 `__init__` 也不会自动补调父类初始化。


---

# 09｜协议、描述符与元编程

> 本章目标：理解日常语法背后的对象协议。
>
> 阅读重点：先掌握属性查找和方法绑定，再按需要学习描述符、元类及反射。

## 9.1 特殊方法让对象融入语言

对象支持什么语法，由其类型上的特殊方法决定。优先调用 `len(x)`、`str(x)`、`iter(x)`，而不是到处直接调用双下划线方法。

<!-- verify: run -->
```python
class Team:
    def __init__(self, members):
        self._members = list(members)
    def __len__(self):
        return len(self._members)
    def __iter__(self):
        return iter(self._members)
    def __contains__(self, member):
        return member in self._members
    def __getitem__(self, index):
        return self._members[index]
    def __repr__(self):
        return f"Team({self._members!r})"

team = Team(["A", "B"])
assert len(team) == 2
assert "A" in team
assert team[1] == "B" and team[:] == ["A", "B"]
assert list(team) == ["A", "B"]
assert repr(team) == "Team(['A', 'B'])"
```

常用协议包括容器、数值、比较、调用、上下文管理、迭代和异步协议。`__bool__` 定义真值；没有它时可以退到 `__len__`。特殊方法通常从类型查找，因此给单个实例临时赋 `obj.__len__` 不会可靠改变 `len(obj)`。

## 9.2 相等性、哈希与 NotImplemented

<!-- verify: run -->
```python
class UserKey:
    def __init__(self, tenant, user):
        self.tenant, self.user = tenant, user
    def __eq__(self, other):
        if not isinstance(other, UserKey):
            return NotImplemented
        return (self.tenant, self.user) == (other.tenant, other.user)
    __hash__ = None  # 当前对象可变，禁止作为 dict 键

assert UserKey("a", 1) == UserKey("a", 1)
assert UserKey("a", 1) != "a:1"
```

相等对象必须具有相等哈希，且对象作为键期间哈希应稳定。实现 `__eq__` 后不要随意复用按身份的 hash。需要不可变可哈希键，可用 frozen dataclass 且字段都可哈希。

`NotImplemented` 告诉解释器“这个操作数组合我不支持”，允许尝试反向操作或其他回退。`NotImplementedError` 是异常，表示功能未实现，两者完全不同。

### NotImplemented 不等于 False：给另一侧一次协商机会

<!-- verify: run -->
```python
class Left:
    def __add__(self, other):
        return NotImplemented
    def __eq__(self, other):
        return NotImplemented
class Right:
    def __radd__(self, other):
        return 'right handled'

left = Left()
assert left + Right() == 'right handled'
assert (left == object()) is False
assert left == left
assert Left.__hash__ is None
```

两侧都不支持算术或排序时通常抛 TypeError；相等比较协商失败时可退回身份比较。提前返回 False 就是声称“已经比较，确实不等”，可能阻止另一侧实现发挥作用。右侧是更具体的子类时还有反射方法优先规则，不能把所有二元运算都简化成单次左侧方法调用。Python 3.14 起对 NotImplemented 取 bool 会报 TypeError。

## 9.3 运算重载与可调用对象

<!-- verify: run -->
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Vector:
    x: int
    y: int
    def __add__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

class Multiplier:
    def __init__(self, factor):
        self.factor = factor
    def __call__(self, value):
        return value * self.factor

assert Vector(1, 2) + Vector(3, 4) == Vector(4, 6)
assert Multiplier(3)(5) == 15
```

相关方法还有 `__radd__`、`__iadd__`、`__lt__`、`__format__`、`__index__`。重载应符合读者对运算的预期，不要用 `+` 暗中触发数据库写入。

### 特殊方法查类型；整数转换和整数索引不是一个协议

<!-- verify: run -->
```python
class Container:
    def __len__(self):
        return 2

obj = Container()
obj.__len__ = lambda: 99
assert obj.__len__() == 99
assert len(obj) == 2

class Index:
    def __index__(self):
        return 2

assert ['a', 'b', 'c'][Index()] == 'c'
assert list(range(Index())) == [0, 1]
```

隐式特殊方法查找通常绕过实例字典；不能给实例塞一个 `__call__` 就保证它能被调用。`__int__` 表示可转换成整数，`__index__` 表示具有精确整数身份，可用于切片、range 等。`__getitem__` 要自行处理整数与 slice；`__contains__` 缺失时成员测试可能迭代并消耗输入。自定义协议时除了成功结果，还要保持正确的异常类型。

## 9.4 属性访问：getattr 与 getattribute

<!-- verify: run -->
```python
class Config:
    def __init__(self, values):
        self.values = values
    def __getattr__(self, name):
        try:
            return self.values[name]
        except KeyError as exc:
            raise AttributeError(name) from exc

config = Config({"timeout": 3})
assert config.timeout == 3
assert getattr(config, "missing", 10) == 10
assert hasattr(config, "timeout")
```

`__getattr__` 在普通查找失败后调用；`__getattribute__` 参与几乎所有实例属性访问，容易递归。后者内部读取属性通常要用 `object.__getattribute__(self, name)`。`hasattr` 可能执行属性 getter，不应把它当成无副作用元数据查询。

### 属性查找顺序解释了 property 和方法绑定

在普通 `object.__getattribute__` 的实例属性查找下，可以按以下简化过程理解：

1. 沿类的 MRO 寻找同名类属性；若找到具有读取能力的数据描述符，先执行它。
2. 检查实例字典中的同名属性。
3. 使用类中的非数据描述符或普通类属性；非数据描述符在此执行绑定。
4. 常规查找失败后，属性访问机制才尝试 `__getattr__`。

自定义 `__getattribute__`、元类属性访问和特殊方法隐式查找有各自细节，这个顺序用于理解普通实例，不应当作覆盖所有对象访问的伪代码实现。

<!-- verify: run -->
```python
class NonData:
    def __get__(self, instance, owner=None):
        return "from descriptor"

class Example:
    label = NonData()

    @property
    def fixed(self):
        return "from property"

    def method(self):
        return self

obj = Example()
assert obj.label == "from descriptor"
obj.__dict__["label"] = "from instance"
obj.__dict__["fixed"] = "ignored"
assert obj.label == "from instance"
assert obj.fixed == "from property"
bound = obj.method
assert bound.__self__ is obj
assert bound.__func__ is Example.method
assert bound() is obj
```

普通函数作为类属性时是非数据描述符，访问 `obj.method` 得到绑定方法，因此实例参数会自动传入。property 即使没有 setter，也具有数据描述符行为，所以不能用实例字典同名键绕过普通属性读取。需要不触发描述符的检查工具时，可以研究 `inspect.getattr_static`。

## 9.5 描述符：复用属性管理逻辑

<!-- verify: run -->
```python
class Positive:
    def __set_name__(self, owner, name):
        self.storage = "_" + name
    def __get__(self, instance, owner=None):
        if instance is None:
            return self
        return getattr(instance, self.storage)
    def __set__(self, instance, value):
        if value <= 0:
            raise ValueError("必须为正数")
        setattr(instance, self.storage, value)

class Product:
    price = Positive()
    stock = Positive()
    def __init__(self, price, stock):
        self.price, self.stock = price, stock

p = Product(10, 2)
p.price = 20
assert p.price == 20 and p.stock == 2
```

实现 `__get__`、`__set__` 或 `__delete__` 的类可参与描述符协议。提供 `__set__` / `__delete__` 的是数据描述符，通常优先于实例字典；只有 `__get__` 的非数据描述符通常可被实例同名属性遮蔽。property、方法绑定都与这套机制相关。

### 描述符对象属于类，字段值通常属于实例

描述符自身一般由全部实例共享，把用户值写到 `self.value` 会造成串值；应通过 instance 的字典或其他按实例隔离的存储保存。描述符必须放在类属性位置才能正常参与普通属性访问；放进实例字典不会自动调用它的 `__get__`。

`__set_name__` 是建类时的命名通知，不是每次赋值的回调；运行时追加描述符须自行调用通知，且复用同一描述符对象到多个字段需要管理多个名称。只读 property 仍是数据描述符，赋值报错；`cached_property` 通常计算后把结果写进实例字典，可覆盖或删除以重新计算，因而要求合适的实例字典，也不等于锁保护的只计算一次。[描述符指南](https://docs.python.org/3.14/howto/descriptor.html)

## 9.6 类创建、__new__ 与元类

<!-- verify: run -->
```python
class UpperText(str):
    def __new__(cls, value):
        return super().__new__(cls, value.upper())

assert UpperText("go") == "GO"
Dynamic = type("Dynamic", (), {"kind": "demo"})
assert Dynamic().kind == "demo"
```

不可变类型的值通常在 `__new__` 中构造。类本身也是对象，通常由 type 创建。元类可以控制类创建，但多数注册 / 检查需求用类装饰器或 `__init_subclass__` 更直观。

<!-- verify: run -->
```python
class Plugin:
    registry = {}
    def __init_subclass__(cls, *, name, **kwargs):
        super().__init_subclass__(**kwargs)
        Plugin.registry[name] = cls

class CsvPlugin(Plugin, name="csv"):
    pass

assert Plugin.registry["csv"] is CsvPlugin

class RequireRun(type):
    def __new__(mcls, name, bases, namespace):
        if "run" not in namespace:
            raise TypeError("类必须显式定义 run")
        return super().__new__(mcls, name, bases, namespace)

class Job(metaclass=RequireRun):
    def run(self):
        return "ok"

assert Job().run() == "ok"
```

这是最小机制示例，不是完整插件系统；并发注册、继承方法、重复名称、模块发现与热加载都需要额外规则。元类会引入继承冲突和理解成本，只有普通机制不足时才使用。

### 类创建阶段和实例创建阶段应分开

模块执行到 class 语句时，先执行类体收集命名空间，再由元类创建类对象，并执行相关钩子和类装饰器。随后调用 `MyClass(...)` 才是实例创建阶段，通常由元类的调用逻辑组织 `__new__` 与 `__init__`。

<!-- verify: run -->
```python
events = []
class Base:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        events.append("subclass:" + cls.__name__)

def register(cls):
    events.append("decorate:" + cls.__name__)
    return cls

@register
class Item(Base):
    events.append("class body")
    def __init__(self):
        events.append("instance")

assert events == ["class body", "subclass:Item", "decorate:Item"]
item = Item()
assert events[-1] == "instance"
```

`__set_name__` 在正常类创建时通知描述符名称；创建完类后再随意挂一个描述符，不会自动重复该通知。需要字段管理时优先 property，需要复用字段规则时用描述符，需要对子类注册时考虑 `__init_subclass__`；只有必须控制类创建过程时才考虑元类。

验收：面对“实例字典里有值，但读取返回另一个值”，先查是否有数据描述符；面对“还没创建实例就执行了代码”，先查类体和装饰器。不要从这些现象直接推断 Python 随机执行。

### new 和 init 的职责边界

<!-- verify: run -->
```python
events = []
class Factory:
    def __new__(cls):
        events.append('new')
        return {'ready': True}
    def __init__(self):
        events.append('init')

assert Factory() == {'ready': True}
assert events == ['new']
```

在通常的 type 调用流程中，`__new__` 若返回非该类实例，后续不会对它调用本类初始化。若返回该类已有实例，初始化可能再次执行，因此仅靠 new 缓存对象不自动获得正确的单例生命周期。

理解元类还要分开“继承关系”和“实例关系”：`isinstance(MyClass, type)` 讨论谁创建类对象，`issubclass(MyClass, Base)` 讨论实例行为继承。类创建通常经历基类解析、元类选择、`__prepare__` 命名空间、类体执行、元类创建、`__set_name__` 和 `__init_subclass__` 等钩子，再应用类装饰器。多数扩展需求在后两种钩子或装饰器层就能解决。

## 9.7 反射、inspect 与动态执行

<!-- verify: run -->
```python
import inspect

def fetch(path, *, timeout=3):
    return path, timeout

signature = inspect.signature(fetch)
bound = signature.bind("/users", timeout=5)
assert bound.arguments == {"path": "/users", "timeout": 5}
assert callable(fetch)
```

`getattr` / `setattr` / `dir` / `vars` 可以检查或操作对象；`inspect` 处理签名、源码等。`compile` 编译代码对象，`eval` 求表达式值，`exec` 执行语句；限制 globals 字典并不能构成可靠安全沙箱。不要执行不可信输入。

## 9.8 垃圾回收、弱引用与资源

<!-- verify: run -->
```python
import weakref, gc
class Item:
    pass
item = Item()
ref = weakref.ref(item)
assert ref() is item
del item
gc.collect()
assert ref() is None
```

CPython 常结合引用计数和循环垃圾回收，但这不是所有实现共享的精确销毁时机保证。weakref 不维持对象存活，适合部分缓存与观察者关系。不要依赖 `__del__` 关闭数据库、提交事务或释放锁；显式 with 更确定。`id` 只在对象存活期间标识身份，释放后可能复用。

延伸：[数据模型参考](https://docs.python.org/3/reference/datamodel.html)、[描述符指南](https://docs.python.org/3/howto/descriptor.html)。

### 弱引用不拥有对象，slots 也不等于完全禁止动态行为

<!-- verify: run -->
```python
import weakref
class Slotted:
    __slots__ = ('name', '__weakref__')
    def __init__(self, name):
        self.name = name

obj = Slotted('one')
ref = weakref.ref(obj)
held = ref()
assert held is obj
try:
    obj.other = 1
except AttributeError:
    pass
else:
    raise AssertionError('没有实例字典或相应槽')

class Child(Slotted):
    pass
child = Child('two')
child.other = 1
assert child.__dict__ == {'other': 1}
```

取弱引用结果后先保存在局部变量，再判断是否为 None，避免“检查时还活着、再次获取时已经回收”。slots 子类若没继续约束布局，可以重新获得实例字典；要支持弱引用需合适的 `__weakref__` 槽。`weakref.finalize` 的回调也不能偷偷通过绑定方法强引用目标，否则可能延长目标生命周期。垃圾回收负责内存对象可达性，with 负责确定的资源退出，两者不能互相替代。[weakref 参考](https://docs.python.org/3.14/library/weakref.html)


---

# 10｜类型提示与泛型

> 本章目标：把静态契约与运行时解析连接起来。
>
> 阅读重点：理解 Protocol、泛型和方差；对外部 object 做验证后再进入可信业务模型。

## 10.1 注解不会自动强制运行时类型

<!-- verify: run -->
```python
def duplicate(value: int) -> int:
    return value * 2

assert duplicate(3) == 6
assert duplicate("a") == "aa"  # 运行时可执行，静态检查应报告类型不匹配
```

Go 的编译器类型约束不可直接类比 Python 注解。mypy、Pyright 等工具检查源码；Python 默认不会按注解拒绝实参。Pydantic 等第三方工具可以利用注解做解析和校验，它们有自己的语义。

## 10.2 容器、联合、可空与 Callable

<!-- verify: run -->
```python
from collections.abc import Callable, Iterable, Mapping

def summarize(values: Iterable[int]) -> int:
    return sum(values)

def find_name(users: Mapping[int, str], uid: int) -> str | None:
    return users.get(uid)

def apply(value: int, operation: Callable[[int], int]) -> int:
    return operation(value)

scores: dict[str, list[int]] = {"张三": [80, 90]}
point: tuple[int, int] = (1, 2)
assert summarize(range(4)) == 6
assert find_name({}, 1) is None
assert apply(3, lambda n: n + 1) == 4
```

`tuple[int, str]` 是固定长度异构元组，`tuple[int, ...]` 是变长整数元组。返回可空值不等于参数可省略；可省略需要默认值。输入只读时多用 Mapping / Sequence / Iterable，减少对具体容器的耦合。

## 10.3 Any、object、Never 与 Literal

<!-- verify: run -->
```python
from typing import Any, Literal, Never

def fail(message: str) -> Never:
    raise RuntimeError(message)

def normalize(mode: Literal["fast", "safe"]) -> str:
    return mode.upper()

value: object = "abc"
if isinstance(value, str):
    assert value.upper() == "ABC"
payload: Any = {"untyped": True}
assert normalize("safe") == "SAFE"
```

object 表示任意对象，但使用前需证明支持相应操作；Any 允许绕过大量静态检查。`Never` 表示函数不会正常返回。Literal 限定静态值集合，但运行时仍需校验外部输入。

## 10.4 泛型函数与泛型类

兼容 3.11 的写法：

<!-- verify: run -->
```python
from typing import TypeVar, Generic
from collections.abc import Sequence

T = TypeVar("T")

def first(values: Sequence[T]) -> T:
    if not values:
        raise ValueError("空序列")
    return values[0]

class Box(Generic[T]):
    def __init__(self, value: T):
        self.value = value

assert first([1, 2]) == 1
assert Box[str]("python").value == "python"
```

3.12+ 的类型参数与类型别名写法：

<!-- verify: run -->
```python
type UserId = int
type Page[T] = tuple[list[T], int]

def identity[T](value: T) -> T:
    return value

class Container[T]:
    def __init__(self, value: T):
        self.value = value

assert identity("go") == "go"
assert Container(3).value == 3
```

类型别名改善表达但不创造新运行时类型。泛型约束不等于运行时 `isinstance(x, list[int])`，后者不能用于普通参数化内置容器检查。

## 10.5 Protocol：与 Go 接口相近的结构约束

<!-- verify: run -->
```python
from typing import Protocol, runtime_checkable

@runtime_checkable
class Sender(Protocol):
    def send(self, message: str) -> None: ...

class ConsoleSender:
    def send(self, message: str) -> None:
        print(message)

def notify(sender: Sender) -> None:
    sender.send("任务已创建")

notify(ConsoleSender())
assert isinstance(ConsoleSender(), Sender)
```

实现类不必显式继承 Protocol。`runtime_checkable` 只提供有限运行时成员检查，不完整核验方法参数与返回类型；不能把它当 API 输入验证。

## 10.6 TypedDict、Required、NotRequired

<!-- verify: run -->
```python
from typing import TypedDict, NotRequired

class UserPayload(TypedDict):
    id: int
    name: str
    nickname: NotRequired[str]

payload: UserPayload = {"id": 1, "name": "jackie"}
assert isinstance(payload, dict)
assert payload["name"] == "jackie"
```

TypedDict 描述普通 dict 的键结构，不会生成 dataclass，也不执行运行时校验。`NotRequired[str]` 表示键可以不存在；`str | None` 表示键存在时可取 None，含义不同。`total=False` 可把键默认设为可选，Required 则单独恢复必需键。

### 从未知 JSON 到可信内部模型的完整边界

把 json.loads 的结果写成 TypedDict 注解并不完成验证。边界函数应接受 `object`，逐步证明容器、字段、类型和业务范围，然后返回已规范化的内部模型。

<!-- verify: run -->
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class CreateTask:
    title: str
    priority: int

def parse_task(raw: object) -> CreateTask:
    if not isinstance(raw, dict):
        raise ValueError("请求必须为对象")
    if set(raw) - {"title", "priority"}:
        raise ValueError("包含未知字段")
    title = raw.get("title")
    priority = raw.get("priority", 1)
    if not isinstance(title, str) or not 1 <= len(title.strip()) <= 200:
        raise ValueError("标题不能为空且最多 200 个字符")
    if type(priority) is not int or priority not in {1, 2, 3}:
        raise ValueError("优先级必须为 1、2、3")
    return CreateTask(title.strip(), priority)

assert parse_task({"title": " Learn "}) == CreateTask("Learn", 1)
for raw in [None, [], {"title": " "}, {"title": "x", "priority": True},
            {"title": "x", "priority": None}, {"title": "x", "owner": 7}]:
    try:
        parse_task(raw)
    except ValueError:
        pass
    else:
        raise AssertionError(raw)
```

“priority 缺失使用默认值”和“priority 显式为 None”在这里不同。输入规范化只做一次，业务内部接收 CreateTask，而不再反复从未知 dict 猜字段。HTTP 层可以把 ValueError 映射成清楚的 4xx 错误；日志和返回信息是否包含原输入，需要按数据敏感性决定。

如果团队使用 Pydantic 等库，仍要决定严格类型还是自动转换、未知字段策略、默认值和业务范围。库降低解析样板代码，不消除接口设计责任。

## 10.7 TypeGuard、cast 与 overload

<!-- verify: run -->
```python
from typing import TypeGuard, overload

def is_string_list(value: object) -> TypeGuard[list[str]]:
    return isinstance(value, list) and all(isinstance(x, str) for x in value)

@overload
def convert(value: int) -> str: ...
@overload
def convert(value: str) -> int: ...
def convert(value: int | str) -> str | int:
    return str(value) if isinstance(value, int) else int(value)

assert is_string_list(["a", "b"])
assert convert(123) == "123" and convert("123") == 123
```

TypeGuard 告诉检查器某个布尔函数如何收窄类型；函数实现必须诚实。`cast(T, value)` 只是静态声明，返回原对象，不做转换。overload 是多个静态签名加一个运行时实现，不会按参数类型自动在多份同名业务实现之间分派。

### cast、TypeGuard、TypeIs：声明和证明由不同角色完成

<!-- verify: run -->
```python
from typing import cast, TypeIs

raw = '42'
assert cast(int, raw) is raw
assert int(raw) == 42

def is_text(value: object) -> TypeIs[str]:  # 3.13+
    return isinstance(value, str)

assert is_text('x') and not is_text(42)
```

cast 没有执行检查，`int` 才做转换。TypeGuard 的真分支可声明收窄，通常不能据假分支排除该类型；TypeIs 要求目标类型与输入相容，并提供双分支收窄。两者都信任你写的布尔检查，且检查成功后共享可变对象仍可能被其他代码改变。异步代码中在检查与使用之间 await，尤其要考虑这个间隔。

`@overload` 描述多个静态调用关系，运行时仍只有最终实现；`singledispatch` 才按第一个实参类型做运行时分派，且不会检查 `list[int]` 的每个元素。不要用这两种机制代替参数值校验。

## 10.8 ParamSpec 保留装饰器签名

<!-- verify: run -->
```python
from typing import ParamSpec, TypeVar
from collections.abc import Callable
from functools import wraps
P = ParamSpec("P")
R = TypeVar("R")

def logged(fn: Callable[P, R]) -> Callable[P, R]:
    @wraps(fn)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(fn.__name__)
        return fn(*args, **kwargs)
    return wrapper

@logged
def add(a: int, b: int) -> int:
    return a + b

assert add(2, 3) == 5
```

比 `Callable[..., Any]` 更准确地传递参数和返回值关系。更高级的 Concatenate、TypeVarTuple、Self 见 typing 文档，使用前明确它们解决的静态问题。

### 泛型工具解决的关系不同

| 工具 | 表达关系 | 最小场景 |
|---|---|---|
| TypeVar / `def f[T]` | 多处类型必须相关 | 输入 T，返回 T |
| 有约束 TypeVar | 从给定类型集合选一个一致类型 | 两个参数同时为 str 或同时为 bytes |
| bound | 类型必须满足上界，可保留具体子类型 | 接受某基类的子类并返回同型 |
| Self | 返回接收者所属类型 | 链式实例方法、支持继承的类构造方法 |
| ParamSpec | 整组位置/关键字参数关系 | 装饰器原样转发签名 |
| Concatenate | 在参数组前添加参数 | 注入显式上下文参数 |
| TypeVarTuple / Unpack | 可变长度类型序列 | 异构元组的前后组合 |

这些是静态表达能力，不是运行时自动检查或按类型生成代码。`type Alias = ...`（3.12+）创建延迟求值的别名对象，与普通 `Alias = SomeClass` 的运行时对象不同；不要把新式别名直接当构造器或任意 isinstance 目标。`@override`（3.12+）、`@final` 帮助检查器约束继承，也不在运行时禁止方法替换。[typing 参考](https://docs.python.org/3.14/library/typing.html)

## 10.9 方差与常见误区

可变 `list[T]` 通常是不变的：若把 `list[Dog]` 视为 `list[Animal]`，接受者就可能放入 Cat，破坏原列表约束。只读 `Sequence[Dog]` 可以在适当静态规则下作为 `Sequence[Animal]` 使用。Callable 参数通常逆变、返回值通常协变。

<!-- verify: run -->
```python
from typing import NewType, Final, Annotated
UserId = NewType("UserId", int)
DEFAULT_LIMIT: Final = 100
PositiveInt = Annotated[int, "positive"]
uid = UserId(7)
assert uid == 7 and type(uid) is int
```

NewType 主要创建静态区别，Final 不会让运行时赋值报错，Annotated 元数据只有被具体工具读取时才发挥作用。

### 方差由“允许读还是允许写”推导

假设 Dog 是 Animal 的子类。只读取动物的函数可以接受一组 Dog；会向容器加入任意 Animal 的函数不能接受 `list[Dog]`，否则可能加入 Cat。这就是可变 list 不变、只读接口适用协变的直观原因。

下面代码只展示类型检查预期，不运行错误调用。保存成独立文件后交给选定检查器，注释中的 rejected 调用应报告不兼容类型；不要把它当作运行时必然抛错的例子。

```python
from collections.abc import Sequence

class Animal:
    pass
class Dog(Animal):
    pass
class Cat(Animal):
    pass

def inspect_animals(values: Sequence[Animal]) -> int:
    return len(values)

def add_cat(values: list[Animal]) -> None:
    values.append(Cat())

dogs: list[Dog] = [Dog()]
inspect_animals(dogs)  # accepted：只读接口
# add_cat(dogs)        # rejected：会破坏 list[Dog] 的约束
```

Sequence 注解表达调用契约，不能阻止底层列表被其他持有者同时修改。静态只读接口、不可变对象、线程安全是三个不同保证。

其他常用类型工具可以按问题选择：

| 工具 | 解决的问题 | 不提供的保证 |
|---|---|---|
| Self | 返回实际接收者类型，支持链式子类 API | 不自动创建子类对象 |
| NewType | 在静态层区分 UserId 与 OrderId | 不做值转换和合法性校验 |
| Literal / Enum | 有限取值，减少拼写错误 | Literal 不会在运行时拒绝字符串 |
| TypeGuard | 布尔函数成功后收窄类型 | 检查器不证明函数实现诚实 |
| TypeIs（3.13+） | 更严格的双分支类型收窄 | 仍需要正确实现检查 |
| Final | 声明不应重新绑定 | 不递归冻结对象 |
| Annotated | 附带工具可读取的元数据 | 普通 Python 不自动执行元数据规则 |

验收：把“运行通过”“静态检查通过”“外部数据合法”写成三个独立验证结论。此轮只执行 Python 运行示例，未安装 mypy / Pyright，不能据此声称全书类型检查通过。

## 10.10 注解求值与工具运行

Python 3.14 改变了注解求值机制。跨版本代码不要假定 `__annotations__` 的值总是同一种表示；解析注解可使用 `typing.get_type_hints`，但解析不可信注解可能执行代码。3.11—3.13 中 `from __future__ import annotations` 常用于推迟注解处理。

```powershell
python -m pip install mypy
python -m mypy your_package
```

本教程的“错误类型调用演示”故意展示运行时与静态差别，不能把全书所有代码块拼成一个 mypy 必须通过的模块。项目中先对公共 API、数据模型、服务边界添加注解，再逐步提高严格度。

延伸：[typing 官方参考](https://docs.python.org/3/library/typing.html)、[Python 3.14 注解变化](https://docs.python.org/3/whatsnew/3.14.html)。

### 3.14 注解延迟求值不等于字符串化，也不等于不执行代码

<!-- verify: run -->
```python
# 本例要求 Python 3.14，且没有启用 future annotations。
from annotationlib import get_annotations, Format
events = []
def resolve():
    events.append('resolved')
    return int

def convert(value: resolve()) -> int:
    return int(value)

assert events == []
assert convert('3') == 3
assert events == []
annotations = get_annotations(convert, format=Format.VALUE)
assert annotations['value'] is int
assert events == ['resolved']
```

3.11—3.13 未启用 future 时，函数等处的注解通常在定义阶段求值；future annotations 把注解保存为字符串形式。3.14 默认采用延迟求值机制，访问可能触发名称解析和任意表达式执行；它不是把所有注解简单替换成字符串。函数局部变量注解又不同，不会因写 `x: T` 自动创建 x 的值。

`annotationlib` 的 VALUE、FORWARDREF、STRING 用于不同反射需求；`typing.get_type_hints` 用于更高层解析。即使只想显示注解，也不要把处理不可信对象视为天然安全。类型别名和类型参数还有专门的延迟求值/注解作用域规则，不应仅套普通 LEGB。[annotationlib 参考](https://docs.python.org/3.14/library/annotationlib.html)


---

# 11｜异常与上下文管理

> 本章目标：让失败信息和资源生命周期可预测。
>
> 阅读重点：验证进入失败、块内失败、清理顺序与异常传播，避免返回值掩盖异常。

## 11.1 异常分类与传播

语法错误通常在解析代码时发现；运行时错误以异常传播。常见异常有 ValueError、TypeError、KeyError、IndexError、AttributeError、OSError、TimeoutError。业务异常继承 Exception，通常不要直接继承 BaseException。

<!-- verify: run -->
```python
def parse_limit(text):
    value = int(text)
    if not 1 <= value <= 1000:
        raise ValueError("limit 必须在 1..1000")
    return value

try:
    parse_limit("bad")
except ValueError as exc:
    assert "invalid literal" in str(exc)
```

`except Exception` 通常不捕获 KeyboardInterrupt、SystemExit；裸 except 会捕获它们，容易吞掉用户中断和正常退出。

## 11.2 try / except / else / finally

<!-- verify: run -->
```python
events = []
try:
    value = int("42")
except (ValueError, TypeError):
    events.append("失败")
else:
    events.append(value)
finally:
    events.append("清理")
assert events == [42, "清理"]
```

else 只在 try 正常结束后执行；finally 用来清理，通常无论成功失败都会运行，但强制终止进程等情况不能保证。finally 里的 return 或新异常可能掩盖原结果，尽量只做必要清理。

### 异常处理范围决定你会误报什么

下面把解析与业务处理分开：只把 int 转换失败解释为输入格式错误。业务中的 ValueError 不会被错误包装成“不是整数”。

<!-- verify: run -->
```python
def parse_and_apply(raw, operation):
    try:
        number = int(raw)
    except ValueError as exc:
        raise ValueError("输入不是整数") from exc
    else:
        return operation(number)

assert parse_and_apply("3", lambda n: n * 2) == 6
def reject(number):
    raise ValueError("库存不足")

try:
    parse_and_apply("3", reject)
except ValueError as exc:
    assert str(exc) == "库存不足"
else:
    raise AssertionError("业务异常必须原样传播")
```

Go 常把错误放在返回值中显式检查；Python 的异常会沿调用栈传播，必须在具有足够业务上下文的位置处理。底层不应处处打印后返回 None，否则调用方无法区分“没有数据”和“查询失败”。顶层负责把已知业务失败映射为退出码或响应；未知编程错误保留堆栈以便修复。

清理代码如果再失败，会增加新的异常上下文。关键资源操作应考虑如何记录清理失败，同时保留业务失败原因；不能在 finally 里 `return True` 让整个操作看起来成功。

### return 先求值，再运行 finally；except 的目标会被清理

<!-- verify: run -->
```python
def build():
    result = []
    try:
        return result
    finally:
        result.append('cleanup')

assert build() == ['cleanup']
error = 'old'
try:
    raise ValueError('bad')
except ValueError as error:
    message = str(error)
assert message == 'bad'
assert 'error' not in globals()
```

return 保存的是计算得到的对象，finally 修改那个可变对象仍会影响调用者看到的结果。若 finally 重新绑定局部 result，则不替换先前选定的返回对象。finally 再 return/raise 会掩盖原控制流，应避免这样设计。

except 的目标名称在处理结束时被清除，以减少异常、回溯帧与局部变量形成的引用环；同名旧绑定也不会自动恢复。需要保留诊断时提取简短文本或专门字段，长期保存整个异常及 traceback 会保留大量对象。

## 11.3 自定义异常与异常链

<!-- verify: run -->
```python
class ConfigurationError(Exception):
    pass

def read_port(text):
    try:
        return int(text)
    except ValueError as exc:
        raise ConfigurationError("端口配置不是整数") from exc

try:
    read_port("abc")
except ConfigurationError as exc:
    assert isinstance(exc.__cause__, ValueError)
    exc.add_note("请检查 APP_PORT 环境变量")  # 3.11+
    assert exc.__notes__
```

`raise ... from exc` 保留原因；`from None` 抑制显示隐式上下文，适合你明确不想向外暴露内部细节时，但不要因此丢掉内部日志。捕获后原样传播用裸 `raise`，不必 `raise exc`。

## 11.4 EAFP 与 LBYL

<!-- verify: run -->
```python
data = {"amount": 10}
try:
    amount = data["amount"]
except KeyError:
    amount = 0
assert amount == 10
```

EAFP 倾向“尝试操作，处理失败”；LBYL 倾向“先检查，再操作”。文件是否存在、并发状态等预检查可能与真实操作之间发生变化。异常处理范围要小：不要把十几个操作放进同一个 try，再把全部 KeyError 误判为“输入缺字段”。

## 11.5 ExceptionGroup 与 except*（3.11+）

<!-- verify: run -->
```python
handled = []
try:
    raise ExceptionGroup("批量失败", [ValueError("非法数据"), OSError("读取失败")])
except* ValueError as group:
    handled.extend(type(e).__name__ for e in group.exceptions)
except* OSError as group:
    handled.extend(type(e).__name__ for e in group.exceptions)
assert handled == ["ValueError", "OSError"]
```

普通 except 处理一个异常对象，except* 按类型拆分异常组的子异常，可能执行多个处理分支。未处理部分继续传播。同一 try 不能混用普通 except 和 except*。TaskGroup 会用异常组报告多个任务失败。

### except* 按叶子类型处理，未匹配部分继续抛出

<!-- verify: run -->
```python
seen = []
try:
    try:
        raise ExceptionGroup('batch', [ValueError('value'), TypeError('type')])
    except* ValueError as group:
        seen.append(type(group.exceptions[0]))
except ExceptionGroup as rest:
    assert len(rest.exceptions) == 1
    assert isinstance(rest.exceptions[0], TypeError)
else:
    raise AssertionError('未处理的 TypeError 不能丢失')
assert seen == [ValueError]
```

异常组可能嵌套，实际程序不要假定 `exceptions` 永远是一层叶子。普通 `except ExceptionGroup` 捕获的是整个组；except* 按匹配拆分子组，不能用 return/break/continue 从其处理块跳出。`ExceptionGroup` 只容纳 Exception 子类，涉及 BaseException 的组需理解 BaseExceptionGroup。取消、中断等退出信号不能一律当作普通任务失败吞掉。

## 11.6 with 与上下文管理协议

<!-- verify: run -->
```python
class ManagedResource:
    def __init__(self):
        self.closed = False
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, traceback):
        self.closed = True
        return False  # 不抑制异常

resource = ManagedResource()
with resource as active:
    assert active is resource
assert resource.closed
```

`__enter__` 返回 as 后绑定的对象；`__exit__` 返回真值会抑制块内异常。若 enter 自己失败，通常不会调用该对象的 exit，因此 enter 内部已经获取的资源也要正确回滚。

### enter 失败不代表已获取的资源自动释放

`with manager as value` 先取得管理器并调用 enter，enter 成功返回后才进入代码块。若 enter 内部打开了第一个资源，又在第二个资源上失败，这个管理器的 exit 不会由该 with 自动调用。资源管理器自己要保证初始化失败时回滚已完成的部分。

多个 with 项按嵌套方式进入：第二项进入失败，第一项已经建立的退出逻辑仍会运行。动态资源数量用 ExitStack，可以把这一规则写得清楚：

<!-- verify: run -->
```python
from contextlib import ExitStack, contextmanager

events = []
@contextmanager
def resource(name, fail=False):
    events.append("open:" + name)
    if fail:
        raise OSError(name)
    try:
        yield name
    finally:
        events.append("close:" + name)

try:
    with ExitStack() as stack:
        stack.enter_context(resource("A"))
        stack.enter_context(resource("B"))
        stack.enter_context(resource("C", fail=True))
except OSError:
    pass
else:
    raise AssertionError("C 的获取应失败")
assert events == ["open:A", "open:B", "open:C", "close:B", "close:A"]
```

这里只在 C 的真正资源获取之前故意失败，所以 C 没有待关闭资源。若 C 已经获得底层句柄，就应在它自身获取逻辑的 except/finally 中释放。验收不能只测试正常退出，还应覆盖进入失败、块内失败和清理顺序。

## 11.7 contextmanager 与 finally

<!-- verify: run -->
```python
from contextlib import contextmanager

@contextmanager
def temporary_setting(settings, key, value):
    missing = object()
    previous = settings.get(key, missing)
    settings[key] = value
    try:
        yield settings
    finally:
        if previous is missing:
            settings.pop(key, None)
        else:
            settings[key] = previous

settings = {"mode": "safe"}
with temporary_setting(settings, "mode", "fast"):
    assert settings["mode"] == "fast"
assert settings["mode"] == "safe"
```

生成器上下文管理器必须恰好 yield 一次。yield 前获取资源，finally 清理。这里修改普通字典不适合并发共享配置，示例只说明生命周期。

## 11.8 ExitStack、suppress 与 closing

<!-- verify: run -->
```python
from contextlib import ExitStack, suppress, closing
from io import StringIO

with ExitStack() as stack:
    left = stack.enter_context(StringIO("A"))
    right = stack.enter_context(StringIO("B"))
    assert left.read() + right.read() == "AB"
assert left.closed and right.closed

with suppress(KeyError):
    {}["optional"]

with closing(StringIO("abc")) as stream:
    assert stream.read() == "abc"
```

ExitStack 适合动态数量资源，并按逆序退出；suppress 只应抑制明确允许忽略的异常；closing 适配有 close 但没有上下文协议的对象。异步版本有 asynccontextmanager、AsyncExitStack、aclosing，配合 async with 使用。

延伸：[官方错误和异常](https://docs.python.org/3.14/tutorial/errors.html)、[contextlib](https://docs.python.org/3.14/library/contextlib.html)。

### 可复用、可重入和异步清理：三个不同问题

同一个管理器能否先后进入是“可复用”；能否在尚未退出时再次嵌套进入是“可重入”。文件关闭后不能再用，RLock 支持同线程重入；`@contextmanager` 每次函数调用生成新的管理器，不应重复进入同一个已经耗尽的生成器管理器。一个对象支持 with 不表示它具备以上全部能力。

<!-- verify: run -->
```python
import asyncio
from contextlib import asynccontextmanager, AsyncExitStack, aclosing

async def main():
    events = []
    @asynccontextmanager
    async def resource(name):
        events.append('open ' + name)
        try:
            yield name
        finally:
            events.append('close ' + name)

    async def source():
        try:
            yield 1
            yield 2
        finally:
            events.append('source closed')

    async with AsyncExitStack() as stack:
        await stack.enter_async_context(resource('A'))
        await stack.enter_async_context(resource('B'))
        async with aclosing(source()) as stream:
            async for item in stream:
                assert item == 1
                break
    assert events == ['open A', 'open B', 'source closed', 'close B', 'close A']

asyncio.run(main())
```

提前 break 不应被理解成任意迭代器的自动 close。aclosing 把异步生成器清理放回当前明确的作用域；AsyncExitStack 按逆序等待退出。生成器式上下文管理器捕获块内异常后若不重新抛出，就可能把异常抑制掉，记录日志后通常应 `raise`。[contextlib 参考](https://docs.python.org/3.14/library/contextlib.html)


---

# 12｜文件、编码与数据交换

> 本章目标：构建可诊断、可恢复的数据读写流程。
>
> 阅读重点：重点看编码、CSV 记录、严格 JSON 和写入失败后旧文件的状态。

## 12.1 pathlib 与路径语义

<!-- verify: run -->
```python
from pathlib import Path, PureWindowsPath
from tempfile import TemporaryDirectory

with TemporaryDirectory() as tmp:
    root = Path(tmp)
    file = root / "data" / "report.txt"
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text("你好\nPython", encoding="utf-8")
    assert file.read_text(encoding="utf-8") == "你好\nPython"
    assert file.name == "report.txt" and file.suffix == ".txt"
    assert file.stem == "report"
    assert list(root.rglob("*.txt")) == [file]
assert PureWindowsPath(r"C:\data\a.csv").name == "a.csv"
```

Path 表示当前系统实际路径，PurePath 变体只做语法运算。`/` 拼接路径，绝对路径片段可能替换之前的根；处理用户路径必须另做约束。`resolve()` 规范化绝对路径并可能涉及符号链接，不能把字符串 startswith 当作可靠目录包含判断。

## 12.2 open 模式、编码与换行

| 模式 | 含义 | 主要风险 |
|---|---|---|
| r | 读，文件需存在 | 缺失时失败 |
| w | 写，存在则截断 | 会覆盖旧数据 |
| a | 追加 | 并发记录仍需协调 |
| x | 排他创建 | 已存在时失败 |
| b | 二进制，组合为 rb / wb | 读写 bytes |
| + | 同时读写 | 需要管理位置与缓冲 |

<!-- verify: run -->
```python
from pathlib import Path
from tempfile import TemporaryDirectory
with TemporaryDirectory() as tmp:
    path = Path(tmp) / "lines.txt"
    with path.open("w", encoding="utf-8", newline="\n") as f:
        f.write("第一行\n第二行\n")
    with path.open("r", encoding="utf-8") as f:
        assert [line.rstrip("\n") for line in f] == ["第一行", "第二行"]
    with path.open("rb") as f:
        assert isinstance(f.read(3), bytes)
        f.seek(0)
        assert f.tell() == 0
```

文本模式使用编码和换行转换；明确 encoding 更便于跨平台。大文件逐行 / 分块读取，避免无条件 read()。文本流 tell 的值可能是定位 cookie，不能按任意字节偏移理解。重要数据的持久性还涉及 flush、fsync 和文件系统，不是 close 就能保证掉电不丢。

### 文本流、字节流、当前位置与文件尾

<!-- verify: run -->
```python
from io import BytesIO, TextIOWrapper
raw = BytesIO('甲\r\n乙\n'.encode('utf-8'))
with TextIOWrapper(raw, encoding='utf-8', newline=None) as text:
    assert text.read(1) == '甲'
    position = text.tell()
    assert text.readline() == '\n'
    text.seek(position)
    assert text.read() == '\n乙\n'
    assert text.read() == ''
assert raw.closed
```

文本 read(n) 按字符请求，二进制 read(n) 按字节请求；编码器可能预读底层字节，因此别混用同一文件的文本包装层和原始流位置。文本 EOF 是空字符串，二进制 EOF 是空 bytes，而不是 None。TextIOWrapper 默认关闭时会连同底层流关闭，资源包装涉及所有权传递；需要保留底层流时应明确研究 detach 的约束。

`w` 一打开就截断，后续校验失败不能恢复旧内容；`r+` 不自动截断，写入较短内容可能留下旧尾部。`flush` 主要把 Python 缓冲交给下层，持久化要另看 fsync 和文件系统；`seek`、`flush`、`close` 解决的不是同一个问题。[io 参考](https://docs.python.org/3.14/library/io.html)

## 12.3 StringIO、BytesIO 与临时文件

<!-- verify: run -->
```python
from io import StringIO, BytesIO
from tempfile import TemporaryFile
with StringIO() as text:
    print("a", "b", file=text, sep=",")
    assert text.getvalue() == "a,b\n"
with BytesIO(b"abc") as raw:
    assert raw.read(2) == b"ab"
with TemporaryFile(mode="w+t", encoding="utf-8") as f:
    f.write("temporary")
    f.seek(0)
    assert f.read() == "temporary"
```

内存流便于测试接收文件对象的函数。Windows 对已打开临时文件的再次打开有额外限制；跨进程按名字访问时应明确生命周期和删除策略。

## 12.4 JSON：结构、限制与编码

<!-- verify: run -->
```python
import json
from datetime import datetime, timezone
data = {"name": "张三", "active": True, "tags": ["go", "python"], "note": None}
text = json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False)
assert json.loads(text) == data
assert json.loads(json.dumps((1, 2))) == [1, 2]

def encode(value):
    if isinstance(value, datetime):
        return value.isoformat()
    raise TypeError(f"不支持 {type(value).__name__}")

assert "2026" in json.dumps({"at": datetime(2026, 1, 1, tzinfo=timezone.utc)}, default=encode)
```

JSON 不直接支持 datetime、Decimal、set、自定义类；键最好保持字符串。浮点 NaN / Infinity 不是严格 JSON 数字；序列化接口数据时可用 `allow_nan=False` 阻止非标准输出。`loads` 只解析格式，不验证业务字段和大小限制。

### JSON 的默认解析策略未必符合接口契约

`allow_nan=False` 控制 dumps 序列化；loads 默认仍可接受非标准的 NaN / Infinity。重复对象键通常也会被后一个值覆盖。处理配置、签名或权限相关字段时，应明确是否拒绝这类输入。

<!-- verify: run -->
```python
import json
from decimal import Decimal

def reject_constant(value):
    raise ValueError(f"不允许非有限数字：{value}")

def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"重复键：{key}")
        result[key] = value
    return result

def load_payload(text):
    if len(text.encode("utf-8")) > 4096:
        raise ValueError("请求过大")
    return json.loads(
        text, parse_float=Decimal,
        parse_constant=reject_constant, object_pairs_hook=unique_object,
    )

assert load_payload('{"amount": 0.1}')["amount"] == Decimal("0.1")
for text in ['{"amount": NaN}', '{"role": "user", "role": "admin"}']:
    try:
        load_payload(text)
    except ValueError:
        pass
    else:
        raise AssertionError(text)
```

这只建立格式层策略；顶层是否必须为 dict、amount 是否必填、金额范围以及嵌套深度仍需额外规则。体积限制在真实服务中应尽量发生在读取完整请求之前，而不是已经把数 GB 数据读进内存之后。

JSON 对象键为字符串，整数键往返后会改变类型；tuple 往返变 list；datetime 和 Decimal 需要双方约定格式。跨语言 API 不应靠 Python 私有对象格式猜测对方理解。

## 12.5 CSV：引号、换行与列名

<!-- verify: run -->
```python
import csv
from io import StringIO
stream = StringIO(newline="")
writer = csv.DictWriter(stream, fieldnames=["name", "amount"])
writer.writeheader()
writer.writerow({"name": "张,三", "amount": 100})
stream.seek(0)
rows = list(csv.DictReader(stream))
assert rows == [{"name": "张,三", "amount": "100"}]
assert int(rows[0]["amount"]) == 100
```

真实文件用 `open(..., newline="", encoding="utf-8")`，让 csv 模块管理换行。不要用 split(",") 解析带引号、逗号或换行的单元格。CSV 全是文本，需显式转换；若导出供电子表格打开，还要处理以 `=` 等开头的公式注入风险。

### 流式 CSV 导入要保留行号和字段错误

文件解析成功只是第一步。标题行、缺失列、数字格式、空白和重复记录都需要有可解释的反馈。下面将格式错误定位到数据记录号；CSV 允许带引号字段跨物理行，所以这里不用物理行号混淆记录编号。

<!-- verify: run -->
```python
import csv
from io import StringIO

def read_quantities(stream):
    reader = csv.DictReader(stream)
    if reader.fieldnames != ["sku", "quantity"]:
        raise ValueError("表头必须为 sku,quantity")
    for record_number, row in enumerate(reader, 1):
        if None in row or any(v is None for v in row.values()):
            raise ValueError(f"记录 {record_number} 列数不符")
        sku = row["sku"].strip()
        try:
            quantity = int(row["quantity"])
        except ValueError as exc:
            raise ValueError(f"记录 {record_number} 数量不是整数") from exc
        if not sku or quantity < 0:
            raise ValueError(f"记录 {record_number} 字段范围错误")
        yield sku, quantity

assert list(read_quantities(StringIO("sku,quantity\nA,2\nB,0\n"))) == [("A", 2), ("B", 0)]
try:
    list(read_quantities(StringIO("sku,quantity\nA,bad\n")))
except ValueError as exc:
    assert "记录 1" in str(exc)
else:
    raise AssertionError("无效数量必须报错")
```

本例严格固定列顺序。宽松导入可接受额外列或不同顺序，但要显式设计映射。生成器可能已经产出前几条才在中间失败；若边读边写数据库，需要事务或逐条状态设计，不可把“流式”误当“整体成功”。

## 12.6 TOML 与配置解析（3.11+）

<!-- verify: run -->
```python
import tomllib
config = tomllib.loads('''
[server]
host = "127.0.0.1"
port = 8080
''')
assert config["server"]["port"] == 8080
```

`tomllib.load` 接收二进制文件流，`loads` 接收字符串；标准库只提供读取，不提供 TOML 写入。INI 可用 configparser；环境变量适合部署注入但也要做类型和范围校验。

## 12.7 pickle 与可信边界

<!-- verify: run -->
```python
import pickle
trusted_local_value = {"items": [1, 2]}
raw = pickle.dumps(trusted_local_value, protocol=pickle.HIGHEST_PROTOCOL)
assert pickle.loads(raw) == trusted_local_value
```

pickle 能恢复部分 Python 对象，但加载过程可能执行代码。只对你完全信任且未被篡改的数据使用；不要接收用户上传 pickle，不把它当跨语言稳定协议。缓存文件可被攻击者写入时也不可信。

## 12.8 struct、Base64、压缩与归档

<!-- verify: run -->
```python
import struct, base64, gzip, zipfile
from io import BytesIO
header = struct.pack("!HI", 2, 1024)  # 网络序：无符号 16 位 + 32 位
assert struct.unpack("!HI", header) == (2, 1024)
raw = "中文".encode("utf-8")
assert base64.b64decode(base64.b64encode(raw), validate=True) == raw
assert gzip.decompress(gzip.compress(raw)) == raw
buffer = BytesIO()
with zipfile.ZipFile(buffer, "w") as archive:
    archive.writestr("data.txt", raw)
buffer.seek(0)
with zipfile.ZipFile(buffer) as archive:
    assert archive.read("data.txt") == raw
```

Base64 是编码，不是加密。解压外部归档要限制文件数、解压后大小与路径，防止目录穿越和压缩炸弹；尤其不要不加检查地解包 tar。struct 要对齐协议的长度、大小端与符号位。

## 12.9 XML 与 HTML 解析

<!-- verify: run -->
```python
from xml.etree import ElementTree as ET
from html.parser import HTMLParser
from html import escape
root = ET.fromstring('<users><user id="1">张三</user></users>')
assert root.find("user").attrib["id"] == "1"
assert root.findtext("user") == "张三"

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href"))

parser = Links()
parser.feed('<a href="/docs">教程</a>')
assert parser.links == ["/docs"]
assert escape('<script>') == "&lt;script&gt;"
```

XML 命名空间通常要传 namespace 映射；实际 HTML 常有不完整结构，可按需求选择第三方解析器。不可信 XML 需要资源限制和相应安全解析策略，不能认为标准解析成功就安全。

## 12.10 写入替换与目录操作

<!-- verify: run -->
```python
from pathlib import Path
from tempfile import TemporaryDirectory
import os, shutil
with TemporaryDirectory() as tmp:
    target = Path(tmp) / "config.json"
    staged = target.with_suffix(".tmp")
    staged.write_text('{"ok": true}', encoding="utf-8")
    os.replace(staged, target)
    backup = Path(tmp) / "backup.json"
    shutil.copy2(target, backup)
    assert backup.read_text(encoding="utf-8") == '{"ok": true}'
```

同目录暂存再 replace 可以避免读者看到半写文件，但掉电持久性、权限、并发覆盖和跨文件系统语义仍需额外设计。生产暂存文件名应唯一，避免多个写入者共用 `.tmp`。

### 文件替换提供的是哪一种保证

同目录唯一暂存文件、完整写入、关闭后 replace，可以降低读者看见半份文件的风险。它不自动保证多个写者不会互相覆盖，也不等于断电后绝不丢失。文件系统和平台的持久化规则必须单独确认。

<!-- verify: run -->
```python
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

def save_json(path, value):
    path = Path(path)
    staged = None
    try:
        with NamedTemporaryFile(
            mode="w", encoding="utf-8", newline="\n",
            dir=path.parent, prefix=path.name + ".", suffix=".tmp", delete=False,
        ) as stream:
            staged = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, allow_nan=False)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(staged, path)
    finally:
        if staged is not None:
            staged.unlink(missing_ok=True)

with TemporaryDirectory() as tmp:
    target = Path(tmp) / "settings.json"
    save_json(target, {"mode": "safe"})
    try:
        save_json(target, {"bad": object()})
    except TypeError:
        pass
    else:
        raise AssertionError("不可序列化对象应失败")
    assert json.loads(target.read_text(encoding="utf-8")) == {"mode": "safe"}
    assert list(Path(tmp).iterdir()) == [target]
```

父目录须预先存在；本例不处理权限继承、ACL 保留或多写者协调。Windows 在替换前关闭暂存句柄，避免某些共享模式限制。fsync 文件不能据此推断父目录元数据已持久化，目录同步也有平台差异。

验收：正常写入、新内容序列化失败和目标已存在都应检查；明确“文件内容完整可见”“并发一致”“掉电持久”三个不同层次。

延伸：[输入输出教程](https://docs.python.org/3.14/tutorial/inputoutput.html)、[标准库目录](https://docs.python.org/3.14/library/index.html)。


---

# 13｜常用标准库详解

> 本章目标：用标准库组合出可测试的日常工具。
>
> 阅读重点：把时间、日志、子进程和统计放进真实任务，说明各自成本与边界。

## 13.1 collections：计数、分组、双端队列

<!-- verify: run -->
```python
from collections import Counter, defaultdict, deque, ChainMap
assert Counter("banana").most_common(1) == [("a", 3)]
groups = defaultdict(list)
for user, value in [("A", 10), ("B", 20), ("A", 30)]:
    groups[user].append(value)
assert groups["A"] == [10, 30]
queue = deque([1, 2], maxlen=3)
queue.appendleft(0)
assert queue.popleft() == 0
queue.append(3)
queue.append(4)
assert list(queue) == [2, 3, 4]  # 满时淘汰另一端
config = ChainMap({"port": 9000}, {"port": 8080, "host": "localhost"})
assert config["port"] == 9000 and config["host"] == "localhost"
```

defaultdict 访问缺失键会调用工厂并插入；get 不触发同样行为。ChainMap 查找依次遍历映射，写入通常落在第一个映射，不自动修改找到值的那个底层映射。

## 13.2 heapq、bisect 与 array

<!-- verify: run -->
```python
import heapq
from bisect import bisect_left, insort
from array import array
heap = [5, 1, 3]
heapq.heapify(heap)
assert heapq.heappop(heap) == 1
assert heapq.nlargest(2, [4, 9, 1, 7]) == [9, 7]
values = [1, 3, 5]
assert bisect_left(values, 3) == 1
insort(values, 4)
assert values == [1, 3, 4, 5]
numbers = array("i", [1, 2, 3])
assert sum(numbers) == 6
```

heapq 默认最小堆，堆内部不是整体有序列表。bisect 的查找是二分，但 list 中间插入仍要移动元素，不能据此说插入是 O(log n)。array 是同类基础数值的紧凑容器，类型码尺寸需参考平台，不代替 NumPy 的多维运算。

## 13.3 datetime、时区与单调计时

<!-- verify: run -->
```python
from datetime import datetime, date, timedelta, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
import time
instant = datetime(2026, 10, 15, 8, 0, tzinfo=timezone.utc)
assert instant.isoformat() == "2026-10-15T08:00:00+00:00"
assert datetime.fromisoformat(instant.isoformat()) == instant
assert date(2026, 10, 15) + timedelta(days=2) == date(2026, 10, 17)
try:
    shanghai = instant.astimezone(ZoneInfo("Asia/Shanghai"))
    assert shanghai.hour == 16
except ZoneInfoNotFoundError:
    print("缺少 IANA 时区数据；Windows 可安装 tzdata 后重试")
start = time.perf_counter()
sum(range(100))
assert time.perf_counter() - start >= 0
```

naive datetime 不带时区信息；aware datetime 描述明确时区下的时间。`replace(tzinfo=...)` 是贴标签，`astimezone(...)` 才是按时间点换算。数据库可统一存 UTC，展示时转换；超时、耗时优先用 monotonic / perf_counter，系统时间可能被校准。

### 时间点、日历时间和持续时间分别建模

订单创建时间是一个时间点，可以保存带偏移的 ISO 文本或 UTC 时间戳；“每天当地 09:00 执行”是日历调度规则，需要时区；“最多等 5 秒”是持续时间，应使用单调时钟。把它们全部保存成一个无时区字符串，会把歧义推给每个调用者。

夏令时切换可能使某个当地时间重复或不存在。固定 `timezone(timedelta(hours=8))` 只表达固定偏移，不能代替所有地区的 ZoneInfo 规则。Windows 缺少 IANA 数据时，ZoneInfo 需要额外 tzdata；因此部署验证必须检查时区数据，而不是只检查 import 成功。

<!-- verify: run -->
```python
from datetime import datetime, timezone, timedelta
import time

local = datetime(2026, 1, 1, 8, tzinfo=timezone(timedelta(hours=8)))
utc = local.astimezone(timezone.utc)
assert utc.isoformat() == "2026-01-01T00:00:00+00:00"
assert local.timestamp() == utc.timestamp()
assert local.replace(tzinfo=timezone.utc).timestamp() != utc.timestamp()

deadline = time.monotonic() + 5
remaining = max(0.0, deadline - time.monotonic())
assert 0 <= remaining <= 5
```

最后一段只演示预算计算，不在此等待。串联多个 I/O 步骤时应从同一 deadline 计算剩余预算；每一步都重新给 5 秒，总耗时可能远超调用方期望。

### 时区、时间点与耗时分别选择表示

<!-- verify: run -->
```python
from datetime import datetime, timezone, timedelta
local_zone = timezone(timedelta(hours=8))
local = datetime(2026, 1, 1, 8, tzinfo=local_zone)
utc = local.astimezone(timezone.utc)
assert utc.hour == 0 and utc == local
assert local.replace(tzinfo=timezone.utc).hour == 8
assert local.replace(tzinfo=timezone.utc) != utc
```

`astimezone` 保留同一时间点并换表示；`replace(tzinfo=...)` 改标签，不进行时刻转换。naive datetime 没有完整时区语义，不能随手当 UTC。固定 UTC 偏移没有地区历史和夏令时规则；地区时间用 zoneinfo，并考虑运行环境时区数据库是否可用。夏令时回拨时重复本地时间由 fold 区分；比较绝对时间或计算真实经历时长时可先转 UTC。超时预算用 monotonic，性能测量用 perf_counter，不用会被校时改变的墙上时钟。

## 13.4 re：查找、分组、替换与边界

<!-- verify: run -->
```python
import re
pattern = re.compile(r"(?P<name>[a-z]+)=(?P<value>\d+)")
match = pattern.fullmatch("limit=20")
assert match and match.groupdict() == {"name": "limit", "value": "20"}
assert re.findall(r"\d+", "a12 b34") == ["12", "34"]
assert [m.group() for m in re.finditer(r"\d+", "a12 b34")] == ["12", "34"]
assert re.sub(r"\s+", " ", "a   b\tc") == "a b c"
assert re.split(r"[,;]", "a,b;c") == ["a", "b", "c"]
assert re.escape("a+b") == r"a\+b"
```

`match` 从开头匹配，`search` 任意位置找，`fullmatch` 要求覆盖整个字符串。`*` 零或多次、`+` 一或多次、`?` 可选、`{m,n}` 次数；`.*?` 非贪婪；`(?:...)` 非捕获组。复杂嵌套量词可能造成灾难性回溯，外部模式 / 文本应有限制，不拿正则解析任意 HTML。

## 13.5 argparse：参数、子命令与退出码

<!-- verify: run -->
```python
import argparse
parser = argparse.ArgumentParser(description="订单导出")
parser.add_argument("output")
parser.add_argument("--limit", type=int, default=100)
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args(["report.csv", "--limit", "20", "--verbose"])
assert args.output == "report.csv" and args.limit == 20 and args.verbose
```

真实程序使用 `parse_args()` 读取 sys.argv。type=int 只做转换，不保证正数；范围仍需检查。复杂 CLI 用 add_subparsers；stdout 输出业务结果、stderr 输出错误，退出码 0 表示成功。第 17 章给出完整例子。

## 13.6 logging：等级、延迟格式化与异常

<!-- verify: run -->
```python
import logging
from io import StringIO
output = StringIO()
logger = logging.getLogger("tutorial.orders")
logger.handlers.clear()
logger.propagate = False
handler = logging.StreamHandler(output)
handler.setFormatter(logging.Formatter("%(levelname)s %(name)s %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.info("订单 %s 已创建", 42)
assert "INFO tutorial.orders 订单 42 已创建" in output.getvalue()
logger.removeHandler(handler)
handler.close()
```

库代码用 `getLogger(__name__)`，应用入口集中配置；避免每个模块 basicConfig。常见等级 DEBUG、INFO、WARNING、ERROR、CRITICAL。except 中 `logger.exception(...)` 保留堆栈。使用 `%s` 参数可延迟字符串格式化，但传入参数表达式仍会立即执行。令牌、密码、完整个人信息不进日志。

### 日志用于解释一次操作，而不是重复打印异常

异常最适合在能决定处理策略的边界记录一次。底层抛出、上层映射响应时再记录，通常比每层都打同一堆栈更易读。日志字段至少考虑事件名、请求或任务 ID、耗时、结果；敏感字段使用允许列表，不记录整个请求对象。

<!-- verify: run -->
```python
import logging
from io import StringIO

stream = StringIO()
logger = logging.getLogger("tutorial.request")
handler = logging.StreamHandler(stream)
handler.setFormatter(logging.Formatter("%(levelname)s task=%(task_id)s %(message)s"))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.propagate = False
try:
    context = logging.LoggerAdapter(logger, {"task_id": "T-7"})
    context.info("completed count=%s", 3)
    assert "task=T-7 completed count=3" in stream.getvalue()
finally:
    logger.removeHandler(handler)
    handler.close()
```

Formatter 引用的字段必须在每条记录中存在，因此要把适配器与 handler 的使用范围约束清楚。异步请求上下文可用 ContextVar，见 14.11；大量日志 I/O 可考虑队列式处理，但队列满、退出刷新和丢弃策略仍要设计。

## 13.7 os、sys、平台与环境

<!-- verify: run -->
```python
import os, sys, platform
assert isinstance(os.getpid(), int)
assert sys.version_info >= (3, 11)
print(platform.system(), sys.executable)
value = os.environ.get("PYTHON_TUTORIAL_MODE", "local")
assert isinstance(value, str)
```

不要用硬编码路径拼接实现跨平台；优先 pathlib。环境变量在进程间有继承与快照关系，修改当前进程环境不会反向修改启动它的 shell。

## 13.8 subprocess：参数列表、超时与返回码

<!-- verify: run -->
```python
import subprocess, sys
result = subprocess.run(
    [sys.executable, "-c", "print(6 * 7)"],
    check=True, capture_output=True, text=True, encoding="utf-8", timeout=5,
)
assert result.stdout.strip() == "42"
assert result.returncode == 0
```

优先参数列表而非 shell=True 拼接字符串。check=True 在非零退出码抛 CalledProcessError；timeout 限制等待。大量输出用流式消费，避免 capture_output 无限制占内存。不要把口令放在命令参数中，可能出现在进程列表。

### 子进程不是函数调用：状态、输出和退出需要显式传递

<!-- verify: run -->
```python
import subprocess, sys
result = subprocess.run(
    [sys.executable, '-I', '-c',
     "import sys; print('out'); print('err', file=sys.stderr); sys.exit(3)"],
    capture_output=True, text=True, encoding='utf-8', timeout=5,
)
assert result.returncode == 3
assert result.stdout.strip() == 'out' and result.stderr.strip() == 'err'
```

退出码非零和 stderr 非空不是同一件事；正常程序也可能向 stderr 写进度。`check=True` 让非零退出变成异常。`Popen.wait()` 配合未消费的 PIPE 可能因管道填满而死锁，有限输出用 communicate；无限输出需要持续消费与容量限制。`Popen.communicate(timeout=...)` 超时不会自动替你杀掉子进程，通常还需终止并再次 communicate 回收；高层 run 的处理不同。子进程对环境变量的修改不会写回父进程。

## 13.9 random、secrets、uuid、hashlib 与 hmac

<!-- verify: run -->
```python
import random, secrets, uuid, hashlib, hmac
rng = random.Random(42)
assert rng.randint(1, 10) == 2
assert len(secrets.token_hex(16)) == 32
identifier = uuid.uuid4()
assert uuid.UUID(str(identifier)) == identifier
digest = hashlib.sha256(b"hello").hexdigest()
assert len(digest) == 64
signature = hmac.digest(b"example-key", b"payload", "sha256")
assert hmac.compare_digest(signature, hmac.digest(b"example-key", b"payload", "sha256"))
```

random 用于模拟、采样与可复现测试；安全令牌用 secrets。普通 SHA-256 不能直接用于安全存储密码，密码需要适当的专用口令派生方案。HMAC 提供共享密钥消息认证；签名协议还需时间戳、重放防护、规范化等设计。

## 13.10 其他常见工具

<!-- verify: run -->
```python
from operator import itemgetter, attrgetter
from types import SimpleNamespace, MappingProxyType
from pprint import pformat
from statistics import mean, median
import textwrap, math
assert sorted([("b", 2), ("a", 1)], key=itemgetter(1)) == [("a", 1), ("b", 2)]
assert attrgetter("name")(SimpleNamespace(name="A")) == "A"
view = MappingProxyType({"x": 1})
assert view["x"] == 1
assert mean([1, 2, 6]) == 3 and median([1, 2, 6]) == 2
assert math.gcd(12, 18) == 6
assert textwrap.dedent("  a\n  b") == "a\nb"
assert "'a'" in pformat({"a": [1, 2]})
```

MappingProxyType 是映射只读视图，不会递归冻结底层数据。更多标准库按任务分类见第 20 章，不需要把每个 API 全背下来。

### 标准库组合案例：流式统计慢请求

这里把解析、统计和输出拆开，不依赖 Web 框架。每行是一个 JSON 对象，耗时采用整数毫秒；拒绝 bool、负数与缺字段，错误包含记录号。

<!-- verify: run -->
```python
import json
from collections import Counter

def slow_counts(lines, threshold=100):
    if type(threshold) is not int or threshold < 0:
        raise ValueError("threshold 必须为非负整数")
    counts = Counter()
    for number, line in enumerate(lines, 1):
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError(f"记录 {number} 不是 JSON") from exc
        if not isinstance(item, dict):
            raise ValueError(f"记录 {number} 不是对象")
        route, elapsed = item.get("route"), item.get("elapsed_ms")
        if not isinstance(route, str) or type(elapsed) is not int or elapsed < 0:
            raise ValueError(f"记录 {number} 字段非法")
        if elapsed >= threshold:
            counts[route] += 1
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))

lines = [
    '{"route":"/a","elapsed_ms":120}',
    '{"route":"/b","elapsed_ms":20}',
    '{"route":"/a","elapsed_ms":200}',
]
assert slow_counts(iter(lines)) == [("/a", 2)]
```

输入逐行消费，但 Counter 占用与不同路由数有关。原始 URL 若含用户 ID，键数可能无限增长，应先归一化成路由模板。这里演示函数组合，未包括完整 CLI、行大小限制和坏记录旁路；真实日志管道需要按业务补上。

验收：能用标准库完成需求时，不为一个计数、参数解析或临时目录引入整套框架；也不因“标准库可实现”就重写成熟的 HTTP 连接池或数据库迁移系统。

延伸：[官方标准库总目录](https://docs.python.org/3.14/library/index.html)。


---

# 14｜线程、进程与异步编程

> 本章目标：按工作负载选择并发，并证明失败后会退出。
>
> 阅读重点：重点验证锁的不变量、取消传播、队列容量及远程副作用，不能只看速度。

## 14.1 先选模型，再写并发

| 工作负载 | 常见选择 | 理由与边界 |
|---|---|---|
| 少量顺序任务 | 同步函数 | 简单，可观察，避免无意义调度 |
| 阻塞 I/O 客户端、少量并发 | ThreadPoolExecutor | 复用现有同步库；仍需超时与限流 |
| 大量支持异步的网络 I/O | asyncio | 协作调度；依赖库须支持非阻塞 |
| 纯 Python CPU 密集计算 | ProcessPoolExecutor | 在常规 GIL 构建中多进程可利用多核 |
| 释放 GIL 的原生计算库 | 按库文档选择线程 | 需留意内部线程池与过度并发 |
| 自由线程构建 | 根据支持情况实测 | 不可假定扩展兼容或数据自动安全 |

goroutine 由 Go 运行时调度；asyncio 协程通常在一个事件循环线程中协作运行。不能把 coroutine 当成另一个名称的 goroutine：调度、阻塞库和取消机制都需重新判断。

## 14.2 GIL 与自由线程

常规 CPython 构建中，GIL 使同一解释器中通常只有一个线程执行 Python 字节码；阻塞 I/O 和部分原生扩展会释放它。它不保证一组业务操作原子化，不替代锁。

Python 3.13 起有可选自由线程构建，扩展兼容、运行时状态和性能都需实际确认。不要写“Python 永远不能多线程并行”，也不要写“新版本已普遍取消 GIL”。官方说明：[自由线程支持](https://docs.python.org/3/howto/free-threading-python.html)。

### 判断当前构建，区分吞吐、并行和状态正确性

<!-- verify: run -->
```python
import sys, sysconfig
assert sys.implementation.name
print('implementation:', sys.implementation.name)
print('free-threaded build:', sysconfig.get_config_var('Py_GIL_DISABLED'))
if hasattr(sys, '_is_gil_enabled'):
    print('GIL currently enabled:', sys._is_gil_enabled())
```

构建支持自由线程与当前运行时关闭 GIL 是两个问题，加载不兼容扩展可能重新启用 GIL。并发是多个任务都取得进展，并行是同一时刻实际执行；阻塞 I/O 线程可提高吞吐，不代表纯 Python CPU 循环多核并行。无 GIL 时共享状态更需要明确同步，内置容器的内部保护也不能把“先查再改”变成业务事务。版本号、CPU 占用和某次计数结果都不足以证明线程安全。[自由线程官方说明](https://docs.python.org/3.14/howto/free-threading-python.html)

## 14.3 Thread、Lock 与线程安全

<!-- verify: run -->
```python
from threading import Thread, Lock
total = 0
lock = Lock()

def worker():
    global total
    for _ in range(1000):
        with lock:
            total += 1

threads = [Thread(target=worker) for _ in range(4)]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
assert total == 4000
```

锁保护的是共享状态的不变量，临界区尽量短；避免拿锁时做远程 I/O。RLock 允许同线程重入；Event 适合通知退出；Condition 适合等待条件；Semaphore 控制同时进入数量。不要依赖某个内置操作当前“看上去原子”。

### 线程安全要保护读改写整体

库存扣减包括“读余额、判断足够、写新余额”三个步骤。即便某个容器方法单独安全，把三步拆开仍可能让两个请求同时通过判断。锁应保护业务不变量，而不是只围住最后一条赋值。

<!-- verify: run -->
```python
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

class Inventory:
    def __init__(self, stock):
        self.stock = stock
        self._lock = Lock()
    def take(self, count):
        if type(count) is not int or count <= 0:
            raise ValueError("count 必须为正整数")
        with self._lock:
            if self.stock < count:
                return False
            self.stock -= count
            return True

inventory = Inventory(10)
with ThreadPoolExecutor(max_workers=4) as pool:
    accepted = list(pool.map(inventory.take, [1] * 30))
assert sum(accepted) == 10
assert inventory.stock == 0
```

该锁只保护一个进程中的这个实例。如果服务有多个进程或实例，锁不能协调所有副本，需要数据库条件更新等共享状态机制。测试验证的是不变量，不依赖某次执行“恰好复现竞争”，也不依赖 GIL。

线程队列的停止哨兵只覆盖正常结束；消费者中途异常后不再消费，生产者可能卡在满队列。实际线程 worker 要捕获并报告错误、通知生产者停止，并对阻塞 put/get 设置可退出策略。不能只在主线程 join 然后希望所有工作自动停止。

### 同步原语如何选择，Condition 为什么必须检查谓词

| 原语 | 表达的状态 | 容易误用之处 |
|---|---|---|
| Lock | 一次只有一个持有者进入临界区 | 同线程再次 acquire 可能死锁 |
| RLock | 同线程可重入的锁 | 每次获取都要对应释放；不解决锁顺序冲突 |
| Event | 一个可设置/清除的标志 | 多次 set 不会累计成多条消息 |
| Condition | 锁保护下等待某个状态成立 | notify 不是“条件永久成立”的证明 |
| Semaphore | 可进入区间的许可数 | 不是每秒请求数限制 |
| Barrier | 一组参与者到达同一阶段 | 参与者失败需处理超时或 broken 状态 |

<!-- verify: run -->
```python
from threading import Condition, Thread
condition = Condition()
state = {'ready': False, 'value': None}
result = []

def consume():
    with condition:
        if not condition.wait_for(lambda: state['ready'], timeout=3):
            return
        result.append(state['value'])

thread = Thread(target=consume)
thread.start()
with condition:
    state.update(ready=True, value=42)
    condition.notify_all()
thread.join(timeout=3)
assert not thread.is_alive() and result == [42]
```

Condition.wait 释放相关锁并等待，返回前重新获取；wait_for 用谓词循环避免把一次唤醒当成消费资格。生产者在同一把锁内修改状态并通知，消费者即使晚到也能看到 ready。Thread.start 才启动新线程，直接 run 是普通调用；一个 Thread 只能 start 一次。join 只等线程结束，不会像 Future.result 那样重新抛工作异常。daemon 线程在解释器关闭时可能被突然停止，不能用它保证保存数据。[threading 参考](https://docs.python.org/3.14/library/threading.html)

## 14.4 Queue：生产者消费者与背压

<!-- verify: run -->
```python
from queue import Queue
from threading import Thread
queue = Queue(maxsize=2)
result = []

def consume():
    while True:
        value = queue.get()
        try:
            if value is None:
                return
            result.append(value * 2)
        finally:
            queue.task_done()

consumer = Thread(target=consume)
consumer.start()
for value in [1, 2, 3, None]:
    queue.put(value)
queue.join()
consumer.join()
assert result == [2, 4, 6]
```

有界队列使生产者在积压时等待，是最基本的背压。task_done 必须与每次 get 对应，包括停止哨兵；否则 join 永远等不到。多个消费者需要为每个消费者安排停止条件。

### 队列为空、任务完成和业务成功是三种状态

`get` 把项目拿走后队列可能已空，但 worker 仍在工作；`task_done` 递减未完成计数；`join` 等计数归零，不会判断业务是否成功。异常分支也应结算计数，再通过其他通道报告失败。线程队列的 empty/full/qsize 是瞬时观察，不能用“先判空再 get”代替阻塞/超时或 get_nowait 捕获 Empty。

<!-- verify: run -->
```python
# Python 3.13+：有序关闭队列，不需要拿业务值充当哨兵。
from queue import Queue, ShutDown
queue = Queue(maxsize=2)
queue.put(1)
queue.shutdown()
assert queue.get() == 1
queue.task_done()
queue.join()
try:
    queue.get()
except ShutDown:
    pass
else:
    raise AssertionError('关闭且排空后应终止读取')
```

正常 shutdown 允许消费已排队数据并拒绝新 put；`immediate=True` 会放弃排队数据，可能让 join 返回却没有完成全部业务，不能把它当正常成功。`asyncio.Queue` 有相应关闭 API（3.13+），但不是线程安全队列；异步 get/put 使用 await，task_done 不用 await。两类队列 maxsize=0 都表示无界。[queue](https://docs.python.org/3.14/library/queue.html)、[asyncio.Queue](https://docs.python.org/3.14/library/asyncio-queue.html)

## 14.5 线程池、Future 与完成顺序

<!-- verify: run -->
```python
from concurrent.futures import ThreadPoolExecutor, as_completed

def square(value):
    return value * value

with ThreadPoolExecutor(max_workers=3) as pool:
    assert list(pool.map(square, [1, 2, 3])) == [1, 4, 9]
    futures = [pool.submit(square, n) for n in [1, 2, 3]]
    results = [future.result() for future in as_completed(futures)]
assert sorted(results) == [1, 4, 9]
```

map 按输入顺序返回；as_completed 按完成顺序交付。异常通常在 result 或迭代结果时重新抛出。不要在线程池工作函数内等待同一饱和池中新任务的结果，可能死锁。Future.cancel 无法强杀已经运行的线程；超时返回也不代表后台任务停止。

### Future 的等待超时不终止工作；退出线程池还会等待

<!-- verify: run -->
```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from threading import Event
started, release = Event(), Event()
def work():
    started.set()
    release.wait()
    return 42

with ThreadPoolExecutor(max_workers=1) as pool:
    future = pool.submit(work)
    try:
        assert started.wait(3)
        try:
            future.result(timeout=0)
        except TimeoutError:
            pass
        else:
            raise AssertionError('工作仍被 Event 阻塞')
        assert not future.cancel()
        assert not future.done()
    finally:
        release.set()
    assert future.result(timeout=3) == 42
```

Future 有待运行、运行中、完成/取消等状态，cancel 主要对尚未开始的工作有效。线程池 with 退出通常等待已提交工作；在 with 内捕获超时，不意味着整个 with 会及时返回。`shutdown(cancel_futures=True)` 可取消尚未启动工作，无法强杀运行线程。`map` 按输入顺序取结果可能被最前面的慢任务拖住；3.14 的 buffersize 可约束尚未交付结果的提交积压，较早版本需自行分批。[concurrent.futures 参考](https://docs.python.org/3.14/library/concurrent.futures.html)

## 14.6 进程池与 Windows spawn

下面保存成独立文件再运行，不能直接在某些 REPL 中执行：

```python
from concurrent.futures import ProcessPoolExecutor
import multiprocessing

def square(value):
    return value * value

def main():
    context = multiprocessing.get_context("spawn")
    with ProcessPoolExecutor(max_workers=2, mp_context=context) as pool:
        print(list(pool.map(square, [1, 2, 3])))

if __name__ == "__main__":
    main()
```

工作函数放在可导入模块顶层，参数与结果通常必须可 pickle。lambda、局部函数、连接对象通常不合适。进程不共享普通 Python 对象；通信可用 multiprocessing.Queue、Pipe、共享内存等。大对象序列化与进程启动可能抵消收益。进程启动默认方式会随平台 / 版本变化，明确 context 更便于教学与部署。

### 进程带来隔离，也带来传输与启动成本

spawn 启动新解释器并重新导入主模块，顶层副作用会重复执行，所以入口保护是必要结构。函数参数和结果经序列化传递，不能把父进程的数据库连接当普通数据送过去。工作进程应在自己的生命周期中创建和关闭资源。

调优时先测单个任务成本：几十微秒的小函数可能比进程通信还短，逐个提交反而更慢；适当批处理可以降低调度成本，但过大的批次会降低负载均衡和取消响应。`max_workers` 也不意味着待提交任务队列天然有界。

本书显式选择 spawn，避免依赖平台默认值。Python 3.14 的进程启动默认方式变化应查对应版本的 multiprocessing 文档；不要把“Linux 就一定 fork”写成跨版本约定。自由线程、子解释器和进程池各有对象共享与扩展兼容限制，不能仅看名称判断更快。

### spawn 下用真实子进程证明隔离

下面保存成脚本执行；本项目验证器会把标记块保存成独立文件，所以也可自动运行。

<!-- verify: run -->
```python
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import get_context

def change(values):
    values.append(99)
    return values

if __name__ == '__main__':
    original = [1]
    with ProcessPoolExecutor(max_workers=1, mp_context=get_context('spawn')) as pool:
        assert pool.submit(change, original).result(timeout=8) == [1, 99]
    assert original == [1]
```

spawn 使用新解释器，fork 复制父进程当时状态并具有多线程继承风险，forkserver 经独立服务器创建进程。3.14 在支持的平台上 POSIX 默认改为 forkserver；Windows 和 macOS 常用 spawn，fork 不再是任何平台的默认方式。显式 get_context 更易表达要求，不在可复用库里随意改全局启动方式。

普通全局变量不是进程间共享状态；Manager 提供代理访问，有序列化和往返成本；shared_memory 共享字节区，仍需格式、同步和 close/unlink 所有权。进程队列传送的是序列化数据，不要 put 后继续修改同一输入并假定快照时机。父进程应消费通信数据并正确 join，强行 terminate 可能留下锁或损坏通信状态。[multiprocessing 参考](https://docs.python.org/3.14/library/multiprocessing.html)

## 14.7 async def、await 与 Task

<!-- verify: run -->
```python
import asyncio

async def fetch(value):
    await asyncio.sleep(0.01)  # 模拟可挂起 I/O
    return value * 2

async def main():
    task = asyncio.create_task(fetch(3))
    result = await task
    assert result == 6
    assert await asyncio.gather(fetch(1), fetch(2)) == [2, 4]

asyncio.run(main())
```

调用 async 函数得到 coroutine 对象，不会自动启动。await 允许当前任务在适当位置挂起，但不是每个 await 都必然切走。`time.sleep`、同步 HTTP 请求、大型 CPU 循环会阻塞事件循环。

### 协程函数、协程对象、Task 与 Future

| 对象 | 如何得到 | 谁推进 | 结果如何读取 |
|---|---|---|---|
| 协程函数 | `async def f` | 只是定义 | 调用得到协程对象 |
| 原生协程对象 | `f()` | await 或任务调度 | 通常只能驱动完成一次 |
| asyncio.Task | `create_task(f())` | 所属事件循环 | await，可重复取得已完成结果 |
| asyncio.Future | 底层异步操作结果占位 | 完成方设置结果/异常 | await，不应随意阻塞读取 |
| concurrent.futures.Future | 线程/进程池 submit | 执行器 | result 可阻塞；不是同一种 Future |

<!-- verify: run -->
```python
import asyncio
async def value():
    return 7

async def main():
    coro = value()
    assert await coro == 7
    try:
        await coro
    except RuntimeError:
        pass
    else:
        raise AssertionError('原生协程不能重复驱动')
    task = asyncio.create_task(value())
    assert await task == 7 and await task == 7

asyncio.run(main())
```

连续 `await f(); await g()` 一般串行推进；先创建两个任务再等待才表达并发。默认调度与 eager task factory（3.12+）的立即执行方式不同，不要把 create_task 后首条副作用的固定顺序当作全环境保证。asyncio.Future 未完成时 result() 抛 InvalidStateError，不能拿线程 Future 的阻塞行为套用。跨模型可用 wrap_future、run_in_executor 等桥接，不能直接 await 任意线程池 Future。

## 14.8 TaskGroup 与结构化并发（3.11+）

<!-- verify: run -->
```python
import asyncio

async def job(value):
    await asyncio.sleep(0)
    return value + 1

async def main():
    async with asyncio.TaskGroup() as group:
        tasks = [group.create_task(job(n)) for n in range(3)]
    assert [task.result() for task in tasks] == [1, 2, 3]

asyncio.run(main())
```

离开 TaskGroup 等待子任务完成；某任务发生一般异常时，会取消兄弟任务并汇总异常。gather 默认某任务报错时不会自动提供完全相同的兄弟取消语义；不要把两者当成仅有语法差异。

### 用失败注入证明兄弟任务被取消并清理

下面不用“先睡一小段时间猜另一个任务已启动”，而用 Event 精确建立执行顺序。等待任务先开始，失败任务才抛错；离开 TaskGroup 时必须已执行等待任务的 finally。

<!-- verify: run -->
```python
import asyncio

async def check():
    started = asyncio.Event()
    cleaned = asyncio.Event()
    never = asyncio.Event()

    async def waiting():
        try:
            started.set()
            await never.wait()
        finally:
            cleaned.set()

    async def failing():
        await started.wait()
        raise ValueError("worker failed")

    failures = []
    try:
        async with asyncio.TaskGroup() as group:
            group.create_task(waiting())
            group.create_task(failing())
    except* ValueError as errors:
        failures.extend(errors.exceptions)
    assert len(failures) == 1
    assert cleaned.is_set()

asyncio.run(check())
```

TaskGroup 的作用域给“这些子任务属于谁”一个明确答案。后台 create_task 后完全不保存或等待任务，会让异常无人处理、关闭过程难以保证。独立后台任务可以存在，但应有宿主保存引用、收集失败并负责关闭。

`gather(return_exceptions=True)` 把异常作为结果元素交给调用者，不意味着错误已经处理；必须逐项检查。批量任务选择“任一失败则整体取消”还是“收集部分成功”，属于业务契约，不能只是为了让程序不抛异常而切换选项。

### gather、wait 与 TaskGroup 的责任边界

| API | 常见用途 | 出错/超时后谁收尾 |
|---|---|---|
| TaskGroup | 同一作用域的一组子任务 | 普通子任务失败时取消其余并等待清理，随后报告异常组 |
| gather | 按输入顺序收集结果 | 默认传播首个异常，其他任务通常仍运行；调用方负责余下生命周期 |
| wait | 得到 done/pending 两组任务 | 超时返回 pending，不自动取消，需要调用方取消并等待 |
| as_completed | 优先处理已完成结果 | 提前结束遍历后仍需处理未完成工作 |

TaskGroup 中一个任务自行取消，不等价于普通异常触发的整组失败；KeyboardInterrupt/SystemExit 等有专门传播规则。gather 已经完成异常传播后再 cancel 它，也未必能取消原来的兄弟任务。选择 API 时先定义失败语义，再按文档实现收尾，不要用 `return_exceptions=True` 掩盖缺失的错误处理。

## 14.9 超时、取消与 finally

<!-- verify: run -->
```python
import asyncio

async def main():
    try:
        async with asyncio.timeout(0.01):
            await asyncio.sleep(1)
    except TimeoutError:
        print("超时已处理")

    started = asyncio.Event()
    cleaned = asyncio.Event()
    async def worker():
        try:
            started.set()
            await asyncio.sleep(10)
        finally:
            cleaned.set()
    task = asyncio.create_task(worker())
    await started.wait()
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass
    assert cleaned.is_set()

asyncio.run(main())
```

取消是合作请求，通常在挂起点以 CancelledError 注入；它是 BaseException 子类。清理后通常应重新抛出，避免破坏 TaskGroup / timeout 的机制。业务事务仍需回滚，不要认为取消意味着远程副作用没有发生。

### 超时表示等待预算到期，不表示副作用被撤销

| 操作 | 超时或取消之后可能发生什么 | 调用方要做什么 |
|---|---|---|
| await 一个可取消协程 | 协程通常在挂起点收到取消 | 清理后传播取消，等待退出 |
| 等待线程池任务 | 已运行线程可能继续执行 | 阻塞库本身设置超时，必要时合作停止 |
| HTTP 写请求 | 服务端可能已提交但响应丢失 | 使用幂等键、查询状态或补偿 |
| 数据库操作 | 取决于驱动取消和事务状态 | 回滚或丢弃异常连接，确认提交结果 |
| CPU 循环没有 await | 事件循环不能及时运行取消逻辑 | 分块让出、进程隔离或原生计算 |

`asyncio.timeout` 通常在其上下文之外捕获 TimeoutError。`wait_for` 会请求被等待任务取消并等待相关取消处理，因此实际耗时可以超过指定值。`shield` 保护某个任务免于随等待者取消，不等于让等待者忽略取消，也不替你持有、观察和关闭该任务。

Python 的取消和 Go context 有相似目的，但机制不同：context 依赖被调用代码观察 Done 或 deadline；asyncio 通过任务取消异常和挂起点合作。两者都不保证远程系统回滚已经发生的写入。

### shield 保护的是被等待任务，调用者仍会收到取消

<!-- verify: run -->
```python
import asyncio
async def main():
    ready, release = asyncio.Event(), asyncio.Event()
    async def inner():
        await release.wait()
        return 42
    task = asyncio.create_task(inner())
    async def outer():
        ready.set()
        return await asyncio.shield(task)
    waiter = asyncio.create_task(outer())
    await ready.wait()
    waiter.cancel()
    try:
        await waiter
    except asyncio.CancelledError:
        pass
    else:
        raise AssertionError('外层应收到取消')
    assert not task.done()
    release.set()
    assert await task == 42

asyncio.run(main())
```

这里只演示生命周期差异，显式保留 task 并在结尾等待它。shield 不阻止别人直接取消 task，也不替调用方关闭任务。to_thread 被等待方取消后，实际线程也可能继续做事；必须让阻塞函数自身具备超时或停止协议。取消不是事务回滚，也不保证 finally 中的任意异步清理永远不会再次被取消。[asyncio 任务参考](https://docs.python.org/3.14/library/asyncio-task.html)

## 14.10 限流、异步迭代与 to_thread

<!-- verify: run -->
```python
import asyncio

async def source():
    for n in range(3):
        await asyncio.sleep(0)
        yield n

async def main():
    semaphore = asyncio.Semaphore(2)
    async def bounded(n):
        async with semaphore:
            await asyncio.sleep(0)
            return n * 2
    assert await asyncio.gather(*(bounded(n) for n in range(4))) == [0, 2, 4, 6]
    assert [n async for n in source()] == [0, 1, 2]
    assert await asyncio.to_thread(sum, [1, 2, 3]) == 6

asyncio.run(main())
```

Semaphore 限制进入区间的任务数量，但如果先创建百万个 Task，任务对象仍会占内存。大规模输入采用有界 asyncio.Queue + 固定消费者。to_thread 用于把阻塞 I/O 移出事件循环；常规 GIL 构建中不会让普通 Python CPU 计算神奇并行。

### 单线程 asyncio 也会有竞争；线程锁不能替代异步锁

<!-- verify: run -->
```python
import asyncio
async def main():
    state = {'total': 0}
    both_read = asyncio.Event()
    count = 0
    async def unsafe():
        nonlocal count
        old = state['total']
        count += 1
        if count == 2:
            both_read.set()
        await both_read.wait()
        state['total'] = old + 1
    await asyncio.gather(unsafe(), unsafe())
    assert state['total'] == 1

    lock = asyncio.Lock()
    async def safe():
        async with lock:
            old = state['total']
            await asyncio.sleep(0)
            state['total'] = old + 1
    state['total'] = 0
    await asyncio.gather(safe(), safe())
    assert state['total'] == 2

asyncio.run(main())
```

竞争发生在读改写之间的 await，让两个任务读到相同旧值。这个 Event 反例有确定执行顺序，不依赖碰运气。asyncio.Lock 只协调事件循环任务，不保护其他线程；threading.Lock 的阻塞获取可能卡住整个循环，RLock 又按线程认主，无法区分同一线程的多个协程。跨线程提交回调用 loop.call_soon_threadsafe；run_coroutine_threadsafe 给外部线程返回可等待结果，别在循环自身线程阻塞等待它。

Semaphore 限制同时进行的数量，速率限制控制单位时间次数，背压约束积压；三者不能互相替代。[asyncio 同步原语](https://docs.python.org/3.14/library/asyncio-sync.html)

## 14.11 ContextVar 与异步上下文

<!-- verify: run -->
```python
import asyncio
from contextvars import ContextVar
request_id = ContextVar("request_id", default="-")

async def handle(identifier):
    token = request_id.set(identifier)
    try:
        await asyncio.sleep(0)
        return request_id.get()
    finally:
        request_id.reset(token)

async def main():
    assert await asyncio.gather(handle("A"), handle("B")) == ["A", "B"]

asyncio.run(main())
```

threading.local 按线程隔离，不适合在同一线程承载多个异步请求的请求上下文；ContextVar 按上下文传播。它也不是跨进程分布式上下文自动传播机制。

### ContextVar 复制绑定，不深拷贝绑定的对象

<!-- verify: run -->
```python
import asyncio
from contextvars import ContextVar
request = ContextVar('request', default='unset')
payload = ContextVar('payload')

async def main():
    request.set('before')
    payload.set([])
    async def child():
        payload.get().append('shared')
        return request.get()
    task = asyncio.create_task(child())
    request.set('after')
    assert await task == 'before'
    assert request.get() == 'after'
    assert payload.get() == ['shared']
    assert await asyncio.to_thread(request.get) == 'after'

asyncio.run(main())
```

Task 默认捕获创建时上下文，父任务后来 set 不会追写既有子任务绑定；绑定里的 list 仍共享。避免 `ContextVar(..., default=[])` 形成全局可变默认值，按请求设置独立值并 finally reset token。to_thread 会传播当前上下文，但在线程中的重新绑定不会自动写回调用方。[contextvars 参考](https://docs.python.org/3.14/library/contextvars.html)

## 14.12 退出与运维边界

无论模型如何，都需要：任务数上限、排队上限、超时、失败传播、资源关闭、取消后清理、幂等策略和观测指标。不要仅以“同时打印了两行”证明并行正确。Jupyter 等已有事件循环环境通常直接 await，不能再嵌套 `asyncio.run`。

### 容量分析与退出顺序

假设生产速率长期超过处理速率，无界内存队列只会延后故障。有界队列满后，应明确选择等待、拒绝、落盘或丢弃。Semaphore 只限制进入业务区的数量，不限制任务对象总数；连接池只限制连接数，不限制所有请求等待者。

关闭过程通常是：停止接收新任务，通知生产者结束，等待或取消已有工作，收集异常，关闭网络与数据库资源，最后退出事件循环。每一步都要有最长等待时间和未完成工作处置方式。

验收矩阵至少包括：空输入、单项、输入多于队列容量、一个 worker 失败、生产者失败、调用方取消、下游超时。第 22.6 节给出有界任务数与失败退出示例；不要使用运行速度断言证明并发正确性。

延伸：[asyncio 任务文档](https://docs.python.org/3/library/asyncio-task.html)、[concurrent.futures](https://docs.python.org/3.14/library/concurrent.futures.html)。


---

# 15｜网络、数据库与 Web 开发

> 本章目标：明确网络、事务和 Web 请求的责任边界。
>
> 阅读重点：从 HTTP 错误分类到数据库事务配置，区分函数演示与真实服务验证。

## 15.1 URL、查询参数与 HTTP

<!-- verify: run -->
```python
from urllib.parse import urlencode, urlsplit, parse_qs, quote
query = urlencode({"name": "张三", "page": 1})
url = "https://example.com/users?" + query
parts = urlsplit(url)
assert parts.scheme == "https" and parts.hostname == "example.com"
assert parse_qs(parts.query) == {"name": ["张三"], "page": ["1"]}
assert quote("a/b", safe="") == "a%2Fb"
```

不要手工拼接用户提供的查询字符串；路径段转义与查询参数编码不同。HTTP 需要理解方法、状态码、头、正文、认证、缓存、分页、幂等性和重试。网络超时不证明服务端没有执行请求。

## 15.2 urllib 请求：标准库方案

下面需要联网，域名和接口是示意，未作为验证器网络请求执行：

```python
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
import json

def fetch_json(url):
    request = Request(url, headers={"Accept": "application/json", "User-Agent": "learning-client/1.0"})
    try:
        with urlopen(request, timeout=5) as response:
            raw = response.read(1_000_001)
            if len(raw) > 1_000_000:
                raise ValueError("响应过大")
            return json.loads(raw.decode("utf-8"))
    except HTTPError as exc:
        raise RuntimeError(f"HTTP 状态错误：{exc.code}") from exc
    except URLError as exc:
        raise RuntimeError("网络连接失败") from exc
```

这里假设接口约定 UTF-8 JSON；其他内容应按协议处理。TLS 验证保持启用。socket timeout 不等于严格的整个请求总时限；重定向、读取、DNS、连接各阶段也影响耗时与安全策略。

## 15.3 requests：连接池、超时与状态检查

第三方示意，先安装 requests；不默认访问外部服务：

```python
def get_users(base_url):
    import requests
    with requests.Session() as session:
        response = session.get(
            base_url.rstrip("/") + "/users",
            params={"page": 1},
            timeout=(3, 10),
        )
        response.raise_for_status()
        return response.json()
```

Session 复用连接并管理 cookie；`timeout=(connect, read)` 不是统一总耗时。`.json()` 不代表 HTTP 成功，必须先决定状态码策略。POST 重试需要考虑幂等键与重复副作用。异步客户端用支持异步的库，不在协程中直接调用阻塞 Session。

### HTTP 客户端需要四层错误分类

| 层次 | 示例 | 常见处理 |
|---|---|---|
| 传输 | DNS、连接失败、TLS、读取超时 | 记录阶段与预算，按请求语义决定重试 |
| HTTP | 401、404、429、500 | 按接口约定映射，不一律转空列表 |
| 表示格式 | 非 JSON、错误 Content-Type、超大响应 | 拒绝或报告协议错误 |
| 业务结构 | 缺字段、非法 ID、状态冲突 | 输入模型校验与业务错误 |

一个 `response.json()` 不能覆盖四层。请求成功也可能返回形状错误的 JSON；HTTP 错误也可能有有价值但敏感的响应正文。日志只保留允许的摘要、请求 ID、状态码和耗时。

重试需回答：这个方法是否幂等，服务端是否接受幂等键，重试哪些错误，最多几次，如何退避，总 deadline 剩多少。对 429 可按服务契约读取 Retry-After；对 401 通常先修认证，不是持续重试。成功响应体大小、重定向目标和连接池大小也需要约束。

长期运行应用应把 Session/client 放在明确的应用生命周期中，函数接收客户端依赖以便测试；此处的短函数自己创建 Session 只是最小例子，不能跨函数调用复用同一个连接池。

## 15.4 TCP：字节流、分帧与完整读取

TCP 没有“一个 send 对应一个 recv”的消息边界。Go 网络经验在这里同样适用，Python 不会自动解决粘包与半包。

<!-- verify: run -->
```python
import struct

def receive_exact(sock, size):
    result = bytearray()
    while len(result) < size:
        block = sock.recv(size - len(result))
        if not block:
            raise EOFError("连接提前关闭")
        result.extend(block)
    return bytes(result)

def receive_frame(sock, max_size=1_000_000):
    (size,) = struct.unpack("!I", receive_exact(sock, 4))
    if size > max_size:
        raise ValueError("消息超过上限")
    return receive_exact(sock, size)

class FakeSocket:
    def __init__(self, raw):
        self.raw = raw
    def recv(self, size):
        block, self.raw = self.raw[:min(size, 2)], self.raw[min(size, 2):]
        return block

assert receive_frame(FakeSocket(struct.pack("!I", 5) + b"hello")) == b"hello"
```

真实发送使用 `sendall`，接收配置 timeout，限制帧大小并处理 EOF。长度前缀、分隔符、固定长度是常见协议选择，各有转义和边界问题。

## 15.5 socket、UDP 与 TLS 入口

连接示例需要自己的本地服务；未自动执行：

```python
import socket, ssl

def tls_exchange(host, port, payload):
    context = ssl.create_default_context()
    with socket.create_connection((host, port), timeout=3) as raw:
        with context.wrap_socket(raw, server_hostname=host) as secure:
            secure.sendall(payload)
            return secure.recv(4096)  # 仅演示读取一次，不表示消息一定完整
```

UDP 使用 SOCK_DGRAM、sendto、recvfrom；保留报文边界但不保证到达、顺序和去重。TLS 需要校验证书与主机名；不要用关闭验证“解决证书报错”。高并发服务可用 asyncio streams 或成熟框架，不必手写 select 循环。

## 15.6 SQLite 基础与参数化 SQL

<!-- verify: run -->
```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as conn:
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL UNIQUE)")
    with conn:
        conn.executemany("INSERT INTO users(name) VALUES (?)", [("张三",), ("李四",)])
    row = conn.execute("SELECT id, name FROM users WHERE name = ?", ("张三",)).fetchone()
    assert row["name"] == "张三"
    assert conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] == 2
```

参数元组只有一个元素时要有逗号。占位符负责值，不负责表名 / 列名；动态排序字段应从允许列表映射。不要用 f-string 拼接外部输入到 SQL。

## 15.7 事务、回滚与连接关闭

<!-- verify: run -->
```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:")) as conn:
    conn.execute("CREATE TABLE ledger(id INTEGER PRIMARY KEY, amount INTEGER CHECK(amount > 0))")
    try:
        with conn:
            conn.execute("INSERT INTO ledger(amount) VALUES (?)", (10,))
            conn.execute("INSERT INTO ledger(amount) VALUES (?)", (-1,))
    except sqlite3.IntegrityError:
        pass
    assert conn.execute("SELECT COUNT(*) FROM ledger").fetchone()[0] == 0
```

`with conn:` 按连接事务配置提交 / 回滚，但不会自动 close。示例用 closing 保证关闭。SQLite autocommit 与旧 isolation_level 模式的关系随配置而不同，不要把这段代码泛化为所有驱动的事务规则。大型业务需要明确事务开始点、隔离级别、锁等待、重试与提交失败处理。

### 明确 sqlite3 的事务控制模式（3.12+）

下面是 Python sqlite3 接口的配置区别，不要与 SQLite 底层自动提交状态混成同一个概念：

| 连接选项 | 核心行为 | 使用约束 |
|---|---|---|
| `autocommit=False` | DB-API 风格保持事务；commit / rollback 后会打开新事务 | 不再随意手写 BEGIN |
| `autocommit=True` | SQLite 自动提交模式；Python commit / rollback 不执行常规提交回滚操作 | 多语句原子性需另外明确控制 |
| `autocommit=sqlite3.LEGACY_TRANSACTION_CONTROL` | 使用旧 isolation_level 规则，DML 可隐式开启事务 | 显式 BEGIN 与隐式事务不能随意混用 |
| 旧模式且 `isolation_level=None` | 不隐式开启事务 | 可用 SQL BEGIN / COMMIT 自己控制 |

不能把不同模式的示例混合拼接。`with conn` 管理事务完成，不会自动关闭连接；在 autocommit=True 时也不能把它当作自动多语句事务。

以下用 3.12+ 的 autocommit=False 明确演示两条写入整体回滚：

<!-- verify: run -->
```python
import sqlite3
from contextlib import closing

with closing(sqlite3.connect(":memory:", autocommit=False)) as connection:
    connection.execute("CREATE TABLE entries(value INTEGER CHECK(value > 0))")
    connection.commit()  # 建表先成为稳定基线
    try:
        with connection:
            connection.execute("INSERT INTO entries VALUES (?)", (10,))
            connection.execute("INSERT INTO entries VALUES (?)", (-1,))
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("第二条写入必须违反约束")
    assert connection.execute("SELECT COUNT(*) FROM entries").fetchone()[0] == 0
```

建表先提交，是为了将 schema 初始化和业务事务分开。否则回滚也可能撤销尚未提交的建表，随后检查会得到“表不存在”，掩盖原本想验证的行为。

第 17 章项目在本机 3.14.5 的默认旧事务模式下使用显式 BEGIN，写入必须放在 repository.transaction() 里。若未来修改连接 autocommit 选项，需要连同 transaction 实现、建表、PRAGMA 生效时机和测试一起调整，不能只改一处 connect。

## 15.8 PostgreSQL / MySQL 驱动与连接池

Python DB-API 规范统一部分接口，不能统一占位符、事务、自动提交和线程安全细节。SQLite 常见 `?`，其他驱动可能 `%s` 或命名样式；`%s` 作为驱动占位符不等于用 `%` 运算符格式化 SQL。

概念示例不连接真实库：

```python
def find_user(connection, uid):
    # 此处假定驱动支持 %s 参数风格，具体以驱动文档为准
    with connection.cursor() as cursor:
        cursor.execute("SELECT id, name FROM users WHERE id = %s", (uid,))
        return cursor.fetchone()
```

连接池要限制连接数、归还连接、设置超时并处理失效连接。不要跨进程复用启动前创建的连接；不要假定一个连接能被任意线程 / 协程同时操作。

### 查询 API 的规模与一致性

OFFSET 分页适合小型稳定数据；大偏移仍可能扫描或跳过许多行。游标分页用稳定排序键，例如 `(created_at, id)`，必须同时处理相同时间戳，不能只用时间字段。排序需要对应索引，并在真实数据库执行计划中确认。

“先查询再更新”在并发下有间隙；扣库存可使用条件更新 `UPDATE ... SET stock = stock - ? WHERE id = ? AND stock >= ?`，检查影响行数，再按驱动和隔离级别处理冲突。数据库事务保护数据库内的操作，不自动覆盖 HTTP、邮件或文件副作用。

连接池的容量应和数据库允许的连接预算共同设计。若每个进程有独立连接池，实际最大连接数可能是 worker 数乘每池上限。驱动是同步还是异步、连接能否跨线程使用、异常后能否归还，都要按所选驱动文档验证。

## 15.9 SQLAlchemy ORM 与映射思想

以下为 SQLAlchemy 2 风格的可手动运行示例，需要 `python -m pip install 'SQLAlchemy>=2,<3'`：

```python
def orm_demo():
    from sqlalchemy import create_engine, select, String
    from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

    class Base(DeclarativeBase):
        pass

    class User(Base):
        __tablename__ = "users"
        id: Mapped[int] = mapped_column(primary_key=True)
        name: Mapped[str] = mapped_column(String(100), nullable=False)

    engine = create_engine("sqlite+pysqlite:///:memory:")
    try:
        Base.metadata.create_all(engine)
        with Session(engine) as session:
            with session.begin():
                session.add(User(name="jackie"))
            return session.scalars(select(User).where(User.name == "jackie")).one().name
    finally:
        engine.dispose()
```

ORM 解决对象与表的映射，不代替索引、分页、事务与 SQL 分析。Session 是工作单元，别全局跨请求共享；警惕懒加载 N+1、会话结束后的属性访问和大批量全量装载。schema 变更用迁移工具，不在每次服务启动时任意 create_all 代替正式迁移。

## 15.10 WSGI、ASGI 与最小应用

WSGI 定义同步 Python Web 应用与服务器的接口。最小应用可以直接调用验证：

<!-- verify: run -->
```python
import json

def app(environ, start_response):
    body = json.dumps({"ok": True}, ensure_ascii=False).encode("utf-8")
    start_response("200 OK", [("Content-Type", "application/json; charset=utf-8"), ("Content-Length", str(len(body)))])
    return [body]

headers = []
result = app({"PATH_INFO": "/"}, lambda status, values: headers.append((status, values)))
assert b"".join(result) == b'{"ok": true}'
assert headers[0][0] == "200 OK"
```

ASGI 使用异步调用与事件消息，支持 HTTP、WebSocket 和生命周期等协议。最小 HTTP 示例：

<!-- verify: run -->
```python
import asyncio

async def application(scope, receive, send):
    if scope["type"] != "http":
        raise RuntimeError("此示例只处理 HTTP")
    await send({"type": "http.response.start", "status": 200, "headers": [(b"content-type", b"text/plain")]})
    await send({"type": "http.response.body", "body": b"ok"})

async def check():
    messages = []
    async def send(message):
        messages.append(message)
    await application({"type": "http"}, None, send)
    assert messages[-1]["body"] == b"ok"

asyncio.run(check())
```

这只是协议演示，不支持所有生产请求或 lifespan。Flask 偏向轻量同步 Web，Django 提供完整应用体系，FastAPI 常用于带类型模型的 ASGI API；选择要结合团队与部署需求。具体生态示例见第 18 章。

## 15.11 请求完整生命周期

实际服务至少考虑：路由匹配、认证、授权、输入解析、业务校验、事务、序列化、异常映射、日志与 trace、超时与取消。Python 的异常应在适当边界映射为 HTTP 状态，不把原始堆栈和数据库错误直接返回给客户端。开发服务器只用于本地调试。

### 将路由层与业务层分开

路由层读取请求，校验认证授权，解析为内部命令，再调用服务。服务组织事务和领域操作；仓储操作 SQL；序列化层把内部模型转换为稳定响应。不要让仓储直接返回 HTTPException，否则 CLI 和测试也被 Web 框架绑定。

同步函数并不低级，async 函数也不天然更快。同步驱动适合相应线程执行模型；异步路由需要异步 I/O 链路或明确线程移交。应用启动时创建共享池，请求开始时取得请求资源，请求结束归还，应用关闭时关闭池。

验收：用 fake 验证服务调用契约，用真实本地 SQLite 验证 SQL 与事务，用目标数据库验证隔离与驱动，再用 HTTP 集成测试验证状态码与序列化。本书运行的 WSGI/ASGI 函数示例没有启动网络服务器，不能据此宣称真实服务部署成功。

延伸：[sqlite3 官方文档](https://docs.python.org/3.14/library/sqlite3.html)、[urllib.request](https://docs.python.org/3.14/library/urllib.request.html)、[SQLAlchemy 官方教程](https://docs.sqlalchemy.org/en/20/tutorial/)。


---

# 16｜测试、调试、性能与安全

> 本章目标：建立行为测试、诊断与性能证据。
>
> 阅读重点：关注失败矩阵、真实资源边界和可复现测量，而不是只追求覆盖率或微基准。

## 16.1 unittest：行为、边界与异常

<!-- verify: run -->
```python
import unittest

def discount(amount, rate):
    if not 0 <= rate <= 1:
        raise ValueError("折扣必须在 0..1")
    return amount * (1 - rate)

class DiscountTests(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(discount(100, 0.2), 80)
    def test_invalid(self):
        with self.assertRaises(ValueError):
            discount(100, 2)
    def test_boundaries(self):
        for rate, expected in [(0, 100), (1, 0)]:
            with self.subTest(rate=rate):
                self.assertEqual(discount(100, rate), expected)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(DiscountTests)
result = unittest.TestResult()
suite.run(result)
assert result.wasSuccessful() and result.testsRun == 3
```

测试要验证契约、边界与副作用，而不是逐行镜像实现。setUp / tearDown 管理每个测试生命周期，addCleanup 可以在准备过程部分失败时更可靠地清理资源。TemporaryDirectory 比固定路径更适合隔离文件测试。

### 把一句需求展开为测试矩阵

以“标题去空白后 1—200 字符，失败不写库”为例，不只测 `"hello"`：

| 输入或状态 | 预期 | 需要观察的状态 |
|---|---|---|
| 普通标题 | 成功 | 返回值、数据库行 |
| 两端空白 | 规范化后成功 | 保存的是规范化标题 |
| 空白、长度 201 | 明确业务错误 | 数据库没有新增 |
| 引号或 SQL 片段 | 作为普通文本保存 | 表仍存在、文本无损 |
| 同一事务第一条合法第二条非法 | 整体失败 | 第一条也已回滚 |
| 进程退出后重启读取 | 仍能读取已提交数据 | 独立连接可见 |

测试名应描述契约。只断言“函数没有抛错”，不能证明返回数据或副作用正确；只 mock execute 被调用，不能证明 SQL 能在数据库执行。单元测试适合纯逻辑，集成测试适合资源边界，少量端到端测试验证整个入口。

不稳定测试常来自真实时钟、任意 sleep、共享目录、网络依赖、随机顺序。优先注入时钟或依赖，使用临时目录、Event 和固定输入。随机性质测试也有价值，但要保留可复现输入或 seed，并避免把预期值写成另一份相同算法。

## 16.2 mock：替换使用位置与检查协作

<!-- verify: run -->
```python
from unittest.mock import Mock, patch

class Service:
    def __init__(self, sender):
        self.sender = sender
    def complete(self, uid):
        self.sender.send(uid, "done")

sender = Mock()
Service(sender).complete(7)
sender.send.assert_called_once_with(7, "done")

with patch("os.environ", {"APP_MODE": "test"}):
    import os
    assert os.environ["APP_MODE"] == "test"
```

patch 要替换“被测代码查找对象的位置”。例如 `service.py` 用 `from client import fetch`，通常 patch `service.fetch`，而不是只 patch `client.fetch`。能用真实内存 SQLite、内存流、简单 fake 时，不必把所有内部函数都 mock。

### fake、mock 和真实资源各自适合什么

fake 是简化但有行为的替代品，例如内存消息发送器；mock 更适合断言调用次数和参数；真实 SQLite 适合证明 SQL 和回滚。若把每一层都 mock，测试可能只证明当前实现互相调用，无法发现协议或 SQL 错误。

<!-- verify: run -->
```python
from unittest.mock import create_autospec

class Sender:
    def send(self, task_id: int, message: str) -> None:
        pass

def notify(sender, task_id):
    sender.send(task_id, "completed")

sender = create_autospec(Sender, instance=True, spec_set=True)
notify(sender, 7)
sender.send.assert_called_once_with(7, "completed")
try:
    sender.send(7)
except TypeError:
    pass
else:
    raise AssertionError("签名错误应被 mock 发现")
```

autospec 能检查调用签名，不能证明第三方系统真的接收了消息，也不会按注解检查每个值的类型。异步方法可用 AsyncMock 并断言 awaited 情况；调用过异步函数不等于已 await。

### autospec 检查调用形状，AsyncMock 区分调用和等待

<!-- verify: run -->
```python
import asyncio
from unittest.mock import create_autospec, AsyncMock
def read(key, *, timeout=1):
    return key
fake = create_autospec(read, return_value='value')
assert fake('k', timeout=2) == 'value'
try:
    fake('k', 2)
except TypeError:
    pass
else:
    raise AssertionError('关键字专用参数不能按位置传入')

async def main():
    fetch = AsyncMock(return_value=42)
    coroutine = fetch('k')
    fetch.assert_called_once_with('k')
    fetch.assert_not_awaited()
    assert await coroutine == 42
    fetch.assert_awaited_once_with('k')
asyncio.run(main())
```

autospec 可以发现错误参数数量或名称，通常不检查注解类型和业务规则。AsyncMock 被调用不代表协程被执行，应验证 awaited。patch 必须替换使用方查找名称的位置；已经捕获进默认参数、闭包或别处局部变量的对象，不会被后来改模块属性自动替换。测试时同时观察输出、异常、清理状态，避免只断言“某个方法调用过”。[unittest.mock 参考](https://docs.python.org/3.14/library/unittest.mock.html)

## 16.3 doctest 与 pytest

<!-- verify: run -->
```python
import doctest
def square(n):
    """计算平方。

    >>> square(3)
    9
    >>> square(-2)
    4
    """
    return n * n

finder = doctest.DocTestFinder()
runner = doctest.DocTestRunner()
for test in finder.find(square):
    runner.run(test)
assert runner.summarize().failed == 0
```

doctest 适合文档中的稳定小例子；复杂浮点、时间、随机输出容易脆弱。pytest 是第三方工具，提供普通 assert、fixture 和参数化，项目按团队惯例选择。不要混淆“文档示例通过”和“完整业务已被充分测试”。

## 16.4 pdb、breakpoint 与 traceback

手动调试代码，只有交互终端中运行：

```python
def investigate(value):
    doubled = value * 2
    breakpoint()
    return doubled + 1
```

常用 pdb 命令：n 下一步、s 进入、c 继续、p 表达式、pp 美化输出、l 查看源码、bt 调用栈、q 退出。IDE 断点同样要观察变量、栈与异常首次抛出位置。读取 traceback 从最终异常和最贴近业务的栈帧定位，而不是只看第一行。

## 16.5 timeit 与 cProfile

<!-- verify: run -->
```python
import timeit, cProfile, pstats
from io import StringIO
elapsed = timeit.timeit("sum(range(100))", number=100)
assert elapsed >= 0
profiler = cProfile.Profile()
profiler.runcall(sum, range(1000))
output = StringIO()
pstats.Stats(profiler, stream=output).sort_stats("cumulative").print_stats(5)
assert "function calls" in output.getvalue()
```

timeit 适合小片段对比；cProfile 寻找调用热点。微基准需要相同输入、环境与重复次数；单次耗时差异不能证明优化。先量端到端瓶颈，再选择算法、减少 I/O 往返、批量处理、缓存或原生库。

### 性能实验需要假设、基线和正确性检查

假设瓶颈是“在大列表中重复查 ID”，可以比较线性扫描与预建 set，但要把 set 构建成本算入适用场景。每次只查一次与建立索引后查十万次，结论可能不同。

<!-- verify: run -->
```python
from timeit import repeat

values = list(range(1000))
needles = [10, 500, 999, 2000]
index = set(values)
def scan():
    return [item in values for item in needles]
def indexed():
    return [item in index for item in needles]

assert scan() == indexed() == [True, True, True, False]
timings = {
    "scan": repeat(scan, number=10, repeat=3),
    "indexed": repeat(indexed, number=10, repeat=3),
}
assert all(t >= 0 for samples in timings.values() for t in samples)
```

不在测试里断言哪种耗时一定更小，避免机器负载导致偶然失败。报告时写明解释器、数据规模、是否含预处理、重复次数及观察范围。对于 Web 服务，数据库往返和序列化常比几条 Python 表达式重要，应先做端到端 profile。

空间也需要测量：缓存和索引减少 CPU 可能增加常驻内存。tracemalloc 主要覆盖 Python 分配，原生数组或外部库的内存还需结合进程指标。

## 16.6 tracemalloc 与对象保留

<!-- verify: run -->
```python
import tracemalloc
tracemalloc.start()
items = [str(i) for i in range(1000)]
current, peak = tracemalloc.get_traced_memory()
assert peak >= current > 0
snapshot = tracemalloc.take_snapshot()
assert snapshot.statistics("lineno")
tracemalloc.stop()
```

tracemalloc 追踪 Python 分配，不一定覆盖所有原生库内存。内存增长可能来自缓存、队列、日志、全局容器、未消费结果，而非引用环本身。先证明对象为何仍被引用，再考虑 gc 调参。

## 16.7 代码质量与 CI 顺序

典型流水线：安装锁定依赖 → 格式 / 静态检查 → 类型检查 → 单元测试 → 集成测试 → 构建 wheel → 干净环境安装检查。工具可选择 Ruff、mypy / Pyright、pytest 等；仓库已有约定优先，不需要同时引入所有工具。

```powershell
python -m unittest discover -s tests -v
python -m doctest -v your_module.py
python -m compileall -q src
```

compileall 只证明语法能编译，不证明依赖存在、类型正确或业务正确。覆盖率百分比不等于断言质量，重点检查失败路径、边界、事务回滚和并发退出。

## 16.8 外部输入与注入边界

<!-- verify: run -->
```python
from pathlib import Path
from tempfile import TemporaryDirectory

def confined_path(root, relative):
    root = Path(root).resolve()
    candidate = (root / relative).resolve()
    if not candidate.is_relative_to(root):
        raise ValueError("路径越过根目录")
    return candidate

with TemporaryDirectory() as tmp:
    assert confined_path(tmp, "reports/a.txt").name == "a.txt"
    try:
        confined_path(tmp, "../outside.txt")
    except ValueError:
        pass
    else:
        raise AssertionError("必须拒绝越界")
```

这是普通应用层目录约束示例；如果攻击者能并发替换符号链接，仍需操作系统级安全打开策略，不能将先 resolve 后 open 当成绝对防护。

常见输入边界与相应做法：

| 边界 | 推荐措施 |
|---|---|
| SQL | 参数化值，标识符允许列表 |
| shell | 参数列表，避免 shell 拼接 |
| HTML | 模板自动转义，按上下文编码 |
| pickle / eval | 不处理不可信输入 |
| HTTP 地址 | 协议 / 主机 / 地址范围限制，防 SSRF |
| 文件 / 归档 | 限制目录、数量、解压后大小 |
| 正则 / JSON | 限输入大小、深度、复杂度和耗时 |
| 认证 / 日志 | 机密管理、脱敏、密码专用派生算法 |

## 16.9 发布与运行边界

容器不自动解决依赖漏洞和权限问题；建议以普通用户运行、设置工作目录、固定基础环境、给进程配置健康检查与终止宽限时间。多 worker 部署时，全局变量不是跨进程共享存储；计划任务、缓存与连接池也要考虑多实例。

教程验证在本机 CPython 3.14.5 完成，不代表其他解释器、其他系统、生产网络、真实数据库或第三方库版本都已验证。需要部署时，在实际环境复现测试。

### 本教程验证器的信任与能力边界

本仓库验证器会执行带标记的代码，因此它是用于可信教材的检查工具，不是执行任意 Markdown 的安全沙箱。`-I` 隔离部分解释器环境、临时工作目录隔离示例产物，但没有操作系统级网络和文件权限沙箱。

“默认不联网”表示本书选中的执行例子不发起外部网络请求，不能解释为任何恶意代码都无法联网。本地链接检查验证文件存在；没有验证外部网址长期可用、Markdown 锚点存在或所有阅读器渲染一致。

工程验收应分层记录：语法检查、示例执行、单元与集成测试、静态类型检查、包构建安装、部署验证。只报告实际完成的层次。具体本轮结果见根目录 VALIDATION.md，不能用旧统计代替新运行。

延伸：[unittest 官方文档](https://docs.python.org/3.14/library/unittest.html)、[调试与性能工具](https://docs.python.org/3.14/library/debug.html)。


---

# 17｜综合实战：SQLite 任务管理器

> 本章目标：读懂一个可运行 CLI 的完整生命周期。
>
> 阅读重点：沿输入、模型、事务、连接关闭和输出追踪，再独立完成扩展练习。

## 17.1 目标与文件

我们把语法、dataclass、类型提示、异常、上下文管理器、SQLite、CLI 和测试串成一个完整例子：新增任务、分页查询、按状态过滤、完成任务、删除任务，并支持 JSON 输出。

| 文件 | 责任 |
|---|---|
| [task_cli.py](examples/task_cli.py) | 模型、仓储、事务、命令行入口 |
| [test_task_cli.py](examples/test_task_cli.py) | 内存数据库、回滚、非法输入、跨进程 CLI 测试 |
| [verify_tutorial.py](scripts/verify_tutorial.py) | 检查本文档集的代码块与链接 |

这是学习项目，故意使用单文件组织便于逐段阅读。项目增长后可以拆成 `models.py`、`repository.py`、`cli.py`，不必一开始就照搬大型服务的全部分层。

## 17.2 运行完整流程

以下命令在仓库根目录执行，`--db` 和 `--json` 放在子命令前：

```powershell
python examples/task_cli.py --help
python examples/task_cli.py --db demo-tasks.db add '学习 Python'
python examples/task_cli.py --db demo-tasks.db add '理解生成器'
python examples/task_cli.py --db demo-tasks.db list --status todo --limit 10
python examples/task_cli.py --db demo-tasks.db done 1
python examples/task_cli.py --db demo-tasks.db --json list --status done
python examples/task_cli.py --db demo-tasks.db delete 2
```

首次在新数据库里创建的 ID 通常从 1 开始；数据库已有数据时，以实际输出 ID 为准。默认输出含 UTC 时间戳；JSON 返回任务数组，即使 add / done 也保持数组格式。

```json
[
  {"id": 1, "title": "学习 Python", "done": true, "created_at": "2026-10-15T08:00:00+00:00"}
]
```

上面的时间是格式示意，实际值来自创建时刻。

## 17.3 数据模型与表约束

Task 使用 `@dataclass(frozen=True, slots=True)`：字段明确、便于比较与输出、避免随意附加属性。数据库中 done 使用 0 / 1，读取时转 bool；对外保持 Python 语义。

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY,
    title TEXT NOT NULL CHECK(length(trim(title)) BETWEEN 1 AND 200),
    done INTEGER NOT NULL DEFAULT 0 CHECK(done IN (0, 1)),
    created_at TEXT NOT NULL
);
```

应用层用 Python strip 检查标题，数据库提供额外 CHECK 约束；二者对各种 Unicode 空白的处理并不完全等价。数据库约束是最后防线，不能代替友好的输入错误。

### 从需求到数据契约

任务 ID 是数据库生成的身份，不是业务排序时间。标题由应用去首尾空白、限制字符数；done 是有限状态；created_at 是带 UTC 偏移的文本。本项目没设计更新审计、软删除、租户或优先级，不应让调用者自行猜测。

SQLite 的 `INTEGER PRIMARY KEY` 与显式 `AUTOINCREMENT` 不同；删除较大 ID 后，某些情况下 ID 可以被复用。因此 CLI 测试应读取实际返回 ID，不把“ID 永不复用”或“始终连续”当契约。若要长期外部引用、审计和分布式生成，应另选身份策略。

金额、复杂状态机等未来字段不应直接塞进 title；它们需要模型、数据库约束和迁移。`CREATE TABLE IF NOT EXISTS` 只能确保表存在，不会把旧表自动更新为新 schema。

## 17.4 仓储与依赖边界

TaskRepository 接收数据库路径，也可使用 `:memory:`。它统一 SQL 与行映射，命令行层不关心 sqlite3.Row 的细节。

- `add(title)` 先去首尾空白并校验长度，再参数化写入。
- `get(id)` 返回 Task，不存在则抛 TaskNotFound。
- `list_tasks(status, limit, offset)` 验证查询条件，稳定按 id 排序。
- `mark_done(id)` 重复调用保持成功，体现幂等操作。
- `delete(id)` 对不存在任务报业务错误，语义与完成操作有所不同。

这些方法假定库内调用方遵守注解类型；外部请求接入时应再加解析边界。分页使用 OFFSET 便于学习，大偏移或并发变化较多时可以改为 `WHERE id > ? ORDER BY id LIMIT ?` 的游标分页。

## 17.5 事务由业务工作单元控制

不要在每个仓储写方法内独立 commit，否则“新增任务并写审计记录”无法保证共同成功 / 共同失败。调用者使用 repository.transaction() 包围一个工作单元。

下面是最小同类模式，真实项目实现见源文件：

<!-- verify: run -->
```python
from contextlib import contextmanager, closing
import sqlite3

@contextmanager
def transaction(connection):
    connection.execute("BEGIN")
    try:
        yield connection
        connection.commit()
    except BaseException:
        connection.rollback()
        raise

with closing(sqlite3.connect(":memory:")) as connection:
    connection.execute("CREATE TABLE values_demo(value INTEGER)")
    with transaction(connection):
        connection.execute("INSERT INTO values_demo VALUES (?)", (7,))
    assert connection.execute("SELECT value FROM values_demo").fetchone()[0] == 7
```

这里捕获 BaseException 是为了确保中断等情形也尝试回滚，随后立即重新抛出，不会吞掉中断。完整项目明确拒绝嵌套事务；需要嵌套工作单元时设计 SAVEPOINT，不要假定再次 BEGIN 可行。成功 / 失败后，仓储上下文始终关闭连接。

### 沿一次 add 命令追踪所有权

1. argparse 得到标题和数据库路径，路径是用户明确选定的持久化位置。
2. TaskRepository 创建并拥有一个连接；初始化失败时关闭已创建连接。
3. transaction 开始工作单元，add 校验标题并插入，随后读取模型。
4. 正常退出事务后提交；异常则回滚并继续传播。
5. 离开仓储上下文关闭连接，CLI 再输出 JSON 或文本。

输出发生在提交之后，所以读取 stdout 成功记录通常意味着本地提交步骤已正常返回。但“提交成功之后进程在输出前退出”仍可能发生；调用方不能因没收到输出就断言没创建任务。要支持可靠重试，可以设计业务请求 ID 和唯一约束，而不是只在客户端重试。

仓储写方法不会自行 commit，这使批量工作可以共用一个事务。与此同时，调用方必须遵守“所有写入置于 transaction 内”的约定；直接调用 add 之后关闭连接，不能期待自动持久化。类型注解不强制这个生命周期规则，测试和 API 设计都应突出它。

嵌套事务当前明确拒绝。若内层捕获了该错误并继续外层，外层不会自动知道业务是否应回滚；调用者必须决定是否传播错误。要提供真正嵌套工作单元，需要 SAVEPOINT 和精确定义的释放、回滚规则。

## 17.6 CLI 参数、错误与退出码

argparse 处理子命令和参数转换；仓储继续执行业务范围校验。数据库连接错误、业务错误输出到 stderr；成功结果输出到 stdout。这样脚本可以可靠地重定向或读取 JSON。

| 结果 | 退出码 | 输出 |
|---|---|---|
| 正常完成 | 0 | stdout |
| 业务或数据库错误 | 1 | stderr |
| CLI 参数错误 | 2 | argparse 的 usage 与错误信息 |

捕获异常只在边界完成。仓储抛出有语义的异常，入口决定如何向用户展示，不在每个函数里打印并返回 None。

## 17.7 如何验证

```powershell
python -B -m unittest discover -s examples -p 'test_*.py' -v
python -B scripts/verify_tutorial.py
```

测试覆盖真实 SQL、标题修剪、状态过滤、分页、重复完成、非法标题、非法查询条件、嵌套事务拒绝、CHECK 约束、SQL 字符串注入、回滚和跨进程持久化。CLI 测试使用临时目录，不污染你的学习数据库。

### 代码阅读与实验顺序

先读 main 的命令分支，再读 TaskRepository 的事务与资源方法，最后读 SQL。这样可以先看到“谁负责提交”，避免从某一行 INSERT 错误推断它会独立提交。

建议在新数据库做四个实验：

| 实验 | 操作 | 应得到的证据 |
|---|---|---|
| 持久性 | 创建后用第二个进程查询 | 能读到相同 ID 与标题 |
| 整体回滚 | 同一事务内合法标题后跟空标题 | 查询不到第一条 |
| 幂等状态 | 对同一 ID 连续 done | 状态相同，不新增任务 |
| 错误通道 | 查询不存在任务或传非法参数 | stderr 有说明，退出码符合约定 |

教学测试已覆盖真实 SQLite 和跨进程 CLI。它没有证明多线程共享同一仓储安全，项目也明确不支持这种用法；没有验证数据库锁竞争、进程被强制终止或磁盘写满。迁移成服务后应增加这些运行场景。

## 17.8 继续练习：CSV 导出

下面是独立可运行的导出函数；接入 CLI 时在 list 分支附近复用仓储查询，而不是重复拼 SQL。

<!-- verify: run -->
```python
import csv
from io import StringIO
from dataclasses import dataclass

@dataclass
class Task:
    id: int
    title: str
    done: bool

def export_tasks(tasks, stream):
    writer = csv.writer(stream)
    writer.writerow(["id", "title", "done"])
    for task in tasks:
        writer.writerow([task.id, task.title, int(task.done)])

stream = StringIO(newline="")
export_tasks([Task(1, "a,b", False)], stream)
stream.seek(0)
assert list(csv.reader(stream)) == [["id", "title", "done"], ["1", "a,b", "0"]]
```

面向电子表格的导出还要决定公式字符串处理。新增 due_at 时，明确时区与 null 语义；新增 HTTP 接口时，增加认证、授权、模型验证和请求事务边界。

## 17.9 从学习项目到服务

单文件 CLI 没有用户隔离、网络接口、迁移系统或多实例任务调度。变成生产服务时，应根据实际需求补齐，而不是通过“把代码装进 Docker”宣布完成。SQLite 文件写并发、连接生命周期与备份要求也需要重新评估。

### 演进为服务时先改边界，再加框架

建议保留 Task 及领域异常，把 SQL 留在 repository，新增 service 负责业务工作单元，再由 CLI 或 HTTP adapter 调用 service。Protocol 可描述服务真正需要的仓储行为，但不要为了形式完整给每个函数增加接口。

| 新需求 | 最少要补的设计 | 关联章节 |
|---|---|---|
| 多用户 | 所有读写都带 owner/tenant 边界；错误信息防泄露 | 10、15、16 |
| 批量导入 | 预校验或明确流式事务；失败策略与结果结构 | 06、12、19 |
| 修改 schema | 迁移版本、旧数据默认值、回滚方案 | 07、15 |
| 发通知 | 提交后触发与重试去重；必要时 outbox | 11、15、22 |
| 长任务 | 状态持久化、取消、恢复、并发上限 | 14、22 |
| 分布式部署 | 共享存储、连接预算、实例关闭与观测 | 13—16 |

验收本章时，能够独立增加一个过滤条件并补失败测试，比仅运行一遍演示命令更有意义。第 19 章提供批量事务和游标分页参考实现；它们作为独立教学例子，不冒充当前 CLI 已支持的新命令。


---

# 18｜生态专题与扩展边界

> 本章目标：按业务需要进入第三方生态。
>
> 阅读重点：本章依赖示例默认仅检查语法；先确认目标版本、数据语义和验收方式。

本章给出 Python 常见应用方向的最小入口。第三方示例用于理解 API 风格，未安装依赖、未联网验证；具体安装兼容性以其官方文档和你的目标 Python 版本为准。不要一次性安装全章依赖。

## 18.1 NumPy：数组、广播与视图

需要 NumPy，手动调用 numpy_demo：

```python
def numpy_demo():
    import numpy as np
    matrix = np.array([[1, 2, 3], [4, 5, 6]], dtype=np.int64)
    assert matrix.shape == (2, 3)
    assert (matrix + np.array([10, 20, 30])).tolist() == [[11, 22, 33], [14, 25, 36]]
    assert matrix.sum(axis=0).tolist() == [5, 7, 9]
    view = matrix[:, :2]
    view[0, 0] = 99
    assert matrix[0, 0] == 99
    independent = matrix.copy()
    independent[0, 0] = 0
    assert matrix[0, 0] == 99
```

NumPy ndarray 通常同质、支持向量化与广播，某些切片返回共享视图；这与普通 Python list 切片不同。`*` 通常逐元素乘法，矩阵乘法用 `@`；dtype 可能溢出，不再拥有 Python int 的任意精度语义。[NumPy 官方入门](https://numpy.org/doc/stable/user/quickstart.html)。

### 把 Python 容器直觉迁移到 ndarray 前先校准

普通 Python list 切片复制外层，NumPy 基本切片常共享数据；高级索引的复制规则又不同。广播按尾部维度对齐，维度相等或其中一个为 1 才能兼容。想知道结果规模，先写出 shape，再执行操作，避免不经意生成巨大中间矩阵。

下面是第三方练习，需要安装兼容版本 NumPy 后手动调用；本轮仅检查语法：

```python
def inspect_array_semantics():
    import numpy as np
    source = np.arange(6).reshape(2, 3)
    view = source[:, :2]
    selected = source[:, [0, 2]]
    assert np.shares_memory(source, view)
    assert not np.shares_memory(source, selected)
    offset = np.array([10, 20, 30])
    assert (source + offset).shape == (2, 3)
    try:
        bool(source)
    except ValueError:
        pass
    else:
        raise AssertionError("多元素数组的真值有歧义")
```

数组条件用元素级比较和明确的 `any` / `all`；复合条件通常用带括号的 `&` / `|`，不要照搬标量 `and` / `or`。向量化改变执行位置，但是否更快仍取决于数据规模、拷贝、dtype 和内存带宽。

## 18.2 pandas：表格、缺失值与聚合

```python
def pandas_demo():
    import pandas as pd
    frame = pd.DataFrame({"user": ["A", "A", "B"], "amount": [10, 20, 30]})
    grouped = frame.groupby("user", as_index=False)["amount"].sum()
    assert grouped.set_index("user")["amount"].to_dict() == {"A": 30, "B": 30}
    filtered = frame.loc[frame["amount"] >= 20, ["user", "amount"]]
    assert len(filtered) == 2
```

DataFrame 有索引、列类型与缺失值规则；操作可能按索引对齐，而不是简单按位置逐项计算。区分 `loc` 标签访问和 `iloc` 位置访问。不要把大数据处理写成逐行 Python 循环，先评估向量化、分块和数据库聚合。[pandas 官方教程](https://pandas.pydata.org/docs/getting_started/intro_tutorials/)。

### 表格操作的错误经常来自索引对齐

Series 的运算可以按标签对齐，两个长度相同的序列并不一定按位置相加。缺失值也有多种表示和 dtype 规则；不能使用 `value == NaN` 判断缺失，应使用库提供的缺失判断。

```python
def inspect_alignment():
    import pandas as pd
    left = pd.Series([10, 20], index=["A", "B"])
    right = pd.Series([1, 2], index=["B", "A"])
    assert (left + right).to_dict() == {"A": 12, "B": 21}
    data = pd.DataFrame({"name": ["A", "B"], "score": [10, None]})
    assert data["score"].isna().tolist() == [False, True]
    data.loc[data["name"] == "A", "score"] = 15
    assert data.loc[0, "score"] == 15
```

本例只检查语法。不同 pandas 版本的复制和 Copy-on-Write 行为可能不同，避免基于旧经验依赖链式赋值。明确用 `.loc[条件, 列] = 值`，升级时查看所用版本文档。把数据库里可以聚合过滤的工作移到 Python 之前，应先比较数据传输与内存成本。

## 18.3 可视化与数值计算

Matplotlib 适合静态图，Plotly 常用于交互图，SciPy 提供科学算法。以下示意需要 Matplotlib，执行会写出图片：

```python
def draw(output_path):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [10, 15, 12], marker="o")
    ax.set(xlabel="Day", ylabel="Orders", title="Order trend")
    fig.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close(fig)
```

中文字体需要明确配置；图形正确性要检查单位、坐标范围、缺失值和聚合口径。机器学习的 scikit-learn、PyTorch 等属于独立专业领域，需要数据划分、评估、防泄漏与部署知识，不能用一段 fit 代码代表完整掌握。

## 18.4 FastAPI：类型模型与请求边界

保存成单独 `app.py`，安装 `fastapi`、`uvicorn` 后，手动用 `python -m uvicorn app:app --host 127.0.0.1 --port 8000` 启动：

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class TaskInput(BaseModel):
    title: str = Field(min_length=1, max_length=200)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/tasks", status_code=201)
def create_task(data: TaskInput):
    title = data.title.strip()
    if not title:
        raise HTTPException(status_code=422, detail="标题不能仅为空白")
    return {"title": title}  # 只示范校验，不持久化
```

async 路由内使用异步驱动或适当地移交阻塞工作；把普通数据库调用放进 async def 不会变为非阻塞。实际项目补鉴权、请求级事务、统一错误和生命周期资源管理。[FastAPI 官方首个应用](https://fastapi.tiangolo.com/tutorial/first-steps/)。

### 从演示 API 到可验证接口

上面的 POST 只返回规范化标题，没有数据库写入；201 只是教学响应，不证明一个真正持久化任务已创建。完整接口需要规定请求和响应 schema、错误码、请求事务和重复提交语义。

练习时先为纯业务函数测试正常标题、空白、长度边界，再对 HTTP 层测试 JSON 解析、422 映射和响应结构。应用 lifespan 适合管理共享客户端和连接池；每个请求取得自己的工作单元，不把全局会话作为所有请求共享事务。

第三方包安装范围应按项目保存，框架、数据校验库、ASGI 服务器版本需要一起验证。本书没有启动 FastAPI 服务，也没有运行其 TestClient；不要把下方学习步骤记作已执行结果。它们属于进一步环境练习。

## 18.5 模板、GUI 与事件驱动

模板引擎把数据渲染为 HTML，必须保留合适的自动转义。GUI 可以从标准库 tkinter 开始；某些 Python 分发未包含 Tk 组件。下面需要图形桌面，调用 gui_demo 才会打开窗口：

```python
def gui_demo():
    import tkinter as tk
    root = tk.Tk()
    root.title("Python 学习")
    label = tk.Label(root, text="点击按钮")
    label.pack(padx=20, pady=10)
    tk.Button(root, text="问候", command=lambda: label.config(text="你好，Python")).pack(pady=10)
    root.mainloop()
```

GUI 主循环与 asyncio 都强调不要在事件线程里长时间阻塞；后台线程更新界面须遵守框架线程规则。海龟绘图 turtle 是教学绘图入口，不是通用企业 UI 框架。

## 18.6 图像、Excel、文档与自动化

Pillow 处理像素图，openpyxl 处理 xlsx，python-docx 处理 docx；这些不是标准库，也不保证百分之百保留所有 Office 功能。Pillow 示例只创建自己的新图片：

```python
def create_image(output_path):
    from PIL import Image, ImageDraw
    with Image.new("RGB", (300, 120), "white") as image:
        ImageDraw.Draw(image).text((20, 40), "Python", fill="black")
        image.save(output_path)
```

批量自动化通常先做文件清单、dry-run、可恢复输出，再处理异常与重试。浏览器自动化应基于明确选择器与状态，不能只依赖固定 sleep；定时任务还需防重复运行和记录最后处理进度。

## 18.7 邮件、MIME 与认证

标准库 email 负责构造邮件，smtplib 负责发送；下面只构造，不发送：

<!-- verify: run -->
```python
from email.message import EmailMessage
message = EmailMessage()
message["Subject"] = "Python 学习进度"
message["From"] = "learner@example.com"
message["To"] = "reader@example.com"
message.set_content("已经学到生成器。")
message.add_alternative("<p>已经学到<strong>生成器</strong>。</p>", subtype="html")
assert message.is_multipart()
assert "Subject:" in message.as_string()
```

真实发送需要服务商要求的 TLS、认证和授权；不把口令写入源码。接收侧常见 IMAP / POP，需处理 MIME、多编码、附件大小与不可信内容。分布式任务队列、邮件发送重试还涉及幂等和外部副作用。

## 18.8 原生扩展、FFI 与嵌入

性能瓶颈可通过算法、批处理、NumPy、Cython、Rust / C 扩展或 ctypes / cffi 改善。FFI 的参数类型、内存所有权和 ABI 不匹配会造成进程崩溃，不再只是普通 Python 异常。

<!-- verify: run -->
```python
import ctypes
class Header(ctypes.Structure):
    _fields_ = [("kind", ctypes.c_uint16), ("length", ctypes.c_uint32)]

header = Header(1, 100)
assert header.kind == 1 and header.length == 100
print(ctypes.sizeof(Header))  # 含平台对齐，不能当成固定网络布局
```

网络数据优先用 struct 明确字节序和布局。构建原生 wheel 要考虑平台、编译器、Python ABI、依赖动态库与自由线程兼容；本章只是入口，不包含完整 C API 教程。

## 18.9 Python 3.14：模板字符串与注解反射

模板字符串 `t"..."` 得到 Template 对象，保留静态片段和插值信息，不直接得到 str。需要渲染器决定编码规则；模板语法本身不自动完成 HTML / SQL 安全处理。

<!-- verify: run -->
```python
name = "张三"
template = t"你好，{name}!"
assert template.strings == ("你好，", "!")
assert template.interpolations[0].value == "张三"
assert template.interpolations[0].expression == "name"
```

3.14 的 annotationlib 提供注解反射选项，例如获取字符串表示，减少必须立即解析前向引用的场景：

<!-- verify: run -->
```python
from annotationlib import get_annotations, Format

def save(value: UnknownAtRuntime) -> None:
    pass

annotations = get_annotations(save, format=Format.STRING)
assert annotations["value"] == "UnknownAtRuntime"
```

仍不要把读取任意不可信对象注解当成绝对无执行风险。参考 [templatelib](https://docs.python.org/3.14/library/string.templatelib.html)、[annotationlib](https://docs.python.org/3.14/library/annotationlib.html)。

## 18.10 更新版本与知识边界

新版 Python 还可能增加内置类型、标准模块或更改弃用行为。升级时先读对应 What's New、迁移说明与依赖兼容矩阵，再在目标解释器验证，而不是只修改 requires-python。本教程主体按 3.14 运行环境编写，不把其他版本 API 混入通用示例。

更深入的专门方向包括：解释器字节码与 AST、编译器前端、子解释器、分布式系统、数值算法、数据工程、机器学习、GUI 框架、嵌入式开发。语言基础掌握后应按目标深入，而不是把所有第三方库都当成 Python 语法的一部分。

### 选生态工具时先写出可验收需求

| 目标 | 首先确定 | 验证方式 |
|---|---|---|
| HTTP API | 同步或异步驱动链、请求量、认证授权 | 请求集成测试与部署压测 |
| 数据清洗 | 输入规模、缺失值、dtype、可容忍内存 | 小样本对照、大样本内存与速度 |
| Office 自动化 | 公式、图表、宏、模板保真要求 | 打开生成文件并检查内容和布局 |
| GUI | 目标平台、主循环、后台工作线程规则 | 真实桌面交互与退出测试 |
| 原生扩展 | 瓶颈证据、ABI、所有权和目标平台 | 构建矩阵、性能与崩溃测试 |

有 Go 基础时还应考虑是否真的需要进程内 FFI。若已有 Go 服务稳定提供网络 API，通过 HTTP/gRPC 交互可能更容易隔离运行时；FFI 可减少调用开销，但引入 ABI、内存和发布复杂性。选择由测量与部署约束决定。

验收：可以解释一个库为何值得引入、最小依赖是什么、哪里只有语法示例、哪里已经在目标环境验证。不要把“某库流行”作为唯一选型理由，也不要把所有生态专题当作语言入门必修。


---

# 19｜练习、参考答案与迁移陷阱

> 本章目标：把知识变成独立实现与失败验证能力。
>
> 阅读重点：先完成题目，再对照答案；进阶题明确输入矩阵、复杂度和副作用。

先尝试独立实现，再阅读答案。断言是预期行为，实际项目要根据业务补充输入限制、错误策略和测试。

## 19.1 练习一：安全计算

要求：把两个整数字符串解析为整数，返回真除法与整除；非法整数或零除数报清晰错误。

<!-- verify: run -->
```python
def calculate(left, right):
    try:
        a, b = int(left), int(right)
    except ValueError as exc:
        raise ValueError("请输入整数字符串") from exc
    if b == 0:
        raise ValueError("除数不能为零")
    return a / b, a // b

assert calculate("7", "2") == (3.5, 3)
assert calculate("-7", "2") == (-3.5, -4)
try:
    calculate("1", "0")
except ValueError as exc:
    assert "零" in str(exc)
```

## 19.2 练习二：保序去重

要求：对可哈希元素去重，保留首次出现顺序；说明不能直接接受 list 元素的原因。

<!-- verify: run -->
```python
def unique(values):
    seen = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            yield value

assert list(unique([3, 1, 3, 2, 1])) == [3, 1, 2]
```

不可哈希元素需要根据业务提取稳定键，或使用线性相等比较。若元素在参与去重期间改变等价关系，需先明确何时取快照。

## 19.3 练习三：订单金额汇总

要求：金额以十进制字符串输入，按用户汇总并按金额降序、用户升序输出。

<!-- verify: run -->
```python
from collections import defaultdict
from decimal import Decimal

def rank_orders(orders):
    totals = defaultdict(lambda: Decimal("0"))
    for order in orders:
        totals[order["user"]] += Decimal(order["amount"])
    return sorted(totals.items(), key=lambda pair: (-pair[1], pair[0]))

orders = [{"user": "A", "amount": "0.1"}, {"user": "B", "amount": "0.3"}, {"user": "A", "amount": "0.2"}]
assert rank_orders(orders) == [("A", Decimal("0.3")), ("B", Decimal("0.3"))]
```

### 进阶要求：坏数据不能静默参与汇总

原答案假定订单结构可信，只演示 Decimal 聚合和排序。面向外部数据时，应补充：订单必须是映射、user 必须为非空字符串、amount 必须是有限数、是否允许负数、精度如何处理。把第 02 章金额解析器与第 10 章边界模型结合，再进入聚合。

验收用例：同用户多笔、两个用户金额相同、空输入、缺用户、`"NaN"`、`"Infinity"`、空金额、退款。注意退款是否允许属于业务决定；测试应该固化已决定的规则，而不是在测试中临时猜测。

复杂度分析：假设 n 笔订单、u 个不同用户，单遍汇总通常 O(n)，最终排序 O(u log u)，额外内存 O(u)。不要把“使用生成器读订单”误写成整个程序 O(1) 内存。

## 19.4 练习四：修改与重新绑定

预测以下断言是否成立，再解释每步对象关系：

<!-- verify: run -->
```python
def update(data):
    data["tags"].append("new")
    data = {"tags": []}
    return data

original = {"tags": []}
returned = update(original)
assert original == {"tags": ["new"]}
assert returned == {"tags": []}
assert original is not returned
```

答案：修改共享内层列表影响调用者，后续重新绑定仅改变局部变量。想隔离原对象需要明确深拷贝或不可变建模。

## 19.5 练习五：闭包工厂

要求：创建三个乘法函数，分别乘 0、1、2，避免晚绑定。

<!-- verify: run -->
```python
def make_multiplier(factor):
    def multiply(value):
        return value * factor
    return multiply

functions = [make_multiplier(i) for i in range(3)]
assert [fn(10) for fn in functions] == [0, 10, 20]
```

工厂每次调用创建独立的外层绑定，比依赖循环末值更直观。

## 19.6 练习六：分批消费迭代器

要求：每批至多三个元素；最后不足也返回；不把所有输入一次物化。

<!-- verify: run -->
```python
from itertools import islice

def batches(values, size):
    if size <= 0:
        raise ValueError("size 必须为正")
    iterator = iter(values)
    while batch := tuple(islice(iterator, size)):
        yield batch

assert list(batches(range(7), 3)) == [(0, 1, 2), (3, 4, 5), (6,)]
```

新版本也可查 itertools.batched；这里手写以展示迭代器共享消费。返回 tuple 避免调用者误修改批次结构。

### 进阶答案：参数立即校验、数据延迟消费

题目要求函数调用时就拒绝非法 size，而不是到 next 才报错；同时保持输入惰性。用普通外层函数加内层生成器：

<!-- verify: run -->
```python
from itertools import islice

def checked_batches(values, size):
    if type(size) is not int or size <= 0:
        raise ValueError("size 必须为正整数")
    def generate():
        iterator = iter(values)
        while batch := tuple(islice(iterator, size)):
            yield batch
    return generate()

seen = []
def source():
    for value in range(5):
        seen.append(value)
        yield value

stream = checked_batches(source(), 2)
assert seen == []
assert next(stream) == (0, 1)
assert seen == [0, 1]
assert list(stream) == [(2, 3), (4,)]
for size in [0, -1, True]:
    try:
        checked_batches([], size)
    except ValueError:
        pass
    else:
        raise AssertionError(size)
```

这里立即校验 size，但没有立即调用 iter(values)，所以非法可迭代对象仍可能到消费时才失败。这是明确的边界选择；若要调用时连可迭代性都检查，就把 iter 移到外层，并解释它可能触发用户对象逻辑。

## 19.7 练习七：只对指定失败重试

要求：最多三次；只有明确的瞬态异常才重试；最后一次保留原异常。示例不 sleep，以便验证。

<!-- verify: run -->
```python
from functools import wraps

class TemporaryFailure(Exception):
    pass

def retry(attempts):
    if attempts < 1:
        raise ValueError("attempts 必须为正")
    def decorate(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            for attempt in range(attempts):
                try:
                    return fn(*args, **kwargs)
                except TemporaryFailure:
                    if attempt == attempts - 1:
                        raise
        return wrapper
    return decorate

calls = []
@retry(3)
def unstable():
    calls.append(1)
    if len(calls) < 3:
        raise TemporaryFailure("稍后重试")
    return "ok"

assert unstable() == "ok" and len(calls) == 3
```

生产应增加退避、抖动、总时限和幂等约束；不要对所有 Exception 无差别重试。异步版本要用 asyncio.sleep 并正确传播取消。

## 19.8 练习八：校验输入模型

要求：输入必须为 dict，id 必须是非 bool 的正整数，name 必须是非空字符串。

<!-- verify: run -->
```python
def parse_user(value):
    if not isinstance(value, dict):
        raise ValueError("必须为对象")
    uid, name = value.get("id"), value.get("name")
    if type(uid) is not int or uid <= 0:
        raise ValueError("id 必须为正整数")
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name 必须为非空字符串")
    return {"id": uid, "name": name.strip()}

assert parse_user({"id": 1, "name": " A "}) == {"id": 1, "name": "A"}
try:
    parse_user({"id": True, "name": "A"})
except ValueError:
    pass
else:
    raise AssertionError("不能接受 bool ID")
```

这里精确 type 检查是刻意拒绝 bool；其他场景未必需要拒绝所有 int 子类，按业务契约决定。

## 19.9 练习九：资源异常后仍释放

要求：业务抛错后仍执行清理，并且原异常继续传播。

<!-- verify: run -->
```python
from contextlib import contextmanager
events = []
@contextmanager
def resource():
    events.append("open")
    try:
        yield "handle"
    finally:
        events.append("close")

try:
    with resource() as handle:
        assert handle == "handle"
        raise ValueError("business failed")
except ValueError:
    pass
assert events == ["open", "close"]
```

## 19.10 练习十：异步并发上限

要求：同时进入业务区的任务不超过两个，并保留输入结果顺序。

<!-- verify: run -->
```python
import asyncio

async def main():
    semaphore = asyncio.Semaphore(2)
    active = peak = 0
    async def work(value):
        nonlocal active, peak
        async with semaphore:
            active += 1
            peak = max(peak, active)
            try:
                await asyncio.sleep(0.001)
                return value * 10
            finally:
                active -= 1
    results = await asyncio.gather(*(work(n) for n in range(6)))
    assert results == [0, 10, 20, 30, 40, 50]
    assert peak == 2 and active == 0

asyncio.run(main())
```

此答案用于有限小任务集；百万输入应改为有界队列和固定 worker，避免预先创建全部 Task。

## 19.11 练习十一：综合项目扩展题

1. 添加 `rename id title`：复用标题校验、参数化 UPDATE、保持事务边界。
2. 添加 `export path`：用 csv.writer，明确是否允许覆盖、字符编码和公式处理。
3. 添加“批量导入”：要求任一条非法时整体回滚；另设计部分成功模式并清晰返回逐条结果。
4. 添加优先级：表约束、模型、排序、迁移、旧数据默认值一起修改。
5. 改为多用户：每个查询和写入都带 tenant / owner 边界，不能只在列表查询过滤。

参考设计：业务服务解析完整批次后开启事务，仓储方法不自行提交；输出和文件写入在提交前后如何协调需要明确。跨数据库与文件的原子性不是普通 with 能自动保证。

### 参考答案 A：批量输入任一非法则整体回滚

为使代码块独立运行，下面使用内存 SQLite 表，演示与第 17 章相同的业务事务思想；它没有给现有 CLI 自动增加 import 子命令。要求输入为一批标题，失败后此前写入也撤销，成功后一次提交。

<!-- verify: run -->
```python
import sqlite3
from contextlib import closing

def import_titles(connection, titles):
    if connection.in_transaction:
        raise ValueError("调用者必须交出空闲连接")
    connection.execute("BEGIN")
    created = []
    try:
        for number, title in enumerate(titles, 1):
            if not isinstance(title, str) or not 1 <= len(title.strip()) <= 200:
                raise ValueError(f"记录 {number} 标题非法")
            cursor = connection.execute(
                "INSERT INTO tasks(title) VALUES (?)", (title.strip(),)
            )
            created.append(cursor.lastrowid)
        connection.commit()
    except BaseException:
        connection.rollback()
        raise
    return created

# isolation_level=None 关闭旧模式中的隐式 BEGIN；事务由上面的 SQL 明确开启。
with closing(sqlite3.connect(":memory:", isolation_level=None)) as connection:
    connection.execute("CREATE TABLE tasks(id INTEGER PRIMARY KEY, title TEXT NOT NULL)")
    try:
        import_titles(connection, iter(["first", " "]))
    except ValueError as exc:
        assert "记录 2" in str(exc)
    else:
        raise AssertionError("非法批次必须失败")
    assert connection.execute("SELECT COUNT(*) FROM tasks").fetchone()[0] == 0
    ids = import_titles(connection, [" A ", "B"])
    assert len(ids) == 2
    assert connection.execute("SELECT title FROM tasks ORDER BY id").fetchall() == [("A",), ("B",)]
```

选择流式写入会把解析时间也放进事务窗口，可能长期占用锁；先全部解析会占内存。大批量任务需要在“整体原子性、锁时长、内存上限”之间作具体设计，不存在只加一个 generator 就全满足的方案。连接提交失败的结果也应按驱动和错误类型处理，不能把所有提交错误都解释为一定未提交。

### 参考答案 B：稳定 ID 的游标分页

要求：按 ID 升序，从上页最后 ID 之后读取，不用 OFFSET；空结果表示本次没有更多记录。示例模型假定 ID 在遍历期间具有所需稳定性，真实并发业务需另定义快照和插入可见性。

<!-- verify: run -->
```python
import sqlite3
from contextlib import closing

def page_after(connection, after_id, limit):
    if type(after_id) is not int or after_id < 0:
        raise ValueError("after_id 必须为非负整数")
    if type(limit) is not int or not 1 <= limit <= 100:
        raise ValueError("limit 必须为 1..100")
    return connection.execute(
        "SELECT id, title FROM tasks WHERE id > ? ORDER BY id LIMIT ?",
        (after_id, limit),
    ).fetchall()

with closing(sqlite3.connect(":memory:")) as connection:
    connection.execute("CREATE TABLE tasks(id INTEGER PRIMARY KEY, title TEXT)")
    with connection:
        connection.executemany("INSERT INTO tasks VALUES (?, ?)", [(1, "A"), (3, "B"), (9, "C")])
    first = page_after(connection, 0, 2)
    second = page_after(connection, first[-1][0], 2)
    assert first == [(1, "A"), (3, "B")]
    assert second == [(9, "C")]
    assert page_after(connection, second[-1][0], 2) == []
```

游标分页不承诺随机跳到第 100 页；排序字段可能更新时会出现另一类一致性问题。对外游标还应包含查询条件、排序规则或版本等信息，避免用户把某次查询的游标混到另一查询。

### 参考设计 C：重命名与多租户

重命名按“解析 ID → 规范化并校验标题 → 参数化 UPDATE → 检查是否存在 → 提交 → 序列化”实现。测试包含空白标题、200/201 长度、目标不存在、SQL 片段和回滚。

多租户不能只给 list 加过滤：get、done、delete、rename、批量写入和唯一约束都需要 tenant 边界。服务应从可信认证上下文取得 tenant，不直接信任请求体中的 tenant 字段。跨租户目标通常按未找到或明确权限策略处理，避免返回其他租户的数据。

## 19.12 Go 迁移陷阱清单

| 误解 | 应用中的正确认识 | 示例位置 |
|---|---|---|
| int 是固定 64 位 | Python int 可增长；外部格式仍有限制 | 02.3 |
| 整数除法向零截断 | `//` 向负无穷取整 | 01.8 |
| list 切片共享底层数组 | 普通 list 切片复制外层 | 03.3 |
| 元组里一切都不能变 | 引用不能替换，被引用对象可变 | 02.2 |
| dict 无序 | Python 3.7+ 保留插入顺序 | 03.1 |
| set 输出顺序可以依赖 | 没有顺序契约 | 03.7 |
| `and` / `or` 返回 bool | 返回操作数 | 01.9 |
| 默认列表每次新建 | 定义时求值，调用共享 | 05.3 |
| 循环创建 lambda 自动保存 i | 闭包晚绑定 | 05.7 |
| 注解等于编译器强制类型 | 主要依赖静态工具 | 10.1 |
| `__field` 是强制 private | 名称改写，不是安全控制 | 08.3 |
| 同名 def 按参数重载 | 后定义覆盖先定义 | 08.6 |
| super 固定调父类 | 沿 MRO 找下一个 | 08.10 |
| 装饰器只是元数据标签 | 会执行并重新绑定函数 / 类名称 | 05.9 |
| GIL 让业务线程安全 | 仍需锁保护复合不变量 | 14.3 |
| async 调用立即运行 | 得到 coroutine，需 await / 调度 | 14.7 |
| 超时等于工作已停止 | 线程和远程请求可能仍在执行 | 14.5、15.1 |
| with sqlite_connection 会 close | 事务上下文不自动关闭连接 | 15.7 |
| `is` 可比较字符串值 | 值用 `==`，身份用 `is` | 02.1 |
| assert 永远执行 | 优化模式可能移除 | 04.9 |
| 任意异常吞掉就稳定 | 应保留故障证据并在边界处理 | 11 |

### Python 易混点总表：先预测，再定位对应原理

每行给出一个需要区分的概念对；“阅读位置”中的数字是本书节号。详细规则和可执行反例已放回相应章节，避免把所有解释塞成一张背诵表。

| 易混概念 | 必须记住的区别 | 阅读位置 |
|---|---|---|
| 名称 / 对象 / 引用 | 重新绑定不修改原对象；原地修改影响别名 | 2.1、5.5 |
| `is` / `==` | 身份与相等协议；不靠驻留比较字符串 | 2.1、9.2 |
| del / 销毁 / close | 解除绑定、内存回收、资源关闭各自独立 | 2.1、9.8、11.6 |
| 不可变 / 可哈希 | 元组含 list 仍不可哈希；身份型可变对象可能可哈希 | 2.10、9.2 |
| 浅拷贝 / 深拷贝 / 赋值 | 外层复制、对象图复制、共享原对象 | 2.9 |
| `+=` / `+` | 原地协议可能先修改再在写回时失败 | 2.2 |
| `/` / `//` / int | 真除、向下取整、转换时向零截断 | 2.3 |
| bool / int | bool 是 int 子类，相等键可能合并 | 2.3、2.10 |
| float / Decimal / Fraction | 表示与精度不同；从 float 转换不能补回原意 | 2.4 |
| round / 业务舍入 | 偶数舍入和浮点表示不能代替明确金额规则 | 2.4、21.14 |
| None / 空值 / 未提供 | 三者可能有不同业务含义，用哨兵区分 | 4.1、5.3 |
| str / bytes / bytearray | 文本码点、不可变字节、可变字节 | 2.5、2.8 |
| 字符 / 码点 / 字节 | 屏幕字符数、len(str)、编码长度不等价 | 2.5 |
| 原始字符串 / 普通字符串 | r 改变字面量转义，不改变字符串类型 | 1.5、2.6 |
| strip / removeprefix | 删两端字符集合与删指定前缀 | 2.6 |
| 单索引 / 切片 | 越界错误与边界截断；反向步长另算 | 3.3 |
| append / extend / `+` | 加一元素、逐项扩展、创建新列表 | 3.2、3.9 |
| sort / sorted | 原地返回 None 与返回新列表 | 3.9 |
| get / setdefault / defaultdict | 是否插入，何时求默认值 | 3.6 |
| dict.fromkeys / 推导式 | 同一个默认对象与每次创建新对象 | 3.4、3.6 |
| 视图 / 快照 / 深不可变 | 只读访问不保证底层数据不再改变 | 3.6、8.9 |
| and/or / bool | 返回短路操作数，不一定返回布尔 | 4.1 |
| 循环 else / try else | 没有 break 与 try 正常到末尾 | 4.4、11.2 |
| match 捕获 / 常量 | 裸名称绑定，限定名称才是值模式 | 4.7 |
| 默认参数 / 调用实参 | 定义时求值与每次调用求值 | 5.3 |
| 参数解包 / 覆盖字典键 | 调用重复关键字会错，字典构造可覆盖 | 5.4 |
| global / nonlocal | 当前模块名称与外层函数已有名称 | 5.6 |
| 类体 / 方法作用域 | 普通方法裸名称不沿类字典查找 | 5.6 |
| 闭包晚绑定 / 默认参数捕获 | 读共享单元与定义时保存对象 | 5.7 |
| 装饰器求值 / 应用 / 调用 | 三个时间点、两种不同顺序 | 5.10 |
| Iterable / Iterator | 可产生迭代器与保存一次消费进度 | 6.1 |
| 生成器函数 / 生成器表达式 | 函数体延迟与最外层 iterable 立即求值 | 6.3、6.4 |
| yield / return / yield from | 交付元素、结束携带结果、协议委托 | 6.5、6.6 |
| groupby / 全局分组 | 只分相邻段，旧组共享底层输入 | 6.8 |
| import / from import | 模块引用与当时属性对象绑定 | 7.1 |
| 工作目录 / 源文件目录 / 包上下文 | 文件定位、模块搜索、相对导入规则不同 | 7.3、7.4 |
| venv / 隔离模式 / 安全沙箱 | 包位置与搜索路径隔离都不是权限沙箱 | 1.2、7.8 |
| 实例属性 / 类属性 | 遮蔽与共享，另受描述符优先级影响 | 8.2、9.4 |
| 实例方法 / classmethod / staticmethod | 隐式接收实例、实际调用类或不绑定 | 8.5 |
| 继承 / super / MRO | super 沿当前实例 MRO 继续，不固定父类 | 8.10 |
| `__new__` / `__init__` | 创建/返回对象与初始化对象 | 9.6 |
| property / cached_property | 描述符访问与实例字典缓存，线程行为不同 | 9.5、22.7 |
| getattr / getattribute / getattr_static | 失败回退、一般访问入口、静态检查 | 9.4、21.6 |
| 数据 / 非数据描述符 | 是否提供 set/delete 影响实例字典优先级 | 9.5 |
| 实例特殊属性 / 隐式特殊方法 | 直接属性访问与从类型查协议不同 | 9.3 |
| NotImplemented / NotImplementedError | 运算协商返回值与异常 | 9.2 |
| frozen / slots / Final | 字段赋值限制、实例布局、静态声明 | 8.9、9.8、10.9 |
| Enum 名称 / 值 / 成员 | `E[name]`、`E(value)` 与成员对象 | 8.9 |
| 类型提示 / 验证 / 转换 | 静态契约、检查输入、构造新值 | 10.1、10.6 |
| Any / object | 放宽检查与要求使用前收窄 | 10.3 |
| Optional / 默认参数 / NotRequired | 值可为 None、参数可省、键可缺 | 10.2、10.6 |
| TypedDict / dataclass | 普通字典结构提示与生成类方法 | 8.8、10.6 |
| cast / TypeGuard / TypeIs | 静态断言与不同收窄关系 | 10.7 |
| overload / singledispatch | 静态签名与运行时类型分派 | 10.7 |
| 延迟注解 / 字符串注解 | 3.14 默认机制与 future 行为不同 | 10.10 |
| Exception / BaseException | 普通失败与中断、退出、取消信号 | 11.1、14.9 |
| raise / raise from / from None | 传播、显式原因、隐藏上下文显示 | 11.3 |
| except / except* | 整个异常对象与异常组匹配部分 | 11.5 |
| with / 事务 | 管理退出，不自动撤销所有副作用 | 11.6、15.7 |
| enter 失败 / 块内失败 | 前者不会自动调用同一个管理器的 exit | 11.6 |
| 可复用 / 可重入 | 先后进入与嵌套进入 | 11.8 |
| 文本 EOF / None | read 返回空 str/bytes 表示文件尾 | 12.2 |
| flush / fsync / close | 缓冲传递、系统持久化请求、资源关闭 | 12.2 |
| astimezone / replace(tzinfo) | 转换同一时间点与更改标签 | 13.3 |
| 墙上时间 / 单调计时 | 展示时间点与度量超时/耗时 | 13.3 |
| GIL / 锁 / 原子业务操作 | 解释器约束不等于业务状态保护 | 14.2、14.3 |
| Thread.run / start / join | 普通调用、启动、等待结束 | 14.3 |
| Event / Queue / Semaphore | 状态通知、传递项目、并发许可 | 14.3、14.4 |
| 队列空 / join 完成 / 成功 | 未排队、已结算、业务成功各自验证 | 14.4 |
| Future 超时 / cancel / 强制停止 | 等待预算、取消请求、终止工作不等价 | 14.5 |
| spawn / fork / forkserver | 新解释器、状态复制、服务器启动 | 14.6 |
| coroutine / Task / Future | 一次性执行体、调度实体、结果占位 | 14.7 |
| await / 并发 / 并行 | 等待协议不保证切换，更不保证多核 | 14.7 |
| gather / TaskGroup / wait | 结果收集、作用域任务管理、状态等待 | 14.8 |
| timeout / shield / 回滚 | 取消与保护等待任务不撤销外部副作用 | 14.9 |
| 线程锁 / asyncio.Lock | 协调对象与阻塞方式不同 | 14.10 |
| 限并发 / 限速 / 背压 | 在途数量、时间速率、积压容量 | 14.10、22.6 |
| ContextVar / threading.local | 执行上下文与线程隔离 | 14.11 |
| mock 被调用 / 被 await | 创建协程与实际执行需分别断言 | 16.2 |
| assert / 输入校验 | 优化模式可能移除断言 | 4.9、16.8 |
| 代码对象 / 函数对象 / 执行帧 | 代码、绑定环境、一次运行状态 | 22.3 |
| 缓存安全 / 只执行一次 | 容器一致性不禁止并发重复计算 | 22.7 |

建议按 [对象模型](docs/tutorial/02-对象模型与基础类型.md)、[函数与作用域](docs/tutorial/05-函数作用域与装饰器.md)、[对象协议](docs/tutorial/09-协议描述符与元编程.md)、[类型提示](docs/tutorial/10-类型提示与泛型.md)、[并发](docs/tutorial/14-线程进程与异步编程.md) 分组做实验，而不是一次背完。

## 19.13 自测完成标准

能解释对象共享，能独立写带装饰器与类型提示的函数，能实现惰性生成器和资源管理器，能设计事务失败测试，能描述 I/O / CPU 并发模型，能把一个依赖清晰、错误可诊断的工具交付给其他人。达到这些标准后，再按工作目标深入 Web、数据或自动化。

### 逐章验收表

| 章节 | 独立完成的任务 | 通过条件 |
|---|---|---|
| 00 | 选择适合自己的路线 | 能区分语义、工程和生态三个层次 |
| 01 | 定位终端与 IDE 的解释器 | 路径、pip、工作目录证据一致 |
| 02 | 预测共享与异常副作用 | 能解释元组增强赋值的失败后状态 |
| 03 | 分组、去重、排序 | 顺序、缺失值和复杂度均明确 |
| 04 | 解析两种命令结构 | 拒绝 bool ID 和约定不允许的额外键 |
| 05 | 编写异步审计装饰器 | 等待真实工作，异常传播，finally 执行 |
| 06 | 写单遍统计与分批函数 | 一次性输入正确，空输入策略明确 |
| 07 | 建立并安装示例包 | 项目外可运行入口；注明是否实际构建验证 |
| 08 | 设计金额或配置模型 | 相等性、可变性与字段规则清楚 |
| 09 | 解释属性查找 | 区分实例字典、数据描述符和绑定方法 |
| 10 | 解析未知请求为模型 | 注解与运行时校验各自负责什么说得清 |
| 11 | 管理多个资源 | 部分获取失败后已取得资源逆序释放 |
| 12 | 导入 CSV 并保存 JSON | 错误记录可定位，失败不破坏旧文件 |
| 13 | 统计日志并输出结果 | 单位、时间、内存增长来源可说明 |
| 14 | 注入任务失败 | 兄弟任务退出并清理，无悬挂生产者 |
| 15 | 实现事务与客户端错误分类 | 区分传输、状态、格式、业务错误 |
| 16 | 建测试矩阵和性能假设 | 失败路径有断言，性能不作脆弱阈值测试 |
| 17 | 跟踪一次命令完整生命周期 | 明确谁提交、谁关闭、谁输出 |
| 18 | 选择一个生态工具 | 安装前提、数据语义和验收方法明确 |
| 19 | 完成批量回滚和分页 | 参考答案关闭后可以独立重写 |
| 20 | 按症状查权威资料 | 找到对应版本与相关原节 |
| 21 | 解释惰性内置函数 | 知道消费多少输入、何时抛错 |
| 22 | 设计缓存与有界流水线 | 明确大小、生命周期、失败与一致性 |

练习评分可以按四项自评：结果正确、边界明确、资源退出正确、解释清晰。只有正常输入成功而没有失败后状态证据，不能算工程练习完成。

### 基础语义综合自测与答案

先遮住答案，用“何时执行、共享谁、谁清理”说明理由，再运行对应章节的断言。

| 题目 | 答案与原因 | 实验位置 |
|---|---|---|
| `items=[[]]*3` 后改 `items[0]`，只影响第一个吗？ | 三个槽指同一内层列表；用推导式逐次构造 | 3.4 |
| `d.get('exists', expensive())` 会调用 expensive 吗？ | 会，函数调用前先求实参 | 3.6 |
| 方法中裸写类体定义的 x，会先读类属性吗？ | 普通方法不会；显式用 self.x 或类限定名 | 5.6 |
| 生成器表达式的 source() 会延迟到 next 才运行吗？ | 最左侧 iterable 表达式立即求值 | 6.4 |
| dataclass frozen 内部列表能 append 吗？ | 可以；frozen 不递归冻结字段值 | 8.9 |
| 给实例赋 `__len__`，len(instance) 一定改变吗？ | 不会按普通实例字典规则读取隐式协议 | 9.3 |
| cast(int, '1') 的结果能直接与整数相加吗？ | 不能，原对象仍为 str | 10.7 |
| return 一个列表后 finally append，调用者能看见吗？ | 能，返回对象已经选定但仍可修改 | 11.2 |
| queue.join 返回说明所有项目成功吗？ | 只说明未完成计数归零 | 14.4 |
| 线程 Future 超时后离开 with 会立刻返回吗？ | 不保证；线程池退出仍可能等待工作 | 14.5 |
| 同一个 coroutine 能 await 两次吗？同一个 Task 呢？ | 原生协程不能重复驱动完成；Task 可重复取结果 | 14.7 |
| asyncio 单线程就没有读改写竞争吗？ | await 分开关键操作即可发生交错 | 14.10 |
| ContextVar 中放 list，就得到任务私有 list 吗？ | 复制绑定并不深拷贝列表 | 14.11 |
| 缓存函数返回 list，调用者修改后下次命中会怎样？ | 其他调用者能看到同一个缓存对象被修改 | 22.7 |

完成标准：至少能独立写出一次失败路径实验，并断言最终状态；能分别说明语言保证、CPython 现象、目标版本限定和未验证环境。只会复述术语不足以解释真实程序。


---

# 20｜知识点索引与参考资料

> 本章目标：按问题和版本查阅权威资料。
>
> 阅读重点：使用症状索引寻找原节；区分本轮已读取页面、未获取正文与未执行环境。

## 20.1 语言核心索引

| 知识点 | 对应章节 |
|---|---|
| 解释器、REPL、脚本、命令行、退出码 | 01、07、13、17 |
| 标识符、缩进、注释、docstring、字面量 | 01、02 |
| 表达式、赋值、增强赋值、海象、解包 | 01—05 |
| 数学、比较、逻辑、位运算、身份、成员运算 | 01—03、21 |
| int、float、complex、bool、None | 02 |
| str、bytes、bytearray、memoryview、Unicode | 02、12 |
| list、tuple、range、dict、set、frozenset | 03 |
| 下标、切片、排序、推导式、容器复杂度 | 03 |
| 条件、循环、break / continue / else、match | 04 |
| 函数、所有参数类型、默认值、注解 | 05、10 |
| LEGB、global / nonlocal、闭包、递归 | 05 |
| 高阶函数、lambda、partial、装饰器、缓存 | 05 |
| Iterable、Iterator、generator、yield from | 06 |
| 模块、包、import、初始化、循环导入 | 07 |
| venv、pip、pyproject、wheel、sdist | 01、07 |
| 类、实例、属性、继承、super、ABC、Enum | 08 |
| dataclass、NamedTuple、frozen、slots | 08 |
| 特殊方法、描述符、反射、元类、弱引用 | 09 |
| 泛型、Protocol、TypedDict、类型收窄、方差 | 10 |
| 异常传播、链、ExceptionGroup、with | 11 |
| 文件、临时文件、序列化、二进制与归档 | 12 |
| 时间、正则、日志、CLI、系统、数学与密码工具 | 13 |
| 线程、进程、队列、锁、GIL、asyncio、取消 | 14 |
| URL、HTTP、TCP / UDP / TLS、数据库、Web 协议 | 15 |
| 测试、mock、调试、性能、内存、安全、部署 | 16 |
| 完整业务 CLI、事务边界、真实测试 | 17 |
| 数据、Web、GUI、邮件、自动化、原生扩展 | 18 |
| t-string、annotationlib、版本兼容 | 00、10、18 |
| 内置函数逐类示例与异步协议 | 21 |
| AST、字节码、插件、项目设计与高级边界 | 22 |

### 从故障现象定位知识点

| 现象 | 优先检查 | 本书位置 |
|---|---|---|
| IDE 能 import，终端找不到包 | 实际解释器、pip 路径、启动目录、src 安装 | 01.2、07.4—7.7 |
| 修改副本影响原数据 | 复制层次、嵌套别名、视图 | 02.9、03.3、18.1 |
| 元组操作抛错后列表仍变了 | 增强赋值的步骤与局部副作用 | 02.2 |
| 缓存数据被别的请求改掉 | 可变返回值共享、缓存键与生命周期 | 05.11、22.7 |
| 局部赋值前读取报错 | 名称在函数体中的绑定判定 | 05.6 |
| 函数返回后读文件报已关闭 | 惰性消费晚于资源释放 | 06.9 |
| 装饰器计时几乎为零 | 只计时创建 coroutine，没有 await | 05.10、14.7 |
| 实例属性读到意外值 | 数据描述符、property、MRO | 09.4—9.5 |
| 注解写 int 仍收到字符串 | 运行时未做边界解析 | 10.1、10.6 |
| with 结束连接仍未关闭 | 连接事务上下文与资源上下文不同 | 15.7 |
| 并发任务内存不断增大 | 任务数、队列与结果分别是否有界 | 14.10、22.6 |
| worker 抛错后主程序挂住 | 生产者仍 put、停止信号和取消传播 | 14.4、14.8、22.6 |
| API 超时但任务已创建 | 远程副作用与响应丢失 | 14.9、17.5 |
| 新包本地成功、安装后失败 | wheel 缺文件或依赖源码工作目录 | 07.7 |
| JSON 解析成功但行为错误 | 重复键、NaN、字段和业务约束 | 10.6、12.4 |

查阅时先定位概念，不只搜索异常名称。相同 TypeError 可以来自参数绑定、类型协议、描述符或错误数据；最后一个异常消息通常只描述直接失败点，还需要结合调用栈和资源状态。

### 对照 Python 官网教程的基础覆盖表（2026-10-26）

本次以官网教程作为主线，再用语言参考、HOWTO 和标准库参考补齐教程有意略写的对象协议、类型提示与并发。以下“覆盖”指教材主题已讲解且有例子或明确交叉引用，不表示逐项复制所有标准库 API。

| 官网教程主题 | 本项目阅读位置 | 本次核对重点 |
|---|---|---|
| 课前说明、解释器使用 | 00、01 | 语言与实现、版本、命令与启动上下文 |
| 数字、文本、列表 | 02、03 | 身份与相等、精度、编码、共享与切片 |
| 控制流与函数定义 | 04、05 | 短路、else、模式捕获、参数绑定、作用域 |
| 数据结构 | 03、06、21 | 原地操作、默认值、迭代、排序与消费 |
| 模块和包 | 07 | import 缓存、相对导入、模块入口、文件路径 |
| 输入输出 | 02.7、12、13 | 格式化、文本/字节流、JSON、资源所有权 |
| 错误和异常 | 11 | 传播、异常链、异常组、with 与清理 |
| 类 | 08、09 | 名称空间、继承、MRO、描述符与绑定 |
| 标准库简介两部分 | 12、13、16、21 | 文件、CLI、时间、正则、日志、测试、弱引用、线程 |
| 虚拟环境和包 | 01.2、07 | 解释器归属、依赖位置、安装与导入区别 |
| 后续学习与交互补充 | 00、01.3、20 | 用 help/dir/官方索引继续查阅 |
| 浮点算术 | 02.4、19.3、21.14 | 二进制误差、近零容差、NaN 与舍入 |
| 附录中的交互启动 | 01.3、07.4、21.9 | REPL 与脚本环境不同，不作为生产入口依赖 |

主线来源：[官方 3.14 教程目录](https://docs.python.org/3.14/tutorial/index.html)。基础阶段可完整学习 01—14、16、19—22 中的语言与标准库主题；15 章只选 urllib/socket/sqlite3，18 章只选 Python 运行时特性。已有框架示例属于历史扩展内容，不是本次基础补全的前置知识。

## 20.2 关键字导航

| 类别 | 语法与示例位置 |
|---|---|
| 字面常量 | True / False / None：01、02 |
| 逻辑与比较 | and / or / not / is / in：01、03 |
| 分支 | if / elif / else：04；match / case（软关键字）：04 |
| 循环 | for / while / break / continue：04 |
| 函数与作用域 | def / return / lambda / global / nonlocal：05 |
| 类 | class：08；super 是内置函数，不是关键字 |
| 模块 | import / from / as：07；as 也用于 with 和模式捕获 |
| 异常 | try / except / finally / raise / assert：04、11 |
| 资源 | with：11 |
| 生成器 | yield：06 |
| 异步 | async / await：14、21 |
| 其他语句 | pass / del：01、04 |
| 软关键字 | type 的类型别名：10；`_` 的模式通配：04 |

软关键字只在特定语法位置特殊，不能套用“任何位置都不能命名”的规则。可用 keyword.kwlist / softkwlist 检查当前解释器，示例见 21。

## 20.3 标准库按任务查阅

| 任务 | 常见模块 | 本教程示例 |
|---|---|---|
| 路径、文件与复制 | pathlib、os、shutil、tempfile、glob | 12、13 |
| 文本与正则 | re、string、textwrap、unicodedata、difflib | 02、13、21 |
| 容器、算法与函数式 | collections、heapq、bisect、array、itertools、functools、operator | 05、06、13 |
| 数值与统计 | math、decimal、fractions、statistics、random | 02、13 |
| 日期时间 | datetime、time、calendar、zoneinfo | 13、21 |
| 数据交换 | json、csv、tomllib、configparser、pickle、struct | 12、21 |
| 压缩与归档 | gzip、bz2、lzma、zipfile、tarfile | 12、21 |
| 进程与并发 | threading、queue、multiprocessing、concurrent.futures、asyncio、contextvars | 14 |
| 网络 | socket、ssl、urllib、http、ipaddress、email、smtplib、imaplib | 15、18、21 |
| 数据库 | sqlite3 | 15、17 |
| 工程支持 | argparse、logging、unittest、doctest、pdb、traceback、warnings | 13、16、21 |
| 性能与内存 | timeit、cProfile、pstats、tracemalloc、gc、weakref | 09、16 |
| 类型与反射 | typing、types、inspect、dataclasses、enum、abc、annotationlib | 08—10、18 |
| 导入与分发元数据 | importlib、importlib.resources、importlib.metadata、venv、ensurepip | 01、07、22 |
| 元编程与运行时 | ast、dis、sys、builtins、keyword | 09、21、22 |
| 认证辅助与编码 | secrets、hashlib、hmac、base64、uuid | 12、13 |

以上是常用领域索引，不承诺逐个讲解标准库每个函数。完整 API 请使用 [对应版本标准库参考](https://docs.python.org/3.14/library/index.html)。偏门模块、平台专用模块和弃用接口应按具体问题查阅。

## 20.4 你提供的五个网站

本书以原创解释和原创示例为主体，核对这些网站的主题组织，并用官方资料校对语义；没有逐页翻译或复制整站内容。

1. [Python 中文官方教程](https://docs.python.org/zh-cn/3/tutorial/index.html)：语言主线、数据结构、函数、类、异常与标准库概览。
2. [廖雪峰 Python 教程](https://liaoxuefeng.com/books/python/introduction/index.html)：基础到对象、I/O、并发、网络与应用方向的组织参考。
3. [菜鸟教程：Python3 元组](https://www.runoob.com/python3/python3-tuple.html)：本轮未能取得正文；元组创建、不可变和可哈希性以官方资料及本地示例核对。
4. [W3Schools Python](https://www.w3schools.com/python/)：小例子、练习式学习的组织参考。
5. [PythonTutorial.net](https://www.pythontutorial.net/)：基础、进阶、OOP 与并发等学习专题导航参考。

外部站点可能更新，示例版本和风格不一定一致。遇到 Python 2 语法、旧异步写法、过度简化的性能结论或兼容性断言，应先核对目标版本。

### 本轮访问证据与参考使用范围（2026-10-20）

| 来源 | 实际访问情况 | 用途 |
|---|---|---|
| Python 官方中文教程 | 可读取；`/3/` 当时显示 3.15.0 文档 | 对照主线范围；精确语义另查固定 3.14 文档 |
| 廖雪峰 introduction 页面 | 可读取简介和课程目录 | 参考语言到应用的组织，不采用笼统性能倍数 |
| 菜鸟指定元组页 | 两次返回 HTTP 530，未取得正文 | 仅保留用户给定入口；元组改用官方资料核对 |
| W3Schools Python 首页 | 可读取主题目录、例子及练习入口 | 参考短例子与练习配套形式 |
| PythonTutorial.net 首页 | 可读取基础、OOP、进阶、并发等导航 | 参考分层路线 |

本地执行器实际为 CPython 3.14.5；在线 `/3.14/` 文档当时已显示其他补丁版本。因此“固定 3.14 文档”固定的是小版本系列，不表示内容逐字对应本地补丁版本。涉及改动过的行为，应结合本地实验和该版本变更记录。

本轮没有遍历五个网站的所有子页，没有获得菜鸟正文，也没有复制任何整站教程。本书的业务代码、反例和练习按本仓库目标原创组织。对应网站的最新内容可能变化，本表是本次访问记录。

## 20.5 权威专题资料

- [Python 语言参考](https://docs.python.org/3/reference/index.html)：语法与语义的正式规则。
- [内置函数](https://docs.python.org/3.14/builtins/functions.html)：准确签名、参数和异常。
- [数据模型](https://docs.python.org/3/reference/datamodel.html)：对象协议、特殊方法和属性机制。
- [typing](https://docs.python.org/3/library/typing.html)：静态类型工具所依据的接口。
- [asyncio tasks](https://docs.python.org/3/library/asyncio-task.html)：TaskGroup、取消、超时与调度。
- [自由线程支持](https://docs.python.org/3/howto/free-threading-python.html)：GIL 相关构建与兼容边界。
- [SQLite 文档](https://docs.python.org/3.14/library/sqlite3.html)：事务配置、连接和 DB-API 差异。
- [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)：构建、安装、分发和 pyproject。
- [Python 3.14 What's New](https://docs.python.org/3/whatsnew/3.14.html)：版本变化与迁移注意点。

### 本轮新增内容的专题出处

| 专题 | 权威资料 | 对应新增讲解 |
|---|---|---|
| 条件表达式、函数参数、匹配 | [控制流教程](https://docs.python.org/3.14/tutorial/controlflow.html)、[Go 语言规范](https://go.dev/ref/spec) | 修正 Go 无三元运算符；参数和 match 边界 |
| 对象与表达式 | [表达式参考](https://docs.python.org/3.14/reference/expressions.html)、[数据模型](https://docs.python.org/3.14/reference/datamodel.html) | 对象关系、运算协议与执行时机 |
| 属性机制 | [描述符指南](https://docs.python.org/3.14/howto/descriptor.html) | 属性查找、数据描述符与方法绑定 |
| 数据类与类型 | [dataclasses](https://docs.python.org/3.14/library/dataclasses.html)、[typing](https://docs.python.org/3.14/library/typing.html) | frozen、替换、类型约束和收窄 |
| JSON 与资源管理 | [json](https://docs.python.org/3.14/library/json.html)、[contextlib](https://docs.python.org/3.14/library/contextlib.html) | 重复键、非有限数、ExitStack |
| 并发与进程 | [asyncio tasks](https://docs.python.org/3.14/library/asyncio-task.html)、[multiprocessing](https://docs.python.org/3.14/library/multiprocessing.html) | TaskGroup 失败、取消与 spawn |
| 测试替代对象 | [unittest.mock](https://docs.python.org/3.14/library/unittest.mock.html) | autospec 的能力边界 |
| 数组和表格 | [NumPy 索引](https://numpy.org/doc/stable/user/basics.indexing.html)、[pandas Copy-on-Write](https://pandas.pydata.org/docs/user_guide/copy_on_write.html) | 视图、复制、索引对齐与版本限制 |
| Web 资源生命周期 | [FastAPI lifespan](https://fastapi.tiangolo.com/advanced/events/) | 启动资源、请求工作单元、关闭 |

技术规则以官方资料为依据，教学选择、案例设计和审阅结论是结合当前仓库作出的分析。参考某个协议文档不代表本地已经部署该协议的全部实现。

### 2026-10-26 基础补全的官方来源与定位

本次实际读取官网教程入口，并逐项打开下面的官方专题页面核对关键语义。`/3/` 会随发布改变，因此新增引用优先固定 `/3.14/`；本地运行 CPython 3.14.5，在线页面补丁版可能更新。以下是本次记录，前面的 2026-10-20 记录保留为历史。

| 补充领域 | 官方资料 | 教材位置 |
|---|---|---|
| 对象、相等、运算和特殊方法 | [数据模型](https://docs.python.org/3.14/reference/datamodel.html)、[表达式](https://docs.python.org/3.14/reference/expressions.html) | 02、03、09、21 |
| 定义、绑定和控制流 | [控制流教程](https://docs.python.org/3.14/tutorial/controlflow.html)、[简单语句](https://docs.python.org/3.14/reference/simple_stmts.html)、[复合语句](https://docs.python.org/3.14/reference/compound_stmts.html) | 01、04、05、11 |
| 作用域、闭包和执行帧 | [执行模型](https://docs.python.org/3.14/reference/executionmodel.html) | 05、10、22 |
| 模块生命周期 | [模块教程](https://docs.python.org/3.14/tutorial/modules.html)、[导入系统](https://docs.python.org/3.14/reference/import.html) | 07 |
| 继承、绑定和描述符 | [类教程](https://docs.python.org/3.14/tutorial/classes.html)、[描述符指南](https://docs.python.org/3.14/howto/descriptor.html) | 08、09 |
| 数据对象与枚举 | [dataclasses](https://docs.python.org/3.14/library/dataclasses.html)、[enum](https://docs.python.org/3.14/library/enum.html) | 08 |
| 静态类型与注解反射 | [typing](https://docs.python.org/3.14/library/typing.html)、[annotationlib](https://docs.python.org/3.14/library/annotationlib.html) | 10 |
| 迭代、缓存、对象生命周期 | [itertools](https://docs.python.org/3.14/library/itertools.html)、[functools](https://docs.python.org/3.14/library/functools.html)、[weakref](https://docs.python.org/3.14/library/weakref.html) | 06、09、22 |
| 文件与资源退出 | [io](https://docs.python.org/3.14/library/io.html)、[contextlib](https://docs.python.org/3.14/library/contextlib.html) | 11、12 |
| 线程、队列和结果对象 | [threading](https://docs.python.org/3.14/library/threading.html)、[queue](https://docs.python.org/3.14/library/queue.html)、[futures](https://docs.python.org/3.14/library/concurrent.futures.html) | 14.1—14.5 |
| 进程与构建差异 | [multiprocessing](https://docs.python.org/3.14/library/multiprocessing.html)、[自由线程](https://docs.python.org/3.14/howto/free-threading-python.html) | 14.2、14.6、22.9 |
| 协程与退出 | [Tasks](https://docs.python.org/3.14/library/asyncio-task.html)、[Runners](https://docs.python.org/3.14/library/asyncio-runner.html) | 14.7—14.9、14.12 |
| 异步共享状态 | [同步原语](https://docs.python.org/3.14/library/asyncio-sync.html)、[异步队列](https://docs.python.org/3.14/library/asyncio-queue.html)、[ContextVar](https://docs.python.org/3.14/library/contextvars.html) | 14.10—14.11 |
| 测试中的调用契约 | [unittest.mock](https://docs.python.org/3.14/library/unittest.mock.html) | 16.2 |

易混知识对照集中在 [19 练习与迁移陷阱](docs/tutorial/19-练习答案与迁移陷阱.md) 的 19.12 节；运行数量、平台范围和未验证内容以 [验证记录](docs/validation.md) 为准。

## 20.6 学完后如何继续

将一段重复手工工作改成可测试 CLI，是 Go 开发者进入 Python 的好练习。随后按目标选择：后端开发深入驱动、ORM、ASGI 与部署；数据工作深入 NumPy、pandas、统计和可视化；自动化深入文件安全、幂等、观察与恢复。语言运行时、C API 和框架源码是后续专题，不必在第一次学习时全部背完。


---

# 21｜内置函数与标准库补充示例

> 本章目标：查清内置工具的消费、返回与副作用规则。
>
> 阅读重点：重点补齐短路、惰性错误、属性反射和警告，不把它们当无副作用的小工具。

本章作为查阅手册，集中补齐常用内置函数及一些标准库入口。示例按当前 CPython 3.14 验证；精确参数规则见 [官方内置函数参考](https://docs.python.org/3.14/builtins/functions.html)。名称看起来像函数，其中一部分实际上是类型，例如 int、list、property、type。

## 21.1 数值转换与数学内置函数

<!-- verify: run -->
```python
assert abs(-7) == 7
assert abs(3 + 4j) == 5
assert int("101", 2) == 5
assert int(-3.9) == -3
assert float("1.25") == 1.25
assert complex(1, 2) == 1 + 2j
assert bool([]) is False
assert round(2.5) == 2 and round(3.5) == 4
assert divmod(17, 5) == (3, 2)
assert pow(2, 5) == 32
assert pow(2, 5, 7) == 4
assert bin(15) == "0b1111" and oct(15) == "0o17" and hex(15) == "0xf"
```

int(float) 向零截断，与 `//` 的取整方向不同。bool 是构造类型；`bool("0")` 仍为 True。数值合法范围、NaN 和无限大应按输入契约单独检查。

## 21.2 文本表示、格式化与字符

<!-- verify: run -->
```python
assert str(123) == "123"
assert repr("a\nb") == "'a\\nb'"
assert ascii("中") == "'\\u4e2d'"
assert chr(65) == "A" and ord("A") == 65
assert format(255, "08b") == "11111111"
assert format(12.345, ".2f") == "12.35"
assert bytes("中", "utf-8") == b"\xe4\xb8\xad"
assert bytearray(3) == bytearray(b"\x00\x00\x00")
assert memoryview(b"abc")[1] == 98
```

ascii 在 repr 的基础上转义非 ASCII 字符。format 使用对象的格式协议；字节与字符串不能直接相加，先明确编码转换。

## 21.3 容器构造、slice 与范围

<!-- verify: run -->
```python
assert list(range(3)) == [0, 1, 2]
assert tuple("ab") == ("a", "b")
assert dict([("a", 1)]) == {"a": 1}
assert set([1, 1, 2]) == {1, 2}
assert frozenset([1, 2]) == frozenset({2, 1})
assert len("中文") == 2
selector = slice(1, 5, 2)
assert [0, 1, 2, 3, 4, 5][selector] == [1, 3]
assert range(2, 9, 2)[2] == 6
```

slice 对象可以把切片规则保存、传递，适合封装索引策略。list / tuple 转换不等于递归拷贝。

## 21.4 聚合、排序与惰性迭代函数

<!-- verify: run -->
```python
assert sum([1, 2, 3], start=10) == 16
assert min([3, 1, 2]) == 1 and max([3, 1, 2]) == 3
assert min([], default=None) is None
assert all([]) is True and any([]) is False
assert sorted(["bbb", "a", "cc"], key=len) == ["a", "cc", "bbb"]
assert list(reversed([1, 2])) == [2, 1]
assert list(enumerate("ab", 1)) == [(1, "a"), (2, "b")]
assert list(zip([1, 2], "ab", strict=True)) == [(1, "a"), (2, "b")]
assert list(map(str, [1, 2])) == ["1", "2"]
assert list(filter(None, [0, 1, "", "a", None])) == [1, "a"]
```

map、filter、zip、enumerate、reversed 通常返回迭代器。all / any 短路；生成器中的副作用不一定全部执行。sum 不适合拼接大量字符串，使用 join。

### 惰性函数会消费输入，短路会留下未消费部分

<!-- verify: run -->
```python
events = []
def check(value):
    events.append(value)
    return value > 0

assert any(check(v) for v in [-1, 2, 3])
assert events == [-1, 2]  # 3 没有被检查

values = iter([0, 1, 2, 3])
assert next(filter(None, values)) == 1
assert list(values) == [2, 3]

paired = zip([1, 2], ["A"], strict=True)
assert next(paired) == (1, "A")
try:
    next(paired)
except ValueError:
    pass
else:
    raise AssertionError("长度不一致在消费时发现")
```

因此不要把必须执行的保存、通知或审计放进 any/all 的生成器里。`zip(strict=True)` 在创建时不预扫描长度，错误可能在产生部分配对之后出现；如果前几对已写入数据库，仍需要事务策略。

空输入的 `all([])` 为 True 表示“没有反例”，不表示至少有一个有效项。权限检查若要求“至少一个角色，且全部角色满足条件”，应分别检查非空与 all，避免空集合意外通过。

| 工具 | 返回类型或性质 | 易错点 |
|---|---|---|
| map / filter | 一次性惰性迭代 | 创建不执行全部工作 |
| sorted | 新 list | 物化全部输入，元素不深拷贝 |
| reversed | 反向迭代器 | 不普遍接受任意一次性生成器 |
| min / max | 单个元素 | 空输入默认报错，可明确 default |
| sum | 聚合结果 | 不适合拼字符串或反复列表连接 |
| enumerate | 计数与元素的迭代器 | 序号不一定是原数据业务 ID |

## 21.5 iter、next 与哨兵读取

<!-- verify: run -->
```python
from io import StringIO
iterator = iter([1])
assert next(iterator) == 1
assert next(iterator, None) is None
stream = StringIO("abcdefg")
chunks = iter(lambda: stream.read(3), "")
assert list(chunks) == ["abc", "def", "g"]
stream.close()
```

两参数 iter(callable, sentinel) 反复调用 callable，到相等哨兵值停止；二进制读取结束哨兵通常是 b""。

## 21.6 类型、身份、哈希与属性反射

<!-- verify: run -->
```python
class Base:
    pass
class Child(Base):
    pass

instance = Child()
assert type(instance) is Child
assert isinstance(instance, Base)
assert issubclass(Child, Base)
assert id(instance) == id(instance)
assert hash((1, 2)) == hash((1, 2))
assert callable(lambda: None)
setattr(instance, "name", "A")
assert getattr(instance, "name") == "A"
assert getattr(instance, "missing", 7) == 7
assert hasattr(instance, "name")
assert vars(instance) == {"name": "A"}
assert "name" in dir(instance)
delattr(instance, "name")
assert not hasattr(instance, "name")
assert isinstance(object(), object)
```

hash 的具体数值可能跨运行不同，不能当持久化 ID；dir 是探索接口，不是严格字段 schema。vars 需要对象提供相应字典；slots 实例可能没有。type 也可接受三参数动态创建类，第 09 章已经演示。

### 反射函数本身也可能触发业务代码

`getattr` 可执行 property getter，`hasattr` 也不只是查字典。属性 getter 内部抛 AttributeError 时，hasattr 可能把它当成“属性不存在”，隐藏内部错误。

<!-- verify: run -->
```python
import inspect

class Example:
    @property
    def value(self):
        raise AttributeError("内部依赖没有准备好")

item = Example()
assert hasattr(item, "value") is False
assert isinstance(inspect.getattr_static(item, "value"), property)
```

调试或框架代码需要区分“列出声明的属性”和“执行属性求值”。不能把 `dir()` 列出的所有名字都 getattr 一遍后当作安全无副作用的序列化。对象还可能有昂贵属性、网络调用或带权限的数据。

## 21.7 命名空间与动态代码

<!-- verify: run -->
```python
def show_local():
    value = 42
    return locals()["value"]

assert show_local() == 42
assert "show_local" in globals()
expression = compile("left + right", "<trusted-example>", "eval")
assert eval(expression, {"left": 2, "right": 3}) == 5
namespace = {}
exec("result = 6 * 7", namespace)
assert namespace["result"] == 42
```

代码只执行固定可信字面量，不接受外部输入。不要依赖修改 locals 返回字典来修改函数局部变量；其行为与作用域、版本有关。`__import__` 是导入机制底层入口，普通动态导入优先 importlib.import_module。

## 21.8 面向对象相关内置对象

property、classmethod、staticmethod、super 的完整示例见 08；它们不是单纯“语法糖标签”。property 可用函数调用形式构造：

<!-- verify: run -->
```python
class Name:
    def __init__(self, value):
        self._value = value
    def get_value(self):
        return self._value
    value = property(get_value)

assert Name("A").value == "A"
```

## 21.9 交互与文件内置函数

input 与 print 见 01，open 见 12，breakpoint 见 16。help 支持交互帮助，也可以对函数或模块显示文档；在验证中将输出收集到内存：

<!-- verify: run -->
```python
from contextlib import redirect_stdout
from io import StringIO
output = StringIO()
with redirect_stdout(output):
    help(len)
assert "len" in output.getvalue()
print("a", "b", sep=":", file=output)
assert output.getvalue().endswith("a:b\n")
```

exit / quit 是交互辅助，不用于正式程序；使用 return 或 raise SystemExit。copyright / credits / license 同样主要是交互环境辅助对象。

## 21.10 aiter、anext 与异步资源协议

<!-- verify: run -->
```python
import asyncio

async def source():
    yield 10
    yield 20

class AsyncResource:
    def __init__(self):
        self.closed = False
    async def __aenter__(self):
        await asyncio.sleep(0)
        return self
    async def __aexit__(self, exc_type, exc, traceback):
        await asyncio.sleep(0)
        self.closed = True
        return False

async def main():
    iterator = aiter(source())
    assert await anext(iterator) == 10
    assert await anext(iterator) == 20
    assert await anext(iterator, None) is None
    resource = AsyncResource()
    async with resource:
        assert not resource.closed
    assert resource.closed

asyncio.run(main())
```

异步迭代器提供 `__aiter__` 和返回 awaitable 的 `__anext__`；耗尽使用 StopAsyncIteration。异步上下文管理允许获取与释放阶段挂起，但必须保证取消时的清理策略。

## 21.11 keyword、warnings 与 traceback

<!-- verify: run -->
```python
import keyword, warnings, traceback
assert keyword.iskeyword("class")
assert keyword.issoftkeyword("match")
with warnings.catch_warnings(record=True) as records:
    warnings.simplefilter("always")
    warnings.warn("旧 API 将被移除", DeprecationWarning, stacklevel=1)
assert len(records) == 1 and records[0].category is DeprecationWarning
try:
    int("bad")
except ValueError:
    trace = traceback.format_exc()
assert "ValueError" in trace
```

warnings 适合可继续运行但需要注意的情况，例如弃用提示；不是所有问题都应该改为 warning。CI 可以把特定警告提升为错误，及时发现未来版本兼容问题。

### 警告不是测试失败，也不是可以永久忽略的消息

弃用警告表示 API 仍可运行但未来可能移除。项目升级时可以对自己控制的代码启用更严格警告策略，同时针对已知第三方问题单独记录处理计划。不要全局无条件屏蔽所有警告，否则兼容性风险会被延后到发布。

```powershell
python -W default -m unittest discover -s examples -v
```

上面是可选诊断命令。`traceback.format_exc()` 应在处理异常时使用，通常用于内部日志；对外响应使用稳定业务错误，不把文件路径、SQL 或完整堆栈直接返回。验收时能区分 warning、exception、日志等级和进程退出码这四个通道。

## 21.12 configparser、calendar、difflib 与 ipaddress

<!-- verify: run -->
```python
from configparser import ConfigParser
from calendar import monthrange
from difflib import unified_diff
from ipaddress import ip_address, ip_network

config = ConfigParser()
config.read_string("[server]\nport=8080\nenabled=yes\n")
assert config.getint("server", "port") == 8080
assert config.getboolean("server", "enabled")
assert monthrange(2024, 2)[1] == 29
diff = "".join(unified_diff(["old\n"], ["new\n"], fromfile="before", tofile="after"))
assert "-old" in diff and "+new" in diff
assert ip_address("192.0.2.5") in ip_network("192.0.2.0/24")
```

IP 字符串比较不能代替地址解析；SSRF 防护还需处理 DNS 解析、重定向、IPv6 和地址重绑定，不能仅凭一次 is_private 判断。

## 21.13 压缩补充与资源限制

<!-- verify: run -->
```python
import bz2, lzma
data = b"python" * 100
assert bz2.decompress(bz2.compress(data)) == data
assert lzma.decompress(lzma.compress(data)) == data
```

不同算法在压缩率、CPU 与内存之间取舍。对不可信输入，限制压缩前文件大小还不够，必须限制解压后的输出量与资源使用。

## 21.14 运算符补充

<!-- verify: run -->
```python
assert (~5) == -6  # 无限精度整数下 ~x == -x - 1
assert (16 >> 2) == 4
assert (5 | 2) == 7
assert 2 not in [1, 3]
assert None is not False

class Matrix:
    def __matmul__(self, other):
        return "matrix product"

assert Matrix() @ Matrix() == "matrix product"
```

`@` 在表达式里表示矩阵乘法协议，在 def / class 前表示装饰器，两者语法位置不同。赋值表达式、条件表达式和短路有不同优先级，复杂组合务必加括号。

### 内置函数的边界值：空输入、截断和进制转换

<!-- verify: run -->
```python
assert all([]) is True and any([]) is False
assert list(zip([1, 2], ['a'])) == [(1, 'a')]
try:
    list(zip([1, 2], ['a'], strict=True))
except ValueError:
    pass
else:
    raise AssertionError('长度不一致不能静默截断')
assert min([], default=None) is None
assert int('010') == 10
assert int('0x10', 0) == 16
assert divmod(-7, 3) == (-3, 2)
assert round(2.5) == 2 and round(3.5) == 4
```

all 的空输入为真，可能让“所有字段合法”在根本没有字段时错误通过，需另外判断必填或非空。zip 默认以最短输入为准；要求一一对应时用 strict（3.10+）。min/max 的 default 只处理空 iterable，不处理不可比较元素。`int(text, 0)` 按前缀推断进制，不意味着接受所有带前导零文本。round 的偶数舍入叠加浮点表示误差，不能替代明确的十进制金额规则。


---

# 22｜高级运行机制与设计案例

> 本章目标：通过设计案例整合对象、并发和生命周期。
>
> 阅读重点：将高级机制用于明确问题，用容量、错误传播和可测试性评价设计。

## 22.1 从源码到 AST

源码首先被解析为语法结构。ast 可以用于代码分析、变换、教学检查和部分 DSL 实现；不是执行任意输入的安全沙箱。

<!-- verify: run -->
```python
import ast
tree = ast.parse("result = left + right")
names = {node.id for node in ast.walk(tree) if isinstance(node, ast.Name)}
assert names == {"result", "left", "right"}
assert any(isinstance(node, ast.Add) for node in ast.walk(tree))
assert ast.literal_eval('{"x": [1, 2]}') == {"x": [1, 2]}
```

literal_eval 只支持有限字面量结构，减少代码执行风险，但复杂 / 巨大输入仍可能消耗内存或栈，必须限制输入规模。语法树结构可能随版本变化。参考 [ast 官方文档](https://docs.python.org/3.14/library/ast.html)。

## 22.2 AST 变换与编译

<!-- verify: run -->
```python
import ast

class ReplaceOne(ast.NodeTransformer):
    def visit_Constant(self, node):
        if type(node.value) is int and node.value == 1:
            return ast.copy_location(ast.Constant(value=10), node)
        return node

tree = ReplaceOne().visit(ast.parse("result = 1 + 2"))
tree = ast.fix_missing_locations(tree)
namespace = {}
exec(compile(tree, "<generated>", "exec"), namespace)
assert namespace["result"] == 12
```

节点位置用于错误报告和编译；变换器应保留它们。代码生成工具应有明确语法和边界测试，避免依赖对源码文本的脆弱替换。

## 22.3 字节码、代码对象与 dis

<!-- verify: run -->
```python
import dis

def add(a, b):
    return a + b

instructions = list(dis.get_instructions(add))
assert instructions
assert add.__code__.co_argcount == 2
assert "a" in add.__code__.co_varnames
print(dis.Bytecode(add).dis())
```

字节码是 CPython 实现细节，指令、缓存和优化会跨版本改变；不要把特定 opcode 列表当语言契约。性能结论需要真实测量，看到几条字节码不意味着知道完整运行成本。参考 [dis 文档](https://docs.python.org/3.14/library/dis.html)。

### 函数对象、代码对象、闭包单元和执行帧

<!-- verify: run -->
```python
def make(offset):
    def apply(value):
        return value + offset
    return apply

a, b = make(10), make(20)
assert a.__code__ is b.__code__
assert a(1) == 11 and b(1) == 21
assert a.__code__.co_freevars == ('offset',)
assert a.__closure__[0].cell_contents == 10
assert b.__closure__[0].cell_contents == 20
assert a.__globals__ is globals()
```

代码对象描述待执行代码；函数对象把代码、全局命名空间、默认参数和闭包等组合起来；一次调用建立运行帧并保存局部状态。相同代码不意味着相同闭包值。生成器和协程会把暂停所需状态保留下来，所以未关闭的对象也可能间接保留大容器或资源。

`locals()` 在函数等优化作用域中的结果不能当成修改真实局部变量的通用接口，3.13 已明确其快照语义；模块 globals 则是实际命名空间字典。调试器、traceback、frame 引用都可能延长局部对象生命周期。递归深度限制是运行环境保护，Python 不保证尾调用消除，深链遍历通常用显式栈。[执行模型](https://docs.python.org/3.14/reference/executionmodel.html)

## 22.4 统一业务边界：策略与依赖注入

Python 可以直接注入函数，不必为每个微小策略构造一组接口、实现类和工厂。

<!-- verify: run -->
```python
from collections.abc import Callable

def checkout(amount: int, pricing: Callable[[int], int], save: Callable[[int], None]) -> int:
    charged = pricing(amount)
    if charged < 0:
        raise ValueError("价格策略返回负数")
    save(charged)
    return charged

saved = []
assert checkout(100, lambda value: value - 10, saved.append) == 90
assert saved == [90]
```

策略无状态时函数足够；策略有配置、生命周期或多个相关方法时用对象 / Protocol。依赖注入的核心是显式接收依赖，并非必须使用框架容器。

### 设计案例：业务策略与副作用分离

函数注入适合简单策略，Protocol 适合多个相关操作或需要生命周期的依赖。下面服务只关心保存行为，不负责连接建立；fake 保存器使业务测试无需数据库。

<!-- verify: run -->
```python
from typing import Protocol
from dataclasses import dataclass

@dataclass(frozen=True)
class Draft:
    title: str

class Store(Protocol):
    def save(self, draft: Draft) -> int: ...

def create_task(store: Store, title: str) -> int:
    normalized = title.strip()
    if not normalized:
        raise ValueError("标题为空")
    return store.save(Draft(normalized))

class MemoryStore:
    def __init__(self):
        self.items = []
    def save(self, draft):
        self.items.append(draft)
        return len(self.items)

store = MemoryStore()
assert create_task(store, " Learn ") == 1
try:
    create_task(store, " ")
except ValueError:
    pass
else:
    raise AssertionError("无效标题不能保存")
assert store.items == [Draft("Learn")]
```

fake 证明业务未对非法输入调用保存，不证明真实数据库提交。真实实现需要仓储集成测试。如果服务将来需要“保存任务并写审计”，应明确把两项放入一个工作单元，避免让每个 save 都提交。

与 Go 接口类似，调用方应描述自己实际需要的最小行为；Python Protocol 的静态保证依赖检查器运行，运行时还需遵守对象和资源约定。

## 22.5 插件发现与入口点

发行包可以通过元数据声明 entry points，宿主按组发现；读取元数据不等于自动运行插件：

<!-- verify: run -->
```python
from importlib.metadata import entry_points
plugins = entry_points(group="tutorial.exporters")
for plugin in plugins:
    print(plugin.name, plugin.value)
```

正式加载通常调用 `plugin.load()`，会导入第三方代码，因此必须信任插件来源。需要处理名称冲突、版本契约、加载失败、隔离与生命周期。参考 [importlib.metadata](https://docs.python.org/3.14/library/importlib.metadata.html)。

## 22.6 有界异步流水线

第 14 章的 Semaphore 限制运行区，本节进一步限制排队数量。固定 worker + 有界队列可以避免为所有输入预建任务。

<!-- verify: run -->
```python
import asyncio

async def pipeline(values, workers=2):
    if workers < 1:
        raise ValueError("workers 必须为正")
    queue = asyncio.Queue(maxsize=workers * 2)
    results = []

    async def produce():
        for index, value in enumerate(values):
            await queue.put((index, value))
        for _ in range(workers):
            await queue.put(None)

    async def consume():
        while True:
            item = await queue.get()
            try:
                if item is None:
                    return
                index, value = item
                await asyncio.sleep(0)
                results.append((index, value * 2))
            finally:
                queue.task_done()

    async with asyncio.TaskGroup() as group:
        group.create_task(produce())
        for _ in range(workers):
            group.create_task(consume())
    return [value for _, value in sorted(results)]

assert asyncio.run(pipeline(range(5))) == [0, 2, 4, 6, 8]
```

TaskGroup 让消费者失败时可取消生产者，避免生产者永远卡在满队列。这里结果仍收集到 list，因此输入排队有界、结果存储不有界；真正流式系统需要流式输出，并设计保序缓冲上限。参考 [asyncio.Queue](https://docs.python.org/3.14/library/asyncio-queue.html)。

### 进一步限制输出内存，并验证失败退出

前面的案例返回 list，结果空间仍为 O(n)。下面使用异步 sink 消费每个结果，任务数固定、队列有界；sink 自己是否保存全部结果仍由它的实现决定。为保持示例简洁，输出按完成顺序，不承诺输入顺序。

<!-- verify: run -->
```python
import asyncio

async def pump(values, handle, sink, workers=2, capacity=4):
    if type(workers) is not int or workers < 1:
        raise ValueError("workers 必须为正整数")
    if type(capacity) is not int or capacity < 1:
        raise ValueError("capacity 必须为正整数")
    queue = asyncio.Queue(maxsize=capacity)
    stop = object()

    async def produce():
        for value in values:
            await queue.put(value)
        for _ in range(workers):
            await queue.put(stop)

    async def consume():
        while True:
            item = await queue.get()
            try:
                if item is stop:
                    return
                result = await handle(item)
                await sink(result)
            finally:
                queue.task_done()

    async with asyncio.TaskGroup() as group:
        group.create_task(produce())
        for _ in range(workers):
            group.create_task(consume())

async def check():
    total = 0
    async def handle(value):
        await asyncio.sleep(0)
        return value * 2
    async def sink(value):
        nonlocal total
        total += value  # 此处没有 await；同一事件循环中完成一次累加
    await pump(range(10), handle, sink)
    assert total == 90

    failed = False
    async def broken(value):
        if value == 2:
            raise ValueError("bad item")
        await asyncio.sleep(0)
        return value
    try:
        async with asyncio.timeout(2):
            await pump(range(100), broken, sink, capacity=1)
    except* ValueError:
        failed = True
    assert failed  # timeout 或其他异常不被吞掉

asyncio.run(check())
```

容量近似为队列 capacity 个元素，加 workers 个处理中元素，以及生产者当前元素和处理临时数据。若单个元素本身很大，仍可能超过内存预算；“队列长度有界”不等于字节数有界。输入 values 也不应预先物化全部数据；它的迭代不能长时间阻塞事件循环。

sink 可能被多个 worker 交错调用，必须支持这种使用方式；若要串行写文件或保持顺序，可增加一个有界输出队列和单独写入者。严格保序可能需要缓存等待慢任务，必须同时设定保序窗口上限。

失败时 TaskGroup 取消生产者和其他消费者，所以生产者即使卡在满队列 put 也能退出。`task_done` 只是队列计数，不等于业务提交成功。已交给 sink 的结果不会因稍后失败自动撤销；本例是流式部分输出语义。

## 22.7 缓存与业务一致性

缓存必须先定义键、失效、大小、并发与正确性边界。下例演示显式版本作为缓存键的一部分：

<!-- verify: run -->
```python
from functools import lru_cache

@lru_cache(maxsize=128)
def compute_price(product_id, catalog_version, base_price):
    return base_price * 2

assert compute_price(1, 1, 100) == 200
assert compute_price(1, 2, 120) == 240
assert compute_price.cache_info().currsize == 2
```

真实系统不能只加个 version 参数就保证一致；调用方要可靠地获得版本，租户 / 权限 / 币种也可能属于键。lru_cache 在同步多线程下的内部安全不等于“相同未命中只执行一次”，也不适合直接缓存 coroutine 对象。

### 缓存一致性至少有五个维度

1. 键是否包含真正影响结果的租户、权限、语言、币种和数据版本。
2. 值是否可变，调用方是否可能污染后续结果。
3. 容量是否有上限，键空间是否被用户输入无限扩大。
4. 失效如何发生，过期期间是否允许读到旧值。
5. 同一键并发未命中是否允许重复计算，是否需要合并请求。

不能直接用 lru_cache 包装 async 函数后期待缓存结果：它缓存的是 coroutine 对象，协程对象通常不能重复 await。缓存最终值、缓存正在执行的 Task，以及给结果加 TTL，是不同设计；错误、取消和多事件循环场景还要分别处理。

函数级缓存适合确定性纯计算。查询缓存涉及数据更新和权限边界，应先定义一致性目标。增加一个 version 参数只有在调用方可靠获得并正确传递版本时才有意义。

### 缓存不仅保存结果，还改变对象所有权

<!-- verify: run -->
```python
from functools import lru_cache, cached_property
@lru_cache(maxsize=2)
def values(key):
    return []
first = values('a')
first.append(1)
assert values('a') is first
assert values('a') == [1]
values.cache_clear()
assert values('a') == []

class Item:
    def __init__(self):
        self.calls = 0
    @cached_property
    def value(self):
        self.calls += 1
        return self.calls
item = Item()
assert item.value == item.value == 1
del item.value
assert item.value == 2
```

lru_cache 保留参数和结果引用，可变返回值被所有命中者共享；方法缓存的 key 通常包含 self，可能延长实例生命。缓存内部线程安全不保证同一未命中工作只执行一次；有副作用的函数不适合直接套缓存。不要直接缓存协程对象或生成器对象：它们有一次性执行/消费状态。

cached_property 将值存入实例字典，3.12+ 不再提供旧实现中的隐式锁；需要“只初始化一次”时自行同步。缓存大小、有效期和主动失效是不同维度，lru_cache 的 maxsize 不是 TTL。[functools 参考](https://docs.python.org/3.14/library/functools.html)

## 22.8 生命周期优先于魔法

服务资源通常在应用启动时创建，在关闭时释放；请求级对象在请求范围内创建与回收。类全局连接、导入时初始化服务和无界后台任务会使测试、重载与多进程运行复杂化。

<!-- verify: run -->
```python
from contextlib import contextmanager, ExitStack
from io import StringIO

@contextmanager
def application_resources():
    with ExitStack() as stack:
        audit = stack.enter_context(StringIO())
        yield {"audit": audit}

with application_resources() as resources:
    resources["audit"].write("started")
    assert resources["audit"].getvalue() == "started"
assert resources["audit"].closed
```

这是生命周期结构示例；实际 HTTP 连接池、数据库池或异步客户端分别使用其上下文管理 / close API。

## 22.9 子解释器、JIT 与运行时边界

子解释器、可选 JIT 和自由线程属于解释器演进专题，是否可用、如何启用以及扩展是否兼容都取决于版本和构建。多解释器不等价于让所有对象可安全共享；原生扩展的全局状态和对象所有权仍是问题。

初次学习应先稳定理解语言协议、进程隔离和异步取消。需要特定部署优化时，再针对实际构建阅读 [对应版本新增特性](https://docs.python.org/3/whatsnew/3.14.html)，进行基准和兼容测试。本书不声称涵盖所有解释器内部实现。

### 语言保证、CPython 实现和可选构建分层阅读

| 层次 | 例子 | 学习时应怎么使用 |
|---|---|---|
| 语言语义 | 名称绑定、比较协议、with 退出规则 | 用来解释跨实现程序行为 |
| CPython 实现 | 引用计数、具体字节码、对象布局 | 调试和测量可用，勿当永久语言承诺 |
| 版本特性 | 3.14 延迟注解、InterpreterPoolExecutor | 标注最低版本并验证部署环境 |
| 构建选项 | 自由线程、实验性 JIT | 确认编译选项、启用状态和依赖兼容性 |

3.14 的 InterpreterPoolExecutor 在不同线程中的独立解释器运行任务，可使用各解释器的 GIL 实现多核执行；模块、全局状态和导入环境隔离，任务与结果的传输仍有序列化等限制。它不是“共享一个普通全局字典却完全不用锁”的线程池。JIT 改变执行实现，不改变对象可变性、取消协议或资源所有权。这里提供选择边界，不把未运行的构建性能写成验证结论。

## 22.10 一个可维护 Python 模块的完成条件

一个模块应有清晰输入与输出、可预测的副作用、显式资源生命周期、可说明的异常策略和适量测试。使用类型提示让调用方读懂契约，使用日志让运行者定位问题，使用性能测量决定优化。Python 的简洁应来自删除不必要结构，而不是省略业务边界。

### 最终设计评审问题

用下面的问题评审自己的 Python 模块，而不是看它用了多少高级语法：

| 维度 | 需要回答的问题 |
|---|---|
| 输入 | 哪些值可信？谁做解析？None、空值、缺失如何区分？ |
| 对象 | 谁拥有可变状态？谁持有引用？返回值是否共享？ |
| 执行 | 工作发生在调用、迭代、await 还是导入阶段？ |
| 失败 | 已产生哪些副作用？异常怎样传播？允许哪些重试？ |
| 资源 | 谁打开、谁关闭？部分初始化失败如何清理？ |
| 容量 | 输入、任务、队列、缓存、结果分别有什么上限？ |
| 类型 | 静态检查证明了什么？运行时还缺什么检查？ |
| 版本 | 使用了哪些新语法？目标解释器与依赖是否验证？ |
| 交付 | 脱离源码目录能运行吗？日志、退出码和测试是否足够？ |

学习结束时应能完成一个可维护的工具或服务模块，并用失败路径实验解释它为什么可靠。AST、元类、JIT 和插件都是解决具体问题的工具，不是“高级 Python”的打卡清单。

