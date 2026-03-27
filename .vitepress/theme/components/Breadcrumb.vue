<script setup lang="ts">
import { computed } from 'vue'
import { useData, useRoute } from 'vitepress'

const route = useRoute()
const { site } = useData()

// 生成面包屑导航
const breadcrumbs = computed(() => {
  const paths = route.path.split('/').filter(Boolean)
  const crumbs = [
    {
      name: '首页',
      path: '/'
    }
  ]

  let currentPath = ''
  paths.forEach((segment, index) => {
    currentPath += '/' + segment
    const isLast = index === paths.length - 1

    // 移除.html 后缀并转换为可读名称
    let name = segment.replace(/\.html$/, '')

    // 处理索引页
    if (name === 'index' || name === '') {
      name = paths[index - 1] || '首页'
    }

    // 转换连字符和数字
    name = name
      .replace(/-/g, ' ')
      .replace(/\./g, ' ')
      .replace(/\b\w/g, c => c.toUpperCase())

    // 中文映射（常见路径）
    const nameMap: Record<string, string> = {
      'Ai': 'AI',
      'Ml': '机器学习',
      'Autogen': 'AutoGen',
      'Coding': '编程',
      'Finance': '金融',
      'StockAnalysis': '股票分析',
      'About': '关于',
      'Papers': '论文研读'
    }

    name = nameMap[name] || name

    if (!isLast) {
      crumbs.push({
        name,
        path: currentPath
      })
    }
  })

  return crumbs
})
</script>

<template>
  <nav class="breadcrumb" aria-label="Breadcrumb">
    <ol class="breadcrumb-list">
      <li v-for="(crumb, index) in breadcrumbs" :key="crumb.path" class="breadcrumb-item">
        <a
          v-if="index < breadcrumbs.length - 1"
          :href="crumb.path"
          class="breadcrumb-link"
        >
          {{ crumb.name }}
        </a>
        <span v-else class="breadcrumb-current">
          {{ crumb.name }}
        </span>
        <svg
          v-if="index < breadcrumbs.length - 1"
          class="breadcrumb-separator"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
        >
          <path d="M9 18l6-6-6-6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </li>
    </ol>
  </nav>
</template>

<style scoped>
.breadcrumb {
  padding: var(--vp-space-4) 0;
  margin-bottom: var(--vp-space-6);
  font-size: 0.875rem;
}

.breadcrumb-list {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 0;
  list-style: none;
  padding: 0;
  margin: 0;
}

.breadcrumb-item {
  display: flex;
  align-items: center;
  gap: var(--vp-space-2);
}

.breadcrumb-link {
  color: var(--vp-c-text-2);
  transition: color var(--vp-transition-fast);
}

.breadcrumb-link:hover {
  color: var(--vp-c-brand-1);
}

.breadcrumb-current {
  color: var(--vp-c-text-1);
  font-weight: 500;
}

.breadcrumb-separator {
  width: 16px;
  height: 16px;
  color: var(--vp-c-text-3);
  flex-shrink: 0;
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .breadcrumb {
    padding: var(--vp-space-2) 0;
  }

  .breadcrumb-list {
    gap: var(--vp-space-1);
  }

  .breadcrumb-separator {
    width: 14px;
    height: 14px;
  }
}
</style>
