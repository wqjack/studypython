# 檔案操作

> 在 iOS 開發中你用 FileManager，Web 開發中 Node.js 用 fs 模組，Python 有內建的 open() 和現代化的 pathlib。

## 讀寫檔案

### 基本讀取

```python
# 讀取整個檔案
with open("data.txt", "r", encoding="utf-8") as f:
    content = f.read()          # 整個檔案內容（字串）

# 逐行讀取
with open("data.txt") as f:
    lines = f.readlines()       # 列表：["line1\n", "line2\n", ...]

# 逐行迭代（記憶體效率最佳，適合大檔案）
with open("data.txt") as f:
    for line in f:
        print(line.strip())     # strip() 去除換行符號

# 讀取為列表（去除換行）
with open("data.txt") as f:
    lines = [line.strip() for line in f]
```

### 對比 Node.js

```javascript
// Node.js
const fs = require('fs');

// 同步讀取
const content = fs.readFileSync('data.txt', 'utf-8');

// 非同步讀取
const content = await fs.promises.readFile('data.txt', 'utf-8');
```

```python
# Python — 預設就是同步的
with open("data.txt", encoding="utf-8") as f:
    content = f.read()
```

### 寫入檔案

```python
# 寫入（覆蓋）
with open("output.txt", "w", encoding="utf-8") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")

# 附加
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("New log entry\n")

# 寫入多行
lines = ["line 1", "line 2", "line 3"]
with open("output.txt", "w") as f:
    f.writelines(line + "\n" for line in lines)

# 更簡潔：用 print 寫入
with open("output.txt", "w") as f:
    print("Hello, World!", file=f)
    print("Second line", file=f)
```

### 開啟模式

| 模式 | 說明 |
|-----|------|
| `"r"` | 讀取（預設） |
| `"w"` | 寫入（覆蓋） |
| `"a"` | 附加 |
| `"x"` | 建立（檔案已存在則報錯） |
| `"b"` | 二進位模式（如 `"rb"`, `"wb"`） |
| `"t"` | 文字模式（預設，如 `"rt"` 同 `"r"`） |
| `"+"` | 讀寫（如 `"r+"`） |

## pathlib — 現代化路徑操作

`pathlib` 是 Python 3.4+ 的路徑操作模組，比 `os.path` 更直覺：

```python
from pathlib import Path

# 建立路徑
p = Path("/Users/alice/project")
p = Path.home() / "project"          # 用 / 運算子組合路徑！
p = Path.cwd()                        # 當前目錄

# 路徑操作
file_path = Path("/Users/alice/project/data/report.csv")
file_path.name          # "report.csv"
file_path.stem          # "report"
file_path.suffix        # ".csv"
file_path.parent        # Path("/Users/alice/project/data")
file_path.parents[1]    # Path("/Users/alice/project")

# 路徑查詢
file_path.exists()      # True/False
file_path.is_file()     # True/False
file_path.is_dir()      # True/False

# 讀寫（Python 3.5+）
content = Path("data.txt").read_text(encoding="utf-8")
Path("output.txt").write_text("Hello!", encoding="utf-8")
data = Path("image.png").read_bytes()
Path("copy.png").write_bytes(data)
```

### 遍歷目錄

```python
from pathlib import Path

project = Path("./my_project")

# 列出目錄內容
for item in project.iterdir():
    print(item.name, "dir" if item.is_dir() else "file")

# Glob 模式匹配（類似終端機的 *.py）
for py_file in project.glob("*.py"):          # 當前目錄的 .py 檔
    print(py_file)

for py_file in project.rglob("*.py"):         # 遞迴搜尋所有 .py 檔
    print(py_file)

# 建立目錄
Path("output/reports").mkdir(parents=True, exist_ok=True)
```

### 對比三種語言的路徑操作

```swift
// Swift (iOS)
let fm = FileManager.default
let docs = fm.urls(for: .documentDirectory, in: .userDomainMask)[0]
let filePath = docs.appendingPathComponent("data.json")
let exists = fm.fileExists(atPath: filePath.path)
```

```javascript
// Node.js
const path = require('path');
const filePath = path.join(__dirname, 'data', 'report.csv');
const exists = fs.existsSync(filePath);
```

```python
# Python
from pathlib import Path
file_path = Path(__file__).parent / "data" / "report.csv"
exists = file_path.exists()
```

## JSON 檔案操作

身為 Web / iOS 開發者，你一定經常處理 JSON：

```python
import json
from pathlib import Path

# 解析 JSON 字串（如同 JSON.parse / JSONDecoder）
data = json.loads('{"name": "Alice", "age": 25}')

# 轉為 JSON 字串（如同 JSON.stringify / JSONEncoder）
json_str = json.dumps(data, indent=2, ensure_ascii=False)

# 讀取 JSON 檔案
with open("config.json", encoding="utf-8") as f:
    config = json.load(f)      # 注意：load（不是 loads）

# 寫入 JSON 檔案
with open("config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

# 更簡潔的寫法（pathlib）
config = json.loads(Path("config.json").read_text())
Path("config.json").write_text(json.dumps(config, indent=2))
```

### 對比

| 操作 | JavaScript | Swift | Python |
|-----|-----------|-------|--------|
| 字串→物件 | `JSON.parse(str)` | `JSONDecoder().decode(T.self, from: data)` | `json.loads(str)` |
| 物件→字串 | `JSON.stringify(obj)` | `JSONEncoder().encode(obj)` | `json.dumps(obj)` |
| 檔案→物件 | `JSON.parse(fs.readFileSync(...))` | — | `json.load(file)` |
| 物件→檔案 | `fs.writeFileSync(..., JSON.stringify(...))` | — | `json.dump(obj, file)` |

## CSV 檔案

```python
import csv

# 讀取 CSV
with open("data.csv", encoding="utf-8") as f:
    reader = csv.DictReader(f)    # 每一行是 dict
    for row in reader:
        print(row["name"], row["age"])

# 寫入 CSV
data = [
    {"name": "Alice", "age": 25},
    {"name": "Bob", "age": 30},
]

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(data)
```

## 暫存檔案

```python
import tempfile

# 建立暫存檔案
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
    f.write("temp data")
    print(f.name)    # /tmp/tmp_xxx.txt

# 建立暫存目錄
with tempfile.TemporaryDirectory() as tmpdir:
    print(tmpdir)    # /tmp/tmp_xxx
    # tmpdir 在 with 區塊結束後自動刪除
```

## 下一步

接下來看 [迭代器與生成器](05-iterators.md)。
