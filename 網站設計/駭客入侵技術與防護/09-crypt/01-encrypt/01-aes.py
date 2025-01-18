from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64

# 生成隨機的密鑰
key = get_random_bytes(16)

# 要加密的消息
data = "這是需要加密的敏感數據。"

# 使用AES加密
cipher = AES.new(key, AES.MODE_CBC)
ciphertext = cipher.encrypt(pad(data.encode(), AES.block_size))

# 將密文和初始向量（IV）一起保存
iv = cipher.iv
ciphertext_with_iv = base64.b64encode(iv + ciphertext)

print(f"加密後的數據（base64編碼）: {ciphertext_with_iv}")

# 解密過程
def decrypt_data(ciphertext_with_iv, key):
    ciphertext_with_iv = base64.b64decode(ciphertext_with_iv)
    iv = ciphertext_with_iv[:16]  # 前16字節是IV
    ciphertext = ciphertext_with_iv[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_data = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_data.decode()

# 解密數據
decrypted_data = decrypt_data(ciphertext_with_iv, key)
print(f"解密後的數據: {decrypted_data}")
