### 跨站腳本攻擊（XSS）

跨站腳本攻擊（Cross-Site Scripting，簡稱 XSS）是一種攻擊手段，攻擊者將惡意的 JavaScript 代碼注入到網頁中，當其他用戶訪問該網頁時，該 JavaScript 代碼便在他們的瀏覽器中執行。這種攻擊通常用來竊取用戶的敏感信息（如 Cookie、會話識別碼）、操控網頁內容或執行其他惡意操作。

XSS 攻擊主要有三種形式：
1. **反射型 XSS**（Reflected XSS）：攻擊者通過 URL 將惡意腳本注入網站，當目標網站返回這些腳本時，腳本會在瀏覽器中執行。
2. **儲存型 XSS**（Stored XSS）：攻擊者將惡意腳本存儲在目標網站的數據庫中，當用戶訪問包含惡意腳本的頁面時，腳本會自動執行。
3. **DOM-based XSS**：攻擊者通過修改網頁的 DOM（Document Object Model）來注入並執行惡意腳本。

### XSS 攻擊的實例

以下示範一個反射型 XSS 攻擊的 Python 範例，假設存在一個簡單的網站表單，允許用戶輸入搜索關鍵字並顯示結果。

#### 1. **危險的 Python 網站代碼**

這段代碼處理來自用戶的輸入，但並未對輸入進行過濾，可能會導致 XSS 攻擊：

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/search')
def search():
    user_input = request.args.get('query', '')
    return render_template_string(f"""
        <h1>Search Results</h1>
        <p>You searched for: {user_input}</p>
    """)

if __name__ == '__main__':
    app.run(debug=True)
```

如果攻擊者在 `query` 參數中輸入如下內容：

```html
<script>alert('XSS Attack!');</script>
```

那麼網頁將顯示 JavaScript 警告框（`alert('XSS Attack!')`）。這就表明了反射型 XSS 攻擊，攻擊者的惡意腳本被注入並執行。

### 2. **防範 XSS 攻擊的方法**

為了防範 XSS 攻擊，開發者可以採取多種措施來過濾和清理用戶輸入：

#### 2.1 **HTML 編碼輸入**

將用戶輸入中的特殊字符轉換為 HTML 實體字符（如 `&lt;` 代替 `<`），可以防止 JavaScript 被執行。這樣用戶的輸入就會以純文本顯示，而不是作為代碼執行。

改進後的 Flask 代碼示例：

```python
from flask import Flask, request, render_template_string
import html

app = Flask(__name__)

@app.route('/search')
def search():
    user_input = request.args.get('query', '')
    sanitized_input = html.escape(user_input)  # HTML 編碼
    return render_template_string(f"""
        <h1>Search Results</h1>
        <p>You searched for: {sanitized_input}</p>
    """)

if __name__ == '__main__':
    app.run(debug=True)
```

這樣，`<script>alert('XSS Attack!');</script>` 會被編碼為 `&lt;script&gt;alert('XSS Attack!');&lt;/script&gt;`，從而防止腳本執行。

#### 2.2 **使用內容安全政策（CSP）**

內容安全政策（Content Security Policy，CSP）是一種瀏覽器機制，允許網站設定哪些資源可以被加載和執行。通過啟用 CSP，網站可以大幅降低 XSS 攻擊的風險。

例如，通過設置 CSP 來限制 JavaScript 代碼的執行：

```http
Content-Security-Policy: script-src 'self';
```

這樣，只允許來自當前域（`self`）的 JavaScript 執行，阻止來自外部來源的腳本執行。

#### 2.3 **輸入驗證與過濾**

對用戶輸入進行適當的驗證和過濾，確保輸入的數據不包含惡意的 HTML 或 JavaScript 代碼。可以使用現有的庫（如 Python 的 `bleach` 庫）來過濾不安全的 HTML 標籤和屬性。

例如，使用 `bleach` 來過濾用戶的輸入：

```python
import bleach

safe_input = bleach.clean(user_input)
```

#### 2.4 **利用框架內建的防禦機制**

大多數現代 Web 框架（如 Django、Flask）都自動對用戶輸入進行轉義，防止 XSS 攻擊。因此，開發者應該依賴框架提供的模板引擎來正確處理用戶輸入。

### 3. **儲存型 XSS 攻擊範例**

在儲存型 XSS 中，攻擊者將惡意腳本存儲到伺服器的資料庫中，並在用戶訪問該頁面時執行。以下是一個示範：

#### 3.1 **簡單的 Flask 儲存型 XSS 示例**

```python
from flask import Flask, request, render_template_string
import sqlite3

app = Flask(__name__)

# 模擬一個簡單的儲存型 XSS 攻擊
def store_comment(comment):
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS comments (content TEXT)")
    cursor.execute("INSERT INTO comments (content) VALUES (?)", (comment,))
    conn.commit()
    conn.close()

@app.route('/comment', methods=['POST'])
def comment():
    user_comment = request.form['comment']
    store_comment(user_comment)
    return "Comment stored!"

@app.route('/comments')
def comments():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM comments")
    comments = cursor.fetchall()
    conn.close()
    return render_template_string("""
        <h1>Comments</h1>
        {% for comment in comments %}
            <p>{{ comment[0] }}</p>
        {% endfor %}
    """, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
```

如果攻擊者將以下內容作為評論提交：

```html
<script>alert('Stored XSS Attack!');</script>
```

當其他用戶訪問該頁面時，該腳本會自動執行，這樣攻擊者便能在用戶的瀏覽器中執行惡意 JavaScript。

#### 3.2 **防範儲存型 XSS**

與反射型 XSS 相似，防範儲存型 XSS 的最佳方法是對用戶輸入進行適當的過濾和編碼。在這個範例中，可以使用 `html.escape` 來清理評論內容。

```python
from flask import Flask, request, render_template_string
import sqlite3
import html

app = Flask(__name__)

def store_comment(comment):
    sanitized_comment = html.escape(comment)  # HTML 編碼
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS comments (content TEXT)")
    cursor.execute("INSERT INTO comments (content) VALUES (?)", (sanitized_comment,))
    conn.commit()
    conn.close()

@app.route('/comment', methods=['POST'])
def comment():
    user_comment = request.form['comment']
    store_comment(user_comment)
    return "Comment stored!"

@app.route('/comments')
def comments():
    conn = sqlite3.connect('comments.db')
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM comments")
    comments = cursor.fetchall()
    conn.close()
    return render_template_string("""
        <h1>Comments</h1>
        {% for comment in comments %}
            <p>{{ comment[0] }}</p>
        {% endfor %}
    """, comments=comments)

if __name__ == '__main__':
    app.run(debug=True)
```

這樣，攻擊者提交的 `<script>` 代碼會被轉義，從而無法執行。

### 結論

XSS 攻擊是非常危險的，能夠竊取用戶的敏感信息，操控網頁內容或進行其他惡意操作。防範 XSS 的關鍵在於正確地處理和過濾用戶輸入，使用 HTML 編碼、內容安全政策（CSP）和框架內建的防禦機制，從而保護網站免受攻擊。