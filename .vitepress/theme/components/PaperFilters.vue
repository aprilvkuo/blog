<script setup lang="ts">
import { ref, computed, emit } from 'vue'

interface Paper {
  title: string
  link: string
  category: string
  tags: string[]
  date?: string
}

const props = defineProps<{
  papers: Paper[]
}>()

const emit = defineEmits<{
  (e: 'filter', papers: Paper[]): void
}>()

// 筛选状态
const searchQuery = ref('')
const selectedCategory = ref<string>('all')
const selectedTags = ref<Set<string>>(new Set())
const sortBy = ref<'date' | 'title'>('date')

// 提取所有分类
const categories = computed(() => {
  const cats = new Set(props.papers.map(p => p.category))
  return ['all', ...Array.from(cats)]
})

// 提取所有标签
const allTags = computed(() => {
  const tags = new Set<string>()
  props.papers.forEach(p => p.tags.forEach(t => tags.add(t)))
  return Array.from(tags).sort()
})

// 切换标签选择
function toggleTag(tag: string) {
  if (selectedTags.value.has(tag)) {
    selectedTags.value.delete(tag)
  } else {
    selectedTags.value.add(tag)
  }
  selectedTags.value = new Set(selectedTags.value)
  applyFilters()
}

// 应用筛选
function applyFilters() {
  let filtered = [...props.papers]

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p =>
      p.title.toLowerCase().includes(query) ||
      p.tags.some(t => t.toLowerCase().includes(query))
    )
  }

  // 分类过滤
  if (selectedCategory.value !== 'all') {
    filtered = filtered.filter(p => p.category === selectedCategory.value)
  }

  // 标签过滤
  if (selectedTags.value.size > 0) {
    filtered = filtered.filter(p =>
      Array.from(selectedTags.value).every(tag => p.tags.includes(tag))
    )
  }

  // 排序
  if (sortBy.value === 'title') {
    filtered.sort((a, b) => a.title.localeCompare(b.title, 'zh-CN'))
  } else if (sortBy.value === 'date') {
    filtered.sort((a, b) => {
      if (!a.date) return 1
      if (!b.date) return -1
      return new Date(b.date).getTime() - new Date(a.date).getTime()
    })
  }

  emit('filter', filtered)
}

// 清除所有筛选
function clearFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'all'
  selectedTags.value = new Set()
  applyFilters()
}

// 计算激活的筛选器数量
const activeFiltersCount = computed(() => {
  let count = 0
  if (searchQuery.value) count++
  if (selectedCategory.value !== 'all') count++
  count += selectedTags.value.size
  return count
})

// 检查标签是否被选中
function isTagSelected(tag: string): boolean {
  return selectedTags.value.has(tag)
}

// 论文数量（由父组件传递更新）
const papersCount = ref(props.papers.length)

// 暴露更新数量的方法给父组件
defineExpose({
  updateCount: (count: number) => {
    papersCount.value = count
  }
})
</script>

<template>
  <div class="paper-filters">
    <!-- 搜索栏 -->
    <div class="filter-section search-section">
      <div class="search-wrapper">
        <svg class="search-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <circle cx="11" cy="11" r="8" stroke-width="2"/>
          <path d="M21 21l-4.35-4.35" stroke-width="2" stroke-linecap="round"/>
        </svg>
        <input
          v-model="searchQuery"
          @input="applyFilters"
          type="text"
          class="search-input"
          placeholder="搜索论文标题或标签..."
        />
        <button
          v-if="searchQuery"
          @click="searchQuery = ''; applyFilters()"
          class="search-clear"
        >
          ×
        </button>
      </div>
    </div>

    <!-- 筛选控制 -->
    <div class="filter-controls">
      <!-- 分类选择 -->
      <div class="filter-group">
        <label class="filter-label">分类</label>
        <select
          v-model="selectedCategory"
          @change="applyFilters"
          class="filter-select"
        >
          <option value="all">全部分类</option>
          <option v-for="cat in categories.filter(c => c !== 'all')" :key="cat" :value="cat">
            {{ cat }}
          </option>
        </select>
      </div>

      <!-- 排序选项 -->
      <div class="filter-group">
        <label class="filter-label">排序</label>
        <select
          v-model="sortBy"
          @change="applyFilters"
          class="filter-select"
        >
          <option value="date">按日期</option>
          <option value="title">按标题</option>
        </select>
      </div>

      <!-- 清除筛选 -->
      <button
        v-if="activeFiltersCount > 0"
        @click="clearFilters"
        class="clear-btn"
      >
        清除筛选
        <span class="clear-count">{{ activeFiltersCount }}</span>
      </button>
    </div>

    <!-- 标签筛选器 -->
    <div class="tags-section">
      <div class="tags-label">标签筛选：</div>
      <div class="tags-cloud">
        <button
          v-for="tag in allTags"
          :key="tag"
          @click="toggleTag(tag)"
          class="tag-btn"
          :class="{ active: isTagSelected(tag) }"
        >
          {{ tag }}
        </button>
      </div>
    </div>

    <!-- 筛选结果统计 -->
    <div class="results-info">
      找到 {{ papersCount }} 篇论文
    </div>
  </div>
</template>

<style scoped>
.paper-filters {
  background: var(--vp-c-bg-soft);
  border-radius: var(--vp-radius-xl);
  padding: var(--vp-space-6);
  margin-bottom: var(--vp-space-8);
  border: 1px solid var(--vp-c-divider);
}

/* 搜索区域 */
.search-section {
  margin-bottom: var(--vp-space-6);
}

.search-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: var(--vp-space-4);
  width: 20px;
  height: 20px;
  color: var(--vp-c-text-3);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: var(--vp-space-3) var(--vp-space-12);
  font-size: 0.95rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: var(--vp-radius-lg);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  transition: all var(--vp-transition-fast);
}

.search-input:focus {
  outline: none;
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 0 0 3px var(--vp-c-brand-soft);
}

.search-input::placeholder {
  color: var(--vp-c-text-3);
}

.search-clear {
  position: absolute;
  right: var(--vp-space-3);
  width: 24px;
  height: 24px;
  border: none;
  background: var(--vp-c-bg-soft);
  color: var(--vp-c-text-2);
  border-radius: 50%;
  font-size: 1.25rem;
  line-height: 1;
  cursor: pointer;
  transition: all var(--vp-transition-fast);
  display: flex;
  align-items: center;
  justify-content: center;
}

.search-clear:hover {
  background: var(--vp-c-brand-soft);
  color: var(--vp-c-brand-1);
}

/* 筛选控制 */
.filter-controls {
  display: flex;
  gap: var(--vp-space-4);
  align-items: flex-end;
  flex-wrap: wrap;
  margin-bottom: var(--vp-space-6);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--vp-space-2);
}

.filter-label {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--vp-c-text-2);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.filter-select {
  padding: var(--vp-space-2) var(--vp-space-4);
  font-size: 0.9rem;
  border: 1px solid var(--vp-c-divider);
  border-radius: var(--vp-radius-md);
  background: var(--vp-c-bg);
  color: var(--vp-c-text-1);
  cursor: pointer;
  min-width: 120px;
  transition: all var(--vp-transition-fast);
}

.filter-select:focus {
  outline: none;
  border-color: var(--vp-c-brand-1);
}

.clear-btn {
  display: flex;
  align-items: center;
  gap: var(--vp-space-2);
  padding: var(--vp-space-2) var(--vp-space-4);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: var(--vp-radius-md);
  cursor: pointer;
  transition: all var(--vp-transition-fast);
  margin-left: auto;
}

.clear-btn:hover {
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
}

.clear-count {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  padding: 0 4px;
  font-size: 0.75rem;
  font-weight: 600;
  color: white;
  background: var(--vp-c-brand-1);
  border-radius: 10px;
}

/* 标签区域 */
.tags-section {
  margin-bottom: var(--vp-space-4);
}

.tags-label {
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--vp-c-text-2);
  margin-bottom: var(--vp-space-3);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.tags-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: var(--vp-space-2);
}

.tag-btn {
  padding: var(--vp-space-2) var(--vp-space-3);
  font-size: 0.8rem;
  font-weight: 500;
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: var(--vp-radius-md);
  cursor: pointer;
  transition: all var(--vp-transition-fast);
}

.tag-btn:hover {
  color: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
}

.tag-btn.active {
  color: white;
  background: var(--vp-c-brand-1);
  border-color: var(--vp-c-brand-1);
  box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

/* 结果信息 */
.results-info {
  font-size: 0.875rem;
  color: var(--vp-c-text-3);
  padding-top: var(--vp-space-4);
  border-top: 1px solid var(--vp-c-divider);
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .paper-filters {
    padding: var(--vp-space-4);
  }

  .filter-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .filter-select {
    width: 100%;
  }

  .clear-btn {
    margin-left: 0;
    justify-content: center;
  }

  .tags-cloud {
    gap: var(--vp-space-1);
  }

  .tag-btn {
    padding: var(--vp-space-1) var(--vp-space-2);
    font-size: 0.75rem;
  }
}
</style>
