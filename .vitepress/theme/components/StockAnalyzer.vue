<template>
  <div class="stock-analyzer">
    <div class="analyzer-card">
      <h2>股票分析</h2>
      <p class="description">输入股票代码或名称，AI 将自动分析并生成报告</p>

      <form @submit.prevent="submitAnalysis" class="analysis-form">
        <div class="form-group">
          <input
            v-model="symbol"
            type="text"
            placeholder="例如：多氟多 或 002594.SZ"
            class="symbol-input"
            required
          />
          <button type="submit" :disabled="isSubmitting" class="submit-btn">
            <span v-if="!isSubmitting">开始分析</span>
            <span v-else class="loading">分析中...</span>
          </button>
        </div>
      </form>

      <!-- 当前任务状态 -->
      <div v-if="currentTask" class="task-status" :class="currentTask.status">
        <div class="status-header">
          <span class="status-icon">{{ getStatusIcon(currentTask.status) }}</span>
          <span class="status-text">{{ getStatusText(currentTask.status) }}</span>
          <span class="status-time">{{ formatTime(currentTask.created_at) }}</span>
        </div>
        <div v-if="currentTask.status === 'pending'" class="status-detail">
          <p>任务已提交，等待处理...</p>
          <div class="progress-bar">
            <div class="progress-indeterminate"></div>
          </div>
        </div>
        <div v-if="currentTask.status === 'running'" class="status-detail">
          <p>正在分析股票数据...</p>
          <div class="progress-bar">
            <div class="progress-indeterminate"></div>
          </div>
        </div>
        <div v-if="currentTask.status === 'completed'" class="status-detail">
          <p class="success">分析完成！</p>
          <a v-if="currentTask.result?.blog_path" :href="'/' + currentTask.result.blog_path" class="view-report-btn">
            查看报告 →
          </a>
        </div>
        <div v-if="currentTask.status === 'failed'" class="status-detail error">
          <p>分析失败：{{ currentTask.result?.error || '未知错误' }}</p>
        </div>
      </div>

      <!-- 历史任务列表 -->
      <div v-if="historyTasks.length > 0" class="history-tasks">
        <h3>最近分析</h3>
        <ul class="task-list">
          <li v-for="task in historyTasks" :key="task.id" class="task-item">
            <span class="task-symbol">{{ task.symbol }}</span>
            <span class="task-status-badge" :class="task.status">{{ getStatusIcon(task.status) }}</span>
            <span class="task-time">{{ formatTime(task.created_at) }}</span>
            <a v-if="task.status === 'completed' && task.result?.blog_path"
               :href="'/' + task.result.blog_path"
               class="view-link">查看</a>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

// API 配置
const API_BASE = '/api/analyze'

// 状态
const symbol = ref('')
const isSubmitting = ref(false)
const currentTask = ref(null)
const historyTasks = ref([])
const pollingInterval = ref(null)

// 提交分析
async function submitAnalysis() {
  if (!symbol.value.trim()) return

  isSubmitting.value = true

  try {
    const response = await fetch(API_BASE, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        symbol: symbol.value,
      }),
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || '提交失败')
    }

    const data = await response.json()
    currentTask.value = {
      id: data.task_id,
      status: data.status,
      symbol: symbol.value,
      created_at: Date.now(),
    }

    // 开始轮询任务状态
    startPolling(data.task_id)

    // 清空输入
    symbol.value = ''

  } catch (error) {
    alert(`提交失败：${error.message}`)
  } finally {
    isSubmitting.value = false
  }
}

// 轮询任务状态
function startPolling(taskId) {
  // 清除之前的轮询
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
  }

  // 立即查询一次
  pollTaskStatus(taskId)

  // 设置轮询
  pollingInterval.value = setInterval(() => {
    pollTaskStatus(taskId)
  }, 3000) // 每 3 秒查询一次
}

async function pollTaskStatus(taskId) {
  try {
    const response = await fetch(`${API_BASE}/${taskId}`, {})

    if (!response.ok) {
      if (response.status === 404) {
        // 任务可能被清理了
        stopPolling()
        return
      }
      throw new Error('查询失败')
    }

    const task = await response.json()
    currentTask.value = task

    // 如果任务已完成或失败，停止轮询
    if (task.status === 'completed' || task.status === 'failed') {
      stopPolling()

      // 添加到历史记录
      if (task.status === 'completed') {
        historyTasks.value.unshift(task)
        // 只保留最近 10 条
        historyTasks.value = historyTasks.value.slice(0, 10)
        // 保存到 localStorage
        saveHistory()
      }

      // 通知用户
      if (task.status === 'completed') {
        // 可以添加 toast 通知
      }
    }
  } catch (error) {
    console.error('轮询失败:', error)
  }
}

function stopPolling() {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
}

// 获取状态图标
function getStatusIcon(status) {
  const icons = {
    pending: '⏳',
    running: '🔍',
    completed: '✅',
    failed: '❌',
  }
  return icons[status] || '❓'
}

// 获取状态文本
function getStatusText(status) {
  const texts = {
    pending: '等待处理',
    running: '分析中',
    completed: '已完成',
    failed: '失败',
  }
  return texts[status] || '未知'
}

// 格式化时间
function formatTime(timestamp) {
  if (!timestamp) return ''
  const date = new Date(timestamp)
  const now = new Date()
  const diff = now - date

  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return `${Math.floor(diff / 60000)}分钟前`
  if (diff < 86400000) return `${Math.floor(diff / 3600000)}小时前`
  return date.toLocaleDateString('zh-CN')
}

// 本地存储历史
function saveHistory() {
  localStorage.setItem('stockAnalysisHistory', JSON.stringify(historyTasks.value))
}

function loadHistory() {
  try {
    const saved = localStorage.getItem('stockAnalysisHistory')
    if (saved) {
      historyTasks.value = JSON.parse(saved)
    }
  } catch (e) {
    console.error('加载历史失败:', e)
  }
}

onMounted(() => {
  loadHistory()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<style scoped>
.stock-analyzer {
  margin: 2rem 0;
}

.analyzer-card {
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--vp-c-divider);
}

.analyzer-card h2 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
}

.description {
  color: var(--vp-c-text-2);
  font-size: 0.875rem;
  margin-bottom: 1.5rem;
}

.analysis-form {
  margin-bottom: 1.5rem;
}

.form-group {
  display: flex;
  gap: 0.75rem;
}

.symbol-input {
  flex: 1;
  padding: 0.75rem 1rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  font-size: 1rem;
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
}

.symbol-input:focus {
  outline: none;
  border-color: var(--vp-c-brand);
}

.submit-btn {
  padding: 0.75rem 1.5rem;
  background: var(--vp-c-brand);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: var(--vp-c-brand-dark);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.task-status {
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1.5rem;
  border: 1px solid;
}

.task-status.pending {
  background: var(--vp-c-yellow-light);
  border-color: var(--vp-c-yellow);
}

.task-status.running {
  background: var(--vp-c-blue-light);
  border-color: var(--vp-c-blue);
}

.task-status.completed {
  background: var(--vp-c-green-light);
  border-color: var(--vp-c-green);
}

.task-status.failed {
  background: var(--vp-c-red-light);
  border-color: var(--vp-c-red);
}

.status-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.status-icon {
  font-size: 1.25rem;
}

.status-time {
  margin-left: auto;
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
}

.status-detail {
  margin-top: 0.75rem;
  font-size: 0.875rem;
}

.status-detail.error {
  color: var(--vp-c-red);
}

.success {
  color: var(--vp-c-green);
}

.progress-bar {
  margin-top: 0.5rem;
  height: 3px;
  background: var(--vp-c-divider);
  border-radius: 2px;
  overflow: hidden;
}

.progress-indeterminate {
  height: 100%;
  width: 30%;
  background: var(--vp-c-brand);
  animation: progress 1.5s infinite;
}

@keyframes progress {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(400%);
  }
}

.view-report-btn {
  display: inline-block;
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: var(--vp-c-brand);
  color: white;
  text-decoration: none;
  border-radius: 6px;
  font-size: 0.875rem;
}

.view-report-btn:hover {
  background: var(--vp-c-brand-dark);
}

.history-tasks {
  border-top: 1px solid var(--vp-c-divider);
  padding-top: 1rem;
}

.history-tasks h3 {
  font-size: 1rem;
  margin-bottom: 0.75rem;
  color: var(--vp-c-text-2);
}

.task-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.task-item {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 0;
  border-bottom: 1px solid var(--vp-c-divider-light);
  font-size: 0.875rem;
}

.task-item:last-child {
  border-bottom: none;
}

.task-symbol {
  flex: 1;
  font-weight: 500;
}

.task-status-badge {
  font-size: 0.75rem;
}

.task-time {
  color: var(--vp-c-text-3);
  font-size: 0.75rem;
}

.view-link {
  padding: 0.25rem 0.5rem;
  color: var(--vp-c-brand);
  text-decoration: none;
  border-radius: 4px;
  font-size: 0.75rem;
}

.view-link:hover {
  background: var(--vp-c-brand-light);
}
</style>
