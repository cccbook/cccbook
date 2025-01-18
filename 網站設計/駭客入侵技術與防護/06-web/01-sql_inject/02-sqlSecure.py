import sqlite3

def safe_query(user, password):
    conn = sqlite3.connect('example.db')
    cursor = conn.cursor()
    query = "SELECT * FROM users WHERE username = ? AND password = ?"
    cursor.execute(query, (user, password))
    result = cursor.fetchone()
    conn.close()
    return result
