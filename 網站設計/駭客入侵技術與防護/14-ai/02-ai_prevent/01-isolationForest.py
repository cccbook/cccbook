import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import numpy as np

# 假設我們有一個數據集，'feature1', 'feature2' 是流量特徵，'label' 是正常（0）或異常（1）
data = {
    'feature1': [0.5, 0.6, 0.7, 0.2, 0.9, 1.1, 0.8, 0.3, 0.1, 0.9, 1.0, 1.2],
    'feature2': [0.1, 0.2, 0.3, 0.1, 0.4, 0.5, 0.4, 0.2, 0.0, 0.6, 0.7, 0.8],
    'label': [0, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 1]  # 0: 正常流量, 1: 攻擊流量
}

df = pd.DataFrame(data)

# 特徵與標籤分開
X = df[['feature1', 'feature2']]
y = df['label']

# 拆分數據集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 初始化 IsolationForest 模型
model = IsolationForest(contamination=0.25)  # 假設有 25% 的攻擊流量

# 訓練模型
model.fit(X_train)

# 進行預測
y_pred = model.predict(X_test)

# 將預測結果轉為二進制格式（1 = 攻擊，0 = 正常）
y_pred = np.where(y_pred == 1, 0, 1)

# 輸出結果
print(classification_report(y_test, y_pred))
