# 型別提示 (Type Hints)

> 如果你喜歡 Swift 的強型別安全或 TypeScript 的漸進式型別系統，Python 的型別提示提供了類似的開發體驗——但是完全可選的。

## 為什麼需要型別提示？

Python 是動態型別語言，但從 3.5 開始支援型別標注。就像 JavaScript 加上 TypeScript 一樣，Python 的型別提示：

- 不影響執行（純粹是給工具和人看的）
- 提升程式碼可讀性
- 讓 IDE 提供更好的自動補全
- 配合 mypy 等工具做靜態型別檢查

| 特性 | Swift | TypeScript | Python Type Hints |
|-----|-------|------------|-------------------|
| 必要性 | 必須 | 選擇性（但幾乎必須） | 完全可選 |
| 檢查時機 | 編譯期 | 編譯期 | 工具檢查（mypy） |
| 執行期影響 | 有 | 有（編譯為 JS） | **無** |

## 基本型別標注

### 變數

```python
# 不標注（合法，但缺少型別資訊）
name = "Alice"
age = 25

# 加上型別標注
name: str = "Alice"
age: int = 25
price: float = 19.99
is_active: bool = True
data: bytes = b"hello"
```

### 函數

```swift
// Swift
func greet(name: String, times: Int = 1) -> String {
    return String(repeating: "Hello, \(name)! ", count: times)
}
```

```typescript
// TypeScript
function greet(name: string, times: number = 1): string {
    return "Hello, " + name + "! ".repeat(times);
}
```

```python
# Python
def greet(name: str, times: int = 1) -> str:
    return f"Hello, {name}! " * times

# 沒有回傳值
def log(message: str) -> None:
    print(message)
```

## 集合型別

### Python 3.9+ 語法（推薦）

```python
# 列表
names: list[str] = ["Alice", "Bob"]
matrix: list[list[int]] = [[1, 2], [3, 4]]

# 字典
scores: dict[str, int] = {"Alice": 85, "Bob": 92}
config: dict[str, str | int | bool] = {"debug": True, "port": 8080}

# 集合
unique_ids: set[int] = {1, 2, 3}

# 元組
point: tuple[int, int] = (3, 4)
record: tuple[str, int, float] = ("Alice", 25, 165.5)
variable_tuple: tuple[int, ...] = (1, 2, 3, 4, 5)    # 可變長度
```

### 對比 TypeScript

```typescript
// TypeScript
const names: string[] = ["Alice", "Bob"];
const scores: Record<string, number> = { Alice: 85 };
const point: [number, number] = [3, 4];
```

```python
# Python
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 85}
point: tuple[int, int] = (3, 4)
```

## Optional 與 Union

### Optional — 可能是 None

類似 Swift 的 Optional 和 TypeScript 的 `T | null`：

```swift
// Swift
var name: String? = nil
func find(id: Int) -> User? { ... }
```

```typescript
// TypeScript
let name: string | null = null;
function find(id: number): User | null { ... }
```

```python
# Python 3.10+（推薦語法）
name: str | None = None

def find(id: int) -> User | None:
    ...

# Python 3.9 及更早
from typing import Optional
name: Optional[str] = None    # 等同 str | None
```

### Union — 多種型別

```python
# Python 3.10+
def process(value: int | str | float) -> str:
    return str(value)

# Python 3.9 及更早
from typing import Union
def process(value: Union[int, str, float]) -> str:
    return str(value)
```

## 進階型別

### Callable — 函數型別

```swift
// Swift
let transform: (Int) -> String = { "\($0)" }
```

```typescript
// TypeScript
const transform: (x: number) => string = (x) => `${x}`;
```

```python
# Python
from collections.abc import Callable

transform: Callable[[int], str] = lambda x: str(x)

# 接收回呼函數
def apply(func: Callable[[int], int], value: int) -> int:
    return func(value)

apply(lambda x: x * 2, 5)    # 10
```

### TypeVar — 泛型

```swift
// Swift
func first<T>(items: [T]) -> T? {
    return items.first
}
```

```typescript
// TypeScript
function first<T>(items: T[]): T | undefined {
    return items[0];
}
```

```python
# Python 3.12+（新語法，最簡潔）
def first[T](items: list[T]) -> T | None:
    return items[0] if items else None

# Python 3.11 及更早
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T | None:
    return items[0] if items else None

# 使用
first([1, 2, 3])        # 型別推斷為 int | None
first(["a", "b", "c"])  # 型別推斷為 str | None
```

### 泛型類別

```python
# Python 3.12+
class Stack[T]:
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

# Python 3.11 及更早
from typing import Generic, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

stack = Stack[int]()
stack.push(1)
stack.push(2)
```

### Protocol — 結構性型別（Duck Typing）

如同 TypeScript 的 interface（結構性型別匹配）：

```typescript
// TypeScript — 結構性型別
interface Printable {
    toString(): string;
}

function log(item: Printable) {
    console.log(item.toString());
}
```

```python
# Python — Protocol
from typing import Protocol

class Printable(Protocol):
    def to_string(self) -> str: ...

def log(item: Printable) -> None:
    print(item.to_string())

class User:
    def to_string(self) -> str:
        return "User(...)"

log(User())    # OK — User 實作了 to_string，不需要顯式繼承
```

### Literal — 字面量型別

```typescript
// TypeScript
type Direction = "north" | "south" | "east" | "west";
```

```python
# Python
from typing import Literal

Direction = Literal["north", "south", "east", "west"]

def move(direction: Direction) -> None:
    print(f"Moving {direction}")

move("north")    # OK
move("up")       # mypy 會報錯
```

### TypedDict — 有結構的字典

```typescript
// TypeScript
interface User {
    name: string;
    age: number;
    email?: string;
}
```

```python
# Python
from typing import TypedDict, NotRequired

class User(TypedDict):
    name: str
    age: int
    email: NotRequired[str]

user: User = {"name": "Alice", "age": 25}    # OK
```

## mypy — 靜態型別檢查

mypy 是 Python 的「TypeScript 編譯器」，在不執行程式碼的情況下檢查型別錯誤：

```bash
pip install mypy

# 檢查單一檔案
mypy main.py

# 檢查整個專案
mypy src/

# 嚴格模式
mypy --strict src/
```

### mypy 配置

```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false
```

### 常見 mypy 錯誤

```python
def greet(name: str) -> str:
    return f"Hello, {name}!"

greet(123)
# error: Argument 1 to "greet" has incompatible type "int"; expected "str"

x: int = "hello"
# error: Incompatible types in assignment (expression has type "str", variable has type "int")

def maybe_none() -> str | None:
    return None

result = maybe_none()
result.upper()
# error: Item "None" of "str | None" has no attribute "upper"

# 修正
if result is not None:
    result.upper()    # OK
```

## 漸進式採用

和 TypeScript 一樣，你可以漸進式地為現有 Python 專案加入型別提示：

1. **先從函數簽名開始** — 參數和回傳值
2. **再加關鍵變數** — 複雜的資料結構
3. **逐步開啟 mypy 嚴格模式**
4. **不需要一次全部加完** — `# type: ignore` 可以跳過特定行

```python
# 第一步：只標函數簽名
def process_order(order_id: int, items: list[dict]) -> bool:
    ...

# 第二步：細化型別
def process_order(order_id: int, items: list[OrderItem]) -> OrderResult:
    ...

# 第三步：加入泛型和 Protocol
def process[T: Processable](items: list[T]) -> ProcessResult[T]:
    ...
```

## 型別提示最佳實踐

1. **公開 API 一定要標型別** — 函數參數、回傳值、類別屬性
2. **局部變數通常不需要** — 型別推斷即可
3. **使用 `from __future__ import annotations`** — 讓型別標注延遲求值，提升效能
4. **善用 `TypeAlias`** — 為複雜型別取別名
5. **配合 IDE 使用** — VS Code + Pylance 提供即時型別檢查

```python
from __future__ import annotations
from typing import TypeAlias

# 為複雜型別取別名
JSON: TypeAlias = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
Middleware: TypeAlias = Callable[[Request, Response], Response]
```

## 恭喜完成！

你已經完成了整個 Python 學習文件的閱讀。回到 [README](../../README.md) 查看完整目錄，或挑選你感興趣的主題深入學習。
