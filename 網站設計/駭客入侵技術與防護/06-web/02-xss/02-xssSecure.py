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
