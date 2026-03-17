---
title: 机器学习基础
description: 机器学习的核心概念和算法
---

# 机器学习基础

## 什么是机器学习

机器学习是一种让计算机从数据中学习的技术，而不是通过明确的编程指令。

### 核心概念

| 术语 | 英文 | 说明 |
|------|------|------|
| 特征 | Feature | 输入数据的属性 |
| 标签 | Label | 预测目标 |
| 模型 | Model | 学习得到的函数 |
| 训练 | Training | 用数据拟合模型 |
| 推理 | Inference | 用模型做预测 |

## 常见算法

### 线性回归

用于预测连续值：

```python
from sklearn.linear_model import LinearRegression
import numpy as np

# 训练数据
X = np.array([[1], [2], [3], [4]])
y = np.array([2, 4, 6, 8])

# 训练模型
model = LinearRegression()
model.fit(X, y)

# 预测
print(model.predict([[5]]))  # 输出：[10.]
```

### 决策树

用于分类和回归任务。

### 神经网络

深度学习的基础构建块。

## 评估指标

- **准确率** (Accuracy)：正确预测的比例
- **精确率** (Precision)：预测为正的样本中有多少真正为正
- **召回率** (Recall)：实际为正的样本中有多少被正确预测
- **F1 分数**：精确率和召回率的调和平均

> 注意：选择合适的评估指标对于模型优化至关重要。
