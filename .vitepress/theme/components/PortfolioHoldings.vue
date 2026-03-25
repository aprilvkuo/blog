<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface Holding {
  symbol: string
  name: string
  market: string
  shares: number
  cost_price: number
  current_price: number
  position_value?: number
  position_value_cny?: number
  position_ratio?: number
  profit_loss: number
  profit_loss_percent: number
  today_profit_loss?: number
  weight?: number
}

interface Account {
  id: string
  name: string
  type: string
  currency: string
  cash?: number
  market_value?: number
  total_value?: number
  profit_loss?: number
  profit_loss_percent?: number
  today_profit_loss?: number
  holdings: Holding[]
  summary?: {
    total_estimated_value_cny?: number
    total_profit_loss_cny?: number
    total_profit_loss_percent?: number
    winners?: number
    losers?: number
  }
}

interface Meta {
  name: string
  last_updated: string
  base_currency: string
  note: string
}

interface PortfolioData {
  meta: Meta
  accounts: Account[]
  notes?: string[]
}

// 在客户端加载持仓数据（从 public 目录的软链接文件）
const portfolio = ref<PortfolioData | null>(null)
const isLoading = ref(true)
const loadError = ref<string | null>(null)

onMounted(async () => {
  try {
    const response = await fetch('/portfolio.json')
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }
    portfolio.value = await response.json()
  } catch (err) {
    loadError.value = err instanceof Error ? err.message : '加载失败'
  } finally {
    isLoading.value = false
  }
})

// 合并所有账户的持仓
const allPositions = computed(() => {
  if (!portfolio.value) return []
  const positions: (Holding & { accountName: string; accountType: string })[] = []
  portfolio.value.accounts.forEach(account => {
    account.holdings.forEach(holding => {
      positions.push({
        ...holding,
        accountName: account.name,
        accountType: account.type
      })
    })
  })
  return positions
})

// 计算总市值
const totalValue = computed(() => {
  return portfolio.value?.accounts.reduce((sum, acc) => {
    return sum + (acc.total_value || acc.summary?.total_estimated_value_cny || 0)
  }, 0) || 0
})

// 计算总盈亏
const totalProfitLoss = computed(() => {
  return allPositions.value.reduce((sum, pos) => {
    return sum + (pos.profit_loss || 0)
  }, 0)
})

// 获取持仓数量
const totalPositions = computed(() => {
  return allPositions.value.length
})

function formatNumber(num: number, decimals: number = 2): string {
  return num.toFixed(decimals).replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

function formatPercent(num: number): string {
  const sign = num >= 0 ? '+' : ''
  return `${sign}${num.toFixed(2)}%`
}

function getMarketLabel(market: string): string {
  const map: Record<string, string> = {
    'US': '美股',
    'HK': '港股',
    'CN': 'A 股'
  }
  return map[market] || market
}

function getStockLink(symbol: string): string {
  // 转换符号格式以匹配股票分析目录
  let normalizedSymbol = symbol

  // 移除前导零（港股）
  if (normalizedSymbol.match(/^0\d{3}\.HK$/)) {
    normalizedSymbol = normalizedSymbol.replace(/^0+/, '')
  }

  return `/finance/stock-analysis/${normalizedSymbol}/`
}
</script>

<template>
  <div class="portfolio-container">
    <!-- 加载状态 -->
    <div v-if="isLoading" class="loading-state">加载持仓数据...</div>

    <!-- 错误状态 -->
    <div v-else-if="loadError" class="error-state">
      <p>加载失败：{{ loadError }}</p>
    </div>

    <!-- 数据展示 -->
    <template v-else-if="portfolio">
      <div class="portfolio-header">
        <div>
          <h2 class="portfolio-title">{{ portfolio.portfolio_name }}</h2>
          <p class="portfolio-notes" v-if="portfolio.notes">{{ portfolio.notes }}</p>
        </div>
        <span class="portfolio-update">更新时间：{{ portfolio.last_updated }}</span>
      </div>

      <!-- 总览卡片 -->
      <div class="overview-cards">
        <div class="overview-card">
          <div class="card-label">持仓数量</div>
          <div class="card-value">{{ totalPositions }} 只</div>
        </div>
        <div class="overview-card">
          <div class="card-label">账户数量</div>
          <div class="card-value">{{ portfolio.accounts.length }} 个</div>
        </div>
        <div class="overview-card">
          <div class="card-label">总盈亏</div>
          <div class="card-value" :class="totalProfitLoss >= 0 ? 'positive' : 'negative'">
            {{ totalProfitLoss >= 0 ? '+' : '' }}{{ formatNumber(totalProfitLoss) }}
          </div>
        </div>
      </div>

      <!-- 账户列表 -->
      <div class="accounts-section">
        <div v-for="(account, index) in portfolio.accounts" :key="index" class="account-card">
        <div class="account-header">
          <h3 class="account-name">{{ account.account_name }}</h3>
          <span class="account-type">{{ account.account_type }} · {{ account.currency }}</span>
        </div>

        <!-- 账户摘要 -->
        <div v-if="account.summary" class="account-summary">
          <span v-if="account.summary.total_market_value" class="summary-item">
            市值：{{ formatNumber(account.summary.total_market_value) }}
          </span>
          <span v-if="account.summary.total_estimated_value_cny" class="summary-item">
            估值：{{ formatNumber(account.summary.total_estimated_value_cny) }}
          </span>
          <span class="summary-item" :class="account.summary.total_profit_loss_percent && account.summary.total_profit_loss_percent >= 0 ? 'positive' : 'negative'">
            盈亏：{{ formatPercent(account.summary.total_profit_loss_percent || 0) }}
          </span>
          <span v-if="account.summary.winners !== undefined" class="summary-item">
            盈利：{{ account.summary.winners }} | 亏损：{{ account.summary.losers }}
          </span>
        </div>

        <!-- 持仓表格 -->
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
              <tr v-for="pos in account.holdings" :key="pos.symbol">
                <td>
                  <a :href="getStockLink(pos.symbol)" class="symbol-link" target="_blank">
                    {{ pos.symbol }}
                  </a>
                </td>
                <td class="name-cell">{{ pos.name }}</td>
                <td><span class="market-tag">{{ getMarketLabel(pos.market) }}</span></td>
                <td class="number-cell">{{ formatNumber(pos.shares, 0) }}</td>
                <td class="number-cell">{{ pos.cost_price ? formatNumber(pos.cost_price) : '-' }}</td>
                <td class="number-cell">{{ pos.current_price ? formatNumber(pos.current_price) : '-' }}</td>
                <td class="number-cell">
                  {{ formatNumber(pos.position_value || pos.position_value_hkd || pos.position_value_cny || 0) }}
                </td>
                <td class="number-cell" :class="pos.profit_loss && pos.profit_loss >= 0 ? 'positive' : 'negative'">
                  {{ pos.profit_loss ? (pos.profit_loss >= 0 ? '+' : '') + formatNumber(pos.profit_loss) : '-' }}
                </td>
                <td class="number-cell" :class="pos.profit_loss_percent && pos.profit_loss_percent >= 0 ? 'positive' : 'negative'">
                  {{ pos.profit_loss_percent ? formatPercent(pos.profit_loss_percent) : '-' }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
    </template>
  </div>
</template>

<style scoped>
.loading-state,
.error-state {
  text-align: center;
  padding: 3rem;
  color: var(--vp-c-text-2);
  font-size: 1rem;
}

.error-state {
  color: #ef4444;
}

<style scoped>
.portfolio-container {
  padding: 1rem;
  max-width: 1400px;
  margin: 0 auto;
}

.portfolio-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.portfolio-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0 0 0.5rem 0;
}

.portfolio-notes {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  margin: 0;
}

.portfolio-update {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  white-space: nowrap;
}

.overview-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
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

.accounts-section {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.account-card {
  background: var(--vp-c-bg-soft);
  border-radius: 8px;
  border: 1px solid var(--vp-c-divider);
  overflow: hidden;
}

.account-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.25rem;
  background: var(--vp-c-bg-alt);
  border-bottom: 1px solid var(--vp-c-divider);
}

.account-name {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.account-type {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
}

.account-summary {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  padding: 0.75rem 1.25rem;
  background: var(--vp-c-bg-alt);
  border-bottom: 1px solid var(--vp-c-divider-light);
}

.summary-item {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
}

.summary-item.positive {
  color: #10b981;
  font-weight: 600;
}

.summary-item.negative {
  color: #ef4444;
  font-weight: 600;
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
  background: var(--vp-c-bg-alt);
  font-weight: 600;
  color: var(--vp-c-text-2);
  white-space: nowrap;
}

.positions-table td {
  color: var(--vp-c-text-1);
}

.positions-table tbody tr:hover {
  background: var(--vp-c-bg-soft);
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

@media (max-width: 768px) {
  .portfolio-header {
    flex-direction: column;
  }

  .positions-table {
    font-size: 0.75rem;
  }

  .positions-table th,
  .positions-table td {
    padding: 0.5rem 0.75rem;
  }
}
</style>
