import socket

# 假裝成另一個IP地址
fake_ip = "192.168.1.100"
target_ip = "192.168.1.1"
target_port = 80

# 創建原始套接字
sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)

# 設定 IP 標頭
ip_header = socket.inet_aton(fake_ip)  # 假冒的源IP
dest_ip = socket.inet_aton(target_ip)  # 目標IP
ip_packet = ip_header + dest_ip  # IP包結構

# 發送偽造的包
sock.sendto(ip_packet, (target_ip, target_port))
print("Spoofed packet sent successfully.")
