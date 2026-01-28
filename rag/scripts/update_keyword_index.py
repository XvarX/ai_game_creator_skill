"""
RAG关键词索引更新辅助脚本
半自动化工具，帮助维护rag/关键词索引.md
"""

import os
from pathlib import Path
from datetime import datetime


def scan_docs_structure(docs_dir="docs"):
    """扫描docs目录结构，获取所有文档"""
    docs_tree = {}

    for root, dirs, files in os.walk(docs_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                rel_path = os.path.relpath(filepath, docs_dir)

                # 获取相对路径的目录结构
                parts = Path(rel_path).parts
                if len(parts) > 1:
                    # 模块/系统名.md
                    module = parts[0]
                    system_name = parts[1]
                else:
                    # 根目录文档
                    module = "根目录"
                    system_name = parts[0]

                if module not in docs_tree:
                    docs_tree[module] = []
                docs_tree[module].append(system_name)

    return docs_tree


def read_existing_index(index_path="rag/关键词索引.md"):
    """读取现有的关键词索引"""
    if not os.path.exists(index_path):
        return None

    with open(index_path, 'r', encoding='utf-8') as f:
        return f.read()


def generate_index_template(docs_tree):
    """生成关键词索引模板"""
    today = datetime.now().strftime("%Y-%m-%d")
    total_docs = sum(len(docs) for docs in docs_tree.values())

    template = f"""# RAG关键词索引 - 项目导航指南

## 项目总览

**项目名称**: [请从游戏大纲文档读取项目名称]
**文档总数**: {total_docs}
**RAG Chunks**: [请从RAG构建输出获取]
**最后更新**: {today}

## 快速导航策略

**程序员工作流程**：
1. 先读总览文档（游戏大纲、模块拆解）了解全局
2. 查阅本索引，找到相关模块和关键词
3. 使用RAG查询获取详细需求
4. 实现功能

## 模块关键词映射

"""

    # 为每个模块生成模板
    for module, systems in sorted(docs_tree.items()):
        if module == "根目录":
            template += f"### 根目录文档\n\n"
            template += f"**相关文档**: docs/\n\n"
        else:
            template += f"### {module}\n\n"
            template += f"**相关文档**: docs/{module}/\n\n"

        template += "**系统列表**:\n"
        for system in sorted(systems):
            system_name = system.replace('.md', '')
            template += f"- {system_name}\n"

        template += "\n**功能关键词**: [请根据文档内容手动补充]\n\n"
        template += "**查询示例**:\n"
        template += "```bash\n"
        template += f"# 查询{module}相关功能\n"
        template += f'python rag/scripts/rag_query.py "{module.split("模块")[0]} 功能"\n'
        template += "```\n\n"
        template += "---\n\n"

    # 添加使用指南
    template += """## 使用指南

### 如何使用此索引

**场景1：实现某个功能**
1. 确认任务：要实现的功能名称
2. 查阅索引：找到相关模块和系统
3. 选择关键词：根据功能名称组合查询词
4. 执行RAG查询
5. 阅读返回的chunks
6. 实现代码

### 常用查询模板

**按模块查询**:
- 核心功能: "核心 玩法 机制"
- 战斗功能: "战斗 伤害 技能"
- 角色功能: "角色 属性 成长"
- UI功能: "UI 界面 交互"
- 数据功能: "数据 存档 配置"

**按功能类型**:
- 计算类: "公式 计算 数值"
- 流程类: "流程 判定 触发"
- 界面类: "UI 界面 布局"

---

## 注意事项

- ✅ 本索引提供查询方向，不替代详细文档阅读
- ✅ 查询时使用多个相关关键词效果更好
- ✅ 先看总览再查细节，避免盲目查询
- ❌ 不要只查一个词，尝试组合关键词

---

## 更新记录

| 日期 | 变更类型 | 说明 |
|------|---------|------|
| {today} | 初始化 | 根据当前文档结构生成索引 |
"""

    return template


def compare_and_suggest(existing_index, docs_tree):
    """对比现有索引和实际文档，提供建议"""
    if existing_index is None:
        print("\n[INFO] 未找到现有关键词索引，将创建新文件")
        return None

    print("\n[INFO] 检测现有索引...")

    # 提取现有索引中提到的文档
    existing_docs = set()
    for line in existing_index.split('\n'):
        if '**相关文档**:' in line or 'docs/' in line:
            # 简单提取，实际可能需要更复杂的解析
            if 'docs/' in line:
                parts = line.split('docs/')
                if len(parts) > 1:
                    existing_docs.add(parts[1].strip('/').strip())

    # 获取实际文档
    actual_docs = set()
    for module, systems in docs_tree.items():
        for system in systems:
            if module == "根目录":
                actual_docs.add(system)
            else:
                actual_docs.add(f"{module}/{system}")

    # 对比差异
    new_docs = actual_docs - existing_docs
    removed_docs = existing_docs - actual_docs

    if new_docs or removed_docs:
        print("\n" + "=" * 60)
        print("[检测到差异] 现有索引与实际文档不一致")
        print("=" * 60)

        if new_docs:
            print(f"\n➕ 新增文档 ({len(new_docs)} 个):")
            for doc in sorted(new_docs):
                print(f"  - {doc}")
            print("\n建议: 请在索引中添加这些文档的关键词映射")

        if removed_docs:
            print(f"\n🗑️  删除文档 ({len(removed_docs)} 个):")
            for doc in sorted(removed_docs):
                print(f"  - {doc}")
            print("\n建议: 请从索引中移除这些文档的条目")

        print("\n提示: 运行时添加 --force 参数可覆盖现有索引")

        return False

    print("\n[OK] 索引与文档结构一致，无需更新")
    return True


def main():
    """主函数"""
    import sys

    force = '--force' in sys.argv

    print("=" * 60)
    print("RAG关键词索引更新辅助工具")
    print("=" * 60)

    # 1. 扫描文档结构
    print("\n[INFO] 扫描文档结构...")
    docs_tree = scan_docs_structure("docs")

    total_modules = len(docs_tree)
    total_docs = sum(len(docs) for docs in docs_tree.values())

    print(f"[OK] 找到 {total_modules} 个模块/目录")
    print(f"[OK] 找到 {total_docs} 个文档")

    # 2. 读取现有索引
    existing_index = read_existing_index("rag/关键词索引.md")

    # 3. 对比差异（如果存在现有索引）
    if existing_index and not force:
        is_consistent = compare_and_suggest(existing_index, docs_tree)
        if is_consistent:
            return

    # 4. 生成新索引
    print("\n[INFO] 生成关键词索引模板...")
    template = generate_index_template(docs_tree)

    # 5. 写入文件
    index_path = "rag/关键词索引.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(template)

    print(f"\n[SUCCESS] 关键词索引已生成: {index_path}")
    print("\n" + "=" * 60)
    print("[下一步] 请手动完善关键词索引")
    print("=" * 60)
    print("\n需要手动完成的工作:")
    print("  1. 填写项目名称（从游戏大纲文档读取）")
    print("  2. 填写RAG Chunks数量（从RAG构建输出获取）")
    print("  3. 为每个系统补充功能关键词")
    print("  4. 根据实际情况调整查询示例")
    print("\n提示: 关键词应该包含系统的核心功能和查询词")


if __name__ == "__main__":
    main()
