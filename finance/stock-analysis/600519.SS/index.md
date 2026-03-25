---
title: 600519.SS 贵州茅台 分析报告
outline: [2, 3]
---

# 600519.SS 贵州茅台 分析报告

<StockTimeline :history="history" />

<script setup>
import { ref } from 'vue'
import data from './history.json?raw'
const history = JSON.parse(data)
</script>

最新报告日期：2026-03-25_1204

## 结论
**决策建议：买入（审慎左侧布局）**
当前贵州茅台处于“估值极端便宜”与“趋势极端弱势”的叠加态。尽管技术面呈现空头排列且存在死亡交叉风险，但基本面提供的安全边际（19.6 倍 PE，36% ROE，3.67% 股息率）足以覆盖短期波动风险。投资组合委员会决定采纳**买入**建议，但执行层面进行修正：采用分批建仓策略，初始仓位控制在 15%-20%，止损线上移至 1320 元，以平衡收益诉求与本金安全。
## 核心逻辑
1.  **估值锚定优势**：当前 PE TTM 约 19.63 倍，处于历史低位区间，远低于公司 36.31% 的 ROE 水平，具备极高的长期配置价值和安全边际。
2.  **现金流堡垒**：公司拥有 5220 亿元货币资金，而有息负债仅 2.69 亿元，极强的造血能力和净现金状态为股价提供了坚实底部支撑。
3.  **逆向交易机会**：技术面的弱势（均线空头、成交量萎缩）恰恰创造了左侧布局的良机，风险收益比大于 3:1，适合利用市场恐慌积累筹码。
## 风险
1.  **技术面杀伤力**：SMA50 与 SMA200 即将形成死亡交叉，可能触发量化模型自动抛售，导致短期股价加速下跌。
2.  **治理透明度疑虑**：1380 亿元“其他应收款”科目虽有风险缓冲，但资金占用效率及透明度问题可能在市场情绪恶化时被放大。
3.  **宏观消费逆风**：全球经济衰退担忧犹存，若高端消费数据不及预期，可能引发估值进一步压缩（戴维斯双杀）。
## 完整报告

- [完整分析报告](latest/complete_report)

### 分析师报告

- [市场分析](latest/1_analysts/market)
- [情绪分析](latest/1_analysts/sentiment)
- [新闻分析](latest/1_analysts/news)
- [基本面分析](latest/1_analysts/fundamentals)

### 研究报告

- [多方观点](latest/2_research/bull)
- [空方观点](latest/2_research/bear)
- [经理总结](latest/2_research/manager)

### 交易计划

- [交易员计划](latest/3_trading/trader)

### 风险评估

- [激进策略](latest/4_risk/aggressive)
- [中性策略](latest/4_risk/neutral)
- [保守策略](latest/4_risk/conservative)

### 投资决策

- [组合决策](latest/5_portfolio/decision)

