import DefaultTheme from 'vitepress/theme'
import './custom.css'
import StockTimeline from './components/StockTimeline.vue'

export default {
  extends: DefaultTheme,
  enhanceApp({ app, router, siteData }) {
    // 全局注册 StockTimeline 组件
    app.component('StockTimeline', StockTimeline)
  }
}
