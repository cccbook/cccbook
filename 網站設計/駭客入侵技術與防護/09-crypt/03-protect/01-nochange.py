import hashlib

# 用SHA-256算法計算消息的哈希值
def calculate_hash(message):
    hash_object = hashlib.sha256()
    hash_object.update(message.encode())
    return hash_object.hexdigest()

# 計算數據的哈希值
message = "這是一段測試數據。"
message_hash = calculate_hash(message)

print(f"消息哈希值: {message_hash}")
