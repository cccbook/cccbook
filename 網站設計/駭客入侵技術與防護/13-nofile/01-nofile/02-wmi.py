import wmi

# 創建 WMI 連接
c = wmi.WMI()

# 執行 PowerShell 命令
command = "powershell -Command \"Get-Process\""
process = c.Win32_Process.Create(CommandLine=command)

print(f"Created process with ID: {process[1]}")
