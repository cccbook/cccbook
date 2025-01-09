from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# 生成RSA公鑰和私鑰對
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

# 使用公鑰加密
cipher_rsa = PKCS1_OAEP.new(public_key)
data = "這是需要加密的消息。"
encrypted_data = cipher_rsa.encrypt(data.encode())

# 將加密的數據轉換為base64編碼
encrypted_data_b64 = base64.b64encode(encrypted_data)
print(f"加密後的數據（base64編碼）: {encrypted_data_b64}")

# 使用私鑰解密
def decrypt_rsa(encrypted_data_b64, private_key):
    encrypted_data = base64.b64decode(encrypted_data_b64)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher_rsa.decrypt(encrypted_data)
    return decrypted_data.decode()

# 解密數據
decrypted_data = decrypt_rsa(encrypted_data_b64, private_key)
print(f"解密後的數據: {decrypted_data}")
