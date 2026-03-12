# REST API 開發

> 身為 Web 開發者，你一定寫過很多 REST API。本章介紹用 Python 建構生產級 API 的最佳實踐，以及更現代的 FastAPI 框架。

## FastAPI — 現代化 Python API 框架

FastAPI 是近年最受歡迎的 Python Web 框架，特色是**自動型別驗證**和**自動生成 API 文件**：

```bash
pip install fastapi uvicorn
```

### Hello World

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# 執行
# uvicorn main:app --reload
```

### 為什麼選 FastAPI？

| 特性 | Express.js | Flask | FastAPI |
|-----|-----------|-------|---------|
| 型別驗證 | 手動 / Joi | 手動 / Marshmallow | **自動**（Pydantic） |
| API 文件 | Swagger（手動） | Swagger（手動） | **自動生成** |
| 非同步 | 原生 | 需要擴充 | **原生** |
| 效能 | 高 | 中 | **高**（接近 Node.js） |
| 型別提示 | TypeScript | 不支援 | **完整支援** |

### 自動型別驗證（Pydantic）

如果你喜歡 TypeScript 的型別安全或 Swift 的 Codable，你會愛上這個：

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

app = FastAPI()

# 定義資料模型（如同 TypeScript interface + 驗證）
class UserCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    age: int
    created_at: datetime

# 請求 body 自動驗證
@app.post("/users", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    # user 已經通過型別驗證，不需要手動檢查
    return {
        "id": 1,
        "name": user.name,
        "email": user.email,
        "age": user.age,
        "created_at": datetime.now()
    }
```

### 對比 TypeScript 的型別驗證

```typescript
// TypeScript + Zod
const UserSchema = z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    age: z.number().int().min(0).max(150),
});

type User = z.infer<typeof UserSchema>;
```

```python
# Python + Pydantic（FastAPI 內建）
class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    age: int = Field(ge=0, le=150)
```

### 路徑參數 + 查詢參數

```python
from typing import Optional

@app.get("/users/{user_id}")
def get_user(user_id: int):                    # 路徑參數，自動轉型
    return {"id": user_id}

@app.get("/users")
def list_users(
    page: int = 1,                              # 查詢參數
    limit: int = 10,
    search: Optional[str] = None,
    sort_by: str = "created_at"
):
    return {"page": page, "limit": limit, "search": search}
```

### 依賴注入

FastAPI 的依賴注入系統非常強大：

```python
from fastapi import Depends, Header, HTTPException

# 驗證 Token
def get_current_user(authorization: str = Header()):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid token")
    token = authorization.split(" ")[1]
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return user

# 使用依賴注入
@app.get("/me")
def read_current_user(user=Depends(get_current_user)):
    return user

@app.get("/my-orders")
def read_my_orders(user=Depends(get_current_user)):
    return {"user": user.name, "orders": []}
```

### 自動生成 API 文件

啟動 FastAPI 後，自動獲得：
- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`
- **OpenAPI JSON:** `http://localhost:8000/openapi.json`

不需要額外配置！

## 生產級 API 結構

```
my_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 設定
│   ├── database.py          # 資料庫連線
│   ├── models/              # SQLAlchemy 模型
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas/             # Pydantic 模型（請求/回應）
│   │   ├── __init__.py
│   │   └── user.py
│   ├── routers/             # 路由（Blueprint/Router）
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── users.py
│   ├── services/            # 業務邏輯
│   │   ├── __init__.py
│   │   └── user_service.py
│   └── middleware/           # 中介軟體
│       ├── __init__.py
│       └── auth.py
├── tests/
│   └── test_users.py
├── pyproject.toml
└── Dockerfile
```

### main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, users

app = FastAPI(
    title="My API",
    description="My awesome API",
    version="1.0.0"
)

# CORS（跨域請求）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 註冊路由
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(users.router, prefix="/api/users", tags=["users"])

@app.get("/health")
def health_check():
    return {"status": "ok"}
```

### routers/users.py

```python
from fastapi import APIRouter, Depends, HTTPException
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def list_users(page: int = 1, limit: int = 20):
    return UserService.get_users(page=page, limit=limit)

@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user: UserCreate):
    return UserService.create_user(user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    user = UserService.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## 測試 API

```python
# tests/test_users.py
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/api/users", json={
        "name": "Alice",
        "email": "alice@example.com",
        "age": 25
    })
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"

def test_get_user_not_found():
    response = client.get("/api/users/999")
    assert response.status_code == 404
```

```bash
# 執行測試
pip install pytest
pytest tests/ -v
```

## 部署

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY pyproject.toml .
RUN pip install .
COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
# 本地執行
uvicorn app.main:app --reload --port 8000

# 生產環境
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 下一步

Web 開發篇完成！接下來進入 [進階主題 — 裝飾器](../05-advanced/01-decorators.md)。
