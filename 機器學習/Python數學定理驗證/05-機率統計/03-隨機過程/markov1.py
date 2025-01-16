import numpy as np
import matplotlib.pyplot as plt

# 定義遷移概率矩陣
P = np.array([[0.7, 0.3],  # 從狀態0到狀態0和狀態1的概率
              [0.4, 0.6]]) # 從狀態1到狀態0和狀態1的概率

# 設定初始狀態
initial_state = np.array([1, 0])  # 初始狀態為狀態0

# 模擬馬爾可夫鏈
n_steps = 1000
states = np.zeros(n_steps, dtype=int)
states[0] = np.argmax(initial_state)

for t in range(1, n_steps):
    states[t] = np.random.choice([0, 1], p=P[states[t-1]])

# 計算長期穩態分佈
long_term_state = np.linalg.matrix_power(P, 1000)[0]
print('long_term_state=', long_term_state)


# 畫出馬爾可夫鏈的結果 (ccc: 這個感覺沒用)
plt.figure(figsize=(10, 6))
plt.plot(states, label="Markov Chain")
plt.xlabel("Time Step")
plt.ylabel("State")
plt.title(f"Markov Chain Simulation with Long-Term State Distribution: {long_term_state}")
plt.show()
