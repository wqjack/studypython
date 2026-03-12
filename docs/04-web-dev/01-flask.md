# Flask 入門

> Flask 是 Python 最受歡迎的輕量級 Web 框架，如果你用過 Express.js (Node.js) 或 Vapor (Swift)，Flask 的概念會非常熟悉。

## 框架對照

| 特性 | Express.js | Vapor (Swift) | Flask | Django |
|-----|-----------|---------------|-------|--------|
| 定位 | 輕量、靈活 | 輕量、型別安全 | 輕量、靈活 | 全功能、約定優於配置 |
| 路由 | `app.get()` | `app.get()` | `@app.route()` | `urls.py` |
| 模板 | EJS / Pug | Leaf | Jinja2 | Django Template |
| ORM | Sequelize | Fluent | SQLAlchemy | Django ORM |
| 學習曲線 | 低 | 中 | 低 | 中高 |

## 安裝

```bash
pip install flask
```

## Hello World

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

```bash
python app.py
# * Running on http://127.0.0.1:5000
```

### 對比 Express.js

```javascript
// Express.js
const express = require('express');
const app = express();

app.get('/', (req, res) => {
    res.send('Hello, World!');
});

app.listen(3000);
```

```python
# Flask — 幾乎一樣的概念，用裝飾器取代 app.get()
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

app.run(port=3000)
```

## 路由

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

# 基本路由
@app.route("/")
def index():
    return "Home page"

# 路徑參數（Express: /users/:id）
@app.route("/users/<int:user_id>")
def get_user(user_id):
    return f"User {user_id}"

# 多種 HTTP 方法
@app.route("/users", methods=["GET", "POST"])
def users():
    if request.method == "GET":
        return jsonify({"users": []})
    elif request.method == "POST":
        data = request.json
        return jsonify(data), 201

# 更簡潔的寫法（Flask 2.0+）
@app.get("/items")
def list_items():
    return jsonify({"items": []})

@app.post("/items")
def create_item():
    data = request.json
    return jsonify(data), 201
```

### 路徑參數型別

```python
@app.route("/users/<int:id>")          # 整數
@app.route("/posts/<slug>")            # 字串（預設）
@app.route("/files/<path:filepath>")   # 路徑（含 /）
@app.route("/price/<float:amount>")    # 浮點數
```

## Request 物件

```python
from flask import request

@app.route("/search")
def search():
    # 查詢參數（Express: req.query）
    keyword = request.args.get("q", "")
    page = request.args.get("page", 1, type=int)

    return jsonify({"keyword": keyword, "page": page})

@app.route("/users", methods=["POST"])
def create_user():
    # JSON body（Express: req.body — 需要 body-parser）
    data = request.json          # Flask 自動解析
    name = data.get("name")

    # 表單資料
    # name = request.form.get("name")

    # 檔案上傳
    # file = request.files.get("avatar")

    # 請求標頭（Express: req.headers）
    auth = request.headers.get("Authorization")

    return jsonify({"name": name}), 201
```

## Response

```python
from flask import jsonify, make_response, redirect, abort

# 回傳 JSON（最常見）
@app.route("/api/data")
def get_data():
    return jsonify({"status": "ok", "data": [1, 2, 3]})

# 自定義狀態碼
@app.route("/api/create")
def create():
    return jsonify({"id": 1}), 201

# 自定義標頭
@app.route("/api/custom")
def custom():
    response = make_response(jsonify({"data": "value"}))
    response.headers["X-Custom-Header"] = "my-value"
    return response

# 重新導向
@app.route("/old-page")
def old_page():
    return redirect("/new-page")

# 回傳錯誤
@app.route("/api/users/<int:id>")
def get_user(id):
    user = find_user(id)
    if not user:
        abort(404)    # 直接回傳 404
    return jsonify(user)
```

## 中介軟體 (Middleware)

```python
# Flask 的中介軟體用 before_request / after_request
# 類似 Express 的 app.use()

@app.before_request
def log_request():
    print(f"{request.method} {request.path}")

@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response

# 錯誤處理
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500
```

## Blueprint — 模組化路由

類似 Express 的 Router：

```javascript
// Express Router
const router = express.Router();
router.get('/', (req, res) => { ... });
app.use('/api/users', router);
```

```python
# Flask Blueprint
from flask import Blueprint

# users.py
users_bp = Blueprint("users", __name__, url_prefix="/api/users")

@users_bp.route("/")
def list_users():
    return jsonify({"users": []})

@users_bp.route("/<int:id>")
def get_user(id):
    return jsonify({"id": id, "name": "Alice"})

# app.py
from users import users_bp
app.register_blueprint(users_bp)
```

## 模板渲染

```python
from flask import render_template

@app.route("/profile/<name>")
def profile(name):
    return render_template("profile.html", name=name, age=25)
```

```html
<!-- templates/profile.html（Jinja2 模板，語法類似 Handlebars） -->
<!DOCTYPE html>
<html>
<body>
    <h1>Hello, {{ name }}!</h1>
    {% if age >= 18 %}
        <p>You are an adult.</p>
    {% else %}
        <p>You are a minor.</p>
    {% endif %}

    <ul>
    {% for item in items %}
        <li>{{ item }}</li>
    {% endfor %}
    </ul>
</body>
</html>
```

## 完整範例：TODO API

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

todos = []
next_id = 1

@app.get("/api/todos")
def list_todos():
    return jsonify(todos)

@app.post("/api/todos")
def create_todo():
    global next_id
    data = request.json
    todo = {
        "id": next_id,
        "title": data["title"],
        "completed": False
    }
    todos.append(todo)
    next_id += 1
    return jsonify(todo), 201

@app.put("/api/todos/<int:todo_id>")
def update_todo(todo_id):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        return jsonify({"error": "Not found"}), 404
    data = request.json
    todo.update(data)
    return jsonify(todo)

@app.delete("/api/todos/<int:todo_id>")
def delete_todo(todo_id):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)
```

## 下一步

接下來看 [REST API 開發](02-rest-api.md)。
