# 資料型別

> Python 是**動態型別**但**強型別**的語言。動態型別像 JavaScript（不需要宣告型別），強型別像 Swift（不會自動隱式轉換）。

## 型別系統對比

| 特性 | Swift | JavaScript | Python |
|-----|-------|------------|--------|
| 型別宣告 | 必須（可推斷） | 不需要 | 不需要（可選標注） |
| 型別檢查時機 | 編譯期 | 執行期 | 執行期 |
| 隱式轉換 | 不允許 | 大量自動轉換 | 不允許 |

```python
# Python 是強型別 — 不像 JS 會自動轉換
"age: " + 25        # TypeError! 不會像 JS 自動轉成 "age: 25"
"age: " + str(25)   # 正確："age: 25"

# 但 Python 是動態型別 — 變數可以改變型別
x = 42              # x 是 int
x = "hello"         # x 現在是 str（Swift 不允許這樣做）
```

## 基本型別

### 數字

```python
# 整數（int）— 沒有大小限制！（不像 Swift 的 Int64 或 JS 的 Number）
big_num = 999_999_999_999_999_999   # 底線分隔增加可讀性
count = 42

# 浮點數（float）
pi = 3.14159
price = 19.99

# 布林（bool）— 注意首字母大寫
is_active = True     # Swift: true / JS: true
is_deleted = False   # Swift: false / JS: false

# 型別轉換（明確的，不像 JS 隱式轉換）
int("42")       # 42
float("3.14")   # 3.14
str(42)         # "42"
bool(0)         # False
bool("")        # False
bool([])        # False — 空集合都是 falsy
```

### Truthy / Falsy 值

Python 和 JavaScript 一樣有 truthy/falsy 的概念：

```python
# Falsy 值（以下在 if 判斷中等同 False）
False
None
0, 0.0
"", '', """"""     # 空字串
[], (), {}         # 空集合
set()

# 其他所有東西都是 Truthy

# 實用場景（和 JS 很像）
items = []
if not items:       # JS: if (!items.length)
    print("List is empty")
```

## 集合型別

### List — 對應 Swift Array / JS Array

Python 的 `list` 就是你熟悉的陣列：

```python
# 建立
fruits = ["apple", "banana", "cherry"]
mixed = [1, "hello", True, 3.14]      # 可以混合型別（像 JS，不像 Swift）
empty = []

# 存取
fruits[0]           # "apple"
fruits[-1]          # "cherry"（負數索引 = 從後面數）
fruits[1:3]         # ["banana", "cherry"]（切片 slice）

# 修改
fruits.append("date")          # 新增到末尾（JS: push）
fruits.insert(0, "avocado")   # 插入到指定位置
fruits.extend(["fig", "grape"])  # 合併（JS: concat / spread）
fruits.pop()                   # 移除最後一個（同 JS）
fruits.remove("banana")        # 移除指定值
del fruits[0]                  # 移除指定索引

# 常用操作
len(fruits)         # 長度（JS: .length / Swift: .count）
"apple" in fruits   # 成員檢測（JS: includes / Swift: contains）
fruits.sort()       # 原地排序
sorted(fruits)      # 回傳新排序列表（不改原本的）
fruits.reverse()    # 原地反轉

# List Comprehension — Python 最強大的特色之一
# 相當於 Swift 的 .map/.filter 或 JS 的 .map().filter()
numbers = [1, 2, 3, 4, 5]

squares = [x ** 2 for x in numbers]                    # [1, 4, 9, 16, 25]
evens = [x for x in numbers if x % 2 == 0]            # [2, 4]
doubled_evens = [x * 2 for x in numbers if x % 2 == 0] # [4, 8]
```

#### 對比 map/filter

```swift
// Swift
let squares = numbers.map { $0 * $0 }
let evens = numbers.filter { $0 % 2 == 0 }
```

```javascript
// JavaScript
const squares = numbers.map(x => x ** 2);
const evens = numbers.filter(x => x % 2 === 0);
```

```python
# Python — List Comprehension（更 Pythonic）
squares = [x ** 2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]

# Python 也有 map/filter，但 List Comprehension 更慣用
squares = list(map(lambda x: x ** 2, numbers))
evens = list(filter(lambda x: x % 2 == 0, numbers))
```

### Tuple — 不可變的 List

```python
# 類似 Swift 的 Tuple
point = (3, 4)
rgb = (255, 128, 0)

x, y = point         # 解構
print(point[0])       # 3

# Tuple 不可修改（和 Swift 的 let array 類似的概念）
# point[0] = 5       # TypeError!

# 常用場景：函數回傳多個值
def get_user():
    return "Alice", 25    # 自動打包成 tuple

name, age = get_user()    # 自動解構
```

### Dict — 對應 Swift Dictionary / JS Object

```python
# 建立（就像 JS 的 Object，但 key 必須是不可變型別）
user = {
    "name": "Alice",
    "age": 25,
    "skills": ["Python", "Swift"]
}

# 存取
user["name"]            # "Alice"（如果 key 不存在會報 KeyError）
user.get("name")        # "Alice"（安全存取）
user.get("email", "")   # ""（key 不存在時的預設值，類似 JS 的 ?? ""）

# 修改
user["email"] = "alice@example.com"    # 新增 / 修改
del user["age"]                        # 刪除
user.update({"age": 26, "city": "Taipei"})  # 批量更新（如同 Object.assign）

# 常用操作
"name" in user          # True（檢查 key 是否存在）
user.keys()             # dict_keys(["name", "skills", "email", ...])
user.values()           # dict_values([...])
user.items()            # dict_items([("name", "Alice"), ...])（key-value pairs）
len(user)               # key 的數量

# Dict Comprehension
prices = {"apple": 30, "banana": 15, "cherry": 50}
expensive = {k: v for k, v in prices.items() if v > 20}
# {"apple": 30, "cherry": 50}

# 合併字典（Python 3.9+）
defaults = {"theme": "light", "lang": "en"}
overrides = {"lang": "zh-TW", "font_size": 14}
config = defaults | overrides    # {"theme": "light", "lang": "zh-TW", "font_size": 14}
```

### Set — 集合（無序、不重複）

```python
# 類似 Swift 的 Set
tags = {"python", "web", "api"}
empty_set = set()       # 注意：{} 是空 dict，不是空 set

# 操作
tags.add("database")
tags.remove("web")       # 不存在會報錯
tags.discard("web")      # 不存在也不報錯（更安全）

# 集合運算
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b        # {1, 2, 3, 4, 5, 6}  聯集
a & b        # {3, 4}              交集
a - b        # {1, 2}              差集
a ^ b        # {1, 2, 5, 6}        對稱差集

# 實用：去除重複
numbers = [1, 2, 2, 3, 3, 3]
unique = list(set(numbers))    # [1, 2, 3]
```

## 型別檢查

```python
# 檢查型別
type(42)                    # <class 'int'>
type("hello")               # <class 'str'>
isinstance(42, int)          # True
isinstance(42, (int, float)) # True（多型別檢查）

# 對比
# Swift: is 關鍵字 + 編譯期檢查
# JS: typeof / instanceof
# Python: type() / isinstance()
```

## 可變 vs 不可變

這是 Python 很重要的概念，和 Swift 的 value type / reference type 有點像：

| 不可變 (Immutable) | 可變 (Mutable) |
|--------------------|---------------|
| `int`, `float`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `frozenset` | `bytearray` |

```python
# 不可變：修改會建立新物件
a = "hello"
b = a
a = a.upper()     # a 指向新物件 "HELLO"，b 仍然是 "hello"

# 可變：修改會影響同一物件
a = [1, 2, 3]
b = a              # b 和 a 指向同一個 list!
a.append(4)
print(b)           # [1, 2, 3, 4] — b 也被改了！

# 如果要複製 list
b = a.copy()       # 淺拷貝
b = a[:]           # 也是淺拷貝
import copy
b = copy.deepcopy(a)  # 深拷貝
```

## 下一步

接下來學習 [流程控制](04-control-flow.md)。
