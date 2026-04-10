---
title: Voice Wake & Talk Mode
type: concept
---

# Voice Wake & Talk Mode

> **定义**: OpenClaw 的语音交互系统，包含语音唤醒 (macOS/iOS) 和持续对话模式 (Android)。

## Voice Wake (语音唤醒)

- **支持平台**: macOS, iOS
- **触发方式**: 唤醒词检测
- **特点**:
  - 本地唤醒词处理
  - 零延迟响应
  - 无需手动激活

## Talk Mode (持续对话)

- **支持平台**: Android
- **触发方式**: 连续语音输入
- **TTS**: ElevenLabs + 系统 fallback
- **特点**:
  - 端到端语音对话
  - 无需点击/输入
  - 车载/居家场景友好

## 与传统语音助手对比

| 维度 | OpenClaw Voice | Siri/Alexa |
|------|----------------|------------|
| **唤醒词** | 自定义 | 固定 |
| **模型** | 任意 LLM | 固定 |
| **技能** | 5400+ ClawHub | 预定义 |
| **记忆** | 跨会话持久化 | 无 |

## 使用场景

- 🚗 车载场景（Android Talk Mode）
- 🏠 居家助手（macOS Voice Wake）
- 📱 移动办公（iOS Voice Wake）

## 相关概念

- [[Agent架构对比]]: 框架对比分析