<script setup lang="ts">
import { ref, computed } from 'vue'
import holdingsData from '../holdings.json?raw'

interface Position {
  symbol: string
  name: string
  shares: number
  avgCost: number
  currentPrice: number
  market: string
}

interface HoldingsData {
  updateDate: string
  totalValue: number
  positions: Position[]
}

const holdings = JSON.parse(holdingsData) as HoldingsData

// 计算每只股票的市值、盈亏等数据
const positionsWithStats = computed(() => {
  return holdings.positions.map(pos => {
    const marketValue = pos.shares * pos.currentPrice
    const costBasis = pos.shares * pos.avgCost
    const profitLoss = marketValue - costBasis
    const profitLossPercent = costBasis > 0 ? (profitLoss / costBasis) * 100 : 0
    return {
      ...pos,
      marketValue,
      costBasis,
      profitLoss,
      profitLossPercent
    }
  })
})

// 计算总持仓市值
const totalMarketValue = computed(() => {
  return positionsWithStats.value.reduce((sum, pos) => sum + pos.marketValue, 0)
})

// 计算总盈亏
const totalProfitLoss = computed(() => {
  return positionsWithStats.value.reduce((sum, pos) => sum + pos.profitLoss, 0)
})

// 计算总盈亏比例
const totalProfitLossPercent = computed(() => {
  const totalCost = positionsWithStats.value.reduce((sum, pos) => sum + pos.costBasis, 0)
  return totalCost > 0 ? (totalProfitLoss.value / totalCost) * 100 : 0
})

function formatNumber(num: number, decimals: number = 2): string {
  return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

function formatPercent(num: number): string {
  const sign = num >= 0 ? '+' : ''
  return `${sign}${num.toFixed(2)}%`
}
</script>

<template>
  <div class="portfolio-container">
    <div class="portfolio-header">
      <h2 class="portfolio-title">我的持仓</h2>
      <span class="portfolio-update">更新时间：{{ holdings.updateDate }}</span>
    </div>

    <!-- 总览卡片 -->
    <div class="overview-cards">
      <div class="overview-card">
        <div class="card-label">总市值</div>
        <div class="card-value">¥{{ formatNumber(totalMarketValue) }}</div>
      </div>
      <div class="overview-card">
        <div class="card-label">总盈亏</div>
        <div class="card-value" :class="totalProfitLoss >= 0 ? 'positive' : 'negative'">
          {{ totalProfitLoss >= 0 ? '+' : '' }}¥{{ formatNumber(totalProfitLoss) }}
        </div>
      </div>
      <div class="overview-card">
        <div class="card-label">总盈亏比例</div>
        <div class="card-value" :class="totalProfitLossPercent >= 0 ? 'positive' : 'negative'">
          {{ formatPercent(totalProfitLossPercent) }}
        </div>
      </div>
    </div>

    <!-- 持仓列表 -->
    <div class="positions-table">
      <table>
        <thead>
          <tr>
            <th>代码</th>
            <th>名称</th>
            <th>市场</th>
            <th>持股数</th>
            <th>成本价</th>
            <th>当前价</th>
            <th>市值</th>
            <th>盈亏</th>
            <th>盈亏%</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="pos in positionsWithStats" :key="pos.symbol">
            <td>
              <a :href="`/finance/stock-analysis/${pos.symbol}/`" class="symbol-link">
                {{ pos.symbol }}
              </a>
            </td>
            <td class="name-cell">{{ pos.name }}</td>
            <td><span class="market-tag">{{ pos.market }}</span></td>
            <td class="number-cell">{{ formatNumber(pos.shares, 0) }}</td>
            <td class="number-cell">¥{{ formatNumber(pos.avgCost) }}</td>
            <td class="number-cell">¥{{ formatNumber(pos.currentPrice) }}</td>
            <td class="number-cell">¥{{ formatNumber(pos.marketValue) }}</td>
            <td class="number-cell" :class="pos.profitLoss >= 0 ? 'positive' : 'negative'">
              {{ pos.profitLoss >= 0 ? '+' : '' }}¥{{ formatNumber(pos.profitLoss) }}
            </td>
            <td class="number-cell" :class="pos.profitLossPercent >= 0 ? 'positive' : 'negative'">
              {{ formatPercent(pos.profitLossPercent) }}
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="positionsWithStats.length === 0" class="empty-notice">
      暂无持仓数据，请在 holdings.json 中添加持仓信息。
    </div>
  </div>
</template>

<style scoped>
.portfolio-container {
  padding: 1rem;
  max-width: 1200px;
  margin: 0 auto;
}

.portfolio-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.portfolio-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.portfolio-update {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
}

.overview-card {
  padding: 1.25rem;
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
}

.card-label {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  margin-bottom: 0.5rem;
}

.card-value {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
}

.card-value.positive {
  color: #10b981;
}

.card-value.negative {
  color: #ef4444;
}

.positions-table {
  overflow-x: auto;
}

.positions-table table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.875rem;
}

.positions-table th,
.positions-table td {
  padding: 0.75rem 1rem;
  text-align: left;
  border-bottom: 1px solid var(--vp-c-divider-light);
}

.positions-table th {
  background: var(--vp-c-bg-soft);
  font-weight: 600;
  color: var(--vp-c-text-2);
  white-space: nowrap;
}

.positions-table td {
  color: var(--vp-c-text-1);
}

.positions-table tbody tr:hover {
  background: var(--vp-c-bg-alt);
}

.number-cell {
  text-align: right;
  font-family: 'SF Mono', Monaco, 'Cascadia Code', monospace;
}

.positive {
  color: #10b981;
}

.negative {
  color: #ef4444;
}

.symbol-link {
  color: var(--vp-c-brand);
  text-decoration: none;
  font-weight: 500;
}

.symbol-link:hover {
  text-decoration: underline;
}

.market-tag {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: var(--vp-c-brand);
  color: white;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.empty-notice {
  text-align: center;
  padding: 3rem;
  color: var(--vp-c-text-2);
  font-size: 1rem;
}
</style>
