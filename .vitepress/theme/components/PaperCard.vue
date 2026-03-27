<script setup lang="ts">
interface Paper {
  title: string
  link: string
  category: string
  tags: string[]
  date?: string
  summary?: string
}

defineProps<{
  paper: Paper
}>()

// 格式化日期
function formatDate(dateStr?: string): string {
  if (!dateStr) return ''
  try {
    const date = new Date(dateStr)
    return date.toLocaleDateString('zh-CN', {
      year: 'numeric',
      month: '2-digit',
      day: '2-digit'
    })
  } catch {
    return dateStr
  }
}

// 获取分类颜色
function getCategoryColor(category: string): string {
  const colors: Record<string, string> = {
    'Agent': '#8b5cf6',
    'RAG': '#06b6d4',
    'Finance': '#10b981',
    'Multimodal': '#f59e0b',
    'Optimization': '#3b82f6',
    'Memory': '#ec4899',
    'Framework': '#6366f1',
    'World Model': '#14b8a6',
    'RL': '#f43f5e'
  }
  return colors[category] || '#3b82f6'
}
</script>

<template>
  <a :href="paper.link" class="paper-card">
    <div class="card-header">
      <span
        class="category-badge"
        :style="{ backgroundColor: getCategoryColor(paper.category) + '20', color: getCategoryColor(paper.category) }"
      >
        {{ paper.category }}
      </span>
      <span v-if="paper.date" class="paper-date">
        {{ formatDate(paper.date) }}
      </span>
    </div>

    <h3 class="paper-title">{{ paper.title }}</h3>

    <p v-if="paper.summary" class="paper-summary">
      {{ paper.summary }}
    </p>

    <div class="card-footer">
      <div class="tags-wrapper">
        <span
          v-for="tag in paper.tags.slice(0, 5)"
          :key="tag"
          class="paper-tag"
        >
          {{ tag }}
        </span>
        <span
          v-if="paper.tags.length > 5"
          class="paper-tag more"
        >
          +{{ paper.tags.length - 5 }}
        </span>
      </div>
    </div>
  </a>
</template>

<style scoped>
.paper-card {
  display: block;
  padding: var(--vp-space-6);
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: var(--vp-radius-lg);
  transition: all var(--vp-transition-base);
  text-decoration: none;
}

.paper-card:hover {
  border-color: var(--vp-c-brand-2);
  box-shadow: var(--vp-shadow-md);
  transform: translateY(-4px);
  text-decoration: none;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--vp-space-3);
  gap: var(--vp-space-2);
}

.category-badge {
  display: inline-block;
  padding: var(--vp-space-1) var(--vp-space-2);
  font-size: 0.75rem;
  font-weight: 600;
  border-radius: var(--vp-radius-sm);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.paper-date {
  font-size: 0.75rem;
  color: var(--vp-c-text-3);
  white-space: nowrap;
}

.paper-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: var(--vp-space-3);
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.paper-card:hover .paper-title {
  color: var(--vp-c-brand-1);
}

.paper-summary {
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  line-height: 1.6;
  margin-bottom: var(--vp-space-4);
  display: -webkit-box;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: flex-start;
  align-items: center;
}

.tags-wrapper {
  display: flex;
  flex-wrap: wrap;
  gap: var(--vp-space-2);
}

.paper-tag {
  display: inline-block;
  padding: var(--vp-space-1) var(--vp-space-2);
  font-size: 0.75rem;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg-soft);
  border-radius: var(--vp-radius-sm);
  transition: all var(--vp-transition-fast);
}

.paper-tag:hover {
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
}

.paper-tag.more {
  font-weight: 600;
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .paper-card {
    padding: var(--vp-space-4);
  }

  .paper-title {
    font-size: 1rem;
  }

  .paper-summary {
    -webkit-line-clamp: 3;
  }
}
</style>
