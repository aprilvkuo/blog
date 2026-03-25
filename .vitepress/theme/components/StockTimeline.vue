<script setup lang="ts">
import { ref, computed } from 'vue'

interface HistoryItem {
  date: string
  displayDate: string
  displayTime?: string
  sentiment: 'bull' | 'bear' | 'neutral'
  sentimentLabel: string
  sentimentIcon: string
  summary: string
  signals: string[]
  score?: number
  analystReports?: string[]
  reportPath: string
}

const props = defineProps<{
  history: HistoryItem[]
}>()

// 计算报告总数
const totalReports = computed(() => props.history.length)

const expandedItems = ref<Set<string>>(new Set())

const sentimentColors = {
  bull: 'color: #10b981;',
  bear: 'color: #ef4444;',
  neutral: 'color: #f59e0b;'
}

function toggleExpand(date: string) {
  if (expandedItems.value.has(date)) {
    expandedItems.value.delete(date)
  } else {
    expandedItems.value.add(date)
  }
  expandedItems.value = new Set(expandedItems.value)
}

function isExpanded(date: string): boolean {
  return expandedItems.value.has(date)
}
</script>

<template>
  <div class="timeline-container">
    <div class="timeline-header-row">
      <h3 class="timeline-title">📅 历史分析</h3>
      <span class="timeline-count" v-if="totalReports > 0">共 {{ totalReports }} 份报告</span>
    </div>
    <div class="timeline">
      <div
        v-for="item in history"
        :key="item.date"
        class="timeline-item"
        :class="{ expanded: isExpanded(item.date) }"
      >
        <div class="timeline-header" @click="toggleExpand(item.date)">
          <div class="timeline-date-wrapper">
            <span class="timeline-date">{{ item.displayDate }}</span>
            <span class="timeline-time" v-if="item.displayTime">{{ item.displayTime }}</span>
          </div>
          <span
            class="timeline-sentiment"
            :style="sentimentColors[item.sentiment]"
          >
            {{ item.sentimentIcon }} {{ item.sentimentLabel }}
          </span>
          <span class="timeline-toggle">{{ isExpanded(item.date) ? '−' : '+' }}</span>
        </div>

        <div v-if="isExpanded(item.date)" class="timeline-content">
          <div class="timeline-summary">
            <strong>结论:</strong> {{ item.summary }}
          </div>
          <div v-if="item.analystReports && item.analystReports.length" class="timeline-analysts">
            <strong>分析报告:</strong>
            <span class="analyst-tags">
              <span v-for="(report, index) in item.analystReports" :key="index" class="analyst-tag">
                {{ report }}
              </span>
            </span>
          </div>
          <div v-if="item.signals && item.signals.length" class="timeline-signals">
            <strong>信号:</strong>
            <ul>
              <li v-for="(signal, index) in item.signals" :key="index">{{ signal }}</li>
            </ul>
          </div>
          <div v-if="item.score" class="timeline-score">
            <strong>评分:</strong> {{ item.score }}/10
          </div>
          <a :href="item.reportPath" class="timeline-link">查看完整报告 →</a>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.timeline-container {
  margin-top: 2rem;
  padding: 1.5rem;
  background: var(--vp-c-bg-soft);
  border-radius: 12px;
  border: 1px solid var(--vp-c-divider);
}

.timeline-header-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 1rem;
}

.timeline-title {
  font-size: 1rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin: 0;
}

.timeline-count {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  font-weight: 500;
}

.timeline {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.timeline-item {
  border: 1px solid var(--vp-c-divider-light);
  border-radius: 8px;
  overflow: hidden;
  transition: all 0.2s ease;
}

.timeline-item:hover {
  border-color: var(--vp-c-brand);
}

.timeline-item.expanded {
  border-color: var(--vp-c-brand);
  background: var(--vp-c-bg-alt);
}

.timeline-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  cursor: pointer;
  user-select: none;
  gap: 1rem;
}

.timeline-date {
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--vp-c-text-2);
  white-space: nowrap;
}

.timeline-date-wrapper {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.timeline-time {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
  white-space: nowrap;
}

.timeline-sentiment {
  font-size: 0.875rem;
  font-weight: 600;
  white-space: nowrap;
}

.timeline-toggle {
  font-size: 1.25rem;
  font-weight: 300;
  color: var(--vp-c-text-3);
  width: 1.5rem;
  text-align: center;
}

.timeline-content {
  padding: 1rem 1rem 1rem;
  border-top: 1px solid var(--vp-c-divider-light);
  font-size: 0.875rem;
  line-height: 1.6;
}

.timeline-summary {
  margin-bottom: 0.75rem;
  color: var(--vp-c-text-2);
}

.timeline-analysts {
  margin-bottom: 0.75rem;
  color: var(--vp-c-text-2);
}

.analyst-tags {
  display: inline-flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-left: 0.5rem;
}

.analyst-tag {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: var(--vp-c-brand);
  color: white;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 500;
}

.timeline-signals {
  margin-bottom: 0.75rem;
  color: var(--vp-c-text-2);
}

.timeline-signals ul {
  margin: 0.5rem 0 0 1.25rem;
  padding: 0;
}

.timeline-signals li {
  margin-bottom: 0.25rem;
  color: var(--vp-c-text-3);
}

.timeline-score {
  margin-bottom: 0.75rem;
  color: var(--vp-c-text-2);
}

.timeline-link {
  display: inline-block;
  color: var(--vp-c-brand);
  text-decoration: none;
  font-weight: 500;
  transition: opacity 0.2s;
}

.timeline-link:hover {
  opacity: 0.8;
  text-decoration: underline;
}

@media (max-width: 768px) {
  .timeline-header {
    flex-wrap: wrap;
    gap: 0.5rem;
  }

  .timeline-date {
    order: 1;
  }

  .timeline-sentiment {
    order: 2;
  }

  .timeline-toggle {
    margin-left: auto;
    order: 3;
  }
}
</style>
