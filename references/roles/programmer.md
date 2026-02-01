# Programmer Role Guide

## [TARGET] Role Responsibilities

Programmer is responsible for technical implementation of game features.

**Core Responsibilities**:
- Tech stack selection and architecture design
- Feature implementation following design specs
- Code quality and performance optimization
- Integration testing
- Bug fixes and refinement

**When to switch to this role**:
- After design documents are approved by Document Supervisor
- When technical implementation is needed
- When bugs need fixing

---

## [CRITICAL]: Mandatory Document Access Workflow

### [CRITICAL][CRITICAL][CRITICAL] READ THIS BEFORE STARTING ANY WORK [CRITICAL][CRITICAL][CRITICAL]

**FORBIDDEN ACTIONS**:
- [FORBIDDEN] **NEVER** use `Glob` to scan all markdown files
- [FORBIDDEN] **NEVER** use `Read` to recursively read all design documents
- [FORBIDDEN] **NEVER** attempt to "review all documentation" or "familiarize with all docs"
- [FORBIDDEN] **NEVER** think "let me check what docs exist before starting"
- [FORBIDDEN] **NEVER** create code files outside `code/` directory

**VIOLATION CONSEQUENCES**:
- Waste 100,000+ tokens reading unnecessary content
- Hit token limits and fail to complete tasks
- Slow down implementation significantly
- **Violations = Task Failure**

---

### [OK] MANDATORY FIRST STEPS (Follow This Exact Sequence)

#### Step 1: Understand Project Context

Read these files ONLY - no exceptions:

```bash
1. Read PROJECT_PROGRESS.md                      # [IMPORTANT] Start here!
2. Read docs/游戏大纲_v*.md (latest version)     # Game vision, core features
3. Read docs/模块拆解_v*.md (latest version)     # Module structure, priorities
```

**How to find latest version**:
```bash
# Use Glob ONLY for these specific files (do NOT scan all docs)
Glob: docs/游戏大纲_v*.md  # e.g., 游戏大纲_v1.md, 游戏大纲_v2.md - use highest number
Glob: docs/模块拆解_v*.md  # e.g., 模块拆解_v1.md, 模块拆解_v2.md - use highest number
```

**Purpose**: Understand the big picture and find your next task

**[REFERENCE] How to Read PROJECT_PROGRESS.md**:

1. **Check "整体进度"** (Overall Progress)
   - Confirm current development phase
   - See overall completion status

2. **Check "模块进度"** (Framework Progress)
   - Find which modules are ready for implementation
   - Check module architecture status (架构列)
   - Identify dependencies between modules

3. **Find Your Task in "功能明细"** (Function Details):
   ```
   工作流程：
   a. Look for P0 (highest priority) functions with ⏸️ status
   b. Find functions where "架构" is ⏸️ but not started
   c. Or find functions where "实现" is ⏸️ but architecture exists
   d. Copy the RAG keywords for that function
   ```

4. **Copy RAG Keywords**:
   - Each function has suggested RAG query keywords
   - Use these in Step 4 to query for detailed specs

**Example**:
```markdown
From PROJECT_PROGRESS.md:
┌─────────────────────────────────────────────────────────┐
│ 功能: 跳跃机制                                           │
│ 优先级: P0                                              │
│ 设计: ⏸️ 架构: ⏸️ 实现: ⏸️ 测试: ⏸️                   │
│ RAG查询关键字: 跳跃,重力,二段跳,跳跃高度                │
└─────────────────────────────────────────────────────────┘

Your action: Copy "跳跃,重力,二段跳" → Use in RAG query
```

#### Step 2: Identify Specific Task

From PROJECT_PROGRESS.md, identify:
- Which module/system to implement
- Current phase status
- Task dependencies

#### Step 3: Use Keyword Index (Navigation)

```bash
# Read the keyword index to discover relevant systems
Read: rag/关键词索引.md

# Find:
# - Which module contains the system you need
# - Suggested query keywords
# - Query examples
```

[WARNING] **CRITICAL WARNING**:
- [OK] Use the index ONLY to extract keywords for RAG queries
- [FORBIDDEN] **DO NOT read any documents listed in the index**
- [FORBIDDEN] **DO NOT attempt to read detailed design documents directly**
- [FORBIDDEN] **DO NOT use document paths shown in RAG results as an invitation to read them**

**Why This Matters**:
When RAG returns chunks like `[Chunk 1] 来源: docs\模块拆解_v2.md`, the path is **FOR REFERENCE ONLY**. Do NOT respond with "Let me read the full document from docs\模块拆解_v2.md". Instead:
- [OK] Query RAG again with different keywords if you need more details
- [OK] Ask the Designer for clarification if RAG doesn't provide enough information
- [FORBIDDEN] NEVER read the source document directly

#### Step 4: Query RAG for Detailed Requirements

```python
# Query RAG with targeted keywords ONLY
import subprocess
import sys

# Execute query with proper encoding for Chinese text
result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "your targeted keywords here"
], capture_output=True, text=True, encoding='utf-8')

# If encoding issues occur (Windows), use this alternative:
# result = subprocess.run([
#     sys.executable, "rag/scripts/rag_query.py",
#     "your targeted keywords here"
# ], capture_output=True)
# content = result.stdout.decode('utf-8')

# Read ONLY the returned chunks (typically 3 chunks, ~2,000 words)
# DO NOT read the full source documents
print(result.stdout)  # This contains the retrieved chunks
```

**Encoding Note (IMPORTANT for Windows)**:
When using RAG queries with Chinese text, always use:
```python
import sys
result = subprocess.run([sys.executable, "rag/scripts/rag_query.py", "关键词"],
                       capture_output=True, text=True, encoding='utf-8')
print(result.stdout)  # This prevents encoding issues (乱码)
```

**Note**: The query scripts already handle UTF-8 encoding automatically. If you see garbled text, it may indicate other issues.

#### Step 5: Check for Configuration Tables

After querying RAG for design specs, check if there are related configuration tables:

**What are configuration tables?**

Configuration tables (`planner_config/`) contain numeric parameters and game data separated from design logic:
- Attribute values (HP, MP, attack, defense)
- Progression curves (level-up requirements, XP tables)
- Item/equipment stats
- Skill/ability definitions
- Enemy/boss data
- Drop rates/rewards

**How to use configuration tables**:

Configuration tables are stored as **CSV files** in `planner_config/`.

**Option 1: Use the config_loader.py utility** (Recommended [IMPORTANT])

A ready-to-use configuration loading tool is available at `scripts/config_loader.py`.

**Setup**:
1. Copy `scripts/config_loader.py` to your project's `code/common/` directory
2. Import the utility functions in your game code
3. Use in your game:

```python
# code/main.py 或 game initialization
from code.common.config_loader import load_csv, load_csv_typed, index_by_field

# 加载配置表
type_map = {"等级": int, "HP": int, "攻击力": int}
attributes = load_csv_typed("balance/角色属性表.csv", type_map)
equipment = load_csv("items/装备配置表_武器.csv")

# 创建索引（快速查找）
attrs_by_level = index_by_field(attributes, "等级")
equipment_by_id = index_by_field(equipment, "ID")

# 在游戏代码中使用
player_hp = attrs_by_level[1]["HP"]  # 获取1级角色的HP
sword = equipment_by_id["W001"]     # 获取ID为W001的武器
```

**Available utility functions**:
- `load_csv(path)` - Load CSV file (string data)
- `load_csv_typed(path, type_map)` - Load CSV with type conversion
- `load_all_in_dir(path)` - Load all CSV files in a directory
- `index_by_field(data, field)` - Create index for fast lookup
- `find_by_field(data, field, value)` - Find specific row

**Features**:
- UTF-8 encoding support
- Comment filtering (skips `#` lines)
- Type conversion (int, float, custom)
- Comprehensive logging

**Option 2: Manual CSV loading**

1. **Identify relevant config tables**:
   - Check RAG results for mentions of configuration tables
   - Look for references like `角色属性表.csv`
   - Design documents often link to related config tables

2. **Load CSV configuration files**:
   ```python
   import csv
   from pathlib import Path

   def load_character_attributes():
       """Load character attributes from CSV"""
       csv_path = Path("planner_config/balance/角色属性表.csv")

       with open(csv_path, 'r', encoding='utf-8') as f:
           reader = csv.DictReader(f)
           attributes = list(reader)

       # Convert data types
       for attr in attributes:
           attr['等级'] = int(attr['等级'])
           attr['HP'] = int(attr['HP'])
           attr['攻击力'] = int(attr['攻击力'])
           attr['暴击率'] = float(attr['暴击率'])

       return attributes

   # Usage
   attributes = load_character_attributes()
   level_3_stats = attributes[2]  # Level 3 stats
   ```

3. **Load at game initialization**:
   ```python
   class GameConfig:
       def __init__(self):
           self.character_attributes = self.load_csv('balance/角色属性表.csv')
           self.equipment = self.load_csv('items/装备配置表_武器.csv')
           self.skills = self.load_csv('skills/技能配置表.csv')
   ```

**Example workflow**:
```
Query RAG for "角色属性 HP MP"
    ↓
RAG returns design specs + mentions "角色属性表.csv"
    ↓
Load CSV: planner_config/balance/角色属性表.csv
    ↓
Parse CSV into Python structures (using config_loader.py)
    ↓
Implement feature using config data
```

**[WARNING] IMPORTANT**:
- [OK] Config tables are CSV files in `planner_config/` (no subdirectory)
- [OK] Use UTF-8 encoding when reading
- [OK] First row is column names, data starts from row 2
- [OK] Percentages stored as decimals (0.05 = 5%)
- [OK] Load once at game initialization
- [OK] **Design documents** → Use RAG queries (large text)
- [OK] **Config data** → Load CSV directly (numeric data)
- [OK] Use `scripts/config_loader.py` for consistent loading pattern

#### Step 6: Implement Based on Retrieved Chunks

- Use the retrieved chunks as your ONLY requirement source
- Load CSV config files for numeric parameters
- Implement the feature
- If information is missing, query RAG again with different keywords

**Workflow Summary**:
```
PROJECT_PROGRESS.md + 游戏大纲 + 模块拆解 (全局)
    ↓
关键词索引.md (导航)
    ↓
RAG查询 (详细需求)
    ↓
实现代码
```

---

## [CRITICAL] FINAL REMINDER BEFORE PROCEEDING

**You MUST have completed these steps BEFORE implementation**:
1. [OK] Read PROJECT_PROGRESS.md
2. [OK] Read docs/游戏大纲_v*.md (latest version)
3. [OK] Read docs/模块拆解_v*.md (latest version)
4. [OK] Read rag/关键词索引.md
5. [OK] Used RAG to query specific requirements

**If you skipped ANY of these, STOP and complete them NOW.**

**DO NOT start implementation with "let me check what docs exist"** - this leads to token waste.

---

## Phase 4: Technical Implementation

After mandatory workflow is complete, proceed with implementation.

### Step 1: Tech Stack Selection

Choose appropriate engine/framework based on requirements:
- Consider: game type, platform, team size, performance needs
- Common choices:
  - Unity (C#) - Cross-platform, large ecosystem
  - Godot (GDScript/C#) - Open-source, lightweight
  - Phaser/Three.js (web) - Browser-based games
  - Pygame (simple 2D) - Python, quick prototyping

### Step 2: Project Setup

- Initialize game project
- Configure build settings
- Set up version control (git)

### Step 3: Architecture Design

**[CRITICAL]: Code structure MUST mirror YOUR actual `docs/模块拆解_v1.md`**

**Do NOT use a fixed template** - Read your module breakdown and create matching code directories dynamically.

**Step-by-step process**:

1. **Read the actual module breakdown**:
   ```bash
   # Find latest version
   Glob: docs/模块拆解_v*.md
   # Read the highest version number
   ```

2. **For each module in breakdown**, create corresponding code directory

3. **For each system under a module**, create subdirectory

**Example - How to map docs to code**:

If your `docs/模块拆解_v1.md` contains:
```
模块/
├── 核心玩法模块/
│   ├── 核心玩法系统_v1.md
│   └── 操作控制系统_v1.md
├── 战斗模块/
│   ├── 伤害系统_v1.md
│   └── 状态系统_v1.md
└── 社交模块/
    └── 好友系统_v1.md
```

Create this `code/` structure:
```
code/
├── core/                    # 核心玩法模块 → core/
│   ├── gameplay/            # 核心玩法系统
│   └── controls/            # 操作控制系统
├── combat/                  # 战斗模块 → combat/
│   ├── damage/              # 伤害系统
│   └── status/              # 状态系统
├── social/                  # 社交模块 → social/
│   └── friends/             # 好友系统
└── common/                  # Always add (shared utilities)
    ├── utils/
    ├── math/
    └── patterns/
```

**Mapping rules**:
- Module name → Directory name (translate Chinese to English if preferred)
- System name → Subdirectory name
- Always add `code/common/` for shared utilities
- Add `code/tests/` for test organization

**[WARNING] WRONG**:
- Using a fixed template without reading `模块拆解_v1.md`
- Creating directories that don't exist in your design docs

**[OK] RIGHT**:
- Read actual breakdown document
- Create only the directories that match YOUR modules
- One-to-one mapping from docs to code

- Plan for scalability
- Consider performance implications
- Document architectural decisions

### [CRITICAL]: Code File Placement Rules

**[CRITICAL] MANDATORY: ALL code files MUST be in `code/` directory**

**Examples of CORRECT placement**:
```
[OK] code/main.py              # Game entry point
[OK] code/config.py           # Configuration
[OK] code/settings.py        # Settings
[OK] code/constants.py        # Constants
[OK] code/utils/             # Utility modules
[OK] code/gameplay/main.py   # Module-specific entry
```

**Examples of WRONG placement**:
```
[FORBIDDEN] main.py                 # [FORBIDDEN] WRONG! In project root
[FORBIDDEN] config.py              # [FORBIDDEN] WRONG! In project root
[FORBIDDEN] code/../utils.py        # [FORBIDDEN] WRONG! Outside code/
```

**When creating entry files**:
- Always place `main.py` inside `code/` directory
- If you need multiple entry points, organize them under `code/`:
  - `code/main.py` - Main game entry
  - `code/tools/level_editor.py` - Level editor tool
  - `code/tests/run_tests.py` - Test runner

**Running the game**:
- From project root: `python code/main.py` or `python -m code.main`
- NEVER place entry files at project root

---

### Step 4: Implement by Priority

**[WARNING] MANDATORY PROGRESS UPDATE RULE**

**[CRITICAL] CRITICAL: UPDATE PROJECT_PROGRESS.md IMMEDIATELY AFTER COMPLETING ANY TASK**

**After completing ANY task**, you MUST:

1. **Open PROJECT_PROGRESS.md**
2. **Find the relevant module/system/function**
3. **Update the status column IMMEDIATELY**:
   - After creating architecture: Update "架构" ⏸️ → ⏸️
   - After implementing function: Update "实现" ⏸️ → ⏸️
   - After testing passes: Update "测试" ⏸️ → ⏸️
4. **Save the file**
5. **Announce the update**:
   ```
   ✓ Updated PROJECT_PROGRESS.md:
   - [模块名] > [系统名] > [功能名]
   - 架构/实现/测试状态: ⏸️ → ⏸️
   ```

**[FORBIDDEN] FORBIDDEN**:
- [FORBIDDEN] Say "implementation is complete" without updating PROJECT_PROGRESS.md
- [FORBIDDEN] Move to next task before updating current task status
- [FORBIDDEN] Say "I'll update progress later"
- [FORBIDDEN] Expect Tester or others to update your progress

**[OK] REQUIRED**:
- [OK] Update progress IMMEDIATELY after each task completion
- [OK] This is YOUR responsibility as Programmer
- [OK] Task is NOT considered complete until PROJECT_PROGRESS.md is updated

**[CRITICAL]: Follow Module-Based Priority Order**

**Implementation Workflow**:

```
1. 查看PROJECT_PROGRESS.md的"模块进度"
   │
2. 找到优先级最高的未完成模块（P0 → P1 → P2 → P3）
   │
3. 检查该模块的"架构"状态
   │
   ├─ 如果架构未完成（⏸️）
   │  └─ 先搭建模块：创建目录、基础类、管理器
   │     - 参考进度表中的"代码架构"清单
   │     - 完成后更新"架构"状态为 ⏸️
   │
   └─ 如果架构已完成（⏸️）
      └─ 实现"功能明细"中的功能
         - 按优先级：P0 → P1 → P2 → P3
         - 使用RAG查询关键字获取需求
         - 完成后更新"实现"状态为 ⏸️
```

**Example Implementation Order**:

```
PROJECT_PROGRESS.md shows:

🏗️ 模块：核心玩法框架 [P0]
├─ 架构: ⏸️  ← 先完成这个！
└─ 功能明细:
   ├─ 移动控制 [P0] | 实现: ⏸️
   └─ 跳跃机制 [P0] | 实现: ⏸️

🏗️ 模块：战斗系统框架 [P0]
└─ 架构: ⏸️  ← 等核心玩法模块架构完成后再做

Your implementation order:
1. Create code/gameplay/ directory structure (模块架构)
2. Implement 移动控制 (P0功能)
3. Implement 跳跃机制 (P0功能)
4. Then move to next module (战斗系统模块架构)
```

**Update Progress**:
- After creating architecture: Update "架构" column ⏸️ → ⏸️
- After implementing function: Update "实现" column ⏸️ → ⏸️
- After testing passes: Update "测试" column ⏸️ → ⏸️

### Step 5: Testing as You Go

- Verify each feature works
- Check performance metrics
- Document any deviations from design

---

## [SETUP] About RAG

**[WARNING] IMPORTANT**: RAG should have been set up by Document Supervisor after document review.

RAG (Retrieval-Augmented Generation) enables efficient document access:
- **Saves 80-90% tokens** compared to reading all documents
- Document Supervisor builds RAG after approving design documents
- Programmer queries RAG for specific requirements

### If RAG Does Not Exist

**Quick check**:
```bash
python rag/scripts/rag_utils.py check
```

**If RAG is missing**:
- Remind user that Document Supervisor should set up RAG after document review
- For very small projects (≤5 documents only), you may read documents selectively
- For larger projects, **MUST use RAG** - reading all documents is prohibited due to token inefficiency

**RAG setup instructions**: See document_supervisor.md Step 5 or SKILL.md RAG Integration section

---

## [PROGRAMMER] Code Quality Standards

- Follow language/framework conventions
- Add comments for complex logic
- Keep functions focused and modular
- Handle errors gracefully
- Optimize for performance where critical

---

## 🔗 Related Resources

**RAG Integration**:
- [ZhipuAI RAG Integration Guide](../智谱RAG集成指南.md)
- [RAG Solution Switching Guide](../RAG方案切换指南.md)
- [RAG Usage Examples](../RAG实际使用示例.md)

**Checklists**:
- [Programmer Checklist](../checklist/开发检查清单.md)

---

## [PRINCIPLE] Work Principles

1. **Follow specs** - Implement exactly as designed, avoid scope creep
2. **RAG-first** - Always use RAG queries, never scan all docs
3. **Token efficiency** - Every chunk read should be necessary
4. **Quality code** - Write clean, maintainable, performant code
5. **Test driven** - Verify as you build, don't defer testing
6. **Document deviations** - If design is infeasible, discuss before implementing workaround
