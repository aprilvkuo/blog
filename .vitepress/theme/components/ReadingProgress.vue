<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const progress = ref(0)
const isVisible = ref(false)

function updateProgress() {
  const el = document.documentElement
  const scrollTop = el.scrollTop
  const scrollHeight = el.scrollHeight - el.clientHeight
  const scrolled = (scrollTop / scrollHeight) * 100
  progress.value = Math.min(100, Math.max(0, scrolled))

  // 滚动超过 10% 显示进度条
  isVisible.value = scrolled > 10
}

onMounted(() => {
  window.addEventListener('scroll', updateProgress, { passive: true })
  updateProgress()
})

onUnmounted(() => {
  window.removeEventListener('scroll', updateProgress)
})
</script>

<template>
  <div
    class="reading-progress-container"
    :class="{ visible: isVisible }"
  >
    <div
      class="reading-progress-bar"
      :style="{ width: progress + '%' }"
    />
  </div>
</template>

<style scoped>
.reading-progress-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  z-index: 1000;
  background: transparent;
  opacity: 0;
  transition: opacity var(--vp-transition-base);
}

.reading-progress-container.visible {
  opacity: 1;
}

.reading-progress-bar {
  height: 100%;
  background: var(--vp-gradient-brand);
  transition: width var(--vp-transition-fast);
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

/* 暗黑模式适配 */
.dark .reading-progress-bar {
  box-shadow: 0 0 10px rgba(59, 130, 246, 0.7);
}
</style>
