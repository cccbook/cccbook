from flask import Flask, redirect, request

app = Flask(__name__)

@app.before_request
def before_request():
    # 如果不是 HTTPS，則重定向到 HTTPS
    if not request.is_secure:
        return redirect(request.url.replace("http://", "https://", 1))

@app.route('/')
def home():
    return "Hello, Secure World!"

if __name__ == '__main__':
    # 假設已經在具有 SSL 配置的環境中運行
    app.run(ssl_context='adhoc')  # 用於生成自簽名 SSL 憑證
