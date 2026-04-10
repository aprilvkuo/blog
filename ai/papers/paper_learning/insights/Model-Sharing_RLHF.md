---
title: Model-Sharing RLHF
type: concept
---

# Model-Sharing RLHF

> **定义**: 单模型多角色复用技术，通过 LoRA 适配器动态切换，一个模型扮演 Policy/Value/Ref/Reward 四个角色，大幅降低 RLHF 成本。

## 核心要点

- **四个角色**: Policy（策略）、Value（价值）、Ref（参考）、Reward（奖励）
- **适配器切换**: 不同角色 = 不同 LoRA 适配器，动态 `set_adapter()`
- **单模型复用**: 1 个基础模型 + 4 个小适配器，而非 4 个大模型
- **内存节省**: 传统 RLHF 需要 4×模型内存，Model-Sharing 只需 1×

## 示例

```python
# LlamaFactory 的 Model-Sharing RLHF
class ModelSharingRLHF:
    def __init__(self, base_model):
        self.model = base_model  # 共享基础模型

        # 添加 4 个适配器（每个只需几 MB）
        self.model.add_adapter("policy", LoRAConfig())
        self.model.add_adapter("value", LoRAConfig())
        self.model.add_adapter("ref", LoRAConfig())    # frozen
        self.model.add_adapter("reward", LoRAConfig())

    def ppo_step(self, batch):
        # 动态切换角色
        self.model.set_adapter("policy")
        policy_output = self.model(batch)

        self.model.set_adapter("value")
        value_output = self.model(batch)

        self.model.set_adapter("ref")
        ref_output = self.model(batch)  # frozen，不更新

        # 计算 PPO 损失...
```

## 相关论文

- [[LlamaFactory]]: 核心创新，降低 RLHF 门槛

## 相关概念

- [[QLoRA]]: Model-Sharing 的基础技术
- [[模型注册表]]: 自动挂载适配器

---

## 内存对比

| 方案 | 模型数量 | 内存需求 |
|------|----------|----------|
| 传统 RLHF | 4 个大模型 | 4 × 模型大小 |
| **Model-Sharing** | 1 模型 + 4 适配器 | 1 × 模型 + 4 × 几 MB |

**关键洞察**: LoRA 适配器参数量很小（通常 <1% 原模型），四个适配器的额外开销几乎可忽略。