# Python for iOS / Web 开发者快速对照

> 目标：基于你已有的 iOS（Swift）和 Web（JavaScript/TypeScript）经验，快速掌握 Python 的“同构概念”和“关键差异”。

---

## 1. 思维迁移：先把“相同点”连起来

### 1.1 变量与类型

- Python 是**动态类型**，但支持类型标注（Type Hints）
- 体验上接近 JS 运行时 + TS 书写提示

```python
name: str = "Alice"
age: int = 18
is_active: bool = True
```

对照：

- Swift：静态强类型（编译期检查更强）
- TS：可选类型系统（开发体验类似 Python type hints）

### 1.2 函数

```python
def greet(name: str) -> str:
    return f"Hello, {name}"
```

对照：

- Swift: `func greet(_ name: String) -> String`
- TS: `function greet(name: string): string`

### 1.3 集合类型

- `list` 类似 JS Array / Swift Array
- `dict` 类似 JS Object / Map（更接近键值映射）
- `set` 类似 JS Set / Swift Set

```python
users = ["a", "b"]
profile = {"id": 1, "name": "Alice"}
tags = {"ios", "web", "python"}
```

---

## 2. 你会马上用到的 Python 语法习惯

### 2.1 缩进是语法，不是格式

Python 用缩进表示代码块（不像 JS/Swift 主要靠 `{}`）。

```python
if age >= 18:
    print("adult")
else:
    print("minor")
```

### 2.2 真值判断

- 空字符串、空列表、空字典、`0`、`None` 都会被当作 `False`

```python
if not items:
    print("empty")
```

### 2.3 可变与不可变（高频坑点）

- 不可变：`int/float/str/tuple`
- 可变：`list/dict/set`
- 函数默认参数不要用可变对象

```python
# 不推荐
def add_item(x, bucket=[]):
    bucket.append(x)
    return bucket

# 推荐
def add_item(x, bucket=None):
    bucket = bucket or []
    bucket.append(x)
    return bucket
```

---

## 3. 工程化：把你熟悉的流程迁移过来

### 3.1 环境管理

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

对照：

- iOS：不同 target/scheme 的隔离
- Web：`node_modules` + lockfile 的项目隔离

### 3.2 依赖管理

最小可用先用 `pip + requirements.txt`，后续可进阶到 `poetry` / `uv`。

```bash
pip install requests fastapi pytest ruff
pip freeze > requirements.txt
```

### 3.3 代码质量

- `ruff`：Lint + 部分格式化能力（类似 ESLint）
- `pytest`：测试框架（类似 Jest / XCTest 的组合体验）

---

## 4. 异步模型：从 async/await 过渡到 asyncio

Python 有原生 `async/await`，语义和 JS 接近。

```python
import asyncio

async def fetch_data():
    await asyncio.sleep(1)
    return {"ok": True}

async def main():
    result = await fetch_data()
    print(result)

asyncio.run(main())
```

注意：

- CPU 密集任务不是 async 的强项，优先考虑多进程/任务队列
- I/O 密集（HTTP、DB、文件网络）才是 async 优势场景

---

## 5. Web 开发落地建议（你会很快上手）

### 5.1 框架建议：FastAPI

你会获得：

- 接近 TS 的类型提示体验
- 自动生成 OpenAPI 文档
- 现代异步能力（基于 ASGI）

### 5.2 最小 API 示例

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/health")
def health():
    return {"status": "ok"}
```

---

## 6. iOS 场景下的 Python 价值点

- 自动化脚本：批处理资源、生成配置、构建辅助工具
- 数据处理：日志分析、实验数据清洗、报表导出
- 后端协作：快速搭建 mock 服务，提升联调效率
- AI/数据能力补位：生态成熟，上手门槛低

---

## 7. 建议你的第一批练习（务实版）

1. 做一个 CLI：读取 JSON，输出统计结果  
2. 写一个 FastAPI 服务：3 个接口 + 参数校验 + 单元测试  
3. 接入 SQLite：完成简单 CRUD  
4. 增加 CI：执行 `ruff` 和 `pytest`

完成这 4 步后，你就能把 Python 放进日常工程栈，而不是停留在语法学习。

