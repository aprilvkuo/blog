#!/bin/bash
# 股票分析报告同步脚本
# 将 TradingAgents 结果同步到博客的 stock-analysis 目录

set -e

# 配置路径
TRADING_AGENTS_DIR="/Users/egg/Project/TradingAgents"
BLOG_STOCKS_DIR="/Users/egg/Project/blog/finance/stock-analysis"
RESULTS_DIR="$TRADING_AGENTS_DIR/results"

echo "🔄 开始同步股票分析报告..."
echo "   源目录：$RESULTS_DIR"
echo "   目标目录：$BLOG_STOCKS_DIR"

# 创建目标目录
mkdir -p "$BLOG_STOCKS_DIR"

# 生成 index.md 的函数 - 根据实际存在的文件生成链接
generate_index_md() {
    local target_dir="$1"
    local latest_path="$2"
    local source_date="$3"
    local symbol=$(basename "$target_dir")

    # 开始生成 index.md
    cat > "$target_dir/index.md" << EOF
---
title: $symbol 分析报告
outline: [2, 3]
---

# $symbol 股票分析报告

最新报告日期：$source_date

EOF

    # 检查并生成各个部分的链接
    local has_content=false

    # 完整报告
    if [ -f "$latest_path/complete_report.md" ] || [ -f "$latest_path/complete_report.md" ]; then
        has_content=true
        echo "## 核心报告" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
        [ -f "$latest_path/complete_report.md" ] && echo "- [完整分析报告](latest/complete_report)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 最终交易决策 - 直接嵌入内容
    if [ -f "$latest_path/final_trade_decision.md" ]; then
        has_content=true
        echo "## 最终交易决策" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
        # 嵌入最终交易决策的内容
        cat "$latest_path/final_trade_decision.md" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 分析师报告 (1_analysts)
    if [ -d "$latest_path/1_analysts" ]; then
        has_content=true
        echo "### 分析师报告" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
        [ -f "$latest_path/1_analysts/market.md" ] && echo "- [市场分析](latest/1_analysts/market)" >> "$target_dir/index.md"
        [ -f "$latest_path/1_analysts/sentiment.md" ] && echo "- [情绪分析](latest/1_analysts/sentiment)" >> "$target_dir/index.md"
        [ -f "$latest_path/1_analysts/news.md" ] && echo "- [新闻分析](latest/1_analysts/news)" >> "$target_dir/index.md"
        [ -f "$latest_path/1_analysts/fundamentals.md" ] && echo "- [基本面分析](latest/1_analysts/fundamentals)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 研究报告 (2_research)
    if [ -d "$latest_path/2_research" ]; then
        has_content=true
        echo "### 研究报告" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
        [ -f "$latest_path/2_research/bull.md" ] && echo "- [多方观点](latest/2_research/bull)" >> "$target_dir/index.md"
        [ -f "$latest_path/2_research/bear.md" ] && echo "- [空方观点](latest/2_research/bear)" >> "$target_dir/index.md"
        [ -f "$latest_path/2_research/manager.md" ] && echo "- [经理总结](latest/2_research/manager)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 交易计划 (3_trading)
    if [ -d "$latest_path/3_trading" ]; then
        has_content=true
        echo "### 交易计划" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
        [ -f "$latest_path/3_trading/trader.md" ] && echo "- [交易员计划](latest/3_trading/trader)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 风险评估 (4_risk)
    if [ -d "$latest_path/4_risk" ]; then
        has_content=true
        echo "### 风险评估" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
        [ -f "$latest_path/4_risk/aggressive.md" ] && echo "- [激进策略](latest/4_risk/aggressive)" >> "$target_dir/index.md"
        [ -f "$latest_path/4_risk/neutral.md" ] && echo "- [中性策略](latest/4_risk/neutral)" >> "$target_dir/index.md"
        [ -f "$latest_path/4_risk/conservative.md" ] && echo "- [保守策略](latest/4_risk/conservative)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 投资决策 (5_portfolio)
    if [ -d "$latest_path/5_portfolio" ]; then
        has_content=true
        echo "### 投资决策" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
        [ -f "$latest_path/5_portfolio/decision.md" ] && echo "- [组合决策](latest/5_portfolio/decision)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 原始报告
    if [ -f "$latest_path/market_report.md" ] || [ -f "$latest_path/investment_plan.md" ]; then
        has_content=true
        echo "### 原始报告" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
        [ -f "$latest_path/market_report.md" ] && echo "- [市场报告](latest/market_report)" >> "$target_dir/index.md"
        [ -f "$latest_path/sentiment_report.md" ] && echo "- [情绪报告](latest/sentiment_report)" >> "$target_dir/index.md"
        [ -f "$latest_path/news_report.md" ] && echo "- [新闻报告](latest/news_report)" >> "$target_dir/index.md"
        [ -f "$latest_path/fundamentals_report.md" ] && echo "- [基本面报告](latest/fundamentals_report)" >> "$target_dir/index.md"
        [ -f "$latest_path/investment_plan.md" ] && echo "- [投资计划](latest/investment_plan)" >> "$target_dir/index.md"
        [ -f "$latest_path/trader_investment_plan.md" ] && echo "- [交易员投资计划](latest/trader_investment_plan)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 如果没有生成任何内容，添加一个提示
    if [ "$has_content" = false ]; then
        echo "暂无可用的报告文件。" >> "$target_dir/index.md"
    fi
}

# 清理旧的 symbol 链接（如果存在）
if [ -L "$BLOG_STOCKS_DIR/results" ]; then
    echo "🗑️  删除旧的软链接..."
    rm "$BLOG_STOCKS_DIR/results"
fi

# 为每个股票创建目录并复制最新的报告
# 结构：stock-analysis/{SYMBOL}/latest/ -> 指向最新日期的报告
for stock_dir in "$RESULTS_DIR"/*/; do
    if [ -d "$stock_dir" ]; then
        symbol=$(basename "$stock_dir")
        echo "📈 处理 $symbol..."

        # 创建股票目录
        target_dir="$BLOG_STOCKS_DIR/$symbol"
        mkdir -p "$target_dir"

        # 找到最新的日期文件夹
        latest_date=$(ls -t "$stock_dir" | head -n1)

        if [ -n "$latest_date" ]; then
            source_path="$stock_dir$latest_date/reports"
            target_path="$target_dir/latest"

            # 删除旧的 latest 链接或目录
            if [ -L "$target_path" ] || [ -d "$target_path" ]; then
                rm -rf "$target_path"
            fi

            # 复制最新报告
            if [ -d "$source_path" ]; then
                echo "   📄 复制 $latest_date 的报告..."
                cp -r "$source_path" "$target_path"

                # 根据实际存在的文件生成 index.md
                generate_index_md "$target_dir" "$target_path" "$latest_date"
                echo "   ✅ 已生成 index.md"
            fi
        fi
    fi
done

# 生成主索引页面
cat > "$BLOG_STOCKS_DIR/index.md" << EOF
---
title: 股票分析
outline: false
---

# 股票分析报告

本页面展示由 TradingAgents 系统自动生成的股票分析报告。报告每日更新。

## 覆盖股票

EOF

# 添加股票列表（cleanUrls: true 模式下不需要 .md 后缀）
for stock_dir in "$BLOG_STOCKS_DIR"/*/; do
    if [ -d "$stock_dir" ] && [ "$stock_dir" != "$BLOG_STOCKS_DIR/index.md" ]; then
        symbol=$(basename "$stock_dir")
        if [ "$symbol" != "latest" ]; then
            echo "- [$symbol]($symbol/)" >> "$BLOG_STOCKS_DIR/index.md"
        fi
    fi
done

echo ""
echo "✅ 同步完成！"
echo ""
echo "📊 同步的股票分析："
ls -1 "$BLOG_STOCKS_DIR"
echo ""
echo "💡 下一步：将更改提交并推送到 GitHub"
echo "   git add stock-analysis/"
echo "   git commit -m 'chore: 更新股票分析报告'"
echo "   git push"
