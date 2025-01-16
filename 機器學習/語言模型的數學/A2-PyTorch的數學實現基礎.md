### **A2 - PyTorch的數學實現基礎**

在這一部分，我們將介紹如何使用PyTorch進行數學運算和實現機器學習及深度學習模型的數學基礎。PyTorch提供了強大的張量操作和自動微分功能，這些都是數學建模和算法實現的核心工具。

#### **1. 張量（Tensor）基礎**

在PyTorch中，張量（Tensor）是多維矩陣的基本數據結構，類似於NumPy中的ndarray。它是執行數學運算和實現深度學習模型的基礎。

- **創建張量**
  ```python
  import torch
  
  # 創建一個零矩陣
  tensor_zeros = torch.zeros(3, 3)
  
  # 創建一個隨機矩陣
  tensor_rand = torch.rand(3, 3)
  
  # 從NumPy數組創建張量
  import numpy as np
  np_array = np.array([[1, 2], [3, 4]])
  tensor_from_np = torch.tensor(np_array)
  ```

- **基本張量操作**
  ```python
  # 張量加法
  tensor_sum = tensor_zeros + tensor_rand
  
  # 張量乘法（逐元素相乘）
  tensor_mul = tensor_zeros * tensor_rand
  
  # 矩陣乘法（點積）
  tensor_matmul = torch.matmul(tensor_zeros, tensor_rand.T)
  ```

#### **2. 自動微分與梯度計算**

PyTorch提供了自動微分（Autograd）功能，這是訓練深度學習模型時不可或缺的一部分。當你定義了一個張量並設置 `requires_grad=True`，PyTorch會追蹤對這些張量的所有操作，並能夠自動計算梯度。

- **定義需要計算梯度的張量**
  ```python
  x = torch.tensor([1.0, 2.0, 3.0], requires_grad=True)
  ```

- **計算梯度**
  ```python
  # 定義一個簡單的函數
  y = x ** 2 + 3 * x + 5
  
  # 計算y對x的梯度
  y.backward()  # 默認是對所有標量進行求導
  
  # 輸出梯度
  print(x.grad)  # [5. 7. 9.]
  ```

#### **3. 常用數學函數**

PyTorch提供了豐富的數學函數來處理常見的數學運算，包括線性代數、激活函數等。

- **矩陣運算**
  ```python
  # 矩陣轉置
  tensor_transpose = torch.t(tensor_rand)
  
  # 矩陣求逆
  tensor_inv = torch.inverse(tensor_rand)
  ```

- **激活函數**
  ```python
  # Sigmoid 函數
  sigmoid = torch.sigmoid(tensor_rand)
  
  # ReLU 函數
  relu = torch.relu(tensor_rand)
  
  # Tanh 函數
  tanh = torch.tanh(tensor_rand)
  ```

#### **4. 損失函數**

在機器學習中，損失函數用來衡量模型預測與真實值之間的誤差。PyTorch提供了多種內建的損失函數，並支持自定義損失函數。

- **均方誤差損失（MSE Loss）**
  ```python
  criterion = torch.nn.MSELoss()
  output = model(input_data)  # 假設 model 是一個模型，input_data 是模型的輸入
  loss = criterion(output, target_data)  # target_data 是實際的標籤
  ```

- **交叉熵損失（Cross-Entropy Loss）**
  ```python
  criterion = torch.nn.CrossEntropyLoss()
  output = model(input_data)
  loss = criterion(output, target_data)
  ```

#### **5. 優化器**

PyTorch提供了多種優化算法，如SGD、Adam等，用來最小化損失函數。在使用這些優化器時，我們通常會為模型的參數設置梯度，並通過優化器更新這些參數。

- **SGD優化器**
  ```python
  optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
  optimizer.zero_grad()  # 清除之前的梯度
  loss.backward()  # 計算梯度
  optimizer.step()  # 更新模型參數
  ```

- **Adam優化器**
  ```python
  optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
  optimizer.zero_grad()
  loss.backward()
  optimizer.step()
  ```

#### **6. 梯度下降算法**

在深度學習中，梯度下降是最常用的優化方法之一。PyTorch提供了對梯度下降的自動支持，使得我們能夠便捷地實現和測試不同的算法。

- **簡單的梯度下降實現**
  ```python
  # 假設我們有一個損失函數 L(θ) 並且我們需要最小化它
  lr = 0.01  # 設定學習率
  theta = torch.randn(10, requires_grad=True)  # 隨機初始化參數

  for epoch in range(100):
      loss = some_loss_function(theta)  # 計算損失
      loss.backward()  # 計算梯度
      with torch.no_grad():  # 禁止梯度追蹤
          theta -= lr * theta.grad  # 更新參數
          theta.grad.zero_()  # 清空梯度
  ```

#### **7. 深度學習模型**

PyTorch讓我們輕鬆定義和訓練深度學習模型。我們可以使用`torch.nn`模塊來構建神經網絡，並通過自動微分進行訓練。

- **神經網絡結構**
  ```python
  import torch.nn as nn

  class SimpleModel(nn.Module):
      def __init__(self):
          super(SimpleModel, self).__init__()
          self.fc1 = nn.Linear(10, 5)  # 第一層，全連接層
          self.fc2 = nn.Linear(5, 1)   # 第二層，全連接層

      def forward(self, x):
          x = torch.relu(self.fc1(x))  # 使用ReLU激活函數
          x = self.fc2(x)
          return x
  ```

- **模型訓練流程**
  ```python
  model = SimpleModel()
  optimizer = torch.optim.SGD(model.parameters(), lr=0.01)
  criterion = torch.nn.MSELoss()

  for epoch in range(100):
      optimizer.zero_grad()
      output = model(input_data)
      loss = criterion(output, target_data)
      loss.backward()
      optimizer.step()
  ```

---

這些數學基礎和PyTorch的操作使我們能夠實現許多深度學習和機器學習算法，並能夠高效地進行模型的訓練和優化。通過掌握這些基礎，您將能夠深入理解和實踐現代AI技術。