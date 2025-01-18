import re

# 模擬IP黑名單
blocked_ips = set()

# 定義一個簡單的SQL注入攻擊規則
SQL_INJECTION_PATTERN = r"('|\bOR\b|\bAND\b|\b--\b|\bSELECT\b|\bDROP\b|\bINSERT\b)"

def detect_sql_injection(user_input, user_ip):
    """
    檢測用戶輸入是否存在SQL注入攻擊，若發現攻擊則封鎖該IP
    """
    if re.search(SQL_INJECTION_PATTERN, user_input, re.IGNORECASE):
        # 封鎖該IP
        blocked_ips.add(user_ip)
        print(f"攻擊檢測：封鎖IP {user_ip}")
        return True
    return False

# 假設用戶輸入與IP
user_input_1 = "SELECT * FROM users WHERE username = 'admin' AND password = 'password';"
user_input_2 = "normaluserinput"
user_ip_1 = "192.168.1.100"
user_ip_2 = "192.168.1.101"

# 檢查用戶輸入是否安全，若發現攻擊封鎖IP
detect_sql_injection(user_input_1, user_ip_1)
detect_sql_injection(user_input_2, user_ip_2)

# 檢查封鎖的IP
print(f"被封鎖的IP列表：{blocked_ips}")
