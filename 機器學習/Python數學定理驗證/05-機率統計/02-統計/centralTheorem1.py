import numpy as np
import matplotlib.pyplot as plt

# 設置隨機種子
np.random.seed(0)

# 設定參數
sample_size = 1000  # 總樣本數量
sample_count = 1000  # 重複抽樣的次數

# 設定均勻分佈的參數（假設均勻分佈範圍 [0, 1]）
lower, upper = 0, 1

# 抽取樣本並計算樣本均值
sample_means = []
for _ in range(sample_count):
    sample = np.random.uniform(lower, upper, sample_size)
    sample_means.append(np.mean(sample))

# 繪製樣本均值的分佈
plt.hist(sample_means, bins=30, density=True, alpha=0.6, color='g')
plt.title("Sample Means Distribution (Uniform Distribution)")
plt.xlabel("Sample Mean")
plt.ylabel("Density")

# 理論上的正態分佈
mu, sigma = (upper + lower) / 2, (upper - lower) / np.sqrt(12)
x = np.linspace(mu - 4 * sigma / np.sqrt(sample_size), mu + 4 * sigma / np.sqrt(sample_size), 100)
plt.plot(x, (1 / (np.sqrt(2 * np.pi * sigma**2 / sample_size))) * np.exp(-0.5 * ((x - mu) / (sigma / np.sqrt(sample_size)))**2), 'r', label='Normal Distribution')
plt.legend()
plt.show()
