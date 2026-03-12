# 虛擬環境與套件管理

> 如果你用過 npm/yarn 管理 Node.js 套件，或用 CocoaPods/SPM 管理 iOS 依賴，Python 的套件管理概念相同，工具選擇更多。

## 概念對照

| 概念 | npm (Node.js) | CocoaPods (iOS) | Python |
|-----|---------------|-----------------|--------|
| 套件管理器 | npm / yarn | pod | pip / poetry |
| 依賴描述檔 | package.json | Podfile | requirements.txt / pyproject.toml |
| 鎖定檔 | package-lock.json | Podfile.lock | requirements.txt（精確版本）/ poetry.lock |
| 專案隔離 | node_modules（自動） | — | venv（手動建立） |
| 套件倉庫 | npmjs.com | CocoaPods Trunk | pypi.org |
| 執行指令 | npx | — | pipx |

## venv — 虛擬環境

### 為什麼需要虛擬環境？

Node.js 的 `node_modules` 自動在專案目錄下隔離依賴。Python 預設會把套件裝到全域，所以需要手動建立虛擬環境來隔離。

```bash
# 建立虛擬環境
python3 -m venv .venv

# 啟用
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 確認啟用成功
which python       # 應顯示 .venv 內的路徑
pip list           # 乾淨的環境，只有 pip 和 setuptools

# 安裝套件
pip install requests flask

# 匯出依賴（如同 npm shrinkwrap）
pip freeze > requirements.txt

# 退出
deactivate
```

### requirements.txt

```
# requirements.txt（如同 package.json 的 dependencies）
requests==2.31.0
flask==3.0.0
sqlalchemy>=2.0,<3.0
python-dotenv~=1.0.0
```

```bash
# 從 requirements.txt 安裝（如同 npm install）
pip install -r requirements.txt
```

### .gitignore

```gitignore
# 虛擬環境不要加入版本控制（如同 node_modules/）
.venv/
__pycache__/
*.pyc
.env
```

## pyproject.toml — 現代化專案設定

`pyproject.toml` 是 Python 的新標準設定檔，相當於 `package.json`：

```toml
[project]
name = "my-project"
version = "1.0.0"
description = "My awesome project"
requires-python = ">=3.10"
dependencies = [
    "requests>=2.28",
    "flask>=3.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.0",
    "ruff>=0.1",
    "mypy>=1.0",
]

[project.scripts]
my-cli = "my_project.cli:main"

[tool.ruff]
line-length = 88

[tool.mypy]
strict = true
```

## Poetry — 推薦的套件管理工具

Poetry 是 Python 的「npm」，提供完整的依賴管理體驗：

```bash
# 安裝 Poetry
pip install poetry

# 建立新專案（如同 npm init）
poetry new my-project
# 或在現有目錄初始化
poetry init

# 新增依賴（如同 npm install xxx）
poetry add requests
poetry add flask sqlalchemy

# 新增開發依賴（如同 npm install --save-dev）
poetry add --group dev pytest ruff mypy

# 移除依賴
poetry remove requests

# 安裝所有依賴（如同 npm install）
poetry install

# 更新依賴（如同 npm update）
poetry update

# 執行指令（如同 npx / npm run）
poetry run python main.py
poetry run pytest

# 進入虛擬環境 shell
poetry shell
```

### Poetry 的 pyproject.toml

```toml
[tool.poetry]
name = "my-project"
version = "0.1.0"
description = ""
authors = ["Alice <alice@example.com>"]

[tool.poetry.dependencies]
python = "^3.10"
requests = "^2.31"
flask = "^3.0"

[tool.poetry.group.dev.dependencies]
pytest = "^7.4"
ruff = "^0.1"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 常見操作對照

| 操作 | npm | Poetry | pip |
|-----|-----|--------|-----|
| 初始化專案 | `npm init` | `poetry init` | — |
| 安裝所有依賴 | `npm install` | `poetry install` | `pip install -r requirements.txt` |
| 新增套件 | `npm install X` | `poetry add X` | `pip install X` |
| 移除套件 | `npm uninstall X` | `poetry remove X` | `pip uninstall X` |
| 更新套件 | `npm update` | `poetry update` | `pip install --upgrade X` |
| 執行腳本 | `npm run X` / `npx X` | `poetry run X` | — |
| 列出套件 | `npm list` | `poetry show` | `pip list` |
| 鎖定版本 | `package-lock.json` | `poetry.lock` | `pip freeze` |

## pyenv — Python 版本管理

如同 Node.js 的 nvm：

```bash
# 安裝 pyenv
brew install pyenv    # macOS

# 安裝 Python 版本
pyenv install 3.12.0
pyenv install 3.11.6

# 設定全域版本
pyenv global 3.12.0

# 設定專案版本（在專案目錄下）
pyenv local 3.11.6    # 建立 .python-version 檔案
```

## 推薦的專案結構

```
my-project/
├── pyproject.toml           # 專案設定（package.json）
├── poetry.lock              # 鎖定版本（package-lock.json）
├── README.md
├── .gitignore
├── .env                     # 環境變數
├── src/
│   └── my_project/
│       ├── __init__.py
│       ├── main.py
│       ├── models/
│       │   ├── __init__.py
│       │   └── user.py
│       ├── services/
│       │   ├── __init__.py
│       │   └── auth.py
│       └── utils/
│           ├── __init__.py
│           └── helpers.py
└── tests/
    ├── __init__.py
    ├── test_main.py
    └── test_models/
        └── test_user.py
```

## 下一步

接下來看 [網路請求](03-networking.md)。
