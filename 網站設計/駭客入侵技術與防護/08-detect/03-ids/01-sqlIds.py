import re

# 定義一個簡單的SQL注入攻擊規則
SQL_INJECTION_PATTERN = r"('|\bOR\b|\bAND\b|\b--\b|\bSELECT\b|\bDROP\b|\bINSERT\b)"

def detect_sql_injection(user_input):
    """
    檢測用戶輸入是否存在SQL注入攻擊的可能
    """
    if re.search(SQL_INJECTION_PATTERN, user_input, re.IGNORECASE):
        return True
    return False

# 假設用戶輸入
user_input_1 = "SELECT * FROM users WHERE username = 'admin' AND password = 'password';"
user_input_2 = "normaluserinput"

# 檢查用戶輸入是否安全
if detect_sql_injection(user_input_1):
    print("警告：偵測到SQL注入攻擊！")
else:
    print("用戶輸入安全。")

if detect_sql_injection(user_input_2):
    print("警告：偵測到SQL注入攻擊！")
else:
    print("用戶輸入安全。")
