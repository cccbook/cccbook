在這一章節中，網路偵查與掃描技術可以幫助駭客了解目標系統的狀態、發現漏洞並進行攻擊。常見的工具有 Nmap、Wireshark 等，但我們將使用 Python 來模擬一些基本的網路偵查與掃描技術，這包括：

1. **端口掃描（Port Scanning）**：檢測目標系統開放的端口。
2. **服務識別**：根據開放端口識別目標的服務類型。
3. **簡單的 Ping 掃描**：檢查目標是否在線。

### 1. **端口掃描（Port Scanning）**

端口掃描是偵查目標網絡中開放端口的常見技術。通過檢查目標主機的各個端口，攻擊者可以發現哪些端口是開放的，從而推測是否存在可以利用的漏洞。

#### 1.1 **Python 實現端口掃描：**

```python
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
```

這段代碼展示了一個簡單的端口掃描腳本，它會檢查目標 IP（在這裡是 `192.168.1.1`）的多個端口，並打印出哪些端口是開放的。這裡使用了 `ThreadPoolExecutor` 來加速掃描過程。

### 2. **服務識別（Service Identification）**

根據開放的端口，我們可以進一步識別目標服務。例如，端口 80 通常與 HTTP 服務相關，端口 443 通常與 HTTPS 服務相關。這類技術通常與指紋識別工具（如 Nmap）一起使用。

#### 2.1 **Python 實現簡單的服務識別：**

```python
import socket

# 端口與服務映射
PORTS_SERVICES = {
    22: "SSH",
    80: "HTTP",
    443: "HTTPS",
    21: "FTP",
    23: "Telnet",
    25: "SMTP",
}

# 根據端口識別服務
def identify_service(port):
    return PORTS_SERVICES.get(port, "Unknown Service")

# 掃描端口並識別服務
def scan_and_identify_service(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target, port))
            if result == 0:
                service = identify_service(port)
                print(f"Port {port} is open on {target}, Service: {service}")
            else:
                print(f"Port {port} is closed on {target}")
    except socket.error as e:
        print(f"Error scanning port {port} on {target}: {e}")

# 扫描并识别目标服务
target = "192.168.1.1"
ports = [22, 80, 443, 8080, 21]
for port in ports:
    scan_and_identify_service(target, port)
```

在這個範例中，我們根據常見的端口號（如 80、443）來識別相應的服務類型。這能幫助攻擊者理解目標系統正在運行哪些服務，從而尋找漏洞。

### 3. **簡單的 Ping 掃描**

Ping 掃描是檢查目標是否在線的一種常見方式。這可以通過發送 ICMP echo 請求來實現。以下是用 Python 實現簡單的 Ping 掃描。

#### 3.1 **Python 實現 Ping 掃描：**

```python
import os
import platform

# 判斷系統類型
def ping(target):
    # 對於 Windows 使用 'ping -n'
    if platform.system().lower() == "windows":
        response = os.system(f"ping -n 1 {target}")
    else:
        response = os.system(f"ping -c 1 {target}")

    # 根據 Ping 結果返回狀態
    if response == 0:
        print(f"{target} is online")
    else:
        print(f"{target} is offline")

# 執行 Ping 掃描
target = "192.168.1.1"
ping(target)
```

這段代碼簡單地檢查目標 IP 地址是否在線。根據不同的操作系統，會調用適當的 `ping` 命令。若目標在線，它會顯示“online”，否則顯示“offline”。

---

### 結論

這些範例展示了 Python 如何實現網路偵查與掃描的基本技術：
- **端口掃描**可以用來探測開放端口。
- **服務識別**幫助我們根據端口號來識別目標的服務。
- **Ping 掃描**可以檢查目標是否在線。

這些技術是駭客進行偵查的基礎，對於防禦者來說，瞭解這些攻擊方法並加以防範非常重要。