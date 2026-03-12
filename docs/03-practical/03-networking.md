# 網路請求

> 身為 iOS / Web 開發者，你一定非常熟悉 HTTP 請求。Swift 用 URLSession/Alamofire，JavaScript 用 fetch/axios，Python 用 requests/httpx。

## requests — 最受歡迎的 HTTP 庫

```bash
pip install requests
```

### 基本用法

```python
import requests

# GET 請求
response = requests.get("https://api.github.com/users/octocat")
response.status_code      # 200
response.json()           # 自動解析 JSON
response.text             # 原始文字
response.headers          # 回應標頭

# 帶查詢參數
response = requests.get(
    "https://api.example.com/users",
    params={"page": 1, "limit": 20}    # ?page=1&limit=20
)
```

### 對比三種語言

```swift
// Swift (URLSession)
let url = URL(string: "https://api.github.com/users/octocat")!
let (data, response) = try await URLSession.shared.data(from: url)
let user = try JSONDecoder().decode(User.self, from: data)
```

```javascript
// JavaScript (fetch)
const response = await fetch("https://api.github.com/users/octocat");
const user = await response.json();
```

```python
# Python (requests)
import requests
response = requests.get("https://api.github.com/users/octocat")
user = response.json()
```

### POST / PUT / DELETE

```python
import requests

# POST — 送出 JSON
response = requests.post(
    "https://api.example.com/users",
    json={"name": "Alice", "age": 25},     # 自動序列化為 JSON
    headers={"Authorization": "Bearer token123"}
)

# POST — 表單資料
response = requests.post(
    "https://api.example.com/login",
    data={"username": "alice", "password": "secret"}
)

# PUT
response = requests.put(
    "https://api.example.com/users/1",
    json={"name": "Alice Updated"}
)

# DELETE
response = requests.delete("https://api.example.com/users/1")

# PATCH
response = requests.patch(
    "https://api.example.com/users/1",
    json={"age": 26}
)
```

### 錯誤處理

```python
import requests

try:
    response = requests.get("https://api.example.com/data", timeout=10)
    response.raise_for_status()    # 如果狀態碼是 4xx/5xx 就丟出例外
    data = response.json()
except requests.exceptions.Timeout:
    print("Request timed out")
except requests.exceptions.ConnectionError:
    print("Connection error")
except requests.exceptions.HTTPError as e:
    print(f"HTTP error: {e.response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"Request error: {e}")
```

### Session — 持久連線

類似 URLSession 的 session 概念：

```python
import requests

session = requests.Session()

# 設定共用標頭（類似 URLSession 的 configuration）
session.headers.update({
    "Authorization": "Bearer token123",
    "Content-Type": "application/json"
})

# 之後的請求自動帶上這些標頭
response = session.get("https://api.example.com/me")
response = session.get("https://api.example.com/orders")

# Session 也會自動處理 Cookie
session.post("https://example.com/login", data={"user": "alice", "pass": "secret"})
session.get("https://example.com/dashboard")    # 自動帶 Cookie
```

### 檔案上傳

```python
# 上傳檔案
with open("photo.jpg", "rb") as f:
    response = requests.post(
        "https://api.example.com/upload",
        files={"image": ("photo.jpg", f, "image/jpeg")}
    )

# 下載檔案
response = requests.get("https://example.com/large-file.zip", stream=True)
with open("large-file.zip", "wb") as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```

## httpx — 現代化的替代方案

httpx 同時支援同步和非同步，API 和 requests 幾乎相同：

```bash
pip install httpx
```

```python
import httpx

# 同步（和 requests 一樣的 API）
response = httpx.get("https://api.github.com/users/octocat")

# 非同步
import asyncio

async def fetch_users():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.github.com/users/octocat")
        return response.json()

data = asyncio.run(fetch_users())

# 併發請求（如同 Promise.all）
async def fetch_multiple():
    async with httpx.AsyncClient() as client:
        tasks = [
            client.get(f"https://api.example.com/users/{i}")
            for i in range(1, 6)
        ]
        responses = await asyncio.gather(*tasks)
        return [r.json() for r in responses]
```

## Web Scraping — 網頁爬蟲

### BeautifulSoup

```bash
pip install beautifulsoup4 requests
```

```python
import requests
from bs4 import BeautifulSoup

response = requests.get("https://news.ycombinator.com")
soup = BeautifulSoup(response.text, "html.parser")

# 如果你有 Web 經驗，這些選擇器語法會很熟悉
titles = soup.select(".titleline > a")    # CSS 選擇器
for title in titles:
    print(title.text, title["href"])

# 也支援 find / find_all
links = soup.find_all("a", class_="titlelink")
div = soup.find("div", id="content")
```

## 實用模式

### API 客戶端封裝

```python
import requests

class APIClient:
    def __init__(self, base_url, token=None):
        self.session = requests.Session()
        self.base_url = base_url.rstrip("/")
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"

    def _request(self, method, path, **kwargs):
        url = f"{self.base_url}{path}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, path, **kwargs):
        return self._request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self._request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self._request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request("DELETE", path, **kwargs)

# 使用
api = APIClient("https://api.example.com", token="your-token")
users = api.get("/users", params={"page": 1})
new_user = api.post("/users", json={"name": "Alice"})
```

### 重試機制

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retries = Retry(
    total=3,
    backoff_factor=0.5,
    status_forcelist=[500, 502, 503, 504]
)
session.mount("https://", HTTPAdapter(max_retries=retries))
session.mount("http://", HTTPAdapter(max_retries=retries))

response = session.get("https://api.example.com/data")
```

## 下一步

接下來看 [資料庫操作](04-database.md)。
