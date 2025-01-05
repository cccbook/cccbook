import os
import platform

# 判斷系統類型
def ping(target):
    # 對於 Windows 使用 'ping -n'
    if platform.system().lower() == "windows":
        response = os.system(f"ping -n 1 {target}")
    else:
        response = os.system(f"ping -c 1 {target}")

    # 根據 Ping 結果返回狀態
    if response == 0:
        print(f"{target} is online")
    else:
        print(f"{target} is offline")

# 執行 Ping 掃描
target = "192.168.1.1"
ping(target)
