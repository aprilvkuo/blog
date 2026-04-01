#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
股票分析功能设置脚本

运行此脚本自动完成 Cloudflare KV 配置
"""

import subprocess
import json
import os
import sys
import re

def run_command(cmd):
    """运行命令并返回输出"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.returncode, result.stdout, result.stderr

def main():
    print("=" * 60)
    print("股票分析功能设置向导")
    print("=" * 60)

    # 检查 wrangler 是否安装
    print("\n1. 检查 wrangler 是否安装...")
    code, out, err = run_command("wrangler --version")
    if code != 0:
        print("❌ wrangler 未安装，请先运行：npm install -g wrangler")
        sys.exit(1)
    print(f"✅ wrangler 已安装：{out.strip()}")

    # 创建 KV namespace
    print("\n2. 创建 Cloudflare KV namespace...")
    code, out, err = run_command('wrangler kv:namespace create "stock-analysis-tasks"')
    if code != 0:
        print(f"❌ 创建失败：{err}")
        sys.exit(1)

    print(out)

    # 解析 namespace ID
    try:
        match = re.search(r'id "([a-f0-9]+)"', out)
        if match:
            kv_id = match.group(1)
            print(f"\n✅ KV Namespace ID: {kv_id}")
        else:
            print("⚠️ 无法解析 Namespace ID，请手动从上面输出中提取")
            kv_id = input("请输入 KV Namespace ID: ")
    except Exception as e:
        print(f"⚠️ 解析失败：{e}")
        kv_id = input("请输入 KV Namespace ID: ")

    # 更新 wrangler.toml
    print("\n3. 更新 wrangler.toml...")
    wrangler_content = f'''# Cloudflare Pages 配置
name = "egguo-blog"
compatibility_date = "2024-01-01"

# KV Namespace 绑定
kv_namespaces = [
  {{ binding = "TASKS_KV", id = "{kv_id}" }}
]
'''

    with open('wrangler.toml', 'w', encoding='utf-8') as f:
        f.write(wrangler_content)
    print("✅ wrangler.toml 已更新")

    # 设置环境变量提示
    print("\n4. 配置本地环境变量...")
    print(f"""
请将以下环境变量添加到你的 ~/.zshrc 或 ~/.bashrc:

export CLOUDFLARE_API_TOKEN="your_cloudflare_api_token"
export CLOUDFLARE_ACCOUNT_ID="your_account_id"
export KV_NAMESPACE_ID="{kv_id}"

获取 Cloudflare API Token:
  1. 访问 https://dash.cloudflare.com/profile/api-tokens
  2. 创建新的 API Token
  3. 权限要求：
     - Account.Account Holdings (读取)
     - Workers.KV Storage (编辑)

获取 Account ID:
  1. 访问 Cloudflare Dashboard
  2. 右侧显示 Account ID
""")

    # 部署提示
    print("\n5. 部署到 Cloudflare Pages...")
    print("   运行：pnpm run pages:deploy")

    print("\n" + "=" * 60)
    print("✅ 设置完成！")
    print("=" * 60)

    # 询问是否继续部署
    response = input("\n是否现在部署到 Cloudflare Pages? (y/n): ")
    if response.lower() == 'y':
        print("\n开始部署...")
        code, out, err = run_command("pnpm run pages:deploy")
        print(out)
        if err:
            print(err)
        if code == 0:
            print("✅ 部署成功！")
        else:
            print("❌ 部署失败，请检查错误信息")

if __name__ == '__main__':
    main()
