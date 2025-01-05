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
