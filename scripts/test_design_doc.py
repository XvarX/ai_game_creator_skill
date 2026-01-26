#!/usr/bin/env python3
"""
测试策划文档完整性

验证策划文档是否满足交付标准：
- 是否有必需的章节
- 是否有未完成的内容（TBD、待定等）
- 是否足够详细
"""

import os
import sys
import re
from pathlib import Path

def check_file_exists(filepath):
    """检查文件是否存在"""
    if not os.path.exists(filepath):
        return False, f"文件不存在: {filepath}"
    return True, "OK"

def check_required_sections(content):
    """检查必需的章节"""
    required_sections = [
        "# 概述",
        "## 功能需求",
        "## 交互流程",
        "## UI界面",
        "## 技术要求"
    ]

    missing = []
    for section in required_sections:
        if section not in content:
            missing.append(section)

    if missing:
        return False, f"缺少必需章节: {', '.join(missing)}"
    return True, "OK"

def check_unfinished_content(content):
    """检查是否有未完成的内容"""
    unfinished_patterns = [
        r"TBD",
        r"待定",
        r"待讨论",
        r"待补充",
        r"TODO",
        r"\[.*待.*\]",
        r"<.*待.*>"
    ]

    issues = []
    for pattern in unfinished_patterns:
        matches = re.finditer(pattern, content, re.IGNORECASE)
        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            issues.append(f"第{line_num}行: {match.group()}")

    if issues:
        return False, f"发现未完成内容:\n" + "\n".join(issues)
    return True, "OK"

def check_detail_level(content):
    """检查文档详细程度"""
    # 检查功能需求是否具体（至少3个功能点）
    feature_section = re.search(r'## 功能需求\s*(.*?)(?=##|\Z)', content, re.DOTALL)
    if feature_section:
        features = re.findall(r'\d+\.\s*\*\*.*?\*\*', feature_section.group(1))
        if len(features) < 3:
            return False, f"功能需求不够详细，只有{len(features)}个功能点，建议至少3个"

    # 检查是否有示例或表格（表示详细度）
    has_examples = "|" in content or "示例" in content or "```" in content
    if not has_examples:
        return False, "文档缺少具体示例或详细说明"

    return True, "OK"

def validate_design_doc(filepath):
    """验证单个策划文档"""
    print(f"\n验证文档: {filepath}")

    checks = [
        ("文件存在", lambda: check_file_exists(filepath)),
        ("必需章节", lambda: check_required_sections(Path(filepath).read_text(encoding='utf-8'))),
        ("未完成内容", lambda: check_unfinished_content(Path(filepath).read_text(encoding='utf-8'))),
        ("详细程度", lambda: check_detail_level(Path(filepath).read_text(encoding='utf-8'))),
    ]

    all_passed = True
    for name, check_func in checks:
        passed, message = check_func()
        status = "✓" if passed else "✗"
        print(f"  {status} {name}: {message}")
        if not passed:
            all_passed = False

    return all_passed

def main():
    if len(sys.argv) < 2:
        print("用法: python test_design_doc.py <文档路径>")
        print("示例: python test_design_doc.py docs/战斗系统_v1.md")
        sys.exit(1)

    filepath = sys.argv[1]

    if os.path.isdir(filepath):
        # 验证整个目录
        print(f"验证目录: {filepath}")
        all_passed = True
        for file in Path(filepath).glob("*_v*.md"):
            if not validate_design_doc(str(file)):
                all_passed = False

        if all_passed:
            print("\n✓ 所有文档验证通过，可以交付给程序员")
        else:
            print("\n✗ 部分文档未通过验证，需要完善")
            sys.exit(1)
    else:
        # 验证单个文件
        if validate_design_doc(filepath):
            print("\n✓ 文档验证通过，可以交付给程序员")
        else:
            print("\n✗ 文档未通过验证，需要完善")
            sys.exit(1)

if __name__ == "__main__":
    main()
