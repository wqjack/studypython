# 非同步程式設計

> 如果你熟悉 JavaScript 的 async/await 或 Swift 的 structured concurrency，Python 的非同步模型概念相同。但有一些重要差異需要注意。

## 對比

| 特性 | JavaScript | Swift | Python |
|-----|-----------|-------|--------|
| 非同步基礎 | Event Loop | Structured Concurrency | asyncio Event Loop |
| 語法 | `async/await` | `async/await` | `async/await` |
| 並行原語 | `Promise` | `Task` / `TaskGroup` | `coroutine` / `Task` |
| 並行執行 | `Promise.all()` | `async let` / `TaskGroup` | `asyncio.gather()` |
| 執行緒 | 單執行緒 | 多執行緒 | 單執行緒（GIL） |

## 基本語法

### JavaScript vs Python

```javascript
// JavaScript
async function fetchUser(id) {
    const response = await fetch(`/api/users/${id}`);
    const user = await response.json();
    return user;
}

// 呼叫
const user = await fetchUser(1);
```

```python
# Python
import asyncio

async def fetch_user(id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"/api/users/{id}")
        return response.json()

# 呼叫（注意：不能在普通函數中直接 await）
user = asyncio.run(fetch_user(1))

# 在 async 函數中可以直接 await
async def main():
    user = await fetch_user(1)
    print(user)

asyncio.run(main())
```

### 關鍵差異

1. **JavaScript 的 Event Loop 永遠在跑**，任何地方都可以 await。
2. **Python 需要顯式啟動 Event Loop**，用 `asyncio.run()` 進入非同步世界。
3. Python 的普通函數中**不能 await**，必須在 `async def` 中才能用。

## asyncio 基礎

```python
import asyncio

async def greet(name, delay):
    await asyncio.sleep(delay)    # 非阻塞的等待（不同於 time.sleep）
    print(f"Hello, {name}!")
    return name

async def main():
    # 依序執行
    await greet("Alice", 1)
    await greet("Bob", 1)
    # 總共花 2 秒

asyncio.run(main())
```

## 並行執行

### asyncio.gather() — 類似 Promise.all()

```javascript
// JavaScript
const [user, posts, comments] = await Promise.all([
    fetchUser(1),
    fetchPosts(1),
    fetchComments(1)
]);
```

```python
# Python
async def main():
    user, posts, comments = await asyncio.gather(
        fetch_user(1),
        fetch_posts(1),
        fetch_comments(1)
    )
    # 三個請求同時發出，等全部完成
```

### TaskGroup — 結構化並行（Python 3.11+）

類似 Swift 的 TaskGroup：

```swift
// Swift
try await withTaskGroup(of: Data.self) { group in
    group.addTask { await fetchUser(1) }
    group.addTask { await fetchPosts(1) }
}
```

```python
# Python 3.11+
async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_user(1))
        task2 = tg.create_task(fetch_posts(1))

    user = task1.result()
    posts = task2.result()
```

### asyncio.create_task() — 背景執行

```python
async def background_job():
    while True:
        await asyncio.sleep(60)
        print("Running background cleanup...")

async def main():
    # 建立背景任務（不等待它完成）
    task = asyncio.create_task(background_job())

    # 繼續做其他事
    await handle_requests()

    # 如果需要取消
    task.cancel()
```

## 非同步 HTTP 請求

```python
import asyncio
import httpx

async def fetch_all_users(user_ids):
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"https://api.example.com/users/{uid}")
            for uid in user_ids
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]

# 同時發出 100 個請求（不是依序！）
users = asyncio.run(fetch_all_users(range(1, 101)))
```

### 限制並行數量

```python
import asyncio
import httpx

async def fetch_with_limit(user_ids, max_concurrent=10):
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(client, uid):
        async with semaphore:    # 最多同時 10 個請求
            response = await client.get(f"https://api.example.com/users/{uid}")
            return response.json()

    async with httpx.AsyncClient() as client:
        tasks = [fetch_one(client, uid) for uid in user_ids]
        return await asyncio.gather(*tasks)
```

## 非同步迭代

```python
# 非同步生成器
async def fetch_pages(url, total_pages):
    async with httpx.AsyncClient() as client:
        for page in range(1, total_pages + 1):
            response = await client.get(url, params={"page": page})
            yield response.json()

# 非同步 for 迴圈
async def process_all_pages():
    async for page_data in fetch_pages("https://api.example.com/items", 10):
        for item in page_data["items"]:
            process(item)
```

## 非同步 Context Manager

```python
# 非同步 with
async with httpx.AsyncClient() as client:
    response = await client.get(url)

# 自定義
class AsyncDBConnection:
    async def __aenter__(self):
        self.conn = await connect_to_db()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

async with AsyncDBConnection() as conn:
    result = await conn.execute("SELECT * FROM users")
```

## GIL 與多執行緒

Python 有 **GIL (Global Interpreter Lock)**，限制同一時間只有一個執行緒執行 Python 程式碼。這和 JavaScript 的單執行緒類似，但有一些不同：

```python
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

# I/O 密集型任務 → asyncio 或 多執行緒
# CPU 密集型任務 → 多進程

# 在 asyncio 中執行阻塞操作
async def main():
    loop = asyncio.get_event_loop()

    # 用執行緒池跑阻塞的 I/O
    result = await loop.run_in_executor(
        ThreadPoolExecutor(),
        blocking_io_function
    )

    # 用進程池跑 CPU 密集計算
    result = await loop.run_in_executor(
        ProcessPoolExecutor(),
        cpu_intensive_function
    )
```

### 什麼時候用什麼？

| 場景 | 方案 | 類比 |
|-----|------|------|
| HTTP 請求、DB 查詢 | `asyncio` + `await` | JS 的 `async/await` |
| 檔案 I/O、網路 | `asyncio` 或多執行緒 | JS 的 Event Loop |
| CPU 密集計算 | `multiprocessing` | Web Worker |
| 簡單的並行 | `concurrent.futures` | — |

## 在 Web 框架中使用

### FastAPI（原生支援 async）

```python
from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

@app.get("/dashboard")
async def dashboard():
    async with httpx.AsyncClient() as client:
        user, orders, notifications = await asyncio.gather(
            client.get("/api/user/me"),
            client.get("/api/orders"),
            client.get("/api/notifications"),
        )
        return {
            "user": user.json(),
            "orders": orders.json(),
            "notifications": notifications.json(),
        }
```

## 下一步

接下來看最後一個主題 [型別提示](03-type-hints.md)。
