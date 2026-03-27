<script setup lang="ts">
import { computed } from 'vue'

interface Feature {
  icon: string
  title: string
  details: string
  link: string
  linkText: string
}

const props = defineProps<{
  features: Feature[]
}>()

// 计算统计数据
const stats = computed(() => [
  { label: '分类', value: '4', suffix: '+' },
  { label: '论文', value: '20', suffix: '+' },
  { label: '股票分析', value: '15', suffix: '+' },
  { label: '更新', value: '每日', suffix: '' }
])
</script>

<template>
  <section class="home-features">
    <!-- 统计区域 -->
    <div class="features-stats">
      <div v-for="stat in stats" :key="stat.label" class="stat-card">
        <div class="stat-value">
          {{ stat.value }}<span class="stat-suffix">{{ stat.suffix }}</span>
        </div>
        <div class="stat-label">{{ stat.label }}</div>
      </div>
    </div>

    <!-- 特性卡片 -->
    <div class="features-grid">
      <div
        v-for="(feature, index) in features"
        :key="index"
        class="feature-card"
        :style="{ '--animation-delay': `${index * 0.1}s` }"
      >
        <div class="feature-icon">{{ feature.icon }}</div>
        <h3 class="feature-title">{{ feature.title }}</h3>
        <p class="feature-details">{{ feature.details }}</p>
        <a :href="feature.link" class="feature-link">
          {{ feature.linkText }}
          <span class="feature-arrow">→</span>
        </a>
      </div>
    </div>
  </section>
</template>

<style scoped>
.home-features {
  padding: var(--vp-space-16) 0;
  max-width: 1200px;
  margin: 0 auto;
}

/* 统计区域 */
.features-stats {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--vp-space-6);
  margin-bottom: var(--vp-space-16);
  padding: var(--vp-space-8);
  background: var(--vp-c-bg-soft);
  border-radius: var(--vp-radius-xl);
  border: 1px solid var(--vp-c-divider);
}

.stat-card {
  text-align: center;
  padding: var(--vp-space-6);
  transition: transform var(--vp-transition-base);
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 700;
  background: var(--vp-gradient-brand);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-suffix {
  font-size: 1.5rem;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.stat-label {
  margin-top: var(--vp-space-2);
  font-size: 0.875rem;
  color: var(--vp-c-text-2);
  font-weight: 500;
}

/* 特性卡片网格 */
.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--vp-space-8);
}

.feature-card {
  position: relative;
  padding: var(--vp-space-8);
  background: var(--vp-gradient-card);
  border: 1px solid var(--vp-c-divider);
  border-radius: var(--vp-radius-xl);
  transition: all var(--vp-transition-base);
  opacity: 0;
  animation: fadeInUp 0.5s ease forwards;
  animation-delay: var(--animation-delay, 0s);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feature-card:hover {
  border-color: var(--vp-c-brand-2);
  box-shadow: var(--vp-shadow-lg);
  transform: translateY(-8px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: var(--vp-space-4);
  display: inline-block;
  transition: transform var(--vp-transition-bounce);
}

.feature-card:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.feature-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: var(--vp-space-3);
}

.feature-details {
  font-size: 0.95rem;
  color: var(--vp-c-text-2);
  line-height: 1.6;
  margin-bottom: var(--vp-space-6);
}

.feature-link {
  display: inline-flex;
  align-items: center;
  gap: var(--vp-space-2);
  color: var(--vp-c-brand-1);
  font-weight: 500;
  font-size: 0.9rem;
  transition: gap var(--vp-transition-fast);
}

.feature-link:hover {
  gap: var(--vp-space-3);
}

.feature-arrow {
  transition: transform var(--vp-transition-fast);
}

.feature-link:hover .feature-arrow {
  transform: translateX(4px);
}

/* 暗黑模式适配 */
.dark .feature-card {
  background: linear-gradient(145deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%);
}

/* 移动端响应式 */
@media (max-width: 960px) {
  .features-stats {
    grid-template-columns: repeat(2, 1fr);
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .home-features {
    padding: var(--vp-space-8) 0;
  }

  .features-stats {
    grid-template-columns: repeat(2, 1fr);
    gap: var(--vp-space-4);
    padding: var(--vp-space-4);
  }

  .stat-value {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: var(--vp-space-4);
  }

  .feature-card {
    padding: var(--vp-space-6);
  }

  .feature-card:hover {
    transform: none;
  }
}
</style>
