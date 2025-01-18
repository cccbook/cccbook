# 假設字典攻擊的密碼字典
password_dictionary = ["123456", "password", "qwerty", "abc123", "letmein", "1234", "abcd"]

# 假設目標密碼
target_password = "letmein"

def dictionary_attack(target_password, password_list):
    for password in password_list:
        print(f"Trying password: {password}")
        if password == target_password:
            print(f"Password found: {password}")
            return password
    return None

# 開始字典攻擊
dictionary_attack(target_password, password_dictionary)
