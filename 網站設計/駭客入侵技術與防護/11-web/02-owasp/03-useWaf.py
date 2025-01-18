import re

def waf_filter(request_body):
    # 簡單的 WAF 濾波器，過濾惡意的 SQL 和 XSS 攻擊
    patterns = [
        r"SELECT.*FROM",   # SQL 注入嘗試
        r"<script.*?>.*?</script>",  # XSS 攻擊
    ]
    
    for pattern in patterns:
        if re.search(pattern, request_body, re.IGNORECASE):
            return False  # 攔截惡意請求

    return True  # 允許正常請求

# 範例請求
request_body = "<script>alert('XSS')</script>"
if waf_filter(request_body):
    print("Request is safe")
else:
    print("Malicious request detected")
