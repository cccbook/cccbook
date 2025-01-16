import numpy as np

# 設置隨機種子
np.random.seed(0)

# 模擬10000次試驗，定義事件A和事件B
sample_space = 10000
A = np.random.rand(sample_space) < 0.5  # 事件A：隨機數小於0.5
B = np.random.rand(sample_space) < 0.3  # 事件B：隨機數小於0.3

# 計算P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
P_A_union_B = np.sum(A | B) / sample_space  # P(A ∪ B)
P_A = np.sum(A) / sample_space  # P(A)
P_B = np.sum(B) / sample_space  # P(B)
P_A_intersection_B = np.sum(A & B) / sample_space  # P(A ∩ B)

# 驗證加法法則
print(f"P(A ∪ B): {P_A_union_B}")
print(f"P(A) + P(B) - P(A ∩ B): {P_A + P_B - P_A_intersection_B}")

# 模擬10000次試驗，定義條件機率
P_A_given_B = np.sum(A & B) / np.sum(B)  # P(A|B)
P_B_given_A = np.sum(A & B) / np.sum(A)  # P(B|A)

# 驗證乘法法則
P_AB0=np.sum(A&B) / len(A)
P_AB1 = P_B * P_A_given_B
P_AB2 = P_A * P_B_given_A

print(f"P(A ∩ B): {P_AB0}")
print(f"P(A ∩ B) from P(A) * P(B|A): {P_AB1}")
print(f"P(A ∩ B) from P(B) * P(A|B): {P_AB2}")
