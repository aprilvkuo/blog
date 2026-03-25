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

# 是否同步历史报告（设为 false 可加快速度）
SYNC_HISTORY="${SYNC_HISTORY:-false}"

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
        "002594.SZ")   echo "002594.SZ 比亚迪股份" ;;
        "0700.HK")     echo "0700.HK 腾讯控股" ;;
        "1810.HK")     echo "1810.HK 小米集团" ;;
        "300750.SZ")   echo "300750.SZ 宁德时代" ;;
        "300760.SZ")   echo "300760.SZ 迈瑞医疗" ;;
        "600036.SS")   echo "600036.SS 招商银行" ;;
        "600519.SS")   echo "600519.SS 贵州茅台" ;;
        "601138.SS")   echo "601138.SS 工业富联" ;;
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

    # --- 优先显示 summary.md（如果存在） ---
    if [ -f "$source_path/summary.md" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
## 报告摘要

EOF
        # 移除 summary.md 的第一个一级标题（避免与页面标题冲突）和生成时间行，以及空行
        sed -e '1s/^# .*$//' -e '/^> 生成时间.*$/d' -e '/^$/d' "$source_path/summary.md" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 最终交易决策（如果存在且没有 summary.md，则嵌入内容） ---
    if [ -f "$source_path/final_trade_decision.md" ]; then
        # 只有在没有 summary.md 时才嵌入完整内容
        if [ ! -f "$source_path/summary.md" ]; then
            has_content=true
            cat >> "$target_dir/index.md" << 'EOF'
## 最终交易决策

EOF
            cat "$source_path/final_trade_decision.md" >> "$target_dir/index.md"
            echo "" >> "$target_dir/index.md"
        fi
    fi

    # --- 核心报告链接 ---
    if [ -f "$source_path/complete_report.md" ]; then
        has_content=true
        cat >> "$target_dir/index.md" << 'EOF'
## 完整报告

EOF
        echo "- [完整分析报告](latest/complete_report)" >> "$target_dir/index.md"
        echo "" >> "$target_dir/index.md"
    fi

    # --- 最终交易决策链接（如果上面没有嵌入内容） ---
    if [ -f "$source_path/final_trade_decision.md" ]; then
        if [ -f "$source_path/summary.md" ]; then
            # 有 summary.md 时，只显示链接
            echo "- [最终交易决策](latest/final_trade_decision)" >> "$target_dir/index.md"
            echo "" >> "$target_dir/index.md"
        fi
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

    # --- 添加时间轴组件 ---
    cat >> "$target_dir/index.md" << 'EOF'

## 历史分析

<StockTimeline :history="history" />

<script setup>
import { ref } from 'vue'
import data from './history.json?raw'
const history = JSON.parse(data)
</script>
EOF
}

# =============================================================================
# 股票分类
# =============================================================================

get_stock_market() {
    local symbol="$1"
    case "$symbol" in
        # A 股：以 .SS 或 .SZ 结尾
        *.SS|*.SZ) echo "a-share" ;;
        # 港股：以 .HK 结尾
        *.HK) echo "hk-share" ;;
        # 美股：其他都是美股
        *) echo "us-share" ;;
    esac
}

get_market_name() {
    local market="$1"
    case "$market" in
        "a-share") echo "A 股" ;;
        "hk-share") echo "港股" ;;
        "us-share") echo "美股" ;;
        *) echo "$market" ;;
    esac
}

# =============================================================================
# 从报告中提取 sentiment（看多/看空/中性）
# =============================================================================

extract_sentiment() {
    local report_file="$1"
    if [ ! -f "$report_file" ]; then
        echo "neutral"
        return
    fi

    # 直接从文件读取决策行
    local decision_line
    decision_line=$(grep -E "^### 决策建议|^### 执行指令|^### 决策[:：]" "$report_file" | head -1)

    # 判断情感倾向（按优先级）
    # 使用十六进制构造正则表达式，确保管道符没有空格
    local bear_pattern=$(printf '\xe5\x8d\x96\xe5\x87\xba|\xe6\xb8\x85\xe4\xbb\x93|\xe5\x87\x8f\xe6\x8c\x81|\xe5\x87\x8f\xe4\xbb\x93|\xe7\x9c\x8b\xe7\xa9\xba|bear|sell|short')
    local bull_pattern=$(printf '\xe4\xb9\xb0\xe5\x85\xa5|\xe5\x8a\xa0\xe4\xbb\x93|\xe5\xa2\x9e\xe6\x8c\x81|\xe7\x9c\x8b\xe5\xa4\x9a|bull|buy|long')
    local neutral_pattern=$(printf '\xe4\xb8\xad\xe6\x80\xa7|\xe6\x8c\x81\xe6\x9c\x89|\xe8\xa7\x82\xe6\x9c\x9b|neutral|hold')

    if echo "$decision_line" | grep -qE "$bear_pattern"; then
        echo "bear"
    elif echo "$decision_line" | grep -qE "$bull_pattern"; then
        echo "bull"
    elif echo "$decision_line" | grep -qE "$neutral_pattern"; then
        echo "neutral"
    else
        echo "neutral"
    fi
}

# =============================================================================
# 生成时间轴数据 JSON
# =============================================================================

generate_timeline_json() {
    local target_dir="$1"
    local history_dir="$2"

    local json_file="$target_dir/history.json"
    local history_items=()

    # 遍历所有历史报告目录
    for date_dir in "$history_dir"/*/; do
        [ -d "$date_dir" ] || continue
        local date_name
        date_name=$(basename "$date_dir")

        # 查找报告文件（跳过没有报告的目录）
        # 注意：历史目录中文件直接在根目录，不在 reports 子目录
        local report_path="$date_dir"
        if [ ! -d "$report_path" ] || [ ! "$(ls -A "$report_path" 2>/dev/null)" ]; then
            continue
        fi

        # 跳过没有 md 文件的目录
        if ! ls "$report_path"/*.md 1>/dev/null 2>&1; then
            continue
        fi

        # 格式化显示日期
        local display_date
        display_date=$(echo "$date_name" | sed 's/_/ /' | cut -d' ' -f1)

        local decision_file="$report_path/final_trade_decision.md"
        local plan_file="$report_path/investment_plan.md"

        # 确定 sentiment
        local sentiment="neutral"
        local sentiment_label="中性"
        local sentiment_icon="→"

        if [ -f "$decision_file" ]; then
            sentiment=$(extract_sentiment "$decision_file")
        elif [ -f "$plan_file" ]; then
            sentiment=$(extract_sentiment "$plan_file")
        fi

        case "$sentiment" in
            "bull")
                sentiment_label="看多"
                sentiment_icon="↑"
                ;;
            "bear")
                sentiment_label="看空"
                sentiment_icon="↓"
                ;;
            *)
                sentiment_label="中性"
                sentiment_icon="→"
                ;;
        esac

        # 提取简短摘要（优先从 final_trade_decision.md，没有则用 investment_plan.md）
        local summary="暂无摘要"
        if [ -f "$decision_file" ]; then
            # 提取 "### 决策" 或 "### 决策建议：" 行
            summary=$(grep "^### 决策" "$decision_file" | head -1 | sed 's/^### //' | cut -c1-80)
        fi

        # 如果没有决策文件，从 plan 文件提取
        if [ "$summary" = "暂无摘要" ] && [ -f "$plan_file" ]; then
            summary=$(grep "^### 决策" "$plan_file" | head -1 | sed 's/^### //' | cut -c1-80)
            if [ -z "$summary" ]; then
                summary=$(head -1 "$plan_file" | sed 's/^### //' | cut -c1-80)
            fi
        fi

        # JSON 转义
        summary=$(echo "$summary" | sed 's/"/\\"/g' | sed 's/\t/ /g')

        # 生成相对路径（从个股 index.md 到 history/日期目录）
        local rel_date_dir="./history/$date_name"

        # 添加到 JSON 数组
        history_items+=("{\"date\":\"$date_name\",\"displayDate\":\"$display_date\",\"sentiment\":\"$sentiment\",\"sentimentLabel\":\"$sentiment_label\",\"sentimentIcon\":\"$sentiment_icon\",\"summary\":\"$summary\",\"signals\":[],\"reportPath\":\"$rel_date_dir/\"}")
    done

    # 按日期排序（最新的在前）
    local json_content="["
    local first=true
    for item in "${history_items[@]}"; do
        if [ "$first" = true ]; then
            first=false
        else
            json_content+=","
        fi
        json_content+="$item"
    done
    json_content+="]"

    echo "$json_content" > "$json_file"
}

# =============================================================================
# 复制所有历史报告并生成 index.md
# =============================================================================

generate_history_index() {
    local history_dir="$1"
    local date_name="$2"
    local stock_symbol="$3"
    local stock_name="$4"

    # 判断是最新报告还是历史报告
    local is_latest=false
    if [ "$date_name" = "latest" ]; then
        is_latest=true
    fi

    # 计算返回上级目录的相对路径
    local parent_path="../"

    cat > "$history_dir/index.md" << EOF
---
title: ${stock_name} - ${date_name}
outline: [2, 3]
---

# ${stock_name} - ${date_name}

报告日期：${date_name/_/ }

[← 返回 ${stock_name} 主页](${parent_path})

## 报告导航

EOF

    # 核心报告
    if [ -f "$history_dir/complete_report.md" ]; then
        echo "- [完整分析报告](complete_report)" >> "$history_dir/index.md"
    fi
    if [ -f "$history_dir/final_trade_decision.md" ]; then
        echo "- [最终交易决策](final_trade_decision)" >> "$history_dir/index.md"
    fi

    # 分析师报告
    if [ -d "$history_dir/1_analysts" ]; then
        echo "" >> "$history_dir/index.md"
        echo "### 分析师报告" >> "$history_dir/index.md"
        echo "" >> "$history_dir/index.md"
        [ -f "$history_dir/1_analysts/market.md" ] && echo "- [市场分析](1_analysts/market)" >> "$history_dir/index.md"
        [ -f "$history_dir/1_analysts/sentiment.md" ] && echo "- [情绪分析](1_analysts/sentiment)" >> "$history_dir/index.md"
        [ -f "$history_dir/1_analysts/news.md" ] && echo "- [新闻分析](1_analysts/news)" >> "$history_dir/index.md"
        [ -f "$history_dir/1_analysts/fundamentals.md" ] && echo "- [基本面分析](1_analysts/fundamentals)" >> "$history_dir/index.md"
    fi

    # 研究报告
    if [ -d "$history_dir/2_research" ]; then
        echo "" >> "$history_dir/index.md"
        echo "### 研究报告" >> "$history_dir/index.md"
        echo "" >> "$history_dir/index.md"
        [ -f "$history_dir/2_research/bull.md" ] && echo "- [多方观点](2_research/bull)" >> "$history_dir/index.md"
        [ -f "$history_dir/2_research/bear.md" ] && echo "- [空方观点](2_research/bear)" >> "$history_dir/index.md"
        [ -f "$history_dir/2_research/manager.md" ] && echo "- [经理总结](2_research/manager)" >> "$history_dir/index.md"
    fi

    # 交易计划
    if [ -d "$history_dir/3_trading" ]; then
        echo "" >> "$history_dir/index.md"
        echo "### 交易计划" >> "$history_dir/index.md"
        echo "" >> "$history_dir/index.md"
        [ -f "$history_dir/3_trading/trader.md" ] && echo "- [交易员计划](3_trading/trader)" >> "$history_dir/index.md"
    fi

    # 风险评估
    if [ -d "$history_dir/4_risk" ]; then
        echo "" >> "$history_dir/index.md"
        echo "### 风险评估" >> "$history_dir/index.md"
        echo "" >> "$history_dir/index.md"
        [ -f "$history_dir/4_risk/aggressive.md" ] && echo "- [激进策略](4_risk/aggressive)" >> "$history_dir/index.md"
        [ -f "$history_dir/4_risk/neutral.md" ] && echo "- [中性策略](4_risk/neutral)" >> "$history_dir/index.md"
        [ -f "$history_dir/4_risk/conservative.md" ] && echo "- [保守策略](4_risk/conservative)" >> "$history_dir/index.md"
    fi

    # 投资决策
    if [ -d "$history_dir/5_portfolio" ]; then
        echo "" >> "$history_dir/index.md"
        echo "### 投资决策" >> "$history_dir/index.md"
        echo "" >> "$history_dir/index.md"
        [ -f "$history_dir/5_portfolio/decision.md" ] && echo "- [组合决策](5_portfolio/decision)" >> "$history_dir/index.md"
    fi

    # 原始报告
    local has_original=false
    for f in market_report sentiment_report news_report fundamentals_report investment_plan trader_investment_plan; do
        [ -f "$history_dir/${f}.md" ] && has_original=true && break
    done

    if [ "$has_original" = true ]; then
        echo "" >> "$history_dir/index.md"
        echo "### 原始报告" >> "$history_dir/index.md"
        echo "" >> "$history_dir/index.md"
        [ -f "$history_dir/market_report.md" ] && echo "- [市场报告](market_report)" >> "$history_dir/index.md"
        [ -f "$history_dir/sentiment_report.md" ] && echo "- [情绪报告](sentiment_report)" >> "$history_dir/index.md"
        [ -f "$history_dir/news_report.md" ] && echo "- [新闻报告](news_report)" >> "$history_dir/index.md"
        [ -f "$history_dir/fundamentals_report.md" ] && echo "- [基本面报告](fundamentals_report)" >> "$history_dir/index.md"
        [ -f "$history_dir/investment_plan.md" ] && echo "- [投资计划](investment_plan)" >> "$history_dir/index.md"
        [ -f "$history_dir/trader_investment_plan.md" ] && echo "- [交易员投资计划](trader_investment_plan)" >> "$history_dir/index.md"
    fi
}

copy_history_reports() {
    local target_dir="$1"
    local source_base="$2"
    local symbol="$3"

    local history_dir="$target_dir/history"
    mkdir -p "$history_dir"

    local stock_name
    stock_name=$(get_stock_name "$symbol")

    # 复制所有日期目录
    for date_dir in "$source_base"/*/; do
        [ -d "$date_dir" ] || continue
        local date_name
        date_name=$(basename "$date_dir")
        local target_history="$history_dir/$date_name"

        # 复制 reports 目录到历史目录根目录
        if [ -d "$date_dir/reports" ]; then
            mkdir -p "$target_history"
            cp -r "$date_dir/reports"/* "$target_history/" 2>/dev/null || true

            # 为该历史日期生成 index.md
            generate_history_index "$target_history" "$date_name" "$symbol" "$stock_name"
        fi
    done
}

generate_main_index() {
    cat > "$STOCK_ANALYSIS_DIR/index.md" << 'EOF'
---
title: 股票分析
outline: false
---

# 股票分析报告

本页面展示由 TradingAgents 系统自动生成的股票分析报告。报告每日更新。

EOF

    # 收集有最终交易决策的股票，按市场分类
    local a_shares=()
    local hk_shares=()
    local us_shares=()

    for stock_dir in "$STOCK_ANALYSIS_DIR"/*/; do
        [ -d "$stock_dir" ] || continue
        local symbol
        symbol=$(basename "$stock_dir")
        [ "$symbol" = "latest" ] && continue

        # 检查是否存在最终交易决策
        if [ -f "$stock_dir/latest/final_trade_decision.md" ]; then
            local market
            market=$(get_stock_market "$symbol")
            local stock_name
            stock_name=$(get_stock_name "$symbol")
            local link="- [$stock_name]($symbol/)"

            case "$market" in
                "a-share") a_shares+=("$link") ;;
                "hk-share") hk_shares+=("$link") ;;
                "us-share") us_shares+=("$link") ;;
            esac
        fi
    done

    # 生成 A 股部分
    if [ ${#a_shares[@]} -gt 0 ]; then
        echo "## A 股" >> "$STOCK_ANALYSIS_DIR/index.md"
        echo "" >> "$STOCK_ANALYSIS_DIR/index.md"
        for item in "${a_shares[@]}"; do
            echo "$item" >> "$STOCK_ANALYSIS_DIR/index.md"
        done
        echo "" >> "$STOCK_ANALYSIS_DIR/index.md"
    fi

    # 生成港股部分
    if [ ${#hk_shares[@]} -gt 0 ]; then
        echo "## 港股" >> "$STOCK_ANALYSIS_DIR/index.md"
        echo "" >> "$STOCK_ANALYSIS_DIR/index.md"
        for item in "${hk_shares[@]}"; do
            echo "$item" >> "$STOCK_ANALYSIS_DIR/index.md"
        done
        echo "" >> "$STOCK_ANALYSIS_DIR/index.md"
    fi

    # 生成美股部分
    if [ ${#us_shares[@]} -gt 0 ]; then
        echo "## 美股" >> "$STOCK_ANALYSIS_DIR/index.md"
        echo "" >> "$STOCK_ANALYSIS_DIR/index.md"
        for item in "${us_shares[@]}"; do
            echo "$item" >> "$STOCK_ANALYSIS_DIR/index.md"
        done
        echo "" >> "$STOCK_ANALYSIS_DIR/index.md"
    fi
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

        # 检查是否有 summary.md
        if [ ! -f "$stock_dir/latest/summary.md" ]; then
            log_skip "删除 $symbol (无 summary.md)"
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

        # 找到最新的有 summary.md 的日期目录（按时间排序）
        local latest_date=""
        for date_dir in $(ls -t "$stock_dir" 2>/dev/null); do
            if [ -f "$stock_dir$date_dir/reports/summary.md" ]; then
                latest_date="$date_dir"
                break
            fi
        done

        if [ -z "$latest_date" ]; then
            log_skip "$symbol (无 summary.md)"
            ((skipped++)) || true
            continue
        fi

        local source_path="$stock_dir$latest_date/reports"

        log_info "处理 $symbol..."

        local stock_name
        stock_name=$(get_stock_name "$symbol")

        local target_dir="$STOCK_ANALYSIS_DIR/$symbol"
        local target_path="$target_dir/latest"

        # 创建股票目录
        mkdir -p "$target_dir"

        # 删除旧的 latest
        rm -rf "$target_path"

        # 复制最新报告
        cp -r "$source_path" "$target_path"

        # 为 latest 目录生成 index.md
        generate_history_index "$target_path" "latest" "$symbol" "$stock_name"

        # 复制所有历史报告（如果启用）
        if [ "$SYNC_HISTORY" = "true" ]; then
            copy_history_reports "$target_dir" "$stock_dir" "$symbol"
            # 生成时间轴数据 JSON
            generate_timeline_json "$target_dir" "$stock_dir"
        fi

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
