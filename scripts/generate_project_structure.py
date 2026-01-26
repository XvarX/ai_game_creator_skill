#!/usr/bin/env python3
"""
生成游戏项目标准目录结构

根据游戏模块拆解自动创建项目文件夹结构
支持按模块/系统/玩法分类的文档组织
"""

import os
import sys
from pathlib import Path

def create_game_project(game_name, modules=None, base_path="."):
    """
    创建游戏项目目录结构

    Args:
        game_name: 游戏名称
        modules: 模块列表，例如 ["战斗模块", "角色模块", "关卡模块"]
                 如果为None，则创建默认的示例结构
        base_path: 基础路径
    """

    project_path = Path(base_path) / game_name

    # 如果没有提供模块列表，使用默认示例
    if modules is None:
        modules = ["战斗模块", "角色模块", "关卡模块"]

    # 主要目录结构
    directories = [
        "docs",                  # 策划文档
        "docs/模块",             # 模块文档
        "docs/玩法",             # 玩法文档
        "assets",                # 资源文件
        "assets/art",            # 美术资源
        "assets/audio",          # 音频资源
        "assets/fonts",          # 字体资源
        "assets/prefabs",        # 预制体（Unity等）
        "scripts",               # 代码脚本
        "scripts/core",          # 核心系统
        "scripts/gameplay",      # 游戏玩法
        "scripts/ui",            # UI系统
        "scripts/utils",         # 工具类
        "tests",                 # 测试脚本
        "builds",                # 构建输出
        "docs/reference",        # 参考文档
    ]

    # 为每个模块创建子目录
    for module in modules:
        directories.append(f"docs/模块/{module}")

    print(f"创建项目: {project_path}")
    print(f"\n模块列表: {', '.join(modules)}\n")

    # 创建目录
    for dir_name in directories:
        dir_path = project_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ 创建目录: {dir_name}")

    # 创建README
    readme_path = project_path / "README.md"
    readme_content = f"""# {game_name}

## 项目说明
本项目使用游戏开发协作skill创建，采用主策划+执行策划的两层策划体系。

## 目录结构
```
{game_name}/
├── docs/                    # 策划文档
│   ├── 游戏大纲_v1.md
│   ├── 模块拆解_v1.md
│   ├── 模块/                # 各模块文档
│   │   ├── 战斗模块/
│   │   │   ├── 伤害系统_v1.md
│   │   │   └── 状态系统_v1.md
│   │   └── 角色模块/
│   │       ├── 属性系统_v1.md
│   │       └── 成长系统_v1.md
│   └── 玩法/                # 玩法文档
│       ├── 核心玩法_v1.md
│       └── 辅助玩法_v1.md
├── assets/                  # 资源文件
├── scripts/                 # 游戏代码
└── tests/                   # 测试脚本
```

## 开发进度
- [ ] 需求分析（主策划）
- [ ] 模块拆解（主策划）
- [ ] 游戏大纲（主策划）
- [ ] 详细策划（执行策划）
- [ ] 技术实现（程序员）
- [ ] 测试优化（测试员）

## 变更历史
"""
    readme_path.write_text(readme_content, encoding='utf-8')
    print(f"  ✓ 创建: README.md")

    # 创建.gitignore
    gitignore_path = project_path / ".gitignore"
    gitignore_content = """# Build outputs
builds/
*.exe
*.app

# Engine specific
[Dd]ebug/
[Rr]elease/
*.sln
*.user

# IDE
.vs/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp
~$*

# Keep assets but ignore large binaries
assets/art/*.psd
assets/art/*.ai
"""
    gitignore_path.write_text(gitignore_content, encoding='utf-8')
    print(f"  ✓ 创建: .gitignore")

    # 创建模块说明文件
    modules_readme = project_path / "docs" / "模块" / "README.md"
    modules_readme_content = f"""# 模块文档说明

本目录包含各模块的详细策划文档，由执行策划编写。

## 模块列表

{chr(10).join([f'- **{module}**' for module in modules])}

## 文档命名规范

- 文件名格式：`[系统名称]_v[版本号].md`
- 例如：`伤害系统_v1.md`, `角色属性系统_v2.md`

## 注意事项

- 每个系统一个独立文档
- 文档内容必须详细完整
- 修改时更新版本号
- 遵循策划文档模板
"""
    modules_readme.write_text(modules_readme_content, encoding='utf-8')
    print(f"  ✓ 创建: docs/模块/README.md")

    print(f"\n✓ 项目结构创建完成: {project_path}")
    print(f"\n下一步:")
    print(f"  1. 主策划：在 docs/ 目录创建模块拆解文档")
    print(f"  2. 主策划：创建游戏大纲")
    print(f"  3. 执行策划：在各模块目录下创建详细策划文档")
    print(f"  4. 程序员：开始技术实现")

    return project_path

def main():
    if len(sys.argv) < 2:
        print("用法: python generate_project_structure.py <游戏名称> [模块列表] [基础路径]")
        print("\n示例:")
        print("  1. 使用默认模块:")
        print("     python generate_project_structure.py MyGame")
        print("\n  2. 指定自定义模块（用逗号分隔）:")
        print('     python generate_project_structure.py MyGame "战斗模块,角色模块,关卡模块"')
        print("\n  3. 指定基础路径:")
        print('     python generate_project_structure.py MyGame "战斗模块,角色模块" "..')
        sys.exit(1)

    game_name = sys.argv[1]

    # 解析模块列表
    modules = None
    if len(sys.argv) >= 3:
        module_str = sys.argv[2]
        # 检查是否是路径（包含路径分隔符）
        if '/' in module_str or '\\' in module_str or module_str.startswith('.') or module_str.startswith('..'):
            # 这是路径，不是模块列表
            base_path = module_str
        else:
            # 这是模块列表
            modules = [m.strip() for m in module_str.split(',')]
            base_path = sys.argv[3] if len(sys.argv) > 3 else "."
    else:
        base_path = "."

    create_game_project(game_name, modules, base_path)

if __name__ == "__main__":
    main()
