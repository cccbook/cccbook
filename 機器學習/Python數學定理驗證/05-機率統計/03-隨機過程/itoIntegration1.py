import numpy as np
import matplotlib.pyplot as plt

# 設定參數
T = 1.0    # 時間區間
n = 1000   # 時間步數
dt = T/n   # 每步時間
time = np.linspace(0, T, n+1)  # 時間序列

# 模擬布朗運動
dB = np.sqrt(dt) * np.random.randn(n)  # 布朗運動的增量
B = np.cumsum(dB)  # 累積增量，得到布朗運動的路徑
B = np.insert(B, 0, 0)  # 插入初始條件B(0) = 0

# 伊藤積分
f = lambda t, B_t: 2*B_t  # 假設f(s, X_s) = 2*B_s
I = np.cumsum(f(time[:-1], B[:-1]) * dB)  # 計算伊藤積分

# 視覺化
plt.figure(figsize=(10, 6))
plt.plot(time, B, label="Brownian Motion $B_t$")
plt.plot(time[1:], I, label="Itô Integral")
plt.xlabel("Time")
plt.ylabel("Value")
plt.legend()
plt.title("Itô Integral of Brownian Motion")
plt.show()
