import itertools

def brute_force(password):
    # 生成所有字母數字組合
    charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    max_length = 6  # 假設密碼長度為6
    attempts = 0
    
    # 嘗試所有可能的組合
    for length in range(1, max_length+1):
        for guess in itertools.product(charset, repeat=length):
            attempts += 1
            guess_password = ''.join(guess)
            print(f"Attempting: {guess_password}")
            if guess_password == password:
                print(f"Password found: {guess_password}")
                print(f"Total attempts: {attempts}")
                return guess_password
    print("Password not found")
    return None

# 假設目標密碼為 'abc123'
target_password = 'abc123'
brute_force(target_password)
