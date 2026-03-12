# 物件導向程式設計 (OOP)

> 如果你熟悉 Swift 的 class/struct/protocol 或 JavaScript 的 class/prototype，Python 的 OOP 會很容易上手。主要差異在於 Python 更靈活（也更自由）。

## Class 基本定義

### 三種語言對比

```swift
// Swift
class User {
    let name: String
    var age: Int

    init(name: String, age: Int) {
        self.name = name
        self.age = age
    }

    func greet() -> String {
        return "Hi, I'm \(name)"
    }
}

let user = User(name: "Alice", age: 25)
```

```javascript
// JavaScript
class User {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    greet() {
        return `Hi, I'm ${this.name}`;
    }
}

const user = new User("Alice", 25);
```

```python
# Python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        return f"Hi, I'm {self.name}"

user = User("Alice", 25)    # 不需要 new 關鍵字！
```

### 關鍵差異

| 特性 | Swift | JavaScript | Python |
|-----|-------|------------|--------|
| 建構子 | `init()` | `constructor()` | `__init__()` |
| 自身引用 | `self`（隱式） | `this`（隱式） | `self`（**顯式**傳入） |
| 實例化 | `User()` | `new User()` | `User()` |
| 屬性宣告 | 在 class 中宣告 | constructor 中 | `__init__` 中 |

> **重點：** Python 的 `self` 必須作為每個實例方法的第一個參數，這是和 Swift / JS 最大的不同。

## 屬性存取控制

Python 沒有 `private` / `public` / `protected` 關鍵字，用命名慣例表達：

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner            # 公開屬性
        self._balance = balance       # 慣例：_ 前綴 = 受保護（protected）
        self.__pin = "1234"           # 名稱修飾：__ 前綴 = 模擬私有

    def get_balance(self):
        return self._balance

account = BankAccount("Alice", 1000)
account.owner           # "Alice" — 正常存取
account._balance        # 1000 — 可以存取，但慣例上不應該
# account.__pin         # AttributeError — 無法直接存取
account._BankAccount__pin  # "1234" — 但其實還是可以繞過...
```

### Property — 優雅的 getter/setter

類似 Swift 的 computed property：

```swift
// Swift
class Circle {
    var radius: Double
    var area: Double {
        return .pi * radius * radius
    }
}
```

```python
# Python — 用 @property 裝飾器
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(c.radius)      # 5（呼叫 getter）
print(c.area)         # 78.54...（computed property）
c.radius = 10         # 呼叫 setter
# c.radius = -1       # ValueError!
```

## 繼承

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError    # 抽象方法

class Dog(Animal):                    # 繼承語法：class 子類(父類)
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

dog = Dog("Buddy")
dog.speak()    # "Buddy says Woof!"

# 檢查繼承關係
isinstance(dog, Dog)      # True
isinstance(dog, Animal)   # True
issubclass(Dog, Animal)   # True
```

### super() — 呼叫父類方法

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, name, salary, department):
        super().__init__(name, salary)    # 呼叫父類的 __init__
        self.department = department

# 對比 Swift: super.init(name: name, salary: salary)
# 對比 JS: super(name, salary)
```

### 多重繼承

Python 支援多重繼承（Swift 和 JS 都不支援 class 多重繼承）：

```python
class Flyable:
    def fly(self):
        return "Flying!"

class Swimmable:
    def swim(self):
        return "Swimming!"

class Duck(Flyable, Swimmable):    # 多重繼承
    def quack(self):
        return "Quack!"

duck = Duck()
duck.fly()      # "Flying!"
duck.swim()     # "Swimming!"
duck.quack()    # "Quack!"
```

> **MRO (Method Resolution Order):** Python 用 C3 線性化演算法解決多重繼承的方法衝突。可用 `Duck.__mro__` 查看。

## 抽象類別 / 協議

### Swift 用 protocol，Python 用 ABC

```swift
// Swift
protocol Drawable {
    func draw()
}

class Circle: Drawable {
    func draw() { ... }
}
```

```python
# Python — 用 ABC (Abstract Base Class)
from abc import ABC, abstractmethod

class Drawable(ABC):
    @abstractmethod
    def draw(self):
        pass

class Circle(Drawable):
    def draw(self):
        print("Drawing circle")

# d = Drawable()    # TypeError! 不能實例化抽象類別
c = Circle()        # OK
```

### Python 3.8+ Protocol（結構性型別，更像 TypeScript interface）

```python
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("Drawing circle")

def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())    # OK — Circle 實作了 draw()，不需要顯式繼承
```

## 魔術方法 (Dunder Methods)

Python 的魔術方法（雙底線方法）讓你自定義物件的行為，類似 Swift 的 protocol conformance：

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 字串表示（如同 Swift 的 CustomStringConvertible）
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    # 運算子重載（如同 Swift 的 static func +）
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # 相等比較（如同 Swift 的 Equatable）
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    # 可雜湊（如同 Swift 的 Hashable）
    def __hash__(self):
        return hash((self.x, self.y))

    # 長度
    def __len__(self):
        return 2

    # 索引存取
    def __getitem__(self, index):
        return (self.x, self.y)[index]

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)      # (4, 6)
print(v1 * 3)       # (3, 6)
print(v1 == Vector(1, 2))  # True
```

### 常用魔術方法速查

| 魔術方法 | 用途 | Swift 等價 |
|---------|------|-----------|
| `__init__` | 建構子 | `init` |
| `__str__` | 使用者友好的字串 | `description` |
| `__repr__` | 開發者友好的字串 | `debugDescription` |
| `__eq__` | `==` 比較 | `Equatable` |
| `__hash__` | 雜湊值 | `Hashable` |
| `__len__` | `len()` | `count` |
| `__getitem__` | `obj[key]` 存取 | `subscript` |
| `__iter__` | for-in 迭代 | `Sequence` |
| `__enter__/__exit__` | with 語句 | 無直接等價 |
| `__call__` | 將實例當函數呼叫 | `callAsFunction` |

## dataclass — 快速建立資料模型

類似 Swift 的 struct 自動合成的 init / Equatable：

```swift
// Swift struct 自動獲得 memberwise init
struct User {
    let name: String
    let age: Int
}
```

```python
# Python dataclass（Python 3.7+）
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    email: str = ""    # 預設值

user = User("Alice", 25)
print(user)             # User(name='Alice', age=25, email='')
user == User("Alice", 25)  # True — 自動生成 __eq__

# 不可變版本（類似 Swift 的 let）
@dataclass(frozen=True)
class Point:
    x: float
    y: float
```

## 類別方法與靜態方法

```python
class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    # 實例方法 — 需要 self
    def format(self):
        return f"{self.year}-{self.month:02d}-{self.day:02d}"

    # 類別方法 — 接收 cls（類別本身），常用於工廠模式
    # 類似 Swift 的 convenience init 或 JS 的 static factory method
    @classmethod
    def from_string(cls, date_str):
        year, month, day = map(int, date_str.split("-"))
        return cls(year, month, day)

    # 靜態方法 — 不接收 self 或 cls，只是邏輯上屬於這個類別
    @staticmethod
    def is_valid(year, month, day):
        return 1 <= month <= 12 and 1 <= day <= 31

d = Date.from_string("2024-03-15")
Date.is_valid(2024, 13, 1)    # False
```

## 下一步

了解了 OOP，接著看 [模組與套件](02-modules.md)。
