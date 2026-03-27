#!/usr/bin/env python3
"""
论文研读报告同步脚本（增强版）
将 HuggingFace 论文研读报告同步到博客 AI 目录
支持：标签、分类、目录索引
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict

# 配置
SOURCE_DIR = Path("/Users/egg/.openclaw/workspace-ai_scientists/huggingface_papers/completed")
TARGET_DIR = Path("/Users/egg/Project/blog/ai/papers")

# 论文分类映射（按论文名称关键词）
CATEGORY_MAPPING = {
    # Agent/多智能体系统
    'agent': ['AgentScope', 'AutoDev', 'OpenDevin', 'Hyperagents', 'MiroThinker', 'EvoScientist', 'AIScientistv2'],
    # RAG/检索增强生成
    'rag': ['LightRAG', 'GraphRAG', 'Retrieval'],
    # 金融/交易
    'finance': ['TradingAgents', 'FinMem', 'FinAgent'],
    # 多模态
    'multimodal': ['PaddleOCRVL', 'daVinciMagiHuman', 'VideoDetective', 'FishAudioS2'],
    # 模型优化/效率
    'optimization': ['Bitnetcpp', 'PowerInfer', 'OmniFlatten', 'SpecEyes', 'AttentionResiduals'],
    # 记忆系统
    'memory': ['MemOS', 'EverMemOS', 'Mem0', 'MementoSkills'],
    # 工具/框架
    'framework': ['LlamaFactory', 'MinerU2.5', 'MinerUDiffusion', 'SmolDocling', 'LTX2'],
    # 世界模型/环境
    'world_model': ['WildWorld', 'LeWorldModel'],
    # 强化学习
    'rl': ['OpenClawRL', 'SSPO'],
}

# 标签映射（更细粒度）
TAG_MAPPING = {
    # 技术领域
    'llm': ['llm', 'large language model', '大语言模型'],
    'multi-agent': ['multi-agent', 'multi agent', '多智能体', '多 agent'],
    'rag': ['rag', 'retrieval-augmented', '检索增强'],
    'knowledge-graph': ['knowledge graph', '知识图谱', 'graph'],
    'distributed': ['distributed', '分布式', 'parallel'],

    # 应用场景
    'finance': ['finance', 'financial', '金融', '交易', 'trading'],
    'scientific': ['scientific', '科学', 'research'],
    'social-simulation': ['social', 'simulation', '社会', '模拟'],

    # 模型类型
    'vision': ['vision', '视觉', '图像', 'video', 'audio'],
    'speech': ['speech', 'audio', '语音'],
    'ocr': ['ocr', '文本识别'],

    # 优化技术
    'quantization': ['quantization', '量化', 'bitnet'],
    'efficiency': ['efficiency', 'efficient', '高效', 'fast'],
    'optimization': ['optimization', '优化'],
}


def extract_tags_from_content(content: str) -> List[str]:
    """从论文内容中提取标签"""
    tags = set()
    content_lower = content[:2000].lower()  # 只检查前 2000 字符

    for tag, keywords in TAG_MAPPING.items():
        for keyword in keywords:
            if keyword.lower() in content_lower:
                tags.add(tag)
                break

    return list(tags)


def categorize_paper(paper_name: str) -> str:
    """根据论文名称分类"""
    for category, papers in CATEGORY_MAPPING.items():
        for paper in papers:
            if paper.lower() in paper_name.lower():
                return category
    return 'other'  # 默认分类


def get_category_name(category: str) -> str:
    """获取分类的中文名称"""
    category_names = {
        'agent': 'Agent/智能体',
        'rag': 'RAG/检索增强',
        'finance': '金融/交易',
        'multimodal': '多模态',
        'optimization': '模型优化',
        'memory': '记忆系统',
        'framework': '工具/框架',
        'world_model': '世界模型',
        'rl': '强化学习',
        'other': '其他',
    }
    return category_names.get(category, category)


def extract_paper_info(filename: str) -> dict:
    """从文件名提取论文信息"""
    # 文件名格式：PaperName_ArXivNumber_研读报告.md
    match = re.match(r'(.+?)_(\d{4}\.\d{5})_研读报告\.md', filename)
    if not match:
        return None

    paper_name = match.group(1).replace('_', ' ')
    arxiv_id = match.group(2)
    year = arxiv_id.split('.')[0]  # 从 arXiv ID 提取年份

    return {
        'paper_name': paper_name,
        'arxiv_id': arxiv_id,
        'year': year,
        'slug': f"{paper_name}_{arxiv_id}"
    }


def convert_md_to_vuepress(content: str, paper_info: dict) -> str:
    """转换 markdown 为 VitePress 格式，添加标签和分类"""
    # 从内容中提取标签
    extracted_tags = extract_tags_from_content(content)

    # 根据论文名称分类
    category = categorize_paper(paper_info['paper_name'])

    # 合并标签（分类也作为标签）
    all_tags = list(set([category] + extracted_tags))

    # 提取第一个标题作为 description
    first_heading_match = re.search(r'^# (.+?)\n', content, re.MULTILINE)
    description = first_heading_match.group(1)[:200] if first_heading_match else paper_info['paper_name']

    # 添加 Frontmatter（带 tags 和 category）
    frontmatter = f"""---
title: {paper_info['paper_name']}
description: {description}
date: {datetime.now().strftime('%Y-%m-%d')}
arxiv: {paper_info['arxiv_id']}
category: {category}
tags: {all_tags}
outline: [2, 3]
---

"""

    # 添加 arXiv 链接和元信息
    meta_info = f"""::: tip 📄 论文信息
- **arXiv**: [{paper_info['arxiv_id']}](https://arxiv.org/abs/{paper_info['arxiv_id']})
- **分类**: {get_category_name(category)}
- **标签**: {', '.join(all_tags)}
:::

"""

    # 添加目录提示
    toc_tip = """
::: info 📑 目录
本文档包含完整的论文研读报告，包括深度学术速读和技术实现分析两部分。
:::

"""

    return frontmatter + meta_info + toc_tip + content


def generate_papers_index() -> str:
    """生成带分类目录的论文索引页"""
    papers = []

    for md_file in sorted(TARGET_DIR.glob("*.md"), reverse=True):
        # 跳过索引页自身
        if md_file.stem == 'index':
            continue

        content = md_file.read_text(encoding='utf-8')

        # 提取 frontmatter 信息
        title_match = re.search(r'^title: (.+?)$', content, re.MULTILINE)
        arxiv_match = re.search(r'^arxiv: (.+?)$', content, re.MULTILINE)
        category_match = re.search(r'^category: (.+?)$', content, re.MULTILINE)
        tags_match = re.search(r'^tags: \[(.*?)\]', content, re.MULTILINE)
        date_match = re.search(r'^date: (.+?)$', content, re.MULTILINE)

        title = title_match.group(1) if title_match else md_file.stem
        arxiv = arxiv_match.group(1) if arxiv_match else ""
        category = category_match.group(1) if category_match else 'other'
        tags = tags_match.group(1).split(', ') if tags_match else []
        date = date_match.group(1) if date_match else ""

        # 从论文内容中提取摘要（从"结构化摘要"或"## 结论"部分）
        abstract = extract_abstract(content)

        papers.append({
            'title': title,
            'arxiv': arxiv,
            'category': category,
            'tags': tags,
            'date': date,
            'path': md_file.stem,
            'abstract': abstract
        })

    # 按分类组织论文
    papers_by_category = {}
    for paper in papers:
        cat = paper['category']
        if cat not in papers_by_category:
            papers_by_category[cat] = []
        papers_by_category[cat].append(paper)

    # 生成页面内容
    content = f"""---
title: 论文研读
description: AI 论文研读报告集合
outline: false
---

# 📚 论文研读

本页面收录了 AI 领域的论文研读报告，涵盖 Agent、RAG、多模态、模型优化等方向。

## 📊 统计信息

<div class="paper-stats">

"""

    # 统计信息
    total = len(papers)
    content += f"- **总计**: {total} 篇论文\n"
    content += f"- **分类**: {len(papers_by_category)} 个类别\n"

    for cat, cat_papers in sorted(papers_by_category.items()):
        content += f"- **{get_category_name(cat)}**: {len(cat_papers)} 篇\n"

    content += """
</div>

## 📁 分类目录

"""

    # 按分类列出论文（带摘要）
    for category in sorted(papers_by_category.keys()):
        cat_papers = papers_by_category[category]
        cat_name = get_category_name(category)

        content += f"### {cat_name} {{#{category}}}\n\n"
        content += "<div class=\"paper-list\">\n\n"

        for paper in sorted(cat_papers, key=lambda x: x['date'], reverse=True):
            tags_str = ' | '.join(paper['tags'])
            abstract_str = paper['abstract'][:150] + '...' if len(paper['abstract']) > 150 else paper['abstract']

            content += f"- **[{paper['title']}](./{paper['path']})** \n"
            content += f"  - arXiv: `{paper['arxiv']}` · {paper['date']} · {tags_str}\n"
            if abstract_str:
                content += f"  - *{abstract_str}*\n\n"
            else:
                content += "\n"

        content += "</div>\n\n"

    # 添加标签云
    all_tags = set()
    for paper in papers:
        all_tags.update(paper['tags'])

    content += "## 🏷️ 标签云\n\n"
    content += "<div class=\"tag-cloud\">\n\n"
    for tag in sorted(all_tags):
        content += f"<span class=\"tag\">{tag}</span>\n"
    content += "\n</div>\n"

    return content


def extract_abstract(content: str) -> str:
    """从论文内容中提取摘要"""
    # 尝试从"结构化摘要"表格中提取
    # 匹配表格中的"结论"行
    conclusion_match = re.search(r'\|\s*\*\*结论\*\*\s*\|\s*(.+?)\s*\|', content, re.DOTALL)
    if conclusion_match:
        return conclusion_match.group(1).strip()

    # 尝试从"## 结论"部分提取
    conclusion_section = re.search(r'## 结论\s*\n(.*?)(?=## |\Z)', content, re.DOTALL)
    if conclusion_section:
        text = conclusion_section.group(1).strip()
        # 取第一行或前 100 字符
        first_line = text.split('\n')[0].strip()
        return first_line[:200]

    # 尝试从 description 提取
    desc_match = re.search(r'^description: (.+?)$', content, re.MULTILINE)
    if desc_match:
        return desc_match.group(1).strip()

    return ""


def sync_papers() -> None:
    """同步所有论文"""
    print("ℹ️  开始同步论文研读报告...")
    print(f"ℹ️  源目录：{SOURCE_DIR}")
    print(f"ℹ️  目标目录：{TARGET_DIR}")

    # 确保目标目录存在
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    synced = 0
    skipped = 0
    papers_data = []

    for src_file in sorted(SOURCE_DIR.glob("*.md")):
        filename = src_file.name
        paper_info = extract_paper_info(filename)

        if not paper_info:
            print(f"⚠️  跳过：{filename} (文件名格式不匹配)")
            skipped += 1
            continue

        # 读取源内容
        content = src_file.read_text(encoding='utf-8')

        # 转换格式（添加标签和分类）
        new_content = convert_md_to_vuepress(content, paper_info)

        # 提取分类和标签用于索引
        category = categorize_paper(paper_info['paper_name'])
        tags = extract_tags_from_content(content)

        # 目标文件
        target_file = TARGET_DIR / f"{paper_info['slug']}.md"
        target_file.write_text(new_content, encoding='utf-8')

        papers_data.append({
            'title': paper_info['paper_name'],
            'arxiv': paper_info['arxiv_id'],
            'category': category,
            'tags': tags,
            'date': datetime.now().strftime('%Y-%m-%d'),
            'slug': paper_info['slug']
        })

        print(f"✅  {paper_info['paper_name']} ({paper_info['arxiv_id']}) - {get_category_name(category)}")
        synced += 1

    # 生成带分类目录的索引页
    index_content = generate_papers_index()
    index_file = TARGET_DIR / "index.md"
    index_file.write_text(index_content, encoding='utf-8')
    print("📝  已生成论文索引页 (带分类目录)")

    # 保存论文数据 JSON（用于其他页面引用）
    json_file = TARGET_DIR / "papers.json"
    json_file.write_text(json.dumps(papers_data, ensure_ascii=False, indent=2), encoding='utf-8')
    print("📄  已生成论文数据 JSON")

    print()
    print("✅  同步完成！")
    print(f"   已同步：{synced} 篇")
    print(f"   已跳过：{skipped} 篇")


def main():
    sync_papers()


if __name__ == "__main__":
    main()
