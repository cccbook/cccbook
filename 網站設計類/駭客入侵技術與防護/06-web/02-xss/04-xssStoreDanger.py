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
