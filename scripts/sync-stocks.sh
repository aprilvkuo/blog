#!/bin/bash
#
# 股票分析报告同步脚本
# ====================
# 将 TradingAgents 生成的股票分析报告同步到 VitePress 博客
#
# 功能特性:
# - 只同步包含"最终交易决策"的股票
# - 自动生成个股 index.md，嵌入最终交易决策内容
# - 动态生成主索引页面，只展示有效股票
# - 统一股票名称格式（与侧边栏一致）
#
# 使用方法:
#   bash scripts/sync-stocks.sh
#

set -e

# =============================================================================
# 配置区域
# =============================================================================

TRADING_AGENTS_DIR="${TRADING_AGENTS_DIR:-/Users/egg/Project/TradingAgents}"
BLOG_DIR="${BLOG_DIR:-/Users/egg/Project/blog}"
RESULTS_DIR="$TRADING_AGENTS_DIR/results"
STOCK_ANALYSIS_DIR="$BLOG_DIR/finance/stock-analysis"

# =============================================================================
# 股票名称映射（与 VitePress 侧边栏配置保持一致）
# =============================================================================

get_stock_name() {
    local symbol="$1"
    case "$symbol" in
        "0700.HK")     echo "0700.HK 腾讯控股" ;;
        "300750.SZ")   echo "300750.SZ 宁德时代" ;;
        "300760.SZ")   echo "300760.SZ 迈瑞医疗" ;;
        "600036.SS")   echo "600036.SS 招商银行" ;;
        "600519.SS")   echo "600519.SS 贵州茅台" ;;
        "603259.SS")   echo "603259.SS 药明康德" ;;
        "BABA")        echo "BABA 阿里巴巴" ;;
        "DIS")         echo "DIS 迪士尼" ;;
        "MSFT")        echo "MSFT 微软" ;;
        "PDD")         echo "PDD 拼多多" ;;
        "QQQ")         echo "QQQ 纳斯达克 ETF" ;;
        "SPY")         echo "SPY 标普 500ETF" ;;
        *)             echo "$symbol" ;;
    esac
}

# =============================================================================
# 日志函数
# =============================================================================

log_info() {
    echo "ℹ️  $*"
}

log_success() {
    echo "✅  $*"
}

log_skip() {
    echo "⏭️  $*"
}

log_error() {
    echo "❌  $*" >&2
}

# =============================================================================
# 生成个股 index.md
# =============================================================================
# 参数:
#   $1 - 目标目录 (stock-analysis/{SYMBOL})
#   $2 - 报告源目录 (reports/)
#   $3 - 日期字符串
#
generate_index_md() {
    local target_dir="$1"
    local source_path="$2"
    local report_date="$3"
    local symbol
    symbol=$(basename "$target_dir")
    local stock_name
    stock_name=$(get_stock_name "$symbol")

    # 生成 Frontmatter 和标题
    cat > "$target_dir/index.md" << EOF
---
title: $stock_name 分析报告
outline: [2, 3]
---

# $stock_name 分析报告

最新报告日期：$report_date

EOF

    local has_content=false

    # --- 核心报告 ---
    if [ -f "$source_path/complete_report.md" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
## 核心报告

EOF
        echo "- [完整分析报告](latest/complete_report)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 最终交易决策（直接嵌入内容） ---
    if [ -f "$source_path/final_trade_decision.md" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
## 最终交易决策

EOF
        cat "$source_path/final_trade_decision.md" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 分析师报告 ---
    if [ -d "$source_path/1_analysts" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
### 分析师报告

EOF
        [ -f "$source_path/1_analysts/market.md" ] && echo "- [市场分析](latest/1_analysts/market)" >> "$target_dir/index.md"
        [ -f "$source_path/1_analysts/sentiment.md" ] && echo "- [情绪分析](latest/1_analysts/sentiment)" >> "$target_dir/index.md"
        [ -f "$source_path/1_analysts/news.md" ] && echo "- [新闻分析](latest/1_analysts/news)" >> "$target_dir/index.md"
        [ -f "$source_path/1_analysts/fundamentals.md" ] && echo "- [基本面分析](latest/1_analysts/fundamentals)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 研究报告 ---
    if [ -d "$source_path/2_research" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
### 研究报告

EOF
        [ -f "$source_path/2_research/bull.md" ] && echo "- [多方观点](latest/2_research/bull)" >> "$target_dir/index.md"
        [ -f "$source_path/2_research/bear.md" ] && echo "- [空方观点](latest/2_research/bear)" >> "$target_dir/index.md"
        [ -f "$source_path/2_research/manager.md" ] && echo "- [经理总结](latest/2_research/manager)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 交易计划 ---
    if [ -d "$source_path/3_trading" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
### 交易计划

EOF
        [ -f "$source_path/3_trading/trader.md" ] && echo "- [交易员计划](latest/3_trading/trader)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 风险评估 ---
    if [ -d "$source_path/4_risk" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
### 风险评估

EOF
        [ -f "$source_path/4_risk/aggressive.md" ] && echo "- [激进策略](latest/4_risk/aggressive)" >> "$target_dir/index.md"
        [ -f "$source_path/4_risk/neutral.md" ] && echo "- [中性策略](latest/4_risk/neutral)" >> "$target_dir/index.md"
        [ -f "$source_path/4_risk/conservative.md" ] && echo "- [保守策略](latest/4_risk/conservative)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 投资决策 ---
    if [ -d "$source_path/5_portfolio" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
### 投资决策

EOF
        [ -f "$source_path/5_portfolio/decision.md" ] && echo "- [组合决策](latest/5_portfolio/decision)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 原始报告 ---
    local has_original=false
    for f in market_report sentiment_report news_report fundamentals_report investment_plan trader_investment_plan; do
        [ -f "$source_path/${f}.md" ] && has_original=true && break
    done

    if [ "$has_original" = true ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
### 原始报告

EOF
        [ -f "$source_path/market_report.md" ] && echo "- [市场报告](latest/market_report)" >> "$target_dir/index.md"
        [ -f "$source_path/sentiment_report.md" ] && echo "- [情绪报告](latest/sentiment_report)" >> "$target_dir/index.md"
        [ -f "$source_path/news_report.md" ] && echo "- [新闻报告](latest/news_report)" >> "$target_dir/index.md"
        [ -f "$source_path/fundamentals_report.md" ] && echo "- [基本面报告](latest/fundamentals_report)" >> "$target_dir/index.md"
        [ -f "$source_path/investment_plan.md" ] && echo "- [投资计划](latest/investment_plan)" >> "$target_dir/index.md"
        [ -f "$source_path/trader_investment_plan.md" ] && echo "- [交易员投资计划](latest/trader_investment_plan)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # 如果没有生成任何内容，添加提示
    if [ "$has_content" = false ]; then
        echo "暂无可用的报告文件。" >> "$target_dir/index.md"
    fi
}

# =============================================================================
# 生成主索引页面
# =============================================================================

generate_main_index() {
    cat > "$STOCK_ANALYSIS_DIR/index.md" << 'EOF'
---
title: 股票分析
outline: false
---

# 股票分析报告

本页面展示由 TradingAgents 系统自动生成的股票分析报告。报告每日更新。

## 覆盖股票

EOF

    # 只添加有最终交易决策的股票
    for stock_dir in "$STOCK_ANALYSIS_DIR"/*/; do
        [ -d "$stock_dir" ] || continue
        local symbol
        symbol=$(basename "$stock_dir")
        [ "$symbol" = "latest" ] && continue

        # 检查是否存在最终交易决策
        if [ -f "$stock_dir/latest/final_trade_decision.md" ]; then
            local stock_name
            stock_name=$(get_stock_name "$symbol")
            echo "- [$stock_name]($symbol/)" >> "$STOCK_ANALYSIS_DIR/index.md"
        fi
    done
}

# =============================================================================
# 清理无效股票目录
# =============================================================================

cleanup_invalid_stocks() {
    local cleaned=0
    for stock_dir in "$STOCK_ANALYSIS_DIR"/*/; do
        [ -d "$stock_dir" ] || continue
        local symbol
        symbol=$(basename "$stock_dir")
        [ "$symbol" = "latest" ] && continue

        if [ ! -f "$stock_dir/latest/final_trade_decision.md" ]; then
            log_skip "删除 $symbol (无最终交易决策)"
            rm -rf "$stock_dir"
            ((cleaned++)) || true
        fi
    done

    if [ "$cleaned" -gt 0 ]; then
        log_info "已清理 $cleaned 个无效股票目录"
    fi
}

# =============================================================================
# 主流程
# =============================================================================

main() {
    log_info "开始同步股票分析报告..."
    log_info "源目录：$RESULTS_DIR"
    log_info "目标目录：$STOCK_ANALYSIS_DIR"

    # 检查源目录是否存在
    if [ ! -d "$RESULTS_DIR" ]; then
        log_error "TradingAgents 结果目录不存在：$RESULTS_DIR"
        exit 1
    fi

    # 创建目标目录
    mkdir -p "$STOCK_ANALYSIS_DIR"

    # 清理无效股票目录
    cleanup_invalid_stocks

    # 同步每个股票
    local synced=0
    local skipped=0

    for stock_dir in "$RESULTS_DIR"/*/; do
        [ -d "$stock_dir" ] || continue

        local symbol
        symbol=$(basename "$stock_dir")

        # 获取最新日期
        local latest_date
        latest_date=$(ls -t "$stock_dir" 2>/dev/null | head -n1)

        if [ -z "$latest_date" ]; then
            log_skip "$symbol (无可用报告)"
            ((skipped++)) || true
            continue
        fi

        local source_path="$stock_dir$latest_date/reports"

        # 检查最终交易决策是否存在
        if [ ! -f "$source_path/final_trade_decision.md" ]; then
            log_skip "$symbol (无最终交易决策)"
            ((skipped++)) || true
            continue
        fi

        # 检查报告目录是否存在
        if [ ! -d "$source_path" ]; then
            log_error "$symbol 报告目录不存在：$source_path"
            ((skipped++)) || true
            continue
        fi

        log_info "处理 $symbol..."

        local target_dir="$STOCK_ANALYSIS_DIR/$symbol"
        local target_path="$target_dir/latest"

        # 创建股票目录
        mkdir -p "$target_dir"

        # 删除旧的 latest
        rm -rf "$target_path"

        # 复制最新报告
        cp -r "$source_path" "$target_path"

        # 生成 index.md
        generate_index_md "$target_dir" "$target_path" "$latest_date"

        log_success "$symbol 已完成 ($latest_date)"
        ((synced++)) || true
    done

    # 生成主索引页面
    generate_main_index

    # 输出统计
    echo ""
    log_success "同步完成！"
    echo ""
    echo "📊 统计信息:"
    echo "   已同步：$synced 只股票"
    echo "   已跳过：$skipped 只股票"
    echo ""
    echo "📁 股票分析目录:"
    ls -1 "$STOCK_ANALYSIS_DIR"
    echo ""
    log_info "下一步操作:"
    echo "   git add finance/stock-analysis/"
    echo "   git commit -m 'chore: 更新股票分析报告'"
    echo "   git push"
}

# 运行主流程
main "$@"
