import numpy as np
from sklearn.ensemble import IsolationForest

# 假設我們有一組正常行為數據
data = np.array([[30], [31], [29], [32], [30], [29], [30], [80]])  # 正常的 CPU 使用率（最後一個是異常值）

# 初始化 Isolation Forest 模型
model = IsolationForest(contamination=0.1)  # 假設 10% 的樣本是異常的

# 訓練模型
model.fit(data)

# 預測異常值
predictions = model.predict(data)

# 輸出結果
for i, pred in enumerate(predictions):
    status = "異常" if pred == -1 else "正常"
    print(f"數據點 {data[i][0]}: {status}")
