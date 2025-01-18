import itertools
import string

# 假設密碼的長度範圍和字符集
password_length = 4
charset = string.ascii_lowercase + string.digits  # 包括小寫字母和數字

# 假設目標密碼
target_password = "abcd"  # 假設目標密碼是 "abcd"

def brute_force_attack(target_password):
    # 生成所有可能的字符組合
    for length in range(1, password_length + 1):
        for guess in itertools.product(charset, repeat=length):
            guess_password = ''.join(guess)
            print(f"Trying password: {guess_password}")
            if guess_password == target_password:
                print(f"Password found: {guess_password}")
                return guess_password
    return None

# 開始暴力破解
brute_force_attack(target_password)
