---
title: 资产配置策略
description: 如何构建和平衡投资组合
---

# 资产配置策略

资产配置是决定投资回报的最重要因素，研究表明超过 90% 的回报差异来自于资产配置决策。

## 经典配置模型

### 60/40 组合

最经典的股债配置：

- 60% 股票 - 追求增长
- 40% 债券 - 提供稳定收益

```
优点：简单易懂，风险适中
缺点：在低利率环境下债券回报有限
```

### 风险平价

每种资产对组合风险的贡献相等：

| 资产 | 权重 | 风险贡献 |
|------|------|----------|
| 股票 | 25% | 25% |
| 债券 | 50% | 25% |
| 商品 | 15% | 25% |
| 现金 | 10% | 25% |

### 耶鲁模型

机构级分散化配置：

- 国内股票：15%
- 国际发达市场股票：15%
- 新兴市场股票：10%
- 债券：15%
- 房地产：15%
- 私募股权：30%

## 再平衡策略

```python
def rebalance(portfolio, target_weights, threshold=0.05):
    """
    检查是否需要再平衡

    Args:
        portfolio: 当前持仓
        target_weights: 目标权重
        threshold: 再平衡阈值
    """
    current_weights = calculate_weights(portfolio)

    for asset in target_weights:
        drift = abs(current_weights[asset] - target_weights[asset])
        if drift > threshold:
            print(f"{asset} 需要再平衡：偏离 {drift:.2%}")

    return generate_trades(portfolio, target_weights)
```

## 生命周期配置

```
年龄    股票%   债券%   说明
20-30   80-90   10-20   积累期，追求增长
30-45   70-80   20-30   稳定期，适度保守
45-60   50-70   30-50   保守期，保护本金
60+     30-50   50-70   退休期，收入优先
```

> 多元化是唯一免费的午餐。—— 哈里·马科维茨
