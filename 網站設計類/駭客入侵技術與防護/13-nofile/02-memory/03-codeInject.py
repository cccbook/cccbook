import os

# 模擬代碼注入攻擊
def code_injection(command):
    # 假設這是一個存在安全漏洞的系統
    os.system(command)  # 执行用户提供的命令

# 假設攻擊者提供了注入的命令
malicious_command = "echo 'Malicious code executed!' && rm -rf /"  # 這個命令會刪除根目錄
code_injection(malicious_command)
