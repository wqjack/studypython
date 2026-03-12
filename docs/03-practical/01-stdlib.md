# 常用標準庫

> Python 有「電池附帶 (batteries included)」的哲學，標準庫涵蓋範圍遠比 Swift 或 Node.js 的內建模組更廣。以下介紹最實用的模組。

## collections — 進階資料結構

### defaultdict

存取不存在的 key 時自動建立預設值，再也不用檢查 key 是否存在：

```python
from collections import defaultdict

# 普通 dict 要先檢查
word_count = {}
for word in words:
    if word not in word_count:
        word_count[word] = 0
    word_count[word] += 1

# defaultdict 更簡潔
word_count = defaultdict(int)    # 預設值為 0
for word in words:
    word_count[word] += 1

# 分組
groups = defaultdict(list)       # 預設值為 []
for item in items:
    groups[item.category].append(item)
```

### Counter

```python
from collections import Counter

# 計數（超常用）
text = "hello world"
Counter(text)        # Counter({'l': 3, 'o': 2, 'h': 1, 'e': 1, ...})

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counter = Counter(words)
counter.most_common(2)    # [('apple', 3), ('banana', 2)]
counter["apple"]          # 3
```

### namedtuple / deque

```python
from collections import namedtuple, deque

# namedtuple — 有名稱的 tuple（輕量級的 struct/class 替代）
Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
p.x    # 3
p.y    # 4

# deque — 雙端佇列（高效的頭尾操作）
d = deque([1, 2, 3])
d.appendleft(0)     # deque([0, 1, 2, 3])
d.popleft()          # 0 — O(1)，list 的 pop(0) 是 O(n)
d.rotate(1)          # deque([3, 0, 1, 2])
```

## datetime — 日期時間

```python
from datetime import datetime, date, timedelta, timezone

# 當前時間
now = datetime.now()                         # 本地時間
utc_now = datetime.now(timezone.utc)         # UTC 時間

# 建立日期
d = date(2024, 3, 15)
dt = datetime(2024, 3, 15, 10, 30, 0)

# 格式化（如同 DateFormatter）
now.strftime("%Y-%m-%d %H:%M:%S")     # "2024-03-15 10:30:00"
now.strftime("%Y年%m月%d日")            # "2024年03月15日"

# 解析字串
dt = datetime.strptime("2024-03-15", "%Y-%m-%d")

# 時間運算
tomorrow = date.today() + timedelta(days=1)
next_week = datetime.now() + timedelta(weeks=1)
diff = datetime(2024, 12, 31) - datetime(2024, 1, 1)
diff.days    # 365

# ISO 格式（Web API 常用）
now.isoformat()    # "2024-03-15T10:30:00"
datetime.fromisoformat("2024-03-15T10:30:00")
```

### 對比

| 操作 | Swift | JavaScript | Python |
|-----|-------|------------|--------|
| 當前時間 | `Date()` | `new Date()` | `datetime.now()` |
| 格式化 | `DateFormatter` | `Intl.DateTimeFormat` | `strftime()` |
| 時間差 | `TimeInterval` | 毫秒計算 | `timedelta` |

## re — 正規表達式

```python
import re

text = "Email: alice@example.com, bob@test.org"

# 搜尋第一個匹配
match = re.search(r"[\w.]+@[\w.]+", text)
if match:
    print(match.group())    # "alice@example.com"

# 搜尋所有匹配
emails = re.findall(r"[\w.]+@[\w.]+", text)
# ["alice@example.com", "bob@test.org"]

# 替換
cleaned = re.sub(r"\d+", "#", "Room 101, Floor 3")
# "Room #, Floor #"

# 分割
parts = re.split(r"[,;\s]+", "a, b; c d")
# ["a", "b", "c", "d"]

# 編譯（重複使用時效率更高）
email_pattern = re.compile(r"[\w.]+@[\w.]+")
email_pattern.findall(text)

# 命名群組
pattern = r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})"
match = re.match(pattern, "2024-03-15")
match.group("year")     # "2024"
match.group("month")    # "03"
```

## os / shutil — 系統操作

```python
import os
import shutil

# 環境變數（如同 process.env）
api_key = os.environ.get("API_KEY", "default_key")
os.environ["MY_VAR"] = "value"

# 目錄操作
os.makedirs("path/to/dir", exist_ok=True)    # mkdir -p
os.listdir(".")                               # 列出目錄
os.getcwd()                                   # 當前工作目錄

# 檔案操作
shutil.copy("src.txt", "dst.txt")             # 複製檔案
shutil.copytree("src_dir", "dst_dir")         # 複製目錄
shutil.move("old_path", "new_path")           # 移動/重命名
shutil.rmtree("dir_to_delete")               # 刪除目錄（rm -rf）
os.remove("file.txt")                         # 刪除檔案
```

> 推薦使用 `pathlib`（見 [檔案操作](../02-intermediate/04-file-io.md)）取代 `os.path` 的大部分功能。

## functools — 函數工具

```python
from functools import lru_cache, partial, reduce

# lru_cache — 自動快取函數結果（memoization）
@lru_cache(maxsize=128)
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

fibonacci(100)    # 瞬間完成（沒快取的話要算很久）

# partial — 部分套用（類似 JS 的 bind）
def power(base, exp):
    return base ** exp

square = partial(power, exp=2)
cube = partial(power, exp=3)
square(5)    # 25
cube(3)      # 27

# reduce — 累積計算
from functools import reduce
total = reduce(lambda acc, x: acc + x, [1, 2, 3, 4, 5])  # 15
```

## logging — 日誌

比 `print()` 更專業的日誌系統：

```python
import logging

# 基本設定
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

logger.debug("Debug message")       # 除錯資訊
logger.info("Server started")       # 一般資訊
logger.warning("Disk space low")    # 警告
logger.error("Connection failed")   # 錯誤
logger.critical("System crash!")    # 嚴重錯誤

# 帶變數的日誌（不要用 f-string，用 % 格式更高效）
logger.info("User %s logged in from %s", username, ip_address)
```

## hashlib / secrets — 加密與安全

```python
import hashlib
import secrets

# 雜湊
md5 = hashlib.md5(b"hello").hexdigest()
sha256 = hashlib.sha256(b"hello").hexdigest()

# 安全隨機（用於 token、密碼等）
token = secrets.token_hex(32)          # 64 字元的十六進位字串
url_token = secrets.token_urlsafe(32)  # URL 安全的 token
```

## argparse — 命令列參數

```python
import argparse

parser = argparse.ArgumentParser(description="My CLI tool")
parser.add_argument("input", help="Input file path")
parser.add_argument("-o", "--output", default="result.txt", help="Output file")
parser.add_argument("-v", "--verbose", action="store_true", help="Verbose mode")
parser.add_argument("-n", "--count", type=int, default=10, help="Number of items")

args = parser.parse_args()
print(args.input, args.output, args.verbose, args.count)
```

```bash
python script.py data.csv -o result.json -v -n 20
```

## 下一步

接下來看 [虛擬環境與套件管理](02-package-mgmt.md)。
