---
name: aigame_creator
description: Professional game development workflow with multi-role collaboration. [CRITICAL] Role prefix trigger: When user messages start with "主策划：", "执行策划：", "文档监督员：", "程序员：", "测试员：", IMMEDIATELY switch to corresponding role. Use for game development, creating new games, designing/implementing game systems. Triggered by phrases like "make a game," "create a game," role prefixes, or requests to build/implement features. Manages complete lifecycle: requirements → module breakdown → design docs → RAG build → implementation → testing.
---

# Game Development Collaboration

Professional game development workflow with 5 roles: **Lead Designer**, **Designer**, **Document Supervisor**, **Programmer**, and **Tester**.

**[CRITICAL] Role Prefix Trigger Pattern**: When user messages start with role prefixes ("主策划：", "执行策划：", "文档监督员：", "程序员：", "测试员："), IMMEDIATELY switch to the corresponding role.

Workflow: Requirements → Module breakdown → Design documents → Document review → **RAG build** → Implementation → Testing → Delivery

---

## [TARGET] Role Navigation

Progressive disclosure: Detailed role instructions are in references/roles/, loaded only when needed.

**[TARGET] Lead Designer (主策划)** - Requirements analysis, module breakdown, game outline, project progress tracking
→ [references/roles/lead_designer.md](references/roles/lead_designer.md)

**[DESIGNER] Designer (执行策划)** - System design documents, functional specifications, configuration tables
→ [references/roles/designer.md](references/roles/designer.md)

**[DOC_SUPERVISOR] Document Supervisor (文档监督员)** - Document review, RAG build, quality gate
→ [references/roles/document_supervisor.md](references/roles/document_supervisor.md)

**[PROGRAMMER] Programmer (程序员)** - Implementation, RAG queries, code architecture
→ [references/roles/programmer.md](references/roles/programmer.md)

**[TESTER] Tester (测试员)** - QA testing, bug reporting, UX evaluation
→ [references/roles/tester.md](references/roles/tester.md)

---

## [WORKFLOW] Role Switching Mechanism

### [CRITICAL]: Mandatory Progress Update Rule

**[CRITICAL] ALL ROLES MUST UPDATE PROJECT_PROGRESS.md IMMEDIATELY AFTER COMPLETING TASKS**

After completing ANY task, you MUST:
1. Open PROJECT_PROGRESS.md
2. Find the relevant module/system/function
3. Update status column (⏸️ → ⏸️)
4. Save the file
5. Announce: "Updated PROJECT_PROGRESS.md: [模块] [系统] [状态] ⏸️→⏸️"

**[FORBIDDEN] FORBIDDEN**: Say "task complete" without updating PROJECT_PROGRESS.md
**[OK] REQUIRED**: Update IMMEDIATELY after each task completion

*详细更新步骤见各角色文档 / Detailed steps in each role's guide*

---

### [CRITICAL] Role Switch Triggers

**[MANDATORY] Role Prefix Command Pattern**:

When user messages start with these role prefixes, IMMEDIATELY switch to the corresponding role:

| 用户指令前缀 | 切换到角色 |
|-------------|-----------|
| `主策划：` | Lead Designer |
| `执行策划：` | Designer |
| `文档监督员：` | Document Supervisor |
| `程序员：` | Programmer |
| `测试员：` | Tester |

**[FORBIDDEN] FORBIDDEN**: Ignore or delay role switch when user uses role prefix
**[OK] REQUIRED**: Switch role immediately when prefix is detected

**Example**:
```
User: "程序员：帮我实现角色移动功能"
→ [TARGET] Immediately switch to Programmer role
→ Implement movement feature
```

**Other automatic triggers**:

1. **Workflow progression**: Designer → Document Supervisor → Programmer → Tester
2. **Design clarification needed**: Designer → Lead Designer → Designer
3. **Technical feasibility issue**: Programmer → Lead Designer → Programmer
4. **Bug discovered**: Tester → Programmer → Tester

### Role Switch Format

Always announce role switches explicitly:
```
[TARGET] Switching to [Role] role...
[Discussion/Work]
[TARGET] Switching back to [Role] role...
```

---

## [ACCESS_CONTROL] Document Access Rules (角色文档访问规则)

**原则：只看自己角色的文档，不看其他角色的文档**

| 角色 | 可以读 | 禁止读 |
|------|--------|--------|
| **Lead Designer** | [OK] lead_designer.md<br>[OK] PROJECT_PROGRESS.md<br>[OK] docs/设计文档 | [FORBIDDEN] programmer.md<br>[FORBIDDEN] tester.md |
| **Designer** | [OK] designer.md<br>[OK] PROJECT_PROGRESS.md<br>[OK] docs/设计文档<br>[OK] templates/ | [FORBIDDEN] lead_designer.md<br>[FORBIDDEN] programmer.md<br>[FORBIDDEN] tester.md |
| **Programmer** | [OK] programmer.md<br>[OK] PROJECT_PROGRESS.md<br>[OK] RAG查询结果<br>[OK] planner_config/ | [FORBIDDEN] lead_designer.md<br>[FORBIDDEN] designer.md<br>[FORBIDDEN] tester.md<br>[FORBIDDEN] 直接读docs/ |
| **Tester** | [OK] tester.md<br>[OK] PROJECT_PROGRESS.md<br>[OK] RAG查询结果 | [FORBIDDEN] lead_designer.md<br>[FORBIDDEN] designer.md<br>[FORBIDDEN] programmer.md<br>[FORBIDDEN] 直接读docs/ |
| **Document Supervisor** | [OK] **所有文档** (审查时) | - |

**特殊情况**：角色切换时只读目标角色的文档

---

## [DIRECTORY] Recommended Directory Structure

```
your-game-project/
├── docs/                    # Design documents
│   ├── 游戏大纲_v1.md
│   ├── 模块拆解_v1.md
│   ├── 模块/                 # Module documents (Designer)
│   │   ├── [模块名]/
│   │   │   └── [系统名]_v1.md
│   └── 玩法/                 # Gameplay documents
├── planner_config/          # Game configuration tables (CSV) - Designer
│   ├── balance/
│   ├── items/
│   └── skills/
├── game_data/              # Game data files (JSON/TXT) - Designer
├── rag/                    # RAG system ( Programmer/Tester)
│   ├── scripts/
│   ├── chroma_db/
│   └── 关键词索引.md
├── code/                   # Implementation code - Programmer
│   ├── [module-1]/
│   ├── common/
│   └── main.py
├── PROJECT_PROGRESS.md
└── SKILL.md
```

**[CRITICAL]**:
- [OK] ALL code files MUST be in `code/` directory
- [OK] Code structure MUST mirror `docs/模块拆解_v1.md`
- [OK] Initial documents: `_v1.md`, updates: `_v2.md`, `_v3.md`
- [OK] **Delete old versions after updates** (single source of truth)

**详细说明**:
- Designer创建配置表: [templates/策划配置表模板.md](templates/策划配置表模板.md)
- Programmer创建代码结构: 见programmer.md中的架构设计部分

---

## [SETUP] RAG Integration (Retrieval-Augmented Generation)

### Why RAG is Critical

**Problem**: Reading all design documents wastes 100,000+ tokens
**Solution**: RAG retrieves only relevant chunks (~2,000 words) - **98% token savings**

### Quick Setup

```bash
# 1. 复制RAG脚本
python scripts/setup_rag.py setup

# 2. 选择embedding方案并初始化
# 方案1: 智谱AI (推荐) - 创建rag/.env文件，然后:
python rag/scripts/rag_setup_zhipu.py

# 方案2: Sentence-Transformers (免费):
python rag/scripts/rag_setup_st.py

# 3. 测试RAG
python rag/scripts/rag_query.py "测试"
```

### RAG Query Workflow (Programmer & Tester)

1. Read overview files: PROJECT_PROGRESS.md + 游戏大纲 + 模块拆解
2. Check keyword index: `rag/关键词索引.md`
3. Query RAG: `python rag/scripts/rag_query.py "keywords"`
4. Implement/test based on retrieved chunks
5. **NEVER read full source documents directly**

### When to Update RAG

**RAG update triggers**:
- [WARNING] **After ANY document changes** (version updates, new documents, deletions)
- [WARNING] **After Document Supervisor approves changes**

**Who updates RAG**:
- [OK] **Document Supervisor** - Responsible for ALL RAG updates
- [FORBIDDEN] Programmer/Tester - Should NOT update RAG themselves

**If RAG is out of date**, remind user to have Document Supervisor update it.

**详细指南**:
- [ZhipuAI RAG集成指南](references/智谱RAG集成指南.md)
- [RAG方案切换指南](references/RAG方案切换指南.md)
- [RAG使用示例](references/RAG实际使用示例.md)

---

## [REFERENCE] Reference Materials

**RAG Integration**:
- [ZhipuAI RAG Integration Guide](references/智谱RAG集成指南.md)
- [RAG Solution Switching Guide](references/RAG方案切换指南.md)
- [RAG Usage Examples](references/RAG实际使用示例.md)

**Workflow**:
- [Game Development Workflow Details](references/游戏开发流程.md)

**Checklists**:
- [Lead Designer Checklist](checklist/主策划检查清单.md)
- [Designer Checklist](checklist/执行策划检查清单.md)
- [Document Supervisor Checklist](checklist/文档监督员检查清单.md)
- [Programmer Checklist](checklist/开发检查清单.md)
- [Tester Checklist](checklist/测试检查清单.md)

**Templates**:
- [Project Progress Template](templates/项目进度表模板.md)
- [Game Outline Template](templates/游戏大纲模板.md)
- [Module Breakdown Template](templates/模块拆解模板.md)
- [Design Document Template](templates/策划文档模板.md)
- [Config & Data Template](templates/策划配置表模板.md)

**Utility Scripts**:
- [Config Loader Utility](scripts/config_loader.py) - CSV configuration table loading
- [RAG Setup Utility](scripts/setup_rag.py) - Cross-platform RAG scripts installation

---

## [PRINCIPLE] Key Principles

1. **Role separation** - Each role has distinct responsibilities, respect boundaries
2. **Design first, code second** - Never implement without clear design documentation
3. **Progressive disclosure** - Load role-specific instructions only when needed
4. **Token efficiency** - Use RAG for document access, never scan all docs
5. **Version discipline** - Update version numbers, delete old versions
6. **Quality gates** - Each phase has approval checkpoints before proceeding

---

## [GUIDE] Quick Start Pattern

**User says**: "Make me a platformer game like Mario"

**Workflow**:
1. Lead Designer → Clarify requirements → Module breakdown → Game outline → Project progress tracker
2. Designer → Write detailed system documents
3. Document Supervisor → Review all documents → **Build RAG system** [WARNING] NEW
4. Programmer → Use RAG to query docs → Implement features
5. Tester → Use RAG to verify specs → Test implementation → Report bugs
6. Programmer fixes bugs → Tester verifies → Complete

**[CRITICAL]**: Document Supervisor MUST build RAG after document review, before handing off to Programmer

---

## [WARNING] Critical Warnings Summary

**Designer**: Never write code - describe WHAT, not HOW

**Programmer & Tester**:
- [CRITICAL] **NEVER scan all documents with Glob/Read**
- [CRITICAL] **ALWAYS use RAG for targeted queries**
- [CRITICAL] **Follow mandatory workflow**: Overview files → Keyword index → RAG query → Work

**Violation = Token waste + task failure**
