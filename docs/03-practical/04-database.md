# 資料庫操作

> 如果你在 iOS 開發中用過 Core Data / Realm，或在 Web 開發中用過 Sequelize / Prisma / TypeORM，Python 也有對應的 ORM 和原生資料庫操作方式。

## 工具對照

| 用途 | iOS | Web (Node.js) | Python |
|-----|-----|---------------|--------|
| 嵌入式 DB | Core Data / SQLite | SQLite / LevelDB | sqlite3（內建） |
| ORM | Core Data / Realm | Sequelize / Prisma | SQLAlchemy / Django ORM |
| 遷移工具 | Core Data Migration | Prisma Migrate | Alembic |
| NoSQL | — | Mongoose (MongoDB) | PyMongo / Motor |
| 連線池 | — | pg pool | SQLAlchemy |

## SQLite — 內建的嵌入式資料庫

Python 內建 sqlite3 模組，不需要安裝任何東西：

```python
import sqlite3

# 連線（檔案不存在會自動建立）
conn = sqlite3.connect("app.db")
# conn = sqlite3.connect(":memory:")  # 記憶體資料庫（測試用）

# 設定 Row factory（讓查詢結果可以用欄位名稱存取）
conn.row_factory = sqlite3.Row

cursor = conn.cursor()

# 建立表格
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE,
        age INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

# 新增資料（使用參數化查詢防止 SQL Injection）
cursor.execute(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    ("Alice", "alice@example.com", 25)
)

# 批次新增
users = [
    ("Bob", "bob@example.com", 30),
    ("Charlie", "charlie@example.com", 35),
]
cursor.executemany(
    "INSERT INTO users (name, email, age) VALUES (?, ?, ?)",
    users
)

# 查詢
cursor.execute("SELECT * FROM users WHERE age > ?", (25,))
rows = cursor.fetchall()
for row in rows:
    print(row["name"], row["email"], row["age"])

# 查詢單筆
cursor.execute("SELECT * FROM users WHERE id = ?", (1,))
user = cursor.fetchone()

# 更新
cursor.execute("UPDATE users SET age = ? WHERE name = ?", (26, "Alice"))

# 刪除
cursor.execute("DELETE FROM users WHERE name = ?", ("Bob",))

# 提交交易（重要！不 commit 就不會存入）
conn.commit()

# 關閉連線
conn.close()
```

### 使用 Context Manager

```python
import sqlite3

def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn

# 使用 with 確保正確關閉
with get_db() as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
```

## SQLAlchemy — Python 最強大的 ORM

SQLAlchemy 是 Python 生態系中最流行的 ORM，類似 Sequelize / Prisma：

```bash
pip install sqlalchemy
```

### 定義模型

```python
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)
    age = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="author")

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}')>"

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(String)
    author_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    author = relationship("User", back_populates="posts")
```

### 對比 Sequelize (Node.js)

```javascript
// Sequelize
const User = sequelize.define('User', {
    name: { type: DataTypes.STRING, allowNull: false },
    email: { type: DataTypes.STRING, unique: true },
    age: DataTypes.INTEGER,
});
```

```python
# SQLAlchemy
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(200), unique=True)
    age = Column(Integer)
```

### CRUD 操作

```python
# 建立引擎和 Session
engine = create_engine("sqlite:///app.db", echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# 新增
with Session() as session:
    user = User(name="Alice", email="alice@example.com", age=25)
    session.add(user)
    session.commit()

# 查詢
with Session() as session:
    # 查詢所有
    users = session.query(User).all()

    # 條件查詢
    user = session.query(User).filter_by(name="Alice").first()
    user = session.query(User).filter(User.age > 25).all()

    # 排序 + 分頁
    users = (
        session.query(User)
        .order_by(User.created_at.desc())
        .offset(0)
        .limit(10)
        .all()
    )

    # 關聯查詢
    user = session.query(User).filter_by(id=1).first()
    for post in user.posts:
        print(post.title)

# 更新
with Session() as session:
    user = session.query(User).filter_by(id=1).first()
    user.age = 26
    session.commit()

# 刪除
with Session() as session:
    user = session.query(User).filter_by(id=1).first()
    session.delete(user)
    session.commit()
```

### SQLAlchemy 2.0 新語法

```python
from sqlalchemy import select, insert, update, delete

with Session() as session:
    # 新語法：用 select() 取代 session.query()
    stmt = select(User).where(User.age > 25).order_by(User.name)
    users = session.scalars(stmt).all()

    # 帶條件的更新
    stmt = update(User).where(User.name == "Alice").values(age=26)
    session.execute(stmt)

    # 帶條件的刪除
    stmt = delete(User).where(User.age < 18)
    session.execute(stmt)

    session.commit()
```

## 連接其他資料庫

SQLAlchemy 支援多種資料庫，只需要換連線字串：

```python
# SQLite
engine = create_engine("sqlite:///app.db")

# PostgreSQL
engine = create_engine("postgresql://user:password@localhost:5432/mydb")

# MySQL
engine = create_engine("mysql+pymysql://user:password@localhost:3306/mydb")

# 非同步（搭配 asyncio）
from sqlalchemy.ext.asyncio import create_async_engine
engine = create_async_engine("sqlite+aiosqlite:///app.db")
```

## Redis（快取 / Session）

```bash
pip install redis
```

```python
import redis
import json

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

# 基本操作
r.set("key", "value")
r.get("key")                          # "value"
r.set("key", "value", ex=3600)        # 1 小時過期

# 存 JSON
r.set("user:1", json.dumps({"name": "Alice", "age": 25}))
user = json.loads(r.get("user:1"))

# 列表
r.lpush("queue", "task1", "task2")
r.rpop("queue")    # "task1"

# 雜湊
r.hset("user:1", mapping={"name": "Alice", "age": 25})
r.hgetall("user:1")    # {"name": "Alice", "age": "25"}
```

## 下一步

實用篇完成！接下來進入 [Web 開發篇 — Flask 入門](../04-web-dev/01-flask.md)。
