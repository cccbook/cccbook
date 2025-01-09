from flask import Flask, request, render_template_string

# 創建一個簡單的 Flask 應用來演示 XSS
app = Flask(__name__)

@app.route('/')
def index():
    # 用戶輸入模擬
    user_input = request.args.get("name", "")
    # 沒有對用戶輸入進行適當的過濾，容易遭受 XSS 攻擊
    return render_template_string(f"<h1>Hello, {user_input}!</h1>")

if __name__ == "__main__":
    app.run(debug=True)
