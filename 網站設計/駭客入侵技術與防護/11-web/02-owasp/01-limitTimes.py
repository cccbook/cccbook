import time

class LoginAttempt:
    def __init__(self, max_attempts=3, lockout_time=60):
        self.max_attempts = max_attempts
        self.lockout_time = lockout_time
        self.attempts = 0
        self.lockout_time_remaining = 0
    
    def attempt_login(self, password, correct_password):
        if self.lockout_time_remaining > 0:
            print(f"Account locked. Try again in {self.lockout_time_remaining} seconds.")
            return False
        
        if password == correct_password:
            print("Login successful!")
            self.reset_attempts()
            return True
        else:
            self.attempts += 1
            print(f"Incorrect password. Attempt {self.attempts}/{self.max_attempts}")
            
            if self.attempts >= self.max_attempts:
                self.lockout_time_remaining = self.lockout_time
                print(f"Too many failed attempts. Account locked for {self.lockout_time} seconds.")
            
            return False
    
    def reset_attempts(self):
        self.attempts = 0
        self.lockout_time_remaining = 0

    def tick(self):
        # 減少鎖定時間
        if self.lockout_time_remaining > 0:
            self.lockout_time_remaining -= 1

# 使用範例
login_system = LoginAttempt()

correct_password = "secret123"

# 嘗試登錄
login_system.attempt_login("wrongpass", correct_password)
login_system.attempt_login("wrongpass", correct_password)
login_system.attempt_login("wrongpass", correct_password)

# 模擬時間流逝
for _ in range(60):
    login_system.tick()

login_system.attempt_login("secret123", correct_password)
