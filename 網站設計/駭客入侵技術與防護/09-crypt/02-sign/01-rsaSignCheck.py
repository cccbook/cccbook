from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import base64

# 生成 RSA 密鑰對
key = RSA.generate(2048)
private_key = key
public_key = key.publickey()

# 取得私鑰和公鑰的 PEM 格式
private_pem = private_key.export_key().decode()
public_pem = public_key.export_key().decode()

print("私鑰:\n", private_pem)
print("\n公鑰:\n", public_pem)

# 要簽名的消息
message = "這是一個需要簽名的消息。"

# 創建哈希對象，使用 SHA-256 哈希算法
hash_object = SHA256.new(message.encode())

# 使用私鑰進行簽名
signature = pkcs1_15.new(private_key).sign(hash_object)

# 將簽名轉換為 base64 格式，便於傳輸
signature_base64 = base64.b64encode(signature).decode()

print(f"數字簽名（base64編碼）: {signature_base64}")

def verify_signature(message, signature_base64, public_key):
    # 創建哈希對象，使用 SHA-256 哈希算法
    hash_object = SHA256.new(message.encode())
    
    # 將 base64 編碼的簽名解碼
    signature = base64.b64decode(signature_base64)
    
    try:
        # 使用公鑰驗證簽名
        pkcs1_15.new(public_key).verify(hash_object, signature)
        print("簽名驗證成功！")
    except (ValueError, TypeError):
        print("簽名驗證失敗！")

# 驗證數字簽名
verify_signature(message, signature_base64, public_key)
