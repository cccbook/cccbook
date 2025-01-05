from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

# 生成隨機密鑰
key = get_random_bytes(16)  # AES 需要16字節密鑰

# 需要加密的數據
data = "這是需要加密的數據"

# 將數據進行填充，AES需要的數據長度是16的倍數
def pad_data(data):
    while len(data) % 16 != 0:
        data += " "
    return data

# 加密
def encrypt_data(data, key):
    cipher = AES.new(key, AES.MODE_CBC)
    data = pad_data(data)
    encrypted_data = cipher.encrypt(data.encode())
    return base64.b64encode(cipher.iv + encrypted_data).decode()

# 解密
def decrypt_data(encrypted_data, key):
    encrypted_data = base64.b64decode(encrypted_data.encode())
    iv = encrypted_data[:16]
    encrypted_data = encrypted_data[16:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data).decode().rstrip()
    return decrypted_data

# 執行加密與解密
encrypted_data = encrypt_data(data, key)
decrypted_data = decrypt_data(encrypted_data, key)

print(f"加密後數據: {encrypted_data}")
print(f"解密後數據: {decrypted_data}")
