# 流程控制

> Python 的流程控制和 Swift / JS 非常相似，主要差異在於語法格式（縮排取代大括號）和一些 Python 獨有的語法糖。

## 條件判斷

### if / elif / else

```swift
// Swift
if score >= 90 {
    print("A")
} else if score >= 80 {
    print("B")
} else {
    print("C")
}
```

```javascript
// JavaScript
if (score >= 90) {
    console.log("A");
} else if (score >= 80) {
    console.log("B");
} else {
    console.log("C");
}
```

```python
# Python — 注意 elif 不是 else if
if score >= 90:
    print("A")
elif score >= 80:
    print("B")
else:
    print("C")
```

### 三元運算子

```swift
// Swift
let label = score >= 60 ? "Pass" : "Fail"
```

```javascript
// JavaScript
const label = score >= 60 ? "Pass" : "Fail";
```

```python
# Python — 可讀性更好的語法
label = "Pass" if score >= 60 else "Fail"
```

### match-case（Python 3.10+ 的 Pattern Matching）

類似 Swift 的 `switch-case`：

```swift
// Swift
switch statusCode {
case 200:
    print("OK")
case 404:
    print("Not Found")
case 500...599:
    print("Server Error")
default:
    print("Unknown")
}
```

```python
# Python 3.10+
match status_code:
    case 200:
        print("OK")
    case 404:
        print("Not Found")
    case code if 500 <= code <= 599:    # guard 條件
        print("Server Error")
    case _:                              # 預設（同 default）
        print("Unknown")

# 進階：解構 matching（非常像 Swift 的 pattern matching）
match point:
    case (0, 0):
        print("Origin")
    case (x, 0):
        print(f"On x-axis at {x}")
    case (0, y):
        print(f"On y-axis at {y}")
    case (x, y):
        print(f"Point at ({x}, {y})")
```

## 迴圈

### for 迴圈

Python 的 `for` 是 **for-in** 迴圈，和 Swift 的 `for-in` 概念一樣，沒有 C 風格的 `for(i=0; i<n; i++)`：

```python
# 遍歷列表
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# 帶索引遍歷（類似 Swift 的 enumerated()）
for index, fruit in enumerate(fruits):
    print(f"{index}: {fruit}")
# 0: apple
# 1: banana
# 2: cherry

# 指定起始索引
for index, fruit in enumerate(fruits, start=1):
    print(f"{index}: {fruit}")

# 數字範圍（類似 Swift 的 0..<10）
for i in range(5):           # 0, 1, 2, 3, 4
    print(i)

for i in range(2, 8):        # 2, 3, 4, 5, 6, 7
    print(i)

for i in range(0, 10, 2):    # 0, 2, 4, 6, 8（步長為 2）
    print(i)

# 遍歷字典
user = {"name": "Alice", "age": 25}
for key in user:                          # 只遍歷 key
    print(key)

for key, value in user.items():           # 遍歷 key-value
    print(f"{key}: {value}")

# 同時遍歷多個列表（zip）
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]
for name, score in zip(names, scores):
    print(f"{name}: {score}")
```

### while 迴圈

```python
count = 0
while count < 5:
    print(count)
    count += 1     # Python 沒有 ++ 運算子！

# 無限迴圈
while True:
    user_input = input("Enter command (q to quit): ")
    if user_input == "q":
        break
```

### break / continue / else

```python
# break 和 continue 和其他語言一樣
for i in range(10):
    if i == 3:
        continue    # 跳過 3
    if i == 7:
        break       # 在 7 停止
    print(i)        # 0, 1, 2, 4, 5, 6

# Python 獨有：for-else / while-else
# else 區塊在迴圈「正常結束」（沒有 break）時執行
for item in items:
    if item == target:
        print("Found!")
        break
else:
    # 只有在 for 迴圈「沒有」被 break 中斷時才會執行
    print("Not found")

# 等價於其他語言的寫法：
found = False
for item in items:
    if item == target:
        print("Found!")
        found = True
        break
if not found:
    print("Not found")
```

## 推導式 (Comprehension)

這是 Python 最具特色的功能之一，用一行取代 map/filter 的組合：

```python
# List Comprehension
numbers = [1, 2, 3, 4, 5]

# 基本形式：[表達式 for 變數 in 可迭代物件]
squares = [x ** 2 for x in numbers]          # [1, 4, 9, 16, 25]

# 加條件：[表達式 for 變數 in 可迭代物件 if 條件]
even_squares = [x ** 2 for x in numbers if x % 2 == 0]   # [4, 16]

# 巢狀迴圈
pairs = [(x, y) for x in range(3) for y in range(3)]
# [(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)]

# Dict Comprehension
word_lengths = {word: len(word) for word in ["hello", "world", "python"]}
# {"hello": 5, "world": 5, "python": 6}

# Set Comprehension
unique_lengths = {len(word) for word in ["hello", "world", "python"]}
# {5, 6}
```

### 對比三種語言

```swift
// Swift
let squares = numbers.map { $0 * $0 }
let evens = numbers.filter { $0 % 2 == 0 }
let evenSquares = numbers.filter { $0 % 2 == 0 }.map { $0 * $0 }
```

```javascript
// JavaScript
const squares = numbers.map(x => x ** 2);
const evens = numbers.filter(x => x % 2 === 0);
const evenSquares = numbers.filter(x => x % 2 === 0).map(x => x ** 2);
```

```python
# Python
squares = [x ** 2 for x in numbers]
evens = [x for x in numbers if x % 2 == 0]
even_squares = [x ** 2 for x in numbers if x % 2 == 0]
```

## 海象運算子 `:=`（Python 3.8+）

在表達式中同時賦值和使用，減少重複計算：

```python
# 沒有海象運算子
data = get_data()
if data:
    process(data)

# 使用海象運算子
if data := get_data():
    process(data)

# 在 while 中特別有用
while chunk := file.read(1024):
    process(chunk)

# 在 List Comprehension 中避免重複計算
results = [y for x in data if (y := expensive_calc(x)) > threshold]
```

## 下一步

了解了流程控制，接著來看 [函數](05-functions.md)。
