#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析任务轮询脚本

此脚本运行在你的本地机器上，定期从 Cloudflare KV 拉取待处理任务，
执行分析后将结果推送到仓库。

使用方法:
    python3 scripts/poll-tasks.py

配置:
    - CLOUDFLARE_API_TOKEN: Cloudflare API Token
    - CLOUDFLARE_ACCOUNT_ID: Cloudflare Account ID
    - KV_NAMESPACE_ID: KV Namespace ID
    - TRADING_AGENTS_PATH: TradingAgents 项目路径
    - BLOG_REPO_PATH: 博客仓库路径
"""

import os
import sys
import json
import time
import subprocess
import shutil
from datetime import datetime
from pathlib import Path
import urllib.request
import urllib.error

# ============= 配置 =============
POLL_INTERVAL = 30  # 轮询间隔（秒）
TRADING_AGENTS_PATH = Path('/Users/egg/Project/TradingAgents')
BLOG_REPO_PATH = Path('/Users/egg/Project/blog')

# Cloudflare KV 配置
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ACCOUNT_ID = os.getenv('CLOUDFLARE_ACCOUNT_ID')
KV_NAMESPACE_ID = os.getenv('KV_NAMESPACE_ID')

if not all([CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, KV_NAMESPACE_ID]):
    print("❌ 错误：请设置以下环境变量:")
    print("   - CLOUDFLARE_API_TOKEN")
    print("   - CLOUDFLARE_ACCOUNT_ID")
    print("   - KV_NAMESPACE_ID")
    sys.exit(1)

KV_API_BASE = f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/storage/kv/namespaces/{KV_NAMESPACE_ID}"

HEADERS = {
    'Authorization': f'Bearer {CLOUDFLARE_API_TOKEN}',
    'Content-Type': 'application/json'
}


def kv_request(method, key, data=None):
    """Cloudflare KV API 请求"""
    url = f"{KV_API_BASE}/values/{key}"

    req = urllib.request.Request(url, method=method, headers=HEADERS)
    if data:
        req.data = json.dumps(data).encode('utf-8')
        req.add_header('Content-Type', 'application/json')

    try:
        with urllib.request.urlopen(req) as response:
            if method == 'GET':
                return json.loads(response.read().decode('utf-8'))
            return True
    except urllib.error.HTTPError as e:
        print(f"❌ KV API 错误 ({e.code}): {e.read().decode('utf-8')}")
        return None


def get_pending_tasks():
    """获取所有待处理任务"""
    # KV 不支持直接列出所有 key，需要用 list keys
    url = f"{KV_API_BASE}/keys?prefix=pending:"
    req = urllib.request.Request(url, headers=HEADERS)

    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result.get('result', [])
    except urllib.error.HTTPError as e:
        print(f"❌ 列出任务失败：{e.code}")
        return []


def get_task(task_id):
    """获取任务详情"""
    return kv_request('GET', f'task:{task_id}')


def update_task(task_id, task_data):
    """更新任务状态"""
    kv_request('PUT', f'task:{task_id}', task_data)


def delete_pending_key(task_id):
    """删除 pending 标记"""
    url = f"{KV_API_BASE}/values/pending:{task_id}"
    req = urllib.request.Request(url, method='DELETE', headers=HEADERS)
    try:
        urllib.request.urlopen(req)
    except urllib.error.HTTPError as e:
        print(f"删除 pending 标记失败：{e.code}")


def run_analysis(symbol, stock_code=None):
    """
    执行股票分析脚本
    返回：(成功与否，报告路径或错误信息)
    """
    print(f"🔍 开始分析：{symbol} ({stock_code or '未知代码'})")

    # 切换到 TradingAgents 目录
    original_dir = os.getcwd()
    os.chdir(TRADING_AGENTS_PATH)

    try:
        # 构建命令：python -m cli.main -t {symbol}
        cmd = [sys.executable, '-m', 'cli.main', '-t', symbol]
        print(f"执行命令：{' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=600  # 10 分钟超时
        )

        if result.returncode != 0:
            return False, f"分析失败：{result.stderr}"

        # 查找生成的报告
        # 假设报告在 TradingAgents/results/{symbol}/ 目录下
        result_dir = TRADING_AGENTS_PATH / 'results' / symbol
        if not result_dir.exists():
            # 尝试其他可能的路径
            result_dir = TRADING_AGENTS_PATH / 'results'

        if result_dir.exists():
            # 找到最新的报告目录
            report_path = max(result_dir.iterdir(), key=lambda p: p.stat().st_mtime, default=None)
            if report_path:
                print(f"✅ 分析完成，报告路径：{report_path}")
                return True, str(report_path)

        print("⚠️ 未找到报告目录")
        return False, "未找到生成的报告"

    except subprocess.TimeoutExpired:
        return False, "分析超时（>10 分钟）"
    except Exception as e:
        return False, str(e)
    finally:
        os.chdir(original_dir)


def copy_report_to_blog(report_path, symbol):
    """
    复制报告到博客仓库
    返回：报告在博客中的相对路径
    """
    print(f"📋 复制报告到博客：{report_path}")

    # 股票分析目录
    stock_dir = BLOG_REPO_PATH / 'stock-analysis' / symbol
    stock_dir.mkdir(parents=True, exist_ok=True)

    # 复制最新报告
    latest_dir = stock_dir / 'latest'
    if latest_dir.exists():
        shutil.rmtree(latest_dir)

    # 复制整个报告目录
    shutil.copytree(report_path, latest_dir, dirs_exist_ok=True)

    # 生成 index.md
    index_path = stock_dir / 'index.md'
    if not index_path.exists():
        with open(index_path, 'w', encoding='utf-8') as f:
            f.write(f"""---
title: {symbol} 股票分析
description: {symbol} 的股票分析报告
---

# {symbol} 股票分析

<StockTimeline symbol="{symbol}" />

## 最新报告

"""
)

    return f"stock-analysis/{symbol}/latest"


def commit_and_push(symbol):
    """提交并推送更改"""
    original_dir = os.getcwd()
    os.chdir(BLOG_REPO_PATH)

    try:
        # 检查是否有更改
        result = subprocess.run(['git', 'status', '--porcelain', f'stock-analysis/{symbol}'],
                              capture_output=True, text=True)
        if not result.stdout.strip():
            print("ℹ️ 无更改，跳过提交")
            return

        # 添加更改
        subprocess.run(['git', 'add', f'stock-analysis/{symbol}'], check=True)

        # 提交
        date_str = datetime.now().strftime('%Y-%m-%d')
        subprocess.run(
            ['git', 'commit', '-m', f'chore: 添加 {symbol} 股票分析报告 ({date_str})'],
            check=True
        )

        # 推送
        subprocess.run(['git', 'push'], check=True)
        print("✅ 已推送到仓库")

    except subprocess.CalledProcessError as e:
        print(f"❌ Git 操作失败：{e}")
    finally:
        os.chdir(original_dir)


def process_task(task):
    """处理单个任务"""
    task_id = task['id']
    symbol = task['symbol']
    stock_code = task.get('stock_code')

    print(f"\n{'='*50}")
    print(f"处理任务：{task_id}")
    print(f"股票：{symbol} ({stock_code or '未知'})")
    print(f"{'='*50}")

    # 更新状态为 running
    task['status'] = 'running'
    task['updated_at'] = int(time.time() * 1000)
    update_task(task_id, task)

    # 执行分析
    success, result = run_analysis(symbol, stock_code)

    # 更新任务状态
    task['updated_at'] = int(time.time() * 1000)
    if success:
        task['status'] = 'completed'
        task['result'] = {'report_path': result}

        # 复制报告到博客
        try:
            blog_path = copy_report_to_blog(result, symbol)
            task['result']['blog_path'] = blog_path

            # 提交并推送
            commit_and_push(symbol)
        except Exception as e:
            task['status'] = 'failed'
            task['result'] = {'error': f'复制报告失败：{str(e)}'}
    else:
        task['status'] = 'failed'
        task['result'] = {'error': result}

    update_task(task_id, task)

    # 删除 pending 标记
    delete_pending_key(task_id)

    # 存储结果到 KV（方便前端查询）
    kv_request('PUT', f'result:{task_id}', task['result'])

    status_emoji = "✅" if success else "❌"
    print(f"{status_emoji} 任务完成：{task['status']}")


def main():
    """主循环"""
    print("🚀 股票分析任务轮询服务启动")
    print(f"轮询间隔：{POLL_INTERVAL}秒")
    print(f"TradingAgents 路径：{TRADING_AGENTS_PATH}")
    print(f"博客仓库路径：{BLOG_REPO_PATH}")
    print("-" * 50)

    processed_tasks = set()  # 记录已处理的任务，避免重复

    while True:
        try:
            # 获取待处理任务
            pending_keys = get_pending_tasks()

            if pending_keys:
                print(f"\n📬 发现 {len(pending_keys)} 个待处理任务")

                for key_info in pending_keys:
                    task_id = key_info['name'].replace('pending:', '')

                    if task_id in processed_tasks:
                        continue

                    # 获取任务详情
                    task = get_task(task_id)
                    if task:
                        process_task(task)
                        processed_tasks.add(task_id)
            else:
                print(".", end="", flush=True)

            time.sleep(POLL_INTERVAL)

        except KeyboardInterrupt:
            print("\n\n👋 轮询服务已停止")
            break
        except Exception as e:
            print(f"\n❌ 错误：{e}")
            time.sleep(POLL_INTERVAL)


if __name__ == '__main__':
    main()
