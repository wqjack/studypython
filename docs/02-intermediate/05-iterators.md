# 迭代器與生成器

> 迭代器是 Python 的核心概念之一。如果你理解 Swift 的 Sequence/IteratorProtocol 或 JS 的 Iterator/Generator，這裡的概念會很熟悉。

## 可迭代物件 (Iterable)

能被 for-in 遍歷的就是可迭代物件：

```python
# 以下都是可迭代物件
for x in [1, 2, 3]: ...          # list
for x in (1, 2, 3): ...          # tuple
for x in {1, 2, 3}: ...          # set
for k, v in {"a": 1}.items(): ...# dict
for c in "hello": ...            # str
for line in open("file.txt"): ...# 檔案物件
for i in range(10): ...          # range
```

## 迭代器 (Iterator)

迭代器是實作了 `__iter__()` 和 `__next__()` 的物件：

```python
# 手動使用迭代器（平常不需要這樣做，但了解原理很重要）
numbers = [1, 2, 3]
it = iter(numbers)       # 取得迭代器
next(it)                 # 1
next(it)                 # 2
next(it)                 # 3
# next(it)               # StopIteration 例外

# for 迴圈本質上就是這樣做的：
it = iter(numbers)
while True:
    try:
        x = next(it)
        print(x)
    except StopIteration:
        break
```

### 自定義迭代器

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

for n in Countdown(5):
    print(n)    # 5, 4, 3, 2, 1
```

### 對比 Swift 的 Sequence

```swift
// Swift
struct Countdown: Sequence, IteratorProtocol {
    var current: Int
    mutating func next() -> Int? {
        guard current > 0 else { return nil }
        defer { current -= 1 }
        return current
    }
}

for n in Countdown(current: 5) {
    print(n)
}
```

## 生成器 (Generator) — Python 最強大的特色之一

生成器是用 `yield` 關鍵字定義的特殊函數，**惰性 (lazy)** 地產生值。

### 基本用法

```python
def countdown(start):
    while start > 0:
        yield start          # 暫停並回傳值
        start -= 1

# 使用方式和一般迭代器相同
for n in countdown(5):
    print(n)    # 5, 4, 3, 2, 1

# 手動控制
gen = countdown(3)
next(gen)    # 3（執行到 yield 暫停）
next(gen)    # 2（從上次暫停處繼續）
next(gen)    # 1
# next(gen)  # StopIteration
```

### 對比 JavaScript 的 Generator

```javascript
// JavaScript
function* countdown(start) {
    while (start > 0) {
        yield start;
        start--;
    }
}

for (const n of countdown(5)) {
    console.log(n);
}
```

```python
# Python — 幾乎一樣，只是沒有 function*
def countdown(start):
    while start > 0:
        yield start
        start -= 1

for n in countdown(5):
    print(n)
```

### 為什麼用生成器？

**記憶體效率：** 生成器不會一次產生所有值，而是按需計算。

```python
# 不好：一次建立整個列表，佔用大量記憶體
def get_squares_list(n):
    return [x ** 2 for x in range(n)]

# 好：生成器只在需要時計算，記憶體只用一個值的空間
def get_squares_gen(n):
    for x in range(n):
        yield x ** 2

# 處理 1000 萬筆資料
for sq in get_squares_gen(10_000_000):    # 記憶體幾乎不增加
    if sq > 1000:
        break
```

### 生成器表達式

List Comprehension 的惰性版本，用 `()` 取代 `[]`：

```python
# List Comprehension — 立即建立整個列表
squares_list = [x ** 2 for x in range(1000000)]    # 佔用大量記憶體

# Generator Expression — 惰性計算
squares_gen = (x ** 2 for x in range(1000000))     # 幾乎不佔記憶體

# 很多函數直接接受生成器
total = sum(x ** 2 for x in range(1000000))        # 不需要額外的括號
max_val = max(len(line) for line in open("data.txt"))
any_big = any(x > 100 for x in numbers)
```

### yield from — 委託生成器

```python
def flatten(nested_list):
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)   # 委託給子生成器
        else:
            yield item

list(flatten([1, [2, 3], [4, [5, 6]]]))
# [1, 2, 3, 4, 5, 6]
```

## 實用工具：itertools

`itertools` 是 Python 標準庫中的迭代工具箱，提供很多函數式操作：

```python
import itertools

# chain — 串接多個可迭代物件
list(itertools.chain([1, 2], [3, 4], [5]))
# [1, 2, 3, 4, 5]

# islice — 切片迭代器（不支援一般的 [start:stop] 語法）
list(itertools.islice(range(100), 5, 10))
# [5, 6, 7, 8, 9]

# zip_longest — 最長的那個為準（zip 是最短的）
list(itertools.zip_longest([1, 2], [3, 4, 5], fillvalue=0))
# [(1, 3), (2, 4), (0, 5)]

# product — 笛卡爾積（巢狀迴圈的簡化）
list(itertools.product("AB", "12"))
# [('A', '1'), ('A', '2'), ('B', '1'), ('B', '2')]

# groupby — 分組
data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(key, list(group))
# A [('A', 1), ('A', 2)]
# B [('B', 3), ('B', 4)]

# count — 無限計數器
for i in itertools.count(start=10, step=2):
    if i > 20:
        break
    print(i)    # 10, 12, 14, 16, 18, 20

# cycle — 無限循環
colors = itertools.cycle(["red", "green", "blue"])
for _, color in zip(range(7), colors):
    print(color)    # red, green, blue, red, green, blue, red
```

## 進階：生成器的 send / throw / close

```python
def accumulator():
    total = 0
    while True:
        value = yield total
        if value is None:
            break
        total += value

gen = accumulator()
next(gen)           # 0（初始化，執行到第一個 yield）
gen.send(10)        # 10（發送值給 yield 表達式）
gen.send(20)        # 30
gen.send(5)         # 35
```

## 下一步

進階篇完成！接下來進入 [實用篇 — 常用標準庫](../03-practical/01-stdlib.md)。
