import sqlite3

# 模擬SQL注入攻擊
def sql_injection():
    # 創建一個簡單的 SQLite 資料庫
    conn = sqlite3.connect(":memory:")  # 使用內存資料庫
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)")
    cursor.execute("INSERT INTO users (username, password) VALUES ('admin', 'password123')")
    cursor.execute("INSERT INTO users (username, password) VALUES ('user1', 'password456')")
    conn.commit()

    # 假設用戶名和密碼來自 Web 表單
    username = "admin' OR '1'='1"  # 注入的 SQL
    password = "irrelevant"

    # 不安全的查詢（易受 SQL 注入攻擊）
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    result = cursor.fetchone()
    
    if result:
        print(f"Welcome {result[1]}!")  # 輸出用戶名
    else:
        print("Invalid credentials.")

sql_injection()
