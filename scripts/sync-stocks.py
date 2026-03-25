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

            dst_history_dir = history_target / date_dir.name
            dst_history_dir.mkdir(parents=True)
            copy_report_files(src_reports, dst_history_dir)

            # 复制 summary.md
            summary_src = src_reports / "summary.md"
            if summary_src.exists():
                shutil.copy2(summary_src, dst_history_dir / "summary.md")

        # 生成时间轴 JSON
        generate_timeline_json(target_dir, history_target)
    else:
        # 生成空的 history.json
        (target_dir / "history.json").write_text("[]", encoding='utf-8')

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
