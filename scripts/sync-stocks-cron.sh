#!/bin/bash
# 股票分析报告同步脚本 - 用于 cron 定时任务
# 此脚本假设在博客项目目录下执行

set -e

# 切换到博客项目目录
cd /Users/egg/Project/blog

echo "🕐 [$(date '+%Y-%m-%d %H:%M:%S')] 开始同步股票分析报告..."

# 执行同步脚本
./scripts/sync-stocks.sh 2>&1 | tee /tmp/stock-sync.log

# 检查是否有变更
git status --porcelain stock-analysis/ | grep -q . || {
    echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] 无新变更，跳过提交"
    exit 0
}

# 提交并推送
git config user.name "Egg Guo"
git config user.email "egg@egguo.com"

git add stock-analysis/
git commit -m "chore: 自动更新股票分析报告 ($(date +%Y-%m-%d))"

echo "🚀 推送到 GitHub..."
git push origin main

echo "✅ [$(date '+%Y-%m-%d %H:%M:%S')] 同步完成！"
