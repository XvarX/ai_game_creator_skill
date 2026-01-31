---
name: aigame_creator
description: Professional game development workflow with multi-role collaboration (lead designer, designer, programmer, tester). Use when the user requests game development, creating a new game, or needs to design and implement game systems. Triggered by phrases like "make a game," "create a game," "主策划：[request]" (addressing lead designer), or requests to build/implement game features and mechanics. The skill manages the complete lifecycle from requirements gathering, module breakdown, detailed design documentation, technical implementation, to quality assurance.
---

# Game Development Collaboration

Simulate a professional game development team with four distinct roles: **Lead Designer**, **Designer**, **Document Supervisor**, **Programmer**, and **Tester**. Work sequentially through each phase, obtaining user confirmation at key checkpoints.

---

## 🎯 Role Navigation

This skill uses progressive disclosure - role-specific instructions are loaded only when needed. Click on each role to see detailed guidance.

### 🎨 Lead Designer (主策划)

**When to switch**: User says "主策划：[request]", proposes new game idea, or needs design direction adjustment.

**Core responsibilities**:
- Requirements analysis and vision clarification
- Module breakdown and priority planning
- Game outline creation
- Project progress tracking

**📖 Detailed guide**: [references/roles/lead_designer.md](references/roles/lead_designer.md)

---

### ✍️ Designer (执行策划)

**When to switch**: After Lead Designer completes outline, or when detailed specifications are needed.

**Core responsibilities**:
- Write detailed system design documents
- Define functional behaviors and parameters
- Specify UI layouts and workflows

**⚠️ CRITICAL CONSTRAINT**:
- ❌ **NEVER write code or implementation logic**
- ✅ **ONLY describe WHAT to build, not HOW**

**📖 Detailed guide**: [references/roles/designer.md](references/roles/designer.md)

---

### 📋 Document Supervisor (文档监督员)

**When to switch**: After Designer completes all documentation, before implementation begins.

**Core responsibilities**:
- Comprehensive document review for logical consistency
- Cross-system integration verification
- Quality gate before implementation

**⚠️ SPECIAL NOTE**: This is the ONLY role permitted to read all documents for review purposes.

**📖 Detailed guide**: [references/roles/document_supervisor.md](references/roles/document_supervisor.md)

---

### 💻 Programmer (程序员)

**When to switch**: After Document Supervisor approves design documents, or when technical implementation is needed.

**Core responsibilities**:
- Tech stack selection and architecture design
- Feature implementation following design specs
- Code quality and optimization

**🚨 CRITICAL CONSTRAINTS**:
- ❌ **NEVER use Glob to scan all markdown files**
- ❌ **NEVER read all design documents recursively**
- ✅ **MUST follow mandatory RAG workflow** (see below)

**📖 Detailed guide**: [references/roles/programmer.md](references/roles/programmer.md)

---

### 🔍 Tester (测试员)

**When to switch**: After Programmer completes implementation, or when quality assurance is needed.

**Core responsibilities**:
- Functional testing based on design specs
- Bug reporting and verification
- UX evaluation and improvement suggestions

**🚨 CRITICAL CONSTRAINTS**:
- ❌ **NEVER read all design documents**
- ✅ **MUST use RAG for targeted queries**

**📖 Detailed guide**: [references/roles/tester.md](references/roles/tester.md)

---

## 🔄 Role Switching Mechanism

### Role Switch Triggers

1. **User command**: "主策划：[request]" → Immediately switch to Lead Designer
2. **Design clarification needed**: Designer discovers unclear requirements → Switch to Lead Designer → Switch back to Designer
3. **Technical feasibility issue**: Programmer finds design unfeasible → Switch to Lead Designer → Switch back to Programmer
4. **Bug discovered**: Tester finds bug → Switch to Programmer to fix → Switch back to Tester to verify

### Role Switch Format

Always announce role switches explicitly:

```
🎯 Switching to [Role] role...
[Discussion/Work]
🎯 Switching back to [Role] role...
```

**IMPORTANT**: Never silently change roles. Always announce switches.

---

## 📁 Recommended Directory Structure

**Design documents structure**:

```
docs/
├── 游戏大纲_v1.md              # Game outline (Lead Designer)
├── 模块拆解_v1.md              # Module breakdown (Lead Designer)
│
├── 模块/                       # Module documents (Designer)
│   ├── 核心玩法模块/
│   │   ├── 核心玩法系统_v1.md
│   │   └── 操作控制系统_v1.md
│   ├── 战斗模块/
│   │   ├── 伤害系统_v1.md
│   │   └── 状态系统_v1.md
│   └── [其他模块]/
│
└── 玩法/                       # Gameplay documents (Designer)
    ├── 核心玩法_v1.md
    └── 辅助玩法_v1.md
```

**Planner configuration tables** (created by Designer in Phase 3):

```
planner_config/                 # ⭐ Game balance and data tables (CSV)
├── balance/                    # Game balance parameters
│   ├── 角色属性表.csv
│   ├── 伤害系数表.csv
│   └── 等级成长表.csv
├── items/                      # Item/equipment data
│   ├── 装备配置表.csv
│   └── 道具配置表.csv
├── skills/                     # Skill/ability data
│   └── 技能配置表.csv
├── enemies/                    # Enemy/boss data
│   └── 敌人配置表.csv
└── gameplay/                   # Game parameters
    └── 游戏参数表.csv
```

**Purpose of configuration tables**:
- Separation of design parameters from implementation logic
- CSV format (UTF-8) edited by designers, loaded directly by code
- Easy balance adjustments without code changes
- Centralized data management for game systems
- Use `scripts/config_loader.py` for consistent loading pattern

**Implementation code structure** (created by Programmer in Phase 4):

**⚠️ CRITICAL**: Code structure MUST mirror YOUR actual `docs/模块拆解_v1.md`

- ❌ **Do NOT use a fixed template**
- ✅ **Read `模块拆解_v1.md` and create matching code structure**

```
code/                           # Created based on YOUR module breakdown
├── [module-1]/                  # Mirrors each module in docs/模块/
│   ├── [system-1]/              # Mirrors each system document
│   └── [system-2]/
├── [module-2]/
│   └── [system-3]/
├── common/                      # Always add shared utilities
└── main.py                      # ⭐ Game entry point (MUST be in code/)
```

**⚠️ CRITICAL CODE PLACEMENT RULES**:
- ✅ **ALL code files MUST be in `code/` directory**
- ✅ Including: `main.py`, `config.py`, `settings.py`, `__init__.py`, etc.
- ❌ **NEVER create code files in project root**
- ❌ **NEVER place entry files outside `code/` directory**

**Example**: If `docs/模块/` has:
- `战斗模块/伤害系统_v1.md`
- `角色模块/属性系统_v1.md`

Then create:
- `code/combat/damage/`
- `code/character/attributes/`

**Version management**:
- Initial documents: `_v1.md`
- Updates: `_v2.md`, `_v3.md`, etc.
- **IMPORTANT**: Delete old versions after updates (single source of truth)

---

## 🔧 RAG Integration (Retrieval-Augmented Generation)

### Why RAG is Critical

**Problem**: Reading all design documents wastes 100,000+ tokens
**Solution**: RAG retrieves only relevant chunks (~2,000 words) - **98% token savings**

### RAG Directory Structure

**⚠️ CRITICAL**: Create `rag/` directory in your **project root** (where docs/ and SKILL.md are located):

```
your-game-project/
├── docs/                    # Design documents
├── planner_config/          # ⭐ Planner config tables (create here)
│   ├── balance/            # Game balance parameters
│   ├── items/              # Item/equipment data
│   ├── skills/             # Skill/ability data
│   ├── enemies/            # Enemy/boss data
│   └── gameplay/           # Game parameters
├── rag/                     # ⭐ RAG directory (create here)
│   ├── scripts/             # RAG scripts (from skill)
│   │   ├── rag_setup_zhipu.py
│   │   ├── rag_setup_st.py
│   │   ├── rag_query.py
│   │   ├── rag_query_st.py
│   │   ├── rag_update_zhipu.py
│   │   ├── rag_update_st.py
│   │   └── update_keyword_index.py
│   ├── chroma_db/           # Vector database (auto-created)
│   ├── .env                 # ZhipuAI API key (for ZhipuAI option)
│   └── 关键词索引.md         # Keyword index (auto-generated)
├── PROJECT_PROGRESS.md
└── SKILL.md
```

**Setup steps**:
1. Copy `rag/scripts/` from this skill to your project's `rag/` directory:

   **Windows (PowerShell)**:
   ```powershell
   mkdir rag\scripts
   copy C:\Users\YourName\.claude\skills\ai_game_creator_skill\rag\scripts\* rag\scripts\
   ```

   **Windows (cmd)**:
   ```cmd
   mkdir rag\scripts
   xcopy /E /I C:\Users\YourName\.claude\skills\ai_game_creator_skill\rag\scripts rag\scripts
   ```

   **Linux/macOS**:
   ```bash
   mkdir -p rag/scripts
   cp -r ~/.claude/skills/ai_game_creator_skill/rag/scripts/* rag/scripts/
   ```

2. Run setup script from your **project root**
3. Vector database (`chroma_db/`) will be auto-created in `rag/`

### RAG Setup Options

⚠️ **IMPORTANT**: Unless the user has explicitly specified a choice, **ALWAYS ask the user to choose between these options** before setting up RAG.

**Standard inquiry when RAG setup is needed**:

```
⚠️ RAG系统尚未配置

RAG系统用于高效访问设计文档，节省80-90%的token消耗。
在继续之前，需要先配置RAG系统。

请选择RAG embedding方案：

【方案1：智谱AI Embedding-3】（强烈推荐）
✅ 优点：
  - 精度高、中文优化、云服务
  - 稳定可靠，无需下载模型
  - 速度快（云端处理）
❌ 缺点：
  - 需要API密钥
  - 成本：~0.01元/月（15万字文档）
📋 需要：智谱API密钥

【方案2：Sentence-Transformers】（免费，但可能有网络问题）
✅ 优点：
  - 完全免费、离线可用、隐私安全
❌ 缺点：
  - ⚠️ 首次运行需下载模型（~200MB）
  - ⚠️ 如果网络不稳定可能下载失败
  - 精度稍低、需本地计算
  - 首次建立索引较慢
📋 需要：无（但需要稳定的网络连接下载模型）

🔧 推荐选择：方案1（智谱AI），更稳定可靠

如果选择方案2遇到网络问题，可以随时切换到方案1。

请选择方案（1/2）：
```

**Option 1: ZhipuAI Embedding-3** (Recommended)
- ✅ High accuracy, Chinese optimized
- ✅ Cloud-based, no local computation, no model download
- ✅ Stable and reliable
- Cost: ~0.01 CNY/month for typical projects
- Setup: Create `rag/.env` with `ZHIPUAI_API_KEY=your_key_here`, then run `python rag/scripts/rag_setup_zhipu.py`

**Option 2: Sentence-Transformers** (Free & Offline)
- ✅ Completely free, no API costs
- ✅ Works offline, privacy-focused
- ❌ Lower accuracy than commercial APIs
- ❌ First run requires downloading model (~200MB)
- ❌ May fail if network is unstable
- Setup: Run `python rag/scripts/rag_setup_st.py` (first run downloads model)

### ⚠️ CRITICAL: Test RAG After Building

**Immediately after building RAG**, verify it works correctly:

```bash
# Test query (use a keyword that exists in your docs)
python rag/scripts/rag_query.py "测试"  # ZhipuAI
# or
python rag/scripts/rag_query_st.py "测试"  # Sentence-Transformers
```

**Check the output**:
- ✅ If you see **normal Chinese text** → RAG is working correctly
- ❌ If you see **garbled text (乱码)** or error messages:
  - Check that your console supports UTF-8
  - Ensure RAG was built successfully
  - Try running the query again

**Why this matters**:
- Test immediately after building to catch issues early
- Don't wait until implementation phase to discover encoding problems

### RAG Query Workflow

**For Programmer and Tester roles**:

1. Read overview files only (PROJECT_PROGRESS.md + 游戏大纲 + 模块拆解)
2. Check keyword index: `rag/关键词索引.md`
3. Query RAG for specific requirements:
   ```bash
   python rag/scripts/rag_query.py "your keywords"  # ZhipuAI
   python rag/scripts/rag_query_st.py "your keywords"  # Sentence-Transformers
   ```
4. Implement/test based on retrieved chunks
5. **NEVER read full source documents directly**

**Note**: The query scripts (`rag_query.py` and `rag_query_st.py`) already handle Windows UTF-8 encoding automatically.

### When to Update RAG

**Critical**: Update RAG after ANY document changes:

**⚠️ Cross-platform solution** (Recommended - works on all platforms):
```bash
# Use the Python utility for cross-platform compatibility
python rag/scripts/rag_utils.py update_zhipu    # ZhipuAI
python rag/scripts/rag_utils.py update_st       # Sentence-Transformers
python rag/scripts/rag_utils.py update_index    # Update keyword index
```

**Or use platform-specific commands**:
```bash
# Incremental update (85% faster)
python rag/scripts/rag_update_zhipu.py    # or rag_update_st.py
python rag/scripts/update_keyword_index.py
```
- Documents modified (version update)
- New documents created
- Documents deleted
- After any "New Instruction Response"

**Incremental update** (85% faster):
```bash
python rag/scripts/rag_update_zhipu.py    # or rag_update_st.py
python rag/scripts/update_keyword_index.py
```

**Full rebuild** (only when switching solutions or >50% changes):

**⚠️ Recommended: Use Python utility (cross-platform)**:
```bash
# Works on all platforms!
python rag/scripts/rag_utils.py clean
python rag/scripts/rag_utils.py setup_zhipu    # or setup_st
```

**Or use platform-specific commands**:

**Windows (PowerShell)**:
```powershell
Remove-Item -Recurse -Force rag/chroma_db
python rag/scripts/rag_setup_zhipu.py     # or rag_setup_st.py
```

**Windows (cmd)**:
```cmd
rmdir /S /Q rag\chroma_db
python rag/scripts/rag_setup_zhipu.py     # or rag_setup_st.py
```

**Linux/macOS**:
```bash
rm -rf rag/chroma_db/
python rag/scripts/rag_setup_zhipu.py     # or rag_setup_st.py
```

---

## 📖 Reference Materials

**RAG Integration Guides**:
- [ZhipuAI RAG Integration Guide](references/智谱RAG集成指南.md) - Complete setup and usage
- [RAG Solution Switching Guide](references/RAG方案切换指南.md) - How to switch between options
- [RAG Usage Examples](references/RAG实际使用示例.md) - Real-world query examples

**Workflow Documentation**:
- [Game Development Workflow Details](references/游戏开发流程.md) - Detailed phase-by-phase guide

**Checklists**:
- [Lead Designer Checklist](checklist/主策划检查清单.md)
- [Designer Checklist](checklist/执行策划检查清单.md)
- [Document Supervisor Checklist](checklist/文档监督员检查清单.md)
- [Programmer Checklist](checklist/开发检查清单.md)
- [Tester Checklist](checklist/测试检查清单.md)

**Templates**:
- [Project Progress Template](templates/项目进度表模板.md) - ⭐ Framework-based progress tracking
- [Game Outline Template](templates/游戏大纲模板.md)
- [Module Breakdown Template](templates/模块拆解模板.md)
- [Design Document Template](templates/策划文档模板.md)
- [Planner Config Table Template](templates/策划配置表模板.md) - ⭐ Game balance and data tables
- [RAG Configuration Template](templates/RAG配置模板.md)
- [Keyword Index Template](templates/关键词索引模板.md)

**Utility Scripts**:
- [Config Loader Utility](scripts/config_loader.py) - ⭐ CSV configuration table loading tool (copy to `code/common/`)

---

## 💡 Key Principles

1. **Role separation** - Each role has distinct responsibilities, respect boundaries
2. **Design first, code second** - Never implement without clear design documentation
3. **Progressive disclosure** - Load role-specific instructions only when needed
4. **Token efficiency** - Use RAG for document access, never scan all docs
5. **Version discipline** - Update version numbers, delete old versions
6. **Quality gates** - Each phase has approval checkpoints before proceeding

---

## 🎓 Quick Start Pattern

**User says**: "Make me a platformer game like Mario"

**Workflow**:
1. Switch to Lead Designer → Clarify requirements
2. Lead Designer → Module breakdown → Game outline → Project progress tracker
3. Switch to Designer → Write detailed system documents
4. Switch to Document Supervisor → Review all documents
5. Switch to Programmer → Setup RAG → Implement features (using RAG queries)
6. Switch to Tester → Verify implementation → Report bugs
7. Programmer fixes bugs → Tester verifies → Complete

---

## ⚠️ Critical Warnings Summary

**Designer**: Never write code - describe WHAT, not HOW

**Programmer & Tester**:
- 🚨 **NEVER scan all documents with Glob/Read**
- 🚨 **ALWAYS use RAG for targeted queries**
- 🚨 **Follow mandatory workflow**: Overview files → Keyword index → RAG query → Work

**Violation = Token waste + task failure**
