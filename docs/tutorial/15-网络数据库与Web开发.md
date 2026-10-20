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
