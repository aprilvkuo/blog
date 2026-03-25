---
title: 300750.SZ 宁德时代 分析报告
outline: [2, 3]
---

# 300750.SZ 宁德时代 分析报告

最新报告日期：2026-03-25_1134

## 报告摘要

## 结论
**决策建议：减仓 50%**  
当前风险收益比已显著恶化。尽管公司长期基本面优异（ROE 23.83%，现金流充沛），但短期技术面出现高位缩量背离，且基本面存货增速远超营收增速，隐含营运效率下降风险。投资组合经理决定执行**减持 50%**策略，保留 50% 底仓追踪长期趋势，同时锁定部分利润以规避潜在回调。剩余仓位止损位设于 **380 元**，若有效跌破则清仓。
## 核心逻辑
1.  **技术面预警**：股价接近 52 周高点（424.36 元）但成交量萎缩超 60%，MACD 动能衰竭，显示买盘枯竭，高位滞涨大概率为派发信号而非蓄势。
2.  **基本面隐忧**：存货增速（58%）显著高于营收增速（36.6%），虽现金储备可覆盖存货，但营运效率恶化可能导致估值逻辑从“成长股”切换为“周期股”，引发杀估值。
3.  **宏观不确定性**：A/H 股溢价率高达 48% 处于历史极值，收敛风险大；地缘政治制裁虽未完全落地，但已压制估值上限，容错率极低。
## 风险
1.  **存货减值风险**：若行业需求放缓或技术路线迭代，945 亿存货可能面临大幅减值，直接冲击利润表。
2.  **政策黑天鹅**：美国制裁政策若突然加码，可能导致股价跳空低开，预设止损线（380 元）可能失效。
3.  **踏空风险**：保留 50% 底仓旨在防止股价突破前高后彻底踏空，但需警惕减仓后若趋势延续带来的机会成本。
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


## 历史分析

<StockTimeline :history="history" />

<script setup>
import { ref } from 'vue'
import data from './history.json?raw'
const history = JSON.parse(data)
</script>
