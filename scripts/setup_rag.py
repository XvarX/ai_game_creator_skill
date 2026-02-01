#!/usr/bin/env python3
"""
跨平台RAG脚本安装工具
Cross-platform RAG scripts setup utility

自动将RAG脚本从skill目录复制到项目的rag/目录
Automatically copies RAG scripts from skill directory to project's rag/ folder
"""

import shutil
import sys
from pathlib import Path


def find_skill_rag_scripts():
    """查找skill的RAG脚本目录"""
    # 可能的skill路径
    possible_paths = [
        Path.home() / '.claude' / 'skills' / 'ai_game_creator_skill' / 'rag' / 'scripts',
        Path.home() / '.claude' / 'skills' / 'aigame_creator' / 'rag' / 'scripts',
        Path.cwd().parent / 'ai_game_creator_skill' / 'rag' / 'scripts',  # 开发环境
    ]

    for path in possible_paths:
        if path.exists() and (path / 'rag_setup_zhipu.py').exists():
            return path

    return None


def setup_rag_scripts(project_root=None):
    """复制RAG脚本到项目目录"""
    if project_root is None:
        project_root = Path.cwd()

    skill_scripts = find_skill_rag_scripts()
    if not skill_scripts:
        print("❌ 无法找到RAG脚本目录")
        print("   Cannot find RAG scripts directory")
        print(f"\n尝试的路径:")
        for path in [
            Path.home() / '.claude' / 'skills' / 'ai_game_creator_skill' / 'rag' / 'scripts',
            Path.home() / '.claude' / 'skills' / 'aigame_creator' / 'rag' / 'scripts',
        ]:
            print(f"   - {path}")
        return False

    project_rag = project_root / 'rag' / 'scripts'

    # 创建目录
    project_rag.mkdir(parents=True, exist_ok=True)

    # 复制文件
    source_files = list(skill_scripts.glob('*.py'))
    copied = 0
    for file in source_files:
        dest = project_rag / file.name
        shutil.copy2(file, dest)
        copied += 1
        print(f"✓ {file.name} → rag/scripts/{file.name}")

    print(f"\n✅ 成功复制 {copied} 个RAG脚本文件")
    print(f"   Successfully copied {copied} RAG script files")
    print(f"\n目标目录: {project_rag}")
    print(f"Target: {project_rag}")

    return True


def check_rag_exists(project_root=None):
    """检查RAG是否已设置"""
    if project_root is None:
        project_root = Path.cwd()

    chroma_db = project_root / 'rag' / 'chroma_db'

    if chroma_db.exists():
        print("✅ RAG已配置 (RAG is configured)")
        return True
    else:
        print("⚠️  RAG未配置 (RAG not configured)")
        return False


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='跨平台RAG脚本安装工具 / Cross-platform RAG scripts setup'
    )
    parser.add_argument(
        'command',
        choices=['setup', 'check'],
        nargs='?',
        default='setup',
        help='命令: setup(安装脚本) 或 check(检查RAG状态) / Command: setup or check'
    )
    parser.add_argument(
        '--project-root',
        type=Path,
        default=None,
        help='项目根目录 (默认为当前目录) / Project root directory (default: current directory)'
    )

    args = parser.parse_args()

    if args.command == 'setup':
        setup_rag_scripts(args.project_root)
    elif args.command == 'check':
        check_rag_exists(args.project_root)


if __name__ == '__main__':
    main()
