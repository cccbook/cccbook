import socket
from concurrent.futures import ThreadPoolExecutor

# 端口掃描函數
def scan_port(target, port):
    try:
        # 創建一個 socket 對象，並設置超時時間
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))  # 嘗試連接
            if result == 0:
                print(f"Port {port} is open on {target}")
            else:
                print(f"Port {port} is closed on {target}")
    except socket.error as e:
        print(f"Error scanning port {port} on {target}: {e}")

# 使用多線程加快掃描速度
def scan_target(target, ports):
    with ThreadPoolExecutor(max_workers=10) as executor:
        executor.map(lambda port: scan_port(target, port), ports)

# 定義目標與端口範圍
target = "192.168.1.1"  # 假設目標IP地址
ports = [22, 80, 443, 8080, 21]  # 假設要掃描的端口

# 開始掃描
scan_target(target, ports)
