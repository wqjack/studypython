# 環境設置與開發工具

> 就像 iOS 開發需要 Xcode、Web 開發需要 Node.js 一樣，Python 開發也有自己的一套工具鏈。

## 安裝 Python

### macOS

macOS 內建的 Python 版本通常較舊，建議用 Homebrew 安裝：

```bash
brew install python@3.12
```

驗證安裝：

```bash
python3 --version   # Python 3.12.x
pip3 --version      # pip 24.x
```

### Windows

從 [python.org](https://www.python.org/downloads/) 下載安裝，記得勾選 **Add Python to PATH**。

### Linux

```bash
sudo apt update && sudo apt install python3 python3-pip python3-venv
```

## 對比你熟悉的工具

| 用途 | iOS (Swift) | Web (JS/TS) | Python |
|-----|-------------|-------------|--------|
| 語言版本管理 | Xcode 內建 | nvm | pyenv |
| 套件管理 | SPM / CocoaPods | npm / yarn | pip / poetry |
| 專案隔離 | Xcode Project | node_modules | venv |
| REPL | Swift Playground | Node REPL / 瀏覽器 Console | python3 REPL / IPython |
| 程式碼格式化 | SwiftFormat | Prettier | Black / Ruff |
| 靜態檢查 | Swift 編譯器 | ESLint / TSC | mypy / Ruff |

## 虛擬環境（相當於 node_modules 的隔離機制）

在 Web 開發中，每個專案的 `node_modules` 讓依賴彼此隔離。Python 的等價方案是**虛擬環境 (venv)**：

```bash
# 建立虛擬環境（就像 npm init 建立 package.json）
python3 -m venv .venv

# 啟用虛擬環境
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 啟用後，終端機提示會出現 (.venv)
(.venv) $ python --version
(.venv) $ pip install requests   # 安裝套件到虛擬環境

# 退出虛擬環境
deactivate
```

### 依賴檔案對比

```bash
# Web: package.json → package-lock.json
# Python 等價做法：
pip freeze > requirements.txt          # 匯出依賴
pip install -r requirements.txt        # 安裝依賴（如同 npm install）
```

## 推薦開發工具

### 編輯器

- **VS Code + Python 擴充套件** — 最多人使用，你做 Web 開發已經很熟了
- **Cursor** — 內建 AI 輔助，基於 VS Code
- **PyCharm** — 專業 Python IDE（類比 Xcode 之於 Swift）

### VS Code 必裝擴充套件

| 擴充套件 | 用途 |
|---------|------|
| Python (ms-python) | 語法高亮、IntelliSense、除錯 |
| Pylance | 型別檢查（類似 TypeScript 的效果） |
| Ruff | 程式碼格式化與 Lint（類似 ESLint + Prettier） |
| Jupyter | 互動式筆記本（資料分析常用） |

### VS Code settings.json 推薦設定

```json
{
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff",
    "editor.formatOnSave": true,
    "editor.codeActionsOnSave": {
      "source.fixAll": "explicit",
      "source.organizeImports": "explicit"
    }
  },
  "python.analysis.typeCheckingMode": "basic"
}
```

## 第一支 Python 程式

```python
# hello.py
print("Hello, Python!")       # 不需要分號，不需要 main 函數
```

```bash
python3 hello.py
# 輸出：Hello, Python!
```

### 對比三種語言的 Hello World

```swift
// Swift
print("Hello, Swift!")
```

```javascript
// JavaScript
console.log("Hello, JavaScript!");
```

```python
# Python
print("Hello, Python!")
```

## 互動式環境 (REPL)

Python 的 REPL 非常強大，類似 Swift Playground 或瀏覽器的 Console：

```bash
$ python3
>>> 2 + 3
5
>>> "hello".upper()
'HELLO'
>>> exit()
```

進階版可以安裝 **IPython**：

```bash
pip install ipython
ipython    # 有語法高亮、自動補全、魔術命令
```

## 下一步

環境搭好了，接著來看 [基本語法](02-syntax.md)。
