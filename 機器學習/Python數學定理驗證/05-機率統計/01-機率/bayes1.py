
import numpy as np
import matplotlib.pyplot as plt

# 模擬事件 A 和 B
np.random.seed(42)
n_trials = 10000
A = np.random.rand(n_trials) < 0.3  # 事件 A 的概率 P(A) = 0.3
B = np.random.rand(n_trials) < 0.4  # 事件 B 的概率 P(B) = 0.4

# 驗證加法定理
P_A_or_B = np.mean(A | B)
P_A = np.mean(A)
P_B = np.mean(B)
P_A_and_B = np.mean(A & B)
assert np.isclose(P_A_or_B, P_A + P_B - P_A_and_B), "加法定理驗證失敗"

# 驗證乘法定理
P_B_given_A = np.mean(B[A])
assert np.isclose(P_A_and_B, P_A * P_B_given_A), "乘法定理驗證失敗"

P_A_given_B = np.mean(A[B])

print(f"加法定理驗證成功：P(A ∪ B) = {P_A_or_B}")
print(f"乘法定理驗證成功：P(A ∩ B) = {P_A_and_B}")

# 模擬貝葉斯定理
def bayes_theorem(P_B_given_A, P_A, P_B):
    return (P_B_given_A * P_A) / P_B

bayes_theorem(P_B_given_A, P_A, P_B)
print(f"貝葉斯定理驗證：")
print(f"P(A|B) = {P_A_given_B}")
print(f"P(B|A) P(A) / P(B) = {P_B_given_A} * {P_A} / {P_B}= {P_B_given_A * P_A / P_B}")
