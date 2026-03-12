# 模組與套件

> Python 的模組系統對應 Swift 的 import framework 和 JavaScript 的 import/require。概念相同，語法略有不同。

## 對比匯入方式

| 操作 | Swift | JavaScript (ES6) | Python |
|-----|-------|------------------|--------|
| 匯入整個模組 | `import UIKit` | `import * as fs from 'fs'` | `import os` |
| 匯入特定項目 | 不支援 | `import { useState } from 'react'` | `from os import path` |
| 別名 | 不支援 | `import { x as y }` | `import numpy as np` |
| 相對匯入 | 不適用 | `import { x } from './utils'` | `from . import utils` |

## 基本匯入

```python
# 匯入整個模組
import os
import json
os.path.join("/home", "user")
json.dumps({"key": "value"})

# 匯入特定項目（推薦，更清晰）
from os.path import join, exists
from json import dumps, loads
join("/home", "user")

# 別名匯入（常見於長名或慣例）
import numpy as np
import pandas as pd
from datetime import datetime as dt

# 匯入所有（不推薦，會污染命名空間）
from os.path import *    # 避免使用
```

## 自己寫模組

在 Python 中，**每個 .py 檔案就是一個模組**。這比 Swift（需要 framework/module map）和 JS（需要 export）更簡單。

### 目錄結構

```
my_project/
├── main.py
├── utils.py              # 模組
├── models/               # 套件（Package）
│   ├── __init__.py       # 標記這是一個套件（可以為空）
│   ├── user.py
│   └── product.py
└── services/
    ├── __init__.py
    ├── auth.py
    └── payment.py
```

### 定義模組

```python
# utils.py
def format_price(price):
    return f"${price:,.2f}"

def validate_email(email):
    return "@" in email

PI = 3.14159

class Calculator:
    pass
```

### 使用模組

```python
# main.py
import utils
utils.format_price(1234.5)    # "$1,234.50"

from utils import format_price, validate_email
format_price(1234.5)

from models.user import User
from services.auth import login
```

## 套件 (Package)

套件就是包含 `__init__.py` 的目錄，等同於把多個模組組織在一起。

### `__init__.py` 的作用

```python
# models/__init__.py — 可以控制從套件匯入時暴露哪些東西

# 方式 1：重新匯出（簡化使用者的 import 路徑）
from .user import User
from .product import Product

# 使用者就可以：
# from models import User, Product
# 而不需要：
# from models.user import User

# 方式 2：定義 __all__ 控制 from package import * 的行為
__all__ = ["User", "Product"]
```

### 對比 JavaScript 的 index.js

```javascript
// JavaScript — index.js 的重新匯出模式
// models/index.js
export { User } from './user.js';
export { Product } from './product.js';
```

```python
# Python — __init__.py 的重新匯出模式
# models/__init__.py
from .user import User
from .product import Product
```

## 相對匯入 vs 絕對匯入

```python
# 假設結構：
# project/
# ├── services/
# │   ├── __init__.py
# │   ├── auth.py
# │   └── payment.py
# └── models/
#     ├── __init__.py
#     └── user.py

# 在 services/auth.py 中：

# 絕對匯入（推薦）
from models.user import User
from services.payment import process_payment

# 相對匯入
from .payment import process_payment     # 同套件
from ..models.user import User           # 上一層套件
```

## `if __name__ == "__main__"`

這是 Python 的慣例，用來區分「被匯入」和「直接執行」：

```python
# utils.py
def greet(name):
    return f"Hello, {name}!"

# 只有直接執行 python utils.py 時才會跑
# 被其他檔案 import utils 時不會跑
if __name__ == "__main__":
    print(greet("World"))
    print("Running tests...")
```

這有點類似 Swift 的 `@main` 或 Node.js 判斷 `require.main === module`。

## 常見標準庫模組

Python 的「電池附帶 (batteries included)」哲學讓標準庫非常豐富：

```python
import os           # 作業系統操作（檔案系統、環境變數等）
import sys          # Python 直譯器相關
import json         # JSON 處理
import re           # 正規表達式
import datetime     # 日期時間
import pathlib      # 現代化路徑操作
import collections  # 進階資料結構
import itertools    # 迭代工具
import functools    # 函數工具（reduce、cache 等）
import typing       # 型別提示
import unittest     # 單元測試
import logging      # 日誌
import argparse     # 命令列參數解析
import http.server  # 簡易 HTTP 伺服器
import sqlite3      # SQLite 資料庫
import hashlib      # 雜湊
import secrets      # 安全隨機數
```

## 第三方套件

使用 pip 安裝（如同 npm install）：

```bash
pip install requests           # 安裝單一套件
pip install flask sqlalchemy   # 安裝多個套件
pip install requests==2.31.0   # 指定版本
pip install "requests>=2.20"   # 版本範圍

pip list                       # 列出已安裝（npm list）
pip show requests              # 套件資訊
pip uninstall requests         # 移除套件
```

> 更完整的套件管理說明見 [虛擬環境與套件管理](../03-practical/02-package-mgmt.md)。

## 下一步

接下來看 [錯誤處理](03-error-handling.md)。
