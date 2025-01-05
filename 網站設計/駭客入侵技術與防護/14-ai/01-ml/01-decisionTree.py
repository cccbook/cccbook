import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import classification_report

# 假設我們有一些數據，其中 'feature1', 'feature2' 等是網路流量的特徵，'label' 是標記（0 表示正常，1 表示攻擊）
data = {
    'feature1': [0.5, 0.6, 0.7, 0.2, 0.9, 1.1, 0.8, 0.3],
    'feature2': [0.1, 0.2, 0.3, 0.1, 0.4, 0.5, 0.4, 0.2],
    'label': [0, 0, 1, 0, 1, 1, 1, 0]  # 0: 正常, 1: 攻擊
}

df = pd.DataFrame(data)

# 特徵與標籤分開
X = df[['feature1', 'feature2']]
y = df['label']

# 拆分數據集為訓練集和測試集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 創建並訓練模型
model = DecisionTreeClassifier()
model.fit(X_train, y_train)

# 測試模型
y_pred = model.predict(X_test)

# 輸出結果
print(classification_report(y_test, y_pred))
