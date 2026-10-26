---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

<span class="eyebrow">PYTHON · 从语言语义到工程实践</span>

# 把 Python 知识，连成体系。

面向已有 Go 和 Python 基础的开发者。用对象模型解释代码行为，用完整示例掌握类型、资源、事务与并发，再通过一个 SQLite 项目把知识落到工程实践。

[开始学习 →](tutorial/00-导读与学习路线.md){ .md-button .md-button--primary }
[按问题查阅](tutorial/20-知识点索引与参考资料.md){ .md-button }

</div>

<div class="study-stats" markdown>

**23** 个章节　 ·　 **287** 个 Python 代码块　 ·　 **264** 个可执行示例　 ·　 **1** 个综合实战

</div>

## 选择你的学习入口

<div class="grid cards" markdown>

-   **01 / 语言基础**

    ---

    从名称绑定、可变性和容器出发，理解函数、装饰器、迭代器与模块导入。

    [进入基础章节 →](tutorial/01-环境安装与基本语法.md)

-   **02 / 对象模型与工程**

    ---

    串起类与协议、类型提示、异常、上下文管理和标准库的使用边界。

    [理解对象与建模 →](tutorial/08-面向对象与数据建模.md)

-   **03 / 并发与业务实战**

    ---

    学习线程、进程、asyncio 与事务，用真实 SQLite 完成任务管理 CLI。

    [开始并发与实战 →](tutorial/14-线程进程与异步编程.md)

-   **04 / 进阶与问题速查**

    ---

    用迁移陷阱、练习答案、内置函数和高级机制补齐知识链路。

    [打开知识点索引 →](tutorial/20-知识点索引与参考资料.md)

</div>

## 推荐阅读路线

| 你的目标 | 建议路线 |
| --- | --- |
| 只学习 Python 语言与标准库基础 | 01—14 → 16 → 19—22；17 为综合练习，15 选读标准库内容 |
| 系统整理 Python 基础 | 00 导读 → 01—07 语言基础 → 08—13 对象与工程 |
| 从 Go 经验迁移到 Python | 02 对象模型 → 05 函数 → 10 类型提示 → 11 异常 → 14 并发 |
| 完成一个可运行的项目 | 12 文件与数据 → 15 数据库 → 16 测试 → 17 任务管理器 |
| 排查问题、补齐细节 | 19 迁移陷阱 → 20 症状索引 → 21 内置函数 → 22 高级案例 |

## 边读、边运行、边验证

在项目根目录运行任务管理器：

```shell
python examples/task_cli.py --db demo-tasks.db add "学习 Python 对象模型"
python examples/task_cli.py --db demo-tasks.db list
python -B -m unittest discover -s examples -p "test_*.py" -v
```

[示例源码与合订版下载](examples.md) · [验证范围与运行记录](validation.md)

!!! note "版本与范围"
    主体内容面向 Python 3.11+，新版本特性在章节中标注；完整代码块验证需要 Python 3.14+。
    2026-10-26 的补全依据 Python 官网资料，聚焦语言核心、对象与工程、并发和进阶语义；不新增框架知识。
    [易混点总表](tutorial/19-练习答案与迁移陷阱.md) 与 [官网主题覆盖表](tutorial/20-知识点索引与参考资料.md) 提供集中导航。已有第三方扩展的运行边界见验证记录。
