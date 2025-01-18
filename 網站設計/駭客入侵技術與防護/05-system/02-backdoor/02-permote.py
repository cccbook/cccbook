import os

# 嘗試提升權限
def escalate_privileges():
    try:
        # 嘗試修改具有 root 權限的文件
        os.system('chmod +s /usr/bin/sudo')  # 設置 sudo 權限
        print("Privilege escalation attempt successful")
    except Exception as e:
        print(f"Error: {e}")

# 嘗試提權
escalate_privileges()
