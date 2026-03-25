#!/usr/bin/env python3
"""
股票分析报告同步脚本
将 TradingAgents 生成的报告同步到 VitePress 博客目录
"""

import json
import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# 配置
# 支持本地开发和 GitHub Action 环境
if os.environ.get("GITHUB_ACTIONS") == "true":
    # GitHub Action 环境
    SOURCE_DIR = Path(os.environ.get("TRADING_AGENTS_DIR", "/tmp/TradingAgents")) / "results"
    TARGET_DIR = Path(os.environ.get("BLOG_DIR", ".")) / "finance/stock-analysis"
else:
    # 本地环境
    SOURCE_DIR = Path("/Users/egg/Project/TradingAgents/results")
    TARGET_DIR = Path("/Users/egg/Project/blog/finance/stock-analysis")

SYNC_HISTORY = os.environ.get("SYNC_HISTORY", "true").lower() == "true"

# Sentiment 关键词匹配
BULL_PATTERNS = [r'买入', r'做多', r'看多', r'buy', r'Buy', r'BUY']
BEAR_PATTERNS = [r'卖出', r'减仓', r'减持', r'清仓', r'sell', r'Sell', r'SELL', r'做空', r'看空']


def extract_sentiment(summary_path: Path) -> str:
    """从 summary.md 提取 sentiment"""
    if not summary_path.exists():
        return "neutral"

    content = summary_path.read_text(encoding='utf-8')

    # 提取 ## 结论 部分
    conclusion_match = re.search(r'## 结论\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
    if not conclusion_match:
        return "neutral"

    conclusion = conclusion_match.group(1)

    # 检查看涨关键词
    for pattern in BULL_PATTERNS:
        if re.search(pattern, conclusion):
            return "bull"

    # 检查看跌关键词
    for pattern in BEAR_PATTERNS:
        if re.search(pattern, conclusion):
            return "bear"

    return "neutral"


def get_sentiment_label(sentiment: str) -> tuple:
    """获取 sentiment 的标签和图标"""
    if sentiment == "bull":
        return "看多", "↑"
    elif sentiment == "bear":
        return "看空", "↓"
    else:
        return "中性", "→"


def count_analyst_reports(date_dir: Path) -> list:
    """统计分析师报告文件"""
    analysts_dir = date_dir / "1_analysts"
    if not analysts_dir.exists():
        return []

    report_names = []
    for f in sorted(analysts_dir.iterdir()):
        if f.is_file() and f.suffix == '.md':
            # 提取文件名（不含 .md）
            name = f.stem
            # 转换为中文标签
            name_map = {
                "market": "市场",
                "sentiment": "情绪",
                "news": "新闻",
                "fundamentals": "基本面"
            }
            report_names.append(name_map.get(name, name))
    return report_names


def generate_timeline_json(target_dir: Path, history_dir: Path) -> None:
    """生成时间轴 JSON 数据"""
    timeline = []

    if not history_dir.exists():
        # 写入空数组
        (target_dir / "history.json").write_text("[]", encoding='utf-8')
        return

    # 统计历史报告总数
    total_reports = 0

    # 遍历所有历史目录
    for date_dir in sorted(history_dir.iterdir()):
        if not date_dir.is_dir():
            continue

        summary_file = date_dir / "summary.md"
        if not summary_file.exists():
            continue

        total_reports += 1

        # 提取日期和时间
        date_str = date_dir.name  # 格式：2026-03-25_1134
        date_part = date_str.split('_')[0]  # 2026-03-25
        time_part = date_str.split('_')[1] if '_' in date_str else "0000"  # 1134
        # 格式化为 HH:MM
        hour = time_part[:2]
        minute = time_part[2:4]
        formatted_time = f"{hour}:{minute}"

        # 提取 sentiment
        sentiment = extract_sentiment(summary_file)
        label, icon = get_sentiment_label(sentiment)

        # 统计分析师报告
        analyst_reports = count_analyst_reports(date_dir)

        # 读取 summary.md 的前几行作为摘要
        content = summary_file.read_text(encoding='utf-8')
        # 提取 ## 结论 下的决策行
        conclusion_match = re.search(r'## 结论\s*\n(.*?)(?=\n## |\Z)', content, re.DOTALL)
        if conclusion_match:
            conclusion = conclusion_match.group(1)
            # 从结论中提取第一行非空内容作为摘要
            for line in conclusion.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    # 去掉开头的 ** 和结尾的 **
                    summary = re.sub(r'\*\*(.*?)\*\*', r'\1', line)[:200]
                    break
            else:
                summary = ""
        else:
            summary = ""

        timeline.append({
            "date": date_str,
            "displayDate": date_part,
            "displayTime": formatted_time,
            "sentiment": sentiment,
            "sentimentLabel": label,
            "sentimentIcon": icon,
            "summary": summary,
            "signals": [],
            "analystReports": analyst_reports,
            "reportPath": f"./history/{date_str}/"
        })

    # 按日期排序（最新的在前）
    timeline.sort(key=lambda x: x["date"], reverse=True)

    # 写入 JSON
    output_path = target_dir / "history.json"
    output_path.write_text(json.dumps(timeline, ensure_ascii=False, indent=None), encoding='utf-8')
    print(f"  📊 已生成时间轴数据 ({len(timeline)} 条，共 {total_reports} 份报告)")


def copy_report_files(src_dir: Path, dst_dir: Path) -> None:
    """复制报告文件"""
    if not src_dir.exists():
        return

    # 复制指定文件
    files_to_copy = [
        "complete_report.md",
        "final_trade_decision.md",
        "summary.md",
        "market_report.md",
        "sentiment_report.md",
        "news_report.md",
        "fundamentals_report.md",
        "investment_plan.md",
        "trader_investment_plan.md",
    ]

    for filename in files_to_copy:
        src_file = src_dir / filename
        if src_file.exists():
            shutil.copy2(src_file, dst_dir / filename)

    # 复制子目录
    subdirs = ["1_analysts", "2_research", "3_trading", "4_risk", "5_portfolio"]
    for subdir in subdirs:
        src_subdir = src_dir / subdir
        if src_subdir.exists():
            dst_subdir = dst_dir / subdir
            if dst_subdir.exists():
                shutil.rmtree(dst_subdir)
            shutil.copytree(src_subdir, dst_subdir)


def update_index_md(target_dir: Path) -> None:
    """更新 index.md，将历史分析部分移到最前面（标题后，日期前）"""
    index_file = target_dir / "index.md"
    if not index_file.exists():
        return

    content = index_file.read_text(encoding='utf-8')

    # 提取历史分析部分（## 历史分析标题 + 组件 + script）
    history_match = re.search(
        r'\n## 历史分析\n\n<StockTimeline[^>]* />\n\n(<script setup>.*?</script>)',
        content,
        re.DOTALL
    )

    if not history_match:
        return

    history_full = history_match.group(0)

    # 从原位置删除历史分析部分
    content = content.replace(history_full, '')

    # 找到# 标题行
    title_match = re.search(r'^# .*\n', content, re.MULTILINE)
    if not title_match:
        return

    # 在标题后直接插入历史分析和 script，然后是日期
    insert_pos = title_match.end()
    content = content[:insert_pos] + '\n' + history_full + '\n' + content[insert_pos:]

    # 清理多余的空白行
    content = re.sub(r'\n{3,}', '\n\n', content)

    index_file.write_text(content, encoding='utf-8')
    print(f"  📝 已更新 index.md 布局")


def update_stock_analysis_index(target_dir: Path) -> None:
    """更新股票分析主页，列出所有股票"""
    index_file = target_dir / "index.md"

    # 股票名称映射
    stock_names = {
        "000001.SS": "上证指数",
        "002594.SZ": "比亚迪",
        "0700.HK": "腾讯控股",
        "1810.HK": "小米集团",
        "300750.SZ": "宁德时代",
        "300760.SZ": "迈瑞医疗",
        "600036.SS": "招商银行",
        "600519.SS": "贵州茅台",
        "601138.SS": "工业富联",
        "603259.SS": "药明康德",
        "BABA": "阿里巴巴",
        "DIS": "迪士尼",
        "MSFT": "微软",
        "PDD": "拼多多",
        "QQQ": "纳斯达克 ETF",
        "SPY": "标普 500 ETF",
    }

    # 收集所有股票目录
    stocks = []
    for d in sorted(target_dir.iterdir()):
        if d.is_dir() and not d.name.startswith('.'):
            symbol = d.name
            name = stock_names.get(symbol, symbol)
            stocks.append((symbol, name))

    # 生成主页内容
    content = '''---
title: 股票分析
outline: false
---

# 股票分析报告

本页面展示由 TradingAgents 系统自动生成的股票分析报告。报告每日更新。

## A 股

'''
    # A 股
    a_shares = [(s, n) for s, n in stocks if s.endswith('.SS') or s.endswith('.SZ')]
    for symbol, name in a_shares:
        content += f'- [{name} ({symbol})]({symbol}/)\n'

    content += '\n## 港股\n\n'
    # 港股
    hk_shares = [(s, n) for s, n in stocks if s.endswith('.HK')]
    for symbol, name in hk_shares:
        content += f'- [{name} ({symbol})]({symbol}/)\n'

    content += '\n## 美股\n\n'
    # 美股
    us_stocks = [(s, n) for s, n in stocks if not s.endswith('.SS') and not s.endswith('.SZ') and not s.endswith('.HK')]
    for symbol, name in us_stocks:
        content += f'- [{name} ({symbol})]({symbol}/)\n'

    index_file.write_text(content, encoding='utf-8')
    print(f"  📋 已更新股票分析主页 ({len(stocks)} 只股票)")


def remove_empty_sections(target_dir: Path) -> None:
    """删除 index.md 中的空章节"""
    index_file = target_dir / "index.md"
    if not index_file.exists():
        return

    content = index_file.read_text(encoding='utf-8')

    # 删除空的 ## 报告摘要 部分
    content = re.sub(r'\n## 报告摘要\n\n', '\n', content)

    index_file.write_text(content, encoding='utf-8')


def process_stock(symbol: str) -> bool:
    """处理单只股票"""
    src_stock_dir = SOURCE_DIR / symbol
    if not src_stock_dir.exists():
        print(f"⚠️  {symbol} 源目录不存在，跳过")
        return False

    # 找到最新的报告目录
    latest_dir = None
    latest_date = ""
    for d in src_stock_dir.iterdir():
        if d.is_dir() and d.name > latest_date:
            latest_date = d.name
            latest_dir = d

    if not latest_dir:
        print(f"⚠️  {symbol} 没有报告目录，跳过")
        return False

    print(f"ℹ️  处理 {symbol}... (最新：{latest_date})")

    # 目标目录
    target_dir = TARGET_DIR / symbol
    target_dir.mkdir(parents=True, exist_ok=True)

    # 复制最新报告
    latest_target = target_dir / "latest"
    src_reports = latest_dir / "reports"

    if src_reports.exists():
        if latest_target.exists():
            shutil.rmtree(latest_target)
        latest_target.mkdir(parents=True)
        copy_report_files(src_reports, latest_target)

        # 复制 summary.md 到根目录（方便提取）
        summary_src = src_reports / "summary.md"
        if summary_src.exists():
            shutil.copy2(summary_src, latest_target / "summary.md")

    # 处理历史报告
    if SYNC_HISTORY:
        history_target = target_dir / "history"
        if history_target.exists():
            shutil.rmtree(history_target)
        history_target.mkdir(parents=True)

        for date_dir in sorted(src_stock_dir.iterdir()):
            if not date_dir.is_dir():
                continue

            src_reports = date_dir / "reports"
            if not src_reports.exists():
                continue

            # 检查是否有 summary.md
            if not (src_reports / "summary.md").exists():
                continue

            # 检查 1_analysts 目录，如果只有 news.md 一个文件，则跳过该报告
            analysts_dir = src_reports / "1_analysts"
            if analysts_dir.exists():
                md_files = list(analysts_dir.glob("*.md"))
                if len(md_files) == 1 and (analysts_dir / "news.md").exists():
                    print(f"  ⚠️  跳过 {symbol}/{date_dir.name} (只有新闻分析)")
                    continue

            dst_history_dir = history_target / date_dir.name
            dst_history_dir.mkdir(parents=True)
            copy_report_files(src_reports, dst_history_dir)

            # 复制 summary.md
            summary_src = src_reports / "summary.md"
            if summary_src.exists():
                shutil.copy2(summary_src, dst_history_dir / "summary.md")

        # 生成时间轴 JSON
        generate_timeline_json(target_dir, history_target)
        # 更新 index.md 布局（将历史分析移到最前面）
        update_index_md(target_dir)
    else:
        # 生成空的 history.json
        (target_dir / "history.json").write_text("[]", encoding='utf-8')
        # 更新 index.md 布局
        update_index_md(target_dir)

    # 删除 index.md 中的空章节（如空的 ## 报告摘要）
    remove_empty_sections(target_dir)

    print(f"✅  {symbol} 已完成 ({latest_date})")
    return True


def main():
    """主函数"""
    print("ℹ️  开始同步股票分析报告...")
    print(f"ℹ️  源目录：{SOURCE_DIR}")
    print(f"ℹ️  目标目录：{TARGET_DIR}")

    # 确保目标目录存在
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    # 统计
    synced = 0
    skipped = 0

    # 处理所有股票
    if not SOURCE_DIR.exists():
        print(f"❌ 源目录不存在：{SOURCE_DIR}")
        return

    for stock_dir in sorted(SOURCE_DIR.iterdir()):
        if not stock_dir.is_dir():
            continue
        if stock_dir.name.startswith('.'):
            continue

        symbol = stock_dir.name
        if process_stock(symbol):
            synced += 1
        else:
            skipped += 1

    # 更新股票分析主页，列出所有股票
    update_stock_analysis_index(TARGET_DIR)

    print()
    print("✅  同步完成！")
    print()
    print("📊 统计信息:")
    print(f"   已同步：{synced} 只股票")
    print(f"   已跳过：{skipped} 只股票")
    print()
    print("📁 股票分析目录:")
    for d in sorted(TARGET_DIR.iterdir()):
        if d.is_dir():
            print(d.name)
    print()
    print("ℹ️  下一步操作:")
    print("   git add finance/stock-analysis/")
    print("   git commit -m 'chore: 更新股票分析报告'")
    print("   git push")


if __name__ == "__main__":
    main()
