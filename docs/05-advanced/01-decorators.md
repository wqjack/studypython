# 裝飾器 (Decorators)

> 裝飾器是 Python 最具特色的功能之一。如果你用過 TypeScript 的裝飾器（`@Component`）或 Swift 的 property wrapper（`@Published`），概念相似但用途更廣。

## 核心概念

裝飾器本質上就是一個**接收函數、回傳函數**的高階函數：

```python
# 裝飾器的本質
def my_decorator(func):
    def wrapper(*args, **kwargs):
        # 在原函數前做一些事
        print("Before")
        result = func(*args, **kwargs)
        # 在原函數後做一些事
        print("After")
        return result
    return wrapper

# 使用 @ 語法糖
@my_decorator
def say_hello():
    print("Hello!")

# 等同於：
# say_hello = my_decorator(say_hello)

say_hello()
# Before
# Hello!
# After
```

### 對比 TypeScript 裝飾器

```typescript
// TypeScript — 類別/方法裝飾器
function Log(target: any, key: string, descriptor: PropertyDescriptor) {
    const original = descriptor.value;
    descriptor.value = function(...args: any[]) {
        console.log(`Calling ${key}`);
        return original.apply(this, args);
    };
}

class MyClass {
    @Log
    doSomething() { ... }
}
```

```python
# Python — 函數裝飾器（更靈活，可用於任何函數）
def log(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@log
def do_something():
    pass
```

## 保留函數元資料

使用 `functools.wraps` 保留原函數的名稱和文件字串：

```python
from functools import wraps

def my_decorator(func):
    @wraps(func)    # 保留原函數的 __name__, __doc__ 等
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@my_decorator
def greet(name):
    """回傳問候語"""
    return f"Hello, {name}!"

print(greet.__name__)    # "greet"（沒有 @wraps 會顯示 "wrapper"）
print(greet.__doc__)     # "回傳問候語"
```

## 實用裝飾器範例

### 計時器

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    time.sleep(1)

slow_function()    # slow_function took 1.0012s
```

### 重試機制

```python
import time
from functools import wraps

def retry(max_attempts=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts:
                        raise
                    print(f"Attempt {attempt} failed: {e}, retrying in {delay}s...")
                    time.sleep(delay)
        return wrapper
    return decorator

@retry(max_attempts=3, delay=2)
def fetch_data(url):
    import requests
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    return response.json()
```

### 快取 (Memoization)

```python
from functools import wraps

def cache(func):
    memo = {}
    @wraps(func)
    def wrapper(*args):
        if args not in memo:
            memo[args] = func(*args)
        return memo[args]
    return wrapper

@cache
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# Python 內建更好的版本：
from functools import lru_cache

@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### 權限驗證

```python
from functools import wraps

def require_auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Unauthorized"}), 401
        kwargs["current_user"] = verify_token(token)
        return func(*args, **kwargs)
    return wrapper

def require_role(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if user.role != role:
                return jsonify({"error": "Forbidden"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

@app.route("/admin/users")
@require_auth
@require_role("admin")
def admin_users(current_user):
    return jsonify({"users": []})
```

## 帶參數的裝飾器

需要三層巢狀函數：

```python
from functools import wraps

# 不帶參數
def simple_log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

# 帶參數（多一層）
def log(level="INFO"):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"[{level}] Calling {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@log(level="DEBUG")
def process_data():
    pass

process_data()    # [DEBUG] Calling process_data
```

## 類別裝飾器

```python
class Timer:
    def __init__(self, func):
        self.func = func
        wraps(func)(self)

    def __call__(self, *args, **kwargs):
        import time
        start = time.perf_counter()
        result = self.func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{self.func.__name__} took {elapsed:.4f}s")
        return result

@Timer
def slow_function():
    import time
    time.sleep(1)
```

## 多個裝飾器的執行順序

裝飾器從下往上套用，從上往下執行：

```python
@decorator_a        # 3. 最外層，最先執行
@decorator_b        # 2. 中間層
@decorator_c        # 1. 最先套用，最後執行
def my_function():
    pass

# 等同於：
# my_function = decorator_a(decorator_b(decorator_c(my_function)))
```

## 裝飾器在框架中的應用

你已經見過很多了：

```python
# Flask 路由
@app.route("/api/users")

# FastAPI 路由 + 驗證
@app.get("/users", response_model=list[User])

# Property
@property

# 類別方法
@classmethod
@staticmethod

# 資料類別
@dataclass

# 抽象方法
@abstractmethod

# 快取
@lru_cache

# 內建的 functools
@functools.wraps
@functools.total_ordering
@functools.singledispatch
```

## 下一步

接下來看 [非同步程式設計](02-async.md)。
