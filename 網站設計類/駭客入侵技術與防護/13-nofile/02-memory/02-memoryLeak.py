import time

# 模擬內存泄漏
def memory_leak():
    leaked_memory = []
    while True:
        leaked_memory.append('A' * 10**6)  # 每次分配1MB內存
        time.sleep(1)  # 每秒分配一次，持續運行

# 註：這個範例會不斷分配內存，可能會導致系統崩潰。使用時請小心。
# memory_leak()
