# 函數

> Python 的函數系統非常靈活，融合了 Swift 的命名參數和 JavaScript 的一等公民函數特性。

## 基本定義

```swift
// Swift
func greet(name: String) -> String {
    return "Hello, \(name)!"
}
```

```javascript
// JavaScript
function greet(name) {
    return `Hello, ${name}!`;
}
```

```python
# Python
def greet(name):
    return f"Hello, {name}!"
```

## 參數

### 預設參數值

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alice")              # "Hello, Alice!"
greet("Alice", "Hi")        # "Hi, Alice!"
```

### 關鍵字參數（Named Parameters）

你在 Swift 中一定很熟悉命名參數，Python 也支援：

```swift
// Swift — 命名參數是預設行為
func createUser(name: String, age: Int, role: String = "user") -> User
createUser(name: "Alice", age: 25, role: "admin")
```

```python
# Python — 可以用關鍵字方式呼叫
def create_user(name, age, role="user"):
    return {"name": name, "age": age, "role": role}

create_user("Alice", 25)                      # 位置參數
create_user("Alice", 25, role="admin")        # 混合使用
create_user(name="Alice", age=25)             # 全部用關鍵字
create_user(age=25, name="Alice")             # 關鍵字參數可以不按順序
```

### 強制關鍵字參數

```python
# * 後面的參數必須用關鍵字呼叫
def fetch_data(url, *, timeout=30, retry=3):
    pass

fetch_data("https://api.com")                         # OK
fetch_data("https://api.com", timeout=10)              # OK
# fetch_data("https://api.com", 10)                   # TypeError!

# / 前面的參數必須用位置呼叫（Python 3.8+）
def pow(base, exp, /):
    return base ** exp

pow(2, 10)          # OK
# pow(base=2, exp=10)  # TypeError!
```

### *args 和 **kwargs — 可變參數

```python
# *args — 接收任意數量的位置參數（打包成 tuple）
# 類似 Swift 的 variadic parameters 或 JS 的 ...rest
def sum_all(*numbers):
    return sum(numbers)

sum_all(1, 2, 3)        # 6
sum_all(1, 2, 3, 4, 5)  # 15

# **kwargs — 接收任意數量的關鍵字參數（打包成 dict）
def create_element(tag, **attrs):
    attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<{tag} {attr_str}>"

create_element("div", id="app", class_name="container")
# '<div id="app" class_name="container">'

# 組合使用
def api_request(method, url, *args, **kwargs):
    print(f"{method} {url}")
    print(f"args: {args}")
    print(f"kwargs: {kwargs}")
```

### 展開參數（Spread / Unpack）

```javascript
// JavaScript
const args = [1, 2, 3];
func(...args);

const options = { timeout: 30, retry: 3 };
fetch(url, { ...options });
```

```python
# Python — 用 * 和 ** 展開
args = [1, 2, 3]
sum_all(*args)              # 等於 sum_all(1, 2, 3)

options = {"timeout": 30, "retry": 3}
fetch_data(url, **options)  # 等於 fetch_data(url, timeout=30, retry=3)
```

## 回傳值

```python
# 回傳單一值
def square(x):
    return x ** 2

# 回傳多個值（自動打包成 tuple）
def divmod_custom(a, b):
    return a // b, a % b

quotient, remainder = divmod_custom(17, 5)   # 3, 2

# 沒有 return 或 return 沒有值 → 回傳 None
def log(msg):
    print(msg)
    # 隱式回傳 None
```

## Lambda — 匿名函數

```swift
// Swift closure
let double = { (x: Int) -> Int in x * 2 }
```

```javascript
// JavaScript arrow function
const double = (x) => x * 2;
```

```python
# Python lambda（只能是單一表達式）
double = lambda x: x * 2
double(5)    # 10

# 常用於排序、高階函數
users = [("Alice", 25), ("Bob", 30), ("Charlie", 20)]
users.sort(key=lambda user: user[1])     # 按年齡排序

# 等價的完整寫法
def get_age(user):
    return user[1]
users.sort(key=get_age)
```

> **注意：** Python 的 lambda 功能比 Swift closure 和 JS arrow function 弱很多，只能寫一行表達式。複雜邏輯請用 `def` 定義具名函數。

## 高階函數

Python 的函數是一等公民（first-class），可以當參數傳遞、當回傳值，這點和 Swift / JS 一樣：

```python
# 函數當參數（回呼 callback）
def apply(func, value):
    return func(value)

apply(str.upper, "hello")     # "HELLO"
apply(lambda x: x ** 2, 5)   # 25

# 函數當回傳值（工廠模式）
def make_multiplier(factor):
    def multiply(x):
        return x * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
double(5)    # 10
triple(5)    # 15

# 內建高階函數
numbers = [1, 2, 3, 4, 5]

list(map(lambda x: x ** 2, numbers))       # [1, 4, 9, 16, 25]
list(filter(lambda x: x > 3, numbers))     # [4, 5]

from functools import reduce
reduce(lambda acc, x: acc + x, numbers)    # 15

# 但 Pythonic 的寫法是用 Comprehension
[x ** 2 for x in numbers]                  # 比 map 更慣用
[x for x in numbers if x > 3]             # 比 filter 更慣用
sum(numbers)                               # 比 reduce 更直覺
```

## 閉包 (Closure)

和 Swift / JS 一樣，Python 函數可以捕獲外部變數：

```python
def counter():
    count = 0
    def increment():
        nonlocal count   # 必須宣告 nonlocal 才能修改外部變數
        count += 1
        return count
    return increment

c = counter()
c()    # 1
c()    # 2
c()    # 3
```

> **注意 `nonlocal`：** Swift 的 closure 自動捕獲（capture）外部變數，JS 也是。但 Python 的內部函數**讀取**外部變數沒問題，**修改**則需要 `nonlocal` 宣告。

## 裝飾器簡介

裝飾器是 Python 的語法糖，用來包裝函數。概念類似 TypeScript 的裝飾器或 Swift 的 property wrapper：

```python
# 基本概念：裝飾器就是一個接收函數、回傳函數的高階函數
def log_call(func):
    def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    return wrapper

@log_call                # 語法糖，等於 greet = log_call(greet)
def greet(name):
    return f"Hello, {name}!"

greet("Alice")
# Calling greet
# Result: Hello, Alice!
```

> 裝飾器的完整介紹在 [進階主題 - 裝飾器](../05-advanced/01-decorators.md)。

## 文件字串 (Docstring)

```python
def calculate_bmi(weight: float, height: float) -> float:
    """計算 BMI 指數。

    Args:
        weight: 體重（公斤）
        height: 身高（公尺）

    Returns:
        BMI 指數值

    Raises:
        ValueError: 如果身高為零
    """
    if height == 0:
        raise ValueError("Height cannot be zero")
    return weight / (height ** 2)

# 查看文件
help(calculate_bmi)
print(calculate_bmi.__doc__)
```

## 下一步

基礎篇完成！接下來進入 [進階篇 — 物件導向程式設計](../02-intermediate/01-oop.md)。
