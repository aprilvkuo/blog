#!/usr/bin/env python3
"""
论文研读报告同步脚本
将 HuggingFace 论文研读报告同步到博客 AI 目录
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# 配置
SOURCE_DIR = Path("/Users/egg/.openclaw/workspace-ai_scientists/huggingface_papers/completed")
TARGET_DIR = Path("/Users/egg/Project/blog/ai/papers")


def extract_paper_info(filename: str) -> dict:
    """从文件名提取论文信息"""
    # 文件名格式：PaperName_ArXivNumber_研读报告.md
    match = re.match(r'(.+?)_(\d{4}\.\d{5})_研读报告\.md', filename)
    if not match:
        return None

    paper_name = match.group(1).replace('_', ' ')
    arxiv_id = match.group(2)

    return {
        'paper_name': paper_name,
        'arxiv_id': arxiv_id,
        'slug': f"{paper_name}_{arxiv_id}"
    }


def convert_md_to_vuepress(content: str, paper_info: dict) -> str:
    """转换 markdown 为 VitePress 格式"""
    # 提取第一个标题作为 description
    first_heading_match = re.search(r'^# (.+?)\n', content, re.MULTILINE)
    description = first_heading_match.group(1)[:200] if first_heading_match else paper_info['paper_name']

    # 添加 Frontmatter
    frontmatter = f"""---
title: {paper_info['paper_name']}
description: {description}
date: {datetime.now().strftime('%Y-%m-%d')}
arxiv: {paper_info['arxiv_id']}
---

"""

    # 添加 arXiv 链接
    arxiv_link = f"> 📄 arXiv: [{paper_info['arxiv_id']}](https://arxiv.org/abs/{paper_info['arxiv_id']})\n\n"

    return frontmatter + arxiv_link + content


def sync_papers() -> None:
    """同步所有论文"""
    print("ℹ️  开始同步论文研读报告...")
    print(f"ℹ️  源目录：{SOURCE_DIR}")
    print(f"ℹ️  目标目录：{TARGET_DIR}")

    # 确保目标目录存在
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    synced = 0
    skipped = 0

    for src_file in sorted(SOURCE_DIR.glob("*.md")):
        filename = src_file.name
        paper_info = extract_paper_info(filename)

        if not paper_info:
            print(f"⚠️  跳过：{filename} (文件名格式不匹配)")
            skipped += 1
            continue

        # 目标文件
        target_file = TARGET_DIR / f"{paper_info['slug']}.md"

        # 读取内容
        content = src_file.read_text(encoding='utf-8')

        # 转换格式
        new_content = convert_md_to_vuepress(content, paper_info)

        # 写入文件
        target_file.write_text(new_content, encoding='utf-8')

        print(f"✅  {paper_info['paper_name']} ({paper_info['arxiv_id']})")
        synced += 1

    # 更新 AI 索引页
    update_ai_index()

    print()
    print("✅  同步完成！")
    print(f"   已同步：{synced} 篇")
    print(f"   已跳过：{skipped} 篇")


def update_ai_index() -> None:
    """更新 AI 索引页，添加论文链接"""
    index_file = Path("/Users/egg/Project/blog/ai/index.md")

    if not index_file.exists():
        return

    # 收集所有论文
    papers = []
    for md_file in sorted(TARGET_DIR.glob("*.md")):
        content = md_file.read_text(encoding='utf-8')

        # 提取 title
        title_match = re.search(r'^title: (.+?)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else md_file.stem

        # 提取 arxiv
        arxiv_match = re.search(r'^arxiv: (.+?)$', content, re.MULTILINE)
        arxiv = arxiv_match.group(1) if arxiv_match else ""

        papers.append({
            'title': title,
            'arxiv': arxiv,
            'path': f"papers/{md_file.stem}"
        })

    # 读取原文件
    content = index_file.read_text(encoding='utf-8')

    # 查找 ## 论文研读 部分
    papers_section = "\n## 论文研读\n\n"
    if papers:
        papers_section += "最近的论文研读报告：\n\n"
        for paper in papers[:10]:  # 只显示最近 10 篇
            papers_section += f"- [{paper['title']}](papers/{paper['arxiv']}) - arXiv:{paper['arxiv']}\n"
        papers_section += "\n"

    # 如果已存在论文研读部分，替换它
    if "## 论文研读" in content:
        # 删除旧部分
        content = re.sub(r'\n## 论文研读\n.*?(?=\n## |\Z)', '', content, flags=re.DOTALL)

    # 在最后一个 ## 前插入
    content = re.sub(r'(\n## .*)', papers_section + r'\1', content, count=1)

    index_file.write_text(content, encoding='utf-8')
    print("📝  已更新 AI 索引页")


def main():
    sync_papers()


if __name__ == "__main__":
    main()
