import psutil
import time

# 設置 CPU 使用率的閾值
CPU_THRESHOLD = 80  # 超過 80% CPU 使用率視為異常

def monitor_system():
    # 持續監控系統進程
    while True:
        # 獲取所有運行中的進程
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                cpu_usage = proc.info['cpu_percent']
                if cpu_usage > CPU_THRESHOLD:
                    print(f"異常行為檢測：進程 {proc.info['name']} (PID {proc.info['pid']}) 使用 CPU 超過 {CPU_THRESHOLD}% -> 異常")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        
        time.sleep(1)  # 每秒監控一次

# 開始監控系統行為
monitor_system()
