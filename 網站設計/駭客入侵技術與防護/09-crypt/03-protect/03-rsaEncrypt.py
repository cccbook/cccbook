from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# 生成 RSA 密鑰對
key = RSA.generate(2048)
public_key = key.publickey()
private_key = key

# 用公鑰加密數據
def encrypt_with_public_key(data, public_key):
    cipher = PKCS1_OAEP.new(public_key)
    encrypted_data = cipher.encrypt(data.encode())
    return base64.b64encode(encrypted_data).decode()

# 用私鑰解密數據
def decrypt_with_private_key(encrypted_data, private_key):
    encrypted_data = base64.b64decode(encrypted_data.encode())
    cipher = PKCS1_OAEP.new(private_key)
    decrypted_data = cipher.decrypt(encrypted_data).decode()
    return decrypted_data

# 加密與解密操作
data = "這是需要加密的數據"
encrypted_data = encrypt_with_public_key(data, public_key)
decrypted_data = decrypt_with_private_key(encrypted_data, private_key)

print(f"加密後數據: {encrypted_data}")
print(f"解密後數據: {decrypted_data}")
