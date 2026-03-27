import DefaultTheme from 'vitepress/theme'
import './custom.css'
import StockTimeline from './components/StockTimeline.vue'
import ReadingProgress from './components/ReadingProgress.vue'
import Breadcrumb from './components/Breadcrumb.vue'
import HomeFeatures from './components/HomeFeatures.vue'
import PaperFilters from './components/PaperFilters.vue'
import PaperCard from './components/PaperCard.vue'
import Layout from './Layout.vue'

export default {
  ...DefaultTheme,
  Layout,
  enhanceApp({ app, router, siteData }) {
    // 全局注册组件
    app.component('StockTimeline', StockTimeline)
    app.component('ReadingProgress', ReadingProgress)
    app.component('Breadcrumb', Breadcrumb)
    app.component('HomeFeatures', HomeFeatures)
    app.component('PaperFilters', PaperFilters)
    app.component('PaperCard', PaperCard)
  }
}
