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
