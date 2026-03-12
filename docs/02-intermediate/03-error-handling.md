# 錯誤處理

> Python 的錯誤處理使用 try-except，概念和 Swift 的 do-try-catch 及 JavaScript 的 try-catch 相同，但有一些 Python 獨有的特性。

## 語法對比

```swift
// Swift
do {
    let data = try loadFile(path)
    process(data)
} catch FileError.notFound {
    print("File not found")
} catch {
    print("Error: \(error)")
}
```

```javascript
// JavaScript
try {
    const data = loadFile(path);
    process(data);
} catch (error) {
    if (error instanceof FileNotFoundError) {
        console.log("File not found");
    } else {
        console.log(`Error: ${error.message}`);
    }
} finally {
    cleanup();
}
```

```python
# Python
try:
    data = load_file(path)
    process(data)
except FileNotFoundError:
    print("File not found")
except Exception as e:
    print(f"Error: {e}")
finally:
    cleanup()
```

### 關鍵差異

| 特性 | Swift | JavaScript | Python |
|-----|-------|------------|--------|
| try 區塊 | `do { }` | `try { }` | `try:` |
| 捕獲 | `catch` | `catch` | `except` |
| 清理 | `defer` | `finally` | `finally` |
| 丟出 | `throw` | `throw` | `raise` |
| 函數標記 | `throws` | 無 | 無 |
| else 區塊 | 無 | 無 | `else:`（無錯誤時執行） |

## 基本用法

### try-except-else-finally

```python
try:
    result = 10 / divisor
except ZeroDivisionError:
    print("Cannot divide by zero!")
except (TypeError, ValueError) as e:    # 捕獲多種例外
    print(f"Invalid input: {e}")
except Exception as e:                   # 捕獲所有例外（最後的 catch-all）
    print(f"Unexpected error: {e}")
else:
    # 只有在 try 區塊「沒有發生例外」時才執行（Python 獨有）
    print(f"Result: {result}")
finally:
    # 無論如何都會執行（同 JS 的 finally，同 Swift 的 defer）
    print("Cleanup done")
```

> **`else` 的用途：** 把「正常流程的後續操作」放在 `else` 中，可以避免意外捕獲到那些操作中的例外。

### raise — 丟出例外

```python
# 丟出內建例外
raise ValueError("Invalid age: must be positive")
raise TypeError("Expected string, got int")
raise NotImplementedError("Subclass must implement this")

# 重新丟出當前例外
try:
    risky_operation()
except Exception:
    log_error()
    raise           # 重新丟出，不吞掉例外

# 例外鏈（Python 3）
try:
    connect_to_db()
except ConnectionError as e:
    raise RuntimeError("Database unavailable") from e
```

## 常見內建例外

```
BaseException
├── SystemExit                 # sys.exit()
├── KeyboardInterrupt          # Ctrl+C
└── Exception                  # 所有一般例外的基類
    ├── ValueError             # 值不合法（如 int("abc")）
    ├── TypeError              # 型別不對（如 "a" + 1）
    ├── KeyError               # dict 中找不到 key
    ├── IndexError             # list 索引超出範圍
    ├── AttributeError         # 物件沒有該屬性
    ├── FileNotFoundError      # 檔案不存在
    ├── PermissionError        # 權限不足
    ├── IOError                # I/O 操作失敗
    ├── ConnectionError        # 網路連線錯誤
    ├── TimeoutError           # 超時
    ├── ImportError             # import 失敗
    ├── StopIteration          # 迭代器結束
    ├── RuntimeError           # 一般執行錯誤
    └── NotImplementedError    # 未實作
```

## 自定義例外

```python
# 自定義例外（類似 Swift 的 enum Error）
class AppError(Exception):
    """應用程式的基礎例外類別"""
    pass

class ValidationError(AppError):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"Validation error on '{field}': {message}")

class NotFoundError(AppError):
    def __init__(self, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} with id={id} not found")

# 使用
def create_user(name, age):
    if not name:
        raise ValidationError("name", "cannot be empty")
    if age < 0:
        raise ValidationError("age", "must be non-negative")

try:
    create_user("", 25)
except ValidationError as e:
    print(e.field)      # "name"
    print(e.message)    # "cannot be empty"
    print(e)            # "Validation error on 'name': cannot be empty"
except AppError as e:
    print(f"App error: {e}")
```

### 對比 Swift 的 Error Enum

```swift
// Swift
enum AppError: Error {
    case validationError(field: String, message: String)
    case notFound(resource: String, id: Int)
}
```

```python
# Python — 用繼承而非 enum
class AppError(Exception): pass
class ValidationError(AppError): pass
class NotFoundError(AppError): pass
```

## Context Manager — with 語句

Python 的 `with` 語句確保資源被正確釋放，類似 Swift 的 `defer` 但更結構化：

```python
# 最常見：檔案操作
# 不好的寫法
f = open("data.txt")
try:
    content = f.read()
finally:
    f.close()

# Pythonic 的寫法 — with 會自動呼叫 close()
with open("data.txt") as f:
    content = f.read()
# 離開 with 區塊時自動關閉，即使發生例外

# 多個資源
with open("input.txt") as src, open("output.txt", "w") as dst:
    dst.write(src.read())
```

### 自定義 Context Manager

```python
# 方式 1：實作 __enter__ / __exit__
class Timer:
    def __enter__(self):
        import time
        self.start = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.time() - self.start
        print(f"Elapsed: {self.elapsed:.3f}s")
        return False   # 不吞掉例外

with Timer() as t:
    # 做一些耗時操作
    sum(range(1_000_000))
# 自動印出：Elapsed: 0.035s

# 方式 2：用 contextmanager 裝飾器（更簡潔）
from contextlib import contextmanager

@contextmanager
def timer():
    import time
    start = time.time()
    yield    # yield 之前 = __enter__，之後 = __exit__
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.3f}s")

with timer():
    sum(range(1_000_000))
```

## EAFP vs LBYL

Python 社群偏好 **EAFP**（Easier to Ask Forgiveness than Permission），而非 **LBYL**（Look Before You Leap）：

```python
# LBYL 風格（先檢查再操作，Swift / JS 常見思維）
if "name" in user_dict:
    name = user_dict["name"]
else:
    name = "Unknown"

# EAFP 風格（先做再處理例外，更 Pythonic）
try:
    name = user_dict["name"]
except KeyError:
    name = "Unknown"

# 當然，最 Pythonic 的寫法是：
name = user_dict.get("name", "Unknown")
```

## 下一步

接下來看 [檔案操作](04-file-io.md)。
