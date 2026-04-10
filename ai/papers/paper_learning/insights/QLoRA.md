---
title: QLoRA
type: concept
---

# QLoRA

> **定义**: 4 位量化 + LoRA 的组合技术，将模型压缩到 4 位精度后添加 LoRA 适配器，实现极低内存微调。

## 核心要点

- **4 位量化**: 将权重从 16 位压缩到 4 位（内存降低 4×）
- **LoRA 微调**: 只训练低秩适配器（参数量 <1%）
- **组合效果**: 内存降低 ~96%，单卡可微调大模型
- **精度保持**: 量化后性能损失很小

## 示例

```python
# QLoRA 配置
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,           # 4 位量化
    bnb_4bit_quant_type="nf4",   # NormalFloat4 量化
    bnb_4bit_use_double_quant=True,  # 双量化进一步压缩
)

# 加载量化模型
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b",
    quantization_config=bnb_config,
)

# 添加 LoRA 适配器（训练这部分）
model = prepare_model_for_kbit_training(model)
lora_config = LoraConfig(r=8, lora_alpha=32)
model = get_peft_model(model, lora_config)
```

## 相关论文

- [[LlamaFactory]]: 集成支持，核心效率技术

## 相关概念

- [[Model-Sharing RLHF]]: 基于 QLoRA 实现单模型多角色
- [[模型注册表]]: 自动挂载 LoRA 到正确层

---

## 内存对比

| 方法 | Gemma-2B | Llama2-7B | bytes/param |
|------|----------|-----------|-------------|
| Full-tuning | 17.06 GB | 38.72 GB | 18 |
| LoRA | 7.91 GB | 16.32 GB | 1.8 |
| **QLoRA** | **5.21 GB** | **7.52 GB** | **0.6** |

**关键洞察**: QLoRA 内存效率是全量微调的 30 倍，让消费级 GPU 可以微调大模型。