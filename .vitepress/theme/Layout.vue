<script setup lang="ts">
import DefaultTheme from 'vitepress/theme'
import ReadingProgress from './components/ReadingProgress.vue'
import Breadcrumb from './components/Breadcrumb.vue'

const { Layout } = DefaultTheme
</script>

<template>
  <Layout>
    <!-- 阅读进度条 - 在所有页面顶部显示 -->
    <template #layout-top>
      <ReadingProgress />
    </template>

    <!-- 面包屑导航 - 在文档内容上方显示 -->
    <template #doc-before>
      <Breadcrumb />
    </template>
  </Layout>
</template>

<style>
/* 调整布局以适配面包屑 */
.VPDoc .container {
  padding-top: var(--vp-nav-height) !important;
}

.VPDoc .content-container {
  padding-top: 0;
}

/* ReadingProgress 样式 */
.reading-progress-container {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 3px;
  z-index: 9999;
  pointer-events: none;
}
</style>
