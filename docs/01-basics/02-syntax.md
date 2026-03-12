# 基本語法 — 對比 Swift / JavaScript

> Python 的語法設計哲學是「可讀性優先」，如果你習慣了 Swift 的簡潔或 JS 的靈活，Python 會讓你覺得更加直白。

## 最大的不同：縮排取代大括號

Python 用**縮排**來定義程式碼區塊，而不是 `{}` 大括號。這是從其他語言轉來最需要適應的地方。

```swift
// Swift — 用大括號
if score > 60 {
    print("Pass")
} else {
    print("Fail")
}
```

```javascript
// JavaScript — 用大括號
if (score > 60) {
    console.log("Pass");
} else {
    console.log("Fail");
}
```

```python
# Python — 用縮排（4 個空格）
if score > 60:
    print("Pass")
else:
    print("Fail")
```

### 縮排規則

- 統一使用 **4 個空格**（不要用 Tab）
- 同一區塊的縮排必須一致
- 冒號 `:` 表示下一行要開始新的縮排區塊

## 變數宣告

### Swift

```swift
let name: String = "Alice"    // 不可變
var age: Int = 25              // 可變
```

### JavaScript

```javascript
const name = "Alice";          // 不可變
let age = 25;                  // 可變
```

### Python

```python
name = "Alice"    # 直接賦值，不需要 let/var/const
age = 25          # 所有變數都可重新賦值

# Python 沒有「常數」關鍵字，慣例用全大寫表示常數
MAX_RETRY = 3     # 約定俗成，實際上仍可修改
```

**重點差異：**
- Python 不需要宣告關鍵字（`let`、`var`、`const`）
- Python 不需要型別標注（但可以加，見 [型別提示](../05-advanced/03-type-hints.md)）
- Python 不需要分號結尾

## 命名慣例

| 用途 | Swift | JavaScript | Python |
|-----|-------|------------|--------|
| 變數/函數 | camelCase | camelCase | snake_case |
| 類別 | PascalCase | PascalCase | PascalCase |
| 常數 | camelCase | UPPER_SNAKE | UPPER_SNAKE |
| 私有 | `private` 關鍵字 | `#field` / `_` 慣例 | `_` 前綴慣例 |
| 檔案名 | PascalCase.swift | camelCase.js | snake_case.py |

```python
# Python 命名範例
user_name = "Alice"          # 變數：snake_case
MAX_CONNECTIONS = 100        # 常數：UPPER_SNAKE_CASE

def calculate_total():       # 函數：snake_case
    pass

class ShoppingCart:           # 類別：PascalCase
    pass

_internal_cache = {}          # 私有慣例：底線前綴
```

## 註解

```python
# 單行註解（和 Swift、JS 的 // 一樣的概念）

"""
多行註解 / 文件字串（docstring）
類似 Swift 的 /// 或 JS 的 /** */
"""

def greet(name: str) -> str:
    """回傳問候語。這是函數的 docstring。"""
    return f"Hello, {name}!"
```

## 字串

### 字串插值對比

```swift
// Swift
let msg = "Hello, \(name)! You are \(age) years old."
```

```javascript
// JavaScript
const msg = `Hello, ${name}! You are ${age} years old.`;
```

```python
# Python — f-string（Python 3.6+，最推薦）
msg = f"Hello, {name}! You are {age} years old."

# 也支援表達式
msg = f"Next year you'll be {age + 1}."
```

### 常用字串操作

```python
s = "Hello, World!"

s.upper()              # "HELLO, WORLD!"
s.lower()              # "hello, world!"
s.split(", ")          # ["Hello", "World!"]
s.replace("World", "Python")  # "Hello, Python!"
s.startswith("Hello")  # True
s.strip()              # 去除前後空白（如同 JS 的 trim()）
len(s)                 # 13（長度用內建函數，不是 .length 屬性）

# 多行字串
poem = """
    Roses are red,
    Violets are blue,
    Python is great,
    And so are you.
"""
```

## 印出（Print）

```python
print("Hello")                    # 基本輸出
print("a", "b", "c")             # a b c（自動用空格分隔）
print("a", "b", sep=", ")        # a, b（自訂分隔符）
print("no newline", end="")      # 不換行
print(f"{name=}")                 # name='Alice'（除錯用，Python 3.8+）
```

## 運算子

大部分和 Swift / JS 相同，以下列出**不同的地方**：

```python
# 整數除法
10 / 3      # 3.3333...（普通除法，同 JS）
10 // 3     # 3（整數除法，Swift 的 Int 除法效果）
10 % 3      # 1（取餘，三種語言皆同）
2 ** 10     # 1024（次方，JS 也是 **，Swift 沒有這個運算子）

# 邏輯運算子 — 用英文單字而非符號
True and False    # Swift/JS: true && false
True or False     # Swift/JS: true || false
not True          # Swift: !true / JS: !true

# 比較
x == y       # 值比較（同 Swift ==，同 JS ===）
x is y       # 身份比較（同 JS 的 Object.is()，比較記憶體位址）
x != y       # 不等於
x is not y   # 身份不等於
```

## None — Python 的 null

```python
# Swift: nil
# JS: null / undefined
# Python: None

result = None

if result is None:      # 用 is 而不是 ==
    print("No result")

if result is not None:
    print(f"Got: {result}")
```

## 多重賦值

Python 支援非常靈活的賦值方式，這在 Swift 和 JS 中需要解構：

```python
# 同時賦值多個變數
x, y, z = 1, 2, 3

# 交換變數（不需要暫存變數！）
x, y = y, x

# 解構（類似 JS 的 destructuring）
first, *rest = [1, 2, 3, 4]    # first=1, rest=[2, 3, 4]
first, *_, last = [1, 2, 3, 4] # first=1, last=4
```

## 下一步

了解了基本語法，接著來看 [資料型別](03-data-types.md)。
