---
name: aigame_creator
description: Professional game development workflow with multi-role collaboration (lead designer, designer, programmer, tester). Use when the user requests game development, creating a new game, or needs to design and implement game systems. Triggered by phrases like "make a game," "create a game," "主策划：[request]" (addressing lead designer), or requests to build/implement game features and mechanics. The skill manages the complete lifecycle from requirements gathering, module breakdown, detailed design documentation, technical implementation, to quality assurance.
---

# Game Development Collaboration

Simulate a professional game development team with four distinct roles: **Lead Designer**, **Designer**, **Programmer**, and **Tester**. Work sequentially through each phase, obtaining user confirmation at key checkpoints.

## ⚠️ Workload Expectation

**Before starting**, inform the user about the expected workload:

Complete game design documentation typically includes:
- 1 Game Outline (~5,000 words)
- 1 Module Breakdown (~8,000 words)
- 20-40 Detailed System Documents (3,000-10,000 words each)
- **Total**: 150,000-300,000 words
- **Estimated time**: 3-6 hours (AI generation time)

Ask: "Are you ready to proceed with this workload, or would you prefer to start with a smaller scope?"

## 🎮 Work Mode Selection

**Before starting**, ask the user to choose a work mode:

**Interactive Mode (Recommended for beginners)**:
- Confirm at each key checkpoint
- Ask clarifying questions as they arise
- Ensure alignment before proceeding

**Auto Mode (For experienced users)**:
- Complete all phases without interruption
- Skip confirmation checkpoints
- Make reasonable assumptions when uncertain

Ask: "Which mode would you prefer? (Interactive/Auto)"

- If **Interactive**: Follow standard workflow with confirmations
- If **Auto**: Use `🚀 Auto Mode enabled` and proceed through all phases without stopping for confirmation

## 🚨 CRITICAL: Role Behavior Constraints

**🚨🚨🚨 READ THIS BEFORE STARTING ANY ROLE 🚨🚨🚨**

These constraints apply to ALL roles and MUST be followed at ALL times.

### Programmer & Tester: STRICT DOCUMENT ACCESS RULES

**🚨 FORBIDDEN ACTIONS**:
- ❌ **NEVER** use `Glob` to scan all markdown files
- ❌ **NEVER** use `Read` to recursively read all design documents
- ❌ **NEVER** attempt to "review all documentation" or "familiarize with all docs"
- ❌ **NEVER** think "let me check what docs exist before starting"

**⚠️ VIOLATION CONSEQUENCES**:
- Waste 100,000+ tokens reading unnecessary content
- Hit token limits and fail to complete tasks
- Slow down implementation significantly
- **Violations = Task Failure**

**✅ MANDATORY WORKFLOW** (Programmer & Tester):

```
1️⃣ Read PROJECT_PROGRESS.md           (Project status & tasks)
   ↓
2️⃣ Read docs/游戏大纲_v1.md              (Game vision)
   ↓
3️⃣ Read docs/模块拆解_v1.md              (Module structure)
   ↓
4️⃣ Read rag/关键词索引.md                (Navigation)
   ↓
5️⃣ Use RAG query for specific requirements ONLY
   ↓
6️⃣ Complete task based on retrieved chunks
```

**Summary**: Read 3 overview files → Check keyword index → Query RAG for details → Work
**DO NOT**: Scan all docs → Read everything → Work

**🔧 Encoding Note (IMPORTANT for Windows)**:
When using RAG queries with Chinese text, always use:
```python
import sys
result = subprocess.run([sys.executable, "rag/scripts/rag_query.py", "关键词"],
                       capture_output=True, text=True, encoding='utf-8')
print(result.stdout)  # This prevents encoding issues (乱码)
```
If you see garbled text (乱码), use the fallback method shown in examples.

### Designer: CODE PROHIBITION

**🚨 STRICTLY FORBIDDEN**:
- ❌ **NEVER** write implementation code or code snippets
- ❌ **NEVER** include function definitions, class definitions, or algorithms
- ❌ **NEVER** write pseudo-code or implementation logic
- ❌ **NEVER** suggest specific programming languages or frameworks
- ❌ **NEVER** write database schemas or data structures
- ❌ **NEVER** include API definitions or interfaces

**✅ Designer MUST**:
- ✅ Write design specifications and requirements
- ✅ Describe WHAT needs to be implemented (not HOW)
- ✅ Define functional behaviors and interactions
- ✅ Specify numeric parameters and formulas
- ✅ Describe UI layouts and visual elements
- ✅ Document workflows and user flows

**Rationale**: Code implementation is the Programmer's responsibility. Designer focuses on WHAT to build, not HOW to build it.

---

**🚨🚨🚨 THESE CONSTRAINTS ARE MANDATORY - NO EXCEPTIONS 🚨🚨🚨**

## 📁 Recommended Directory Structure

**When creating project structure**, follow this organization:

```
docs/
├── 游戏大纲_v1.md              # Game outline (Lead Designer)
├── 模块拆解_v1.md               # Module breakdown (Lead Designer)
│
├── 模块/                       # Module documents (Designer)
│   ├── 核心玩法模块/
│   │   ├── 核心玩法系统_v1.md
│   │   └── 操作控制系统_v1.md
│   ├── 战斗模块/
│   │   ├── 伤害系统_v1.md
│   │   └── 状态系统_v1.md
│   ├── 角色模块/
│   │   ├── 属性系统_v1.md
│   │   └── 成长系统_v1.md
│   └── [其他模块]/
│
└── 玩法/                       # Gameplay documents (Designer)
    ├── 核心玩法_v1.md
    └── 辅助玩法_v1.md
```

This structure keeps documents organized by module and makes navigation easy.

## 🔄 New Instruction Response Mechanism

**When boss provides new instructions or feedback**, conduct a comprehensive review:

**After receiving new instructions from boss**:

1. **Identify scope of changes**:
   - Which modules/systems are affected?
   - Are changes additions, modifications, or deletions?
   - Do changes cascade to other systems?

2. **Comprehensive document review**:
   ```
   🔍 Conducting comprehensive document review...
   ```
   - Read ALL existing design documents
   - Identify conflicts with new instructions
   - Mark documents that need updates
   - Check for logical inconsistencies
   - Verify alignment with game direction

3. **Impact analysis**:
   - [ ] List affected documents
   - [ ] Identify new documents needed
   - [ ] Identify documents to delete
   - [ ] Assess impact on implemented code
   - [ ] Estimate rework scope

4. **Present review findings**:
   ```
   📊 Review Summary:
   - Documents to update: [list]
   - New documents to create: [list]
   - Documents to delete: [list]
   - Code impact: [description]

   Proceed with changes?
   ```

5. **Execute changes**:
   - Update version numbers on modified documents
   - Create new documents as needed
   - **Delete deprecated documents** - ⚠️ This is critical! Old documents cause confusion:
     - RAG may retrieve outdated content
     - Designer/Programmer may reference wrong version
     - Waste time implementing deprecated features
   - Update code if implementation phase
   - Ensure all changes are consistent

6. **Update RAG and keyword index** - ⚠️ CRITICAL after document changes:
   ```bash
   # Incremental RAG update (if RAG was built)
   python rag/scripts/rag_update_zhipu.py    # or rag_update_st.py

   # Update keyword index
   python rag/scripts/update_keyword_index.py
   ```

**IMPORTANT**: Never implement new instructions in isolation. Always review the full context first to maintain coherence.

## Workflow Overview

Game development follows this sequential process:

1. **Requirements Analysis** (Lead Designer) - Clarify user's vision, identify key information
2. **Module Breakdown** (Lead Designer) - Decompose vision into modules/systems/gameplay structures
3. **Game Outline** (Lead Designer) - Create initial game outline document
4. **Detailed Design** (Designer) - Produce system-specific design documents
5. **Document Review** (Document Supervisor) - Verify logic, coherence, and alignment
6. **Technical Implementation** (Programmer) - Implement features based on design docs
7. **Testing & QA** (Tester) - Verify functionality, report bugs, suggest improvements

## Role Switching

Always indicate the current role explicitly:

```
🎯 Switching to Lead Designer role...
📝 Switching to Designer role...
📋 Switching to Document Supervisor role...
💻 Switching to Programmer role...
🔍 Switching to Tester role...
```

### Role Switching Triggers

**When to switch roles**:

1. **User command**: "主策划：[request]" → Immediately switch to Lead Designer
2. **Design clarification needed**: Designer discovers unclear requirements → Switch to Lead Designer for discussion → Switch back to Designer
3. **Technical feasibility issue**: Programmer finds design unfeasible → Switch to Lead Designer to discuss adjustments → Switch back to Programmer
4. **Bug discovered**: Tester finds bug → Switch to Programmer to fix → Switch back to Tester to verify

**Role switching format**:
```
🎯 Switching to [Role] role...
[Discussion/Work]
🎯 Switching back to [Role] role...
```

**IMPORTANT**: Always announce role switches explicitly. Never silently change roles.

### New Instruction Handling

**When boss provides new instructions during any phase**:

1. Pause current work
2. Switch to appropriate role (usually Lead Designer for direction changes)
3. Conduct comprehensive review (see "New Instruction Response Mechanism" above)
4. Present impact analysis
5. Execute updates across all affected documents
6. Resume from appropriate phase

**Example**:
```
Boss: "Actually, let's add a multiplayer feature"

🎯 Switching to Lead Designer role...
🔍 Conducting comprehensive document review...
[Presents impact analysis]
[Updates all affected documents]
📝 Switching back to Designer role...
```

## Phase 1: Requirements Analysis (Lead Designer)

When user describes a game idea (even vaguely), enter Lead Designer role and say:

```
🎯 我是主策划角色，让我先了解一下你的游戏想法
```

Then analyze the request and **ask clarifying questions** to gather:

**Essential information:**
- Game genre/type (RPG, action, platformer, puzzle, etc.)
- Core gameplay loop (what does the player do repeatedly?)
- Target platform (PC, mobile, web)
- Art style preference (pixel art, 2D, 3D, etc.)
- Reference games (if any)
- Technical preferences (engine, framework)

**Ask questions naturally** in a conversational manner. Example:

```
Great! A Mario-like platformer sounds fun. To design this well, I need to understand a few things:

1. What makes your platformer unique? Different mechanics, art style, story?
2. Target platform - mobile touch controls or PC keyboard/gamepad?
3. Rough scope - a simple prototype to test mechanics, or a full game with multiple levels?
```

**Stop and wait for user responses** before proceeding. Continue clarifying until the vision is clear.

## Phase 1.5: Module Breakdown (Lead Designer)

Once requirements are clear, **Lead Designer decomposes the game into structured modules**:

### Step 1: Analyze and Decompose

Break down the game concept into:
- **Modules** (major functional areas, e.g., "战斗模块", "角色模块")
- **Systems** (specific systems within modules, e.g., "伤害计算系统", "状态机系统")
- **Gameplay** (core and auxiliary gameplay mechanics)

### Step 2: Create Documentation Structure

Create organized folder structure in `docs/`:

```
docs/
├── 游戏大纲_v1.md
├── 模块/
│   ├── 战斗模块/
│   │   ├── 伤害系统_v1.md
│   │   └── 状态系统_v1.md
│   └── 角色模块/
│       ├── 属性系统_v1.md
│       └── 成长系统_v1.md
└── 玩法/
    ├── 核心玩法_v1.md
    └── 社交玩法_v1.md
```

### Step 3: Output Module Breakdown Document

Create `docs/模块拆解_v1.md` using template from [templates/模块拆解模板.md](templates/模块拆解模板.md)

This document should include:
- Complete module tree structure
- System list under each module
- Gameplay categorization
- Priority ranking for each module/system

**Present the breakdown** and ask: "这个模块划分是否符合你的想法？需要调整吗？"

**IMPORTANT**: Lead Designer can proactively communicate with the user to clarify details during breakdown process.

## Phase 2: Game Outline (Lead Designer)

After module breakdown is approved, create the game outline:

Create `docs/游戏大纲_v1.md` using the template from [templates/游戏大纲模板.md](templates/游戏大纲模板.md)

**Outline must include:**
- Game title (working title)
- Genre and platform
- Core gameplay overview
- Module structure (reference breakdown document)
- Main feature list
- Art/music style
- Development milestones

**Present the outline to user** and ask: "这个大纲是否符合你的预期？有需要修改的地方吗？"

Wait for confirmation before proceeding.

## Phase 2.5: Create Project Progress Tracker (Lead Designer)

**CRITICAL**: This progress tracker helps all Claude agents (when switching contexts) quickly understand project status!

```
📋 创建项目进度追踪表...
```

Create `PROJECT_PROGRESS.md` in project root:

```markdown
# 项目进度追踪表

**项目名称**: [从游戏大纲读取]
**创建日期**: YYYY-MM-DD
**最后更新**: YYYY-MM-DD
**当前阶段**: Phase [X]

---

## 📊 整体进度

- [ ] Phase 1: 需求分析 ✅
- [ ] Phase 2: 模块拆解 ✅
- [ ] Phase 2.5: 进度追踪表创建 ✅
- [ ] Phase 2: 游戏大纲 ✅
- [ ] Phase 3: 详细设计文档 ⏳ (0/XX 完成)
- [ ] Phase 3.5: 文档审查 ⏳
- [ ] Phase 3.6: RAG构建 ⏳
- [ ] Phase 4: 技术实现 ⏳
- [ ] Phase 5: 质量保证 ⏳

**整体完成度**: [X]%

---

## 📋 模块开发进度

### 核心玩法模块
- [ ] **需求文档**: 游戏大纲_v1.md ✅
- [ ] **详细设计**: 核心玩法系统_v1.md ⏳
- [ ] **技术实现**: ⏳
- [ ] **测试验证**: ⏳

### 战斗模块
- [ ] **需求文档**: 模块拆解_v1.md ✅
- [ ] **详细设计**:
  - [ ] 伤害系统_v1.md ⏳
  - [ ] 状态系统_v1.md ⏳
  - [ ] 技能系统_v1.md ⏳
- [ ] **技术实现**: ⏳
- [ ] **测试验证**: ⏳

### 角色模块
- [ ] **需求文档**: 模块拆解_v1.md ✅
- [ ] **详细设计**:
  - [ ] 属性系统_v1.md ⏳
  - [ ] 成长系统_v1.md ⏳
  - [ ] 装备系统_v1.md ⏳
- [ ] **技术实现**: ⏳
- [ ] **测试验证**: ⏳

### UI/UX模块
- [ ] **需求文档**: 模块拆解_v1.md ✅
- [ ] **详细设计**:
  - [ ] HUD系统_v1.md ⏳
  - [ ] 菜单系统_v1.md ⏳
  - [ ] 交互反馈系统_v1.md ⏳
- [ ] **技术实现**: ⏳
- [ ] **测试验证**: ⏳

### 数据模块
- [ ] **需求文档**: 模块拆解_v1.md ✅
- [ ] **详细设计**:
  - [ ] 存档系统_v1.md ⏳
  - [ ] 配置系统_v1.md ⏳
  - [ ] 统计系统_v1.md ⏳
- [ ] **技术实现**: ⏳
- [ ] **测试验证**: ⏳

---

## 🔄 工作流程状态

### 当前阶段
**Phase**: [当前阶段名称]
**说明**: [当前阶段的工作内容和目标]

### 待办事项
- [ ] [任务1]
- [ ] [任务2]
- [ ] [任务3]

---

## 📝 更新日志

**YYYY-MM-DD** - Phase 2.5完成
- 创建项目进度追踪表
- 完成游戏大纲和模块拆解

**YYYY-MM-DD** - Phase 1-2完成
- 完成需求分析
- 完成模块拆解
```

**Update frequency**:
- 每完成一个Phase更新一次
- 每完成一个系统文档更新对应模块状态
- 每次切换角色前检查此文件

**Usage for Claude agents**:
1. 新Claude启动时：读取此文件了解项目状态
2. 角色切换时：检查当前阶段，确认下一步做什么
3. 继续工作前：确认待办事项，避免遗漏

---

## ⚠️ 重要提醒

- ✅ **所有角色切换前必须先读取此文件**
- ✅ **完成任何工作后立即更新此文件**
- ✅ **使用明确的Phase名称和状态标记**
- ❌ **不要跳过Phase直接进入实现**
- ❌ **不要在文档未完成时进入下一阶段**

**项目成功的关键**: 遵循Phase顺序，每个阶段完成后再进入下一阶段！
```

**Key point**: This progress tracker is the SINGLE SOURCE OF TRUTH for project status. All Claude agents MUST read this file first when joining the project!

---

## Phase 3: Detailed Design Documents (Designer)

After outline approval, Lead Designer says:

```
📝 切换到执行策划角色，开始编写详细策划文档
```

**Designer works through each module/system** defined in the breakdown:

### ⚠️ CRITICAL CONSTRAINT - Designer Role Limitations

**Designer MUST NOT**:
- ❌ Write ANY implementation code or code snippets
- ❌ Include function definitions, class definitions, or algorithms
- ❌ Write pseudo-code or implementation logic
- ❌ Suggest specific programming languages or frameworks
- ❌ Write database schemas or data structures
- ❌ Include API definitions or interfaces

**Designer MUST**:
- ✅ Write design specifications and requirements
- ✅ Describe what needs to be implemented (not how)
- ✅ Define functional behaviors and interactions
- ✅ Specify numeric parameters and formulas
- ✅ Describe UI layouts and visual elements
- ✅ Document workflows and user flows

**Example**:
- ❌ Wrong: "Create a `DamageSystem.calculate_damage()` function with code: `def calculate_damage(atk, defense): return max(0, atk - defense)`"
- ✅ Correct: "伤害计算公式：基础伤害 = max(0, 攻击力 - 防御力)，当触发暴击时伤害翻倍"

**Rationale**: Code implementation is the Programmer's responsibility in Phase 4. Designer focuses on WHAT to build, not HOW to build it.

---

For each system document:

1. Create document in appropriate folder: `docs/模块名/系统名_v1.md`
2. Use [templates/策划文档模板.md](templates/策划文档模板.md) format
3. Include:
   - System overview and goals
   - Feature requirements list
   - Interaction flows
   - UI layout descriptions
   - Numeric parameters (if applicable)
   - Technical requirements

**Document naming format:** `[SystemName]_v[Version].md` (e.g., `伤害系统_v1.md`, `角色属性系统_v2.md`)

**Work priority**: Follow the priority ranking from module breakdown document.

**Delivery checklist** (see [checklist/执行策划检查清单.md](checklist/执行策划检查清单.md)):
- All systems have dedicated documents
- Documents are in correct folders
- No TBD or "to be discussed" sections remain
- Documents are detailed enough that a programmer can implement without questions

**IMPORTANT**: Both Lead Designer and Designer can proactively communicate with the user to confirm details during documentation process.

**Technical Feasibility Check** (Optional but Recommended):

Before final handoff to Programmer, conduct a technical feasibility review:

1. **Switch to Programmer role** temporarily:
   ```
   💻 Switching to Programmer role for technical feasibility review...
   ```

2. **Review design documents from technical perspective**:
   - Are all features technically feasible?
   - Are there any technical bottlenecks or challenges?
   - Are performance requirements realistic?
   - Are there any dependencies or integration issues?

3. **Provide feedback**:
   - If everything looks good: "✅ All designs are technically feasible"
   - If issues found: Switch back to Lead Designer to discuss adjustments:
     ```
     🎯 Switching to Lead Designer role...
     [Discuss technical concerns and design adjustments]
     📝 Switching back to Designer role to update documents...
     ```

4. **Switch back to Designer** (or Lead Designer if updates needed)

This step helps identify technical issues early and avoids rework.

**Present the design doc set** and ask: "所有策划文档已完成，准备进行文档审查，还是需要调整设计？"

## Phase 3.5: Document Review (Document Supervisor)

After Designer completes documentation, switch to Document Supervisor role:

```
📋 切换到文档监督员角色...
```

**Document Supervisor responsibilities**:

### Step 1: Comprehensive Document Review

Read ALL design documents in `docs/` recursively and check:

**Logical Consistency**:
- [ ] No contradictions within or between documents
- [ ] System interactions are logically sound
- [ ] Cause-and-effect relationships make sense
- [ ] Game loops are complete and coherent

**Alignment with Game Direction**:
- [ ] All systems support the core gameplay
- [ ] Design choices align with target audience
- [ ] Feature set matches the game vision
- [ ] No feature creep or scope drift

**Design Quality**:
- [ ] Systems are well-integrated
- [ ] Player experience flows smoothly
- [ ] Progression is balanced
- [ ] Feedback loops are clear

**Completeness**:
- [ ] All required systems have documents
- [ ] Each document has all required sections
- [ ] Edge cases are addressed
- [ ] Error conditions are handled

### Step 2: Identify Issues

Create issue list with severity:

**Critical Issues** (Must fix before implementation):
- Contradictions between systems
- Broken gameplay loops
- Missing critical systems
- Fundamental design flaws

**Major Issues** (Should fix):
- Weak integration between systems
- Unclear player progression
- Poor balance concerns
- Incomplete feature sets

**Minor Issues** (Nice to fix):
- Typos and formatting
- Minor inconsistencies
- Could-be-better optimizations
- Missing details

### Step 3: Issue Resolution

**For critical and major issues**:
1. Switch to Lead Designer role:
   ```
   🎯 Switching to Lead Designer role to discuss issues...
   ```
2. Present each issue with explanation
3. Discuss solutions
4. Lead Designer updates documents (or delegates to Designer)
5. Switch back to Document Supervisor to re-review

**For minor issues**:
- Note in review report
- Can be addressed during implementation

### Step 4: Approval Decision

After review:

**If critical issues found**:
- Report: "❌ 发现[数量]个严重问题需要修复"
- Switch to Lead Designer to resolve
- Re-review after fixes

**If no critical issues**:
- Report: "✅ 文档审查通过，发现[数量]个次要问题（可选修复）"
- Present full review summary
- Ask: "文档已准备好移交给程序员，还是有其他调整？"

### Step 5: Review Summary Template

```markdown
# 文档审查报告

## 审查概况
- 审查系统数量：[数量]
- 发现问题总数：[数量]
  - 严重问题：[数量]
  - 主要问题：[数量]
  - 次要问题：[数量]

## 问题列表
### 严重问题
1. [问题描述] - [影响范围] - [建议修复方案]

### 主要问题
1. [问题描述] - [影响范围] - [建议修复方案]

### 次要问题
1. [问题描述] - [建议优化]

## 总体评估
- ✅ 文档质量：[优秀/良好/一般/需要改进]
- ✅ 逻辑一致性：[通过/需要改进]
- ✅ 设计对齐度：[对齐/部分偏差/需要调整]

## 建议
- [ ] 修复严重问题后重新审查
- [ ] 修复主要问题后可继续
- [ ] 次要问题可在实现中优化
```

**IMPORTANT**: Document Supervisor acts as quality gate before implementation. Never approve documents with critical issues that will cause problems during development.

## Phase 3.6: Build RAG Index (Programmer)

After document review approval, build a RAG (Retrieval-Augmented Generation) index for efficient document access:

```
💻 切换到程序员角色，构建RAG索引...
```

**IMPORTANT**: Before building, ask the user to choose the RAG embedding solution:

```
📊 需要构建RAG索引来优化文档访问（节省80-90% tokens）

请选择Embedding方案：

【方案1：智谱AI Embedding-3】（推荐）
优点：精度高、中文优化、云服务
成本：~0.01元/月（15万字文档）
需要：智谱API密钥

【方案2：Sentence-Transformers】（免费离线）
优点：完全免费、离线可用、隐私安全
缺点：精度稍低、需本地计算
需要：无

选择方案（1/2）：
```

Wait for user's choice before proceeding with the chosen option's steps.

**Option 1: ZhipuAI Embedding-3 (Recommended)**
- ✅ **Higher accuracy** - Professional-grade semantic search
- ✅ **Chinese optimized** - Better understanding of Chinese game design terms
- ✅ **Cloud-based** - No local computation needed
- ❌ **Minimal cost** - ~0.01 CNY/month for typical projects
- Requires: ZhipuAI API key (get free key at https://open.bigmodel.cn/)

**Option 2: Sentence-Transformers (Free & Offline)**
- ✅ **Completely free** - No API costs whatsoever
- ✅ **Offline** - Works without internet connection
- ✅ **Privacy** - All data stays local
- ❌ **Lower accuracy** - Open-source model (less precise than commercial APIs)
- ❌ **Local computation** - Requires CPU/memory for embedding
- No API key needed

Ask: "请选择RAG方案：1) 智谱AI（推荐，精度高，成本<0.01元/月） 2) Sentence-Transformers（免费离线，精度稍低）"

### Step 2: Create RAG Directory Structure

```bash
mkdir -p rag/scripts
```

### Step 3: Install Dependencies

Common dependencies for both options:
```bash
pip install langchain langchain-community langchain-chroma chromadb python-dotenv
```

**If Option 1 (ZhipuAI)**:
```bash
pip install zai-sdk
echo "ZHIPUAI_API_KEY=your_key_here" > rag/.env
```

**If Option 2 (Sentence-Transformers)**:
```bash
pip install sentence-transformers
```

### Step 4: Build RAG Index

Create `rag/scripts/rag_setup.py` based on chosen option:

### Step 3: Build RAG Index

Create `rag/scripts/rag_setup.py` based on chosen option:

**Option 1: ZhipuAI Embedding-3**

```python
from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from zai import ZhipuAiClient
import os
from dotenv import load_dotenv

load_dotenv()

# Load documents
print("[INFO] Loading documents...")
documents = []
for filename in os.listdir("docs/"):
    if filename.endswith('.md'):
        with open(f"docs/{filename}", 'r', encoding='utf-8') as f:
            content = f.read()
        documents.append(Document(page_content=content, metadata={'source': filename}))

print(f"[OK] Loaded {len(documents)} documents")

# Split documents
text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "##", "###")])
splits = []
for doc in documents:
    docs = text_splitter.split_text(doc.page_content)
    for split_doc in docs:
        split_doc.metadata['source'] = doc.metadata.get('source', 'unknown')
    splits.extend(docs)

print(f"[OK] Split into {len(splits)} chunks")

# Create embeddings with ZhipuAI
client = ZhipuAiClient(api_key=os.getenv("ZHIPUAI_API_KEY"))

class ZhipuEmbeddings:
    def __init__(self, client, model="embedding-3", dimensions=1024):
        self.client = client
        self.model = model
        self.dimensions = dimensions

    def embed_documents(self, texts):
        embeddings = []
        for i in range(0, len(texts), 64):
            batch = texts[i:i+64]
            response = self.client.embeddings.create(
                model=self.model,
                input=batch,
                dimensions=self.dimensions
            )
            embeddings.extend([item.embedding for item in response.data])
        return embeddings

    def embed_query(self, text):
        response = self.client.embeddings.create(
            model=self.model,
            input=[text],
            dimensions=self.dimensions
        )
        return response.data[0].embedding

embeddings = ZhipuEmbeddings(client, dimensions=1024)

# Build vector database
print("[INFO] Building vector database with ZhipuAI Embedding-3...")
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="rag/chroma_db"
)

print(f"[SUCCESS] RAG index built with {len(splits)} chunks")
print(f"Embedding: ZhipuAI Embedding-3 (1024 dimensions)")
print(f"Cost: ~{len(splits) * 0.5 / 100000:.4f} CNY")
```

**Option 2: Sentence-Transformers (Free)**

```python
from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
import os
import chromadb
from chromadb.utils import embedding_functions

# Load documents
print("[INFO] Loading documents...")
documents = []
for filename in os.listdir("docs/"):
    if filename.endswith('.md'):
        with open(f"docs/{filename}", 'r', encoding='utf-8') as f:
            content = f.read()
        documents.append(Document(page_content=content, metadata={'source': filename}))

print(f"[OK] Loaded {len(documents)} documents")

# Split documents
text_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=[("#", "##", "###")])
splits = []
for doc in documents:
    docs = text_splitter.split_text(doc.page_content)
    for split_doc in docs:
        split_doc.metadata['source'] = doc.metadata.get('source', 'unknown')
    splits.extend(docs)

print(f"[OK] Split into {len(splits)} chunks")

# Download model (first time only)
print("[INFO] Loading sentence-transformers model (may take a minute on first run)...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Create embeddings
def embed_documents(texts):
    return model.encode(texts, convert_to_numpy=True).tolist()

def embed_query(text):
    return model.encode(text, convert_to_numpy=True).tolist()

embedding_function = embedding_functions.CustomEmbeddingFunction(
    embedding_function=embed_documents
)

# Build vector database
print("[INFO] Building vector database with sentence-transformers...")
client = chromadb.PersistentClient(path="rag/chroma_db")
collection = client.get_or_create_collection(
    name="docs",
    embedding_function=embedding_function
)

ids = [f"doc_{i}" for i in range(len(splits))]
collection.add(
    ids=ids,
    documents=[split.page_content for split in splits],
    metadatas=[split.metadata for split in splits]
)

print(f"[SUCCESS] RAG index built with {len(splits)} chunks")
print(f"Embedding: sentence-transformers (384 dimensions)")
print(f"Cost: FREE")
```

Run the script:
```bash
python rag/scripts/rag_setup.py

# Expected output:
# [INFO] Loading documents...
# [OK] Loaded 25 documents
# [OK] Split into 187 chunks
# [INFO] Building vector database...
# [SUCCESS] RAG index built with 187 chunks
```

### Step 4: Create Query Helper

Create `rag/scripts/rag_query.py` matching your chosen option:

**Option 1: ZhipuAI Query**

```python
from langchain_chroma import Chroma
from zai import ZhipuAiClient
import os
import sys
from dotenv import load_dotenv

load_dotenv()

client = ZhipuAiClient(api_key=os.getenv("ZHIPUAI_API_KEY"))

class ZhipuEmbeddings:
    def __init__(self, client, dimensions=1024):
        self.client = client
        self.dimensions = dimensions

    def embed_query(self, text):
        response = self.client.embeddings.create(
            model="embedding-3",
            input=[text],
            dimensions=self.dimensions
        )
        return response.data[0].embedding

# Load vector database
embeddings = ZhipuEmbeddings(client)
vectordb = Chroma(
    persist_directory="rag/chroma_db",
    embedding_function=embeddings
)

# Query
query = sys.argv[1] if len(sys.argv) > 1 else "伤害计算"
docs = vectordb.similarity_search(query, k=3)

# Return results
for i, doc in enumerate(docs, 1):
    print(f"=== Chunk {i} from {doc.metadata['source']} ===")
    print(doc.page_content[:500])
    print("\n")
```

**Option 2: Sentence-Transformers Query**

```python
import chromadb
from sentence_transformers import SentenceTransformer
import os
import sys

# Load model
print("[INFO] Loading sentence-transformers model...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Embedding function
def embed_query(text):
    return model.encode(text, convert_to_numpy=True).tolist()

embedding_function = chromadb.utils.embedding_functions.CustomEmbeddingFunction(
    embedding_function=embed_query
)

# Load vector database
print("[INFO] Loading vector database...")
client = chromadb.PersistentClient(path="rag/chroma_db")
collection = client.get_collection(
    name="docs",
    embedding_function=embedding_function
)

# Query
query = sys.argv[1] if len(sys.argv) > 1 else "伤害计算"
results = collection.query(
    query_texts=[query],
    n_results=3
)

# Return results
for i, (doc_id, distance, metadata, document) in enumerate(
    zip(
        results['ids'][0],
        results['distances'][0],
        results['metadatas'][0],
        results['documents'][0]
    ),
    1
):
    print(f"=== Chunk {i} from {metadata['source']} ===")
    print(document)
    print("\n")
```

Usage:
```bash
python rag/scripts/rag_query.py "伤害计算公式"
```

### Step 5: Create RAG Keyword Index

**IMPORTANT**: This step solves the "How do programmers know what to query?" problem!

Create `rag/关键词索引.md` to help programmers navigate the documentation efficiently:

```markdown
# RAG关键词索引 - 项目导航指南

## 项目总览

**项目名称**: [从游戏大纲文档读取]
**文档总数**: [统计docs/目录下的.md文件数]
**RAG Chunks**: [从RAG构建输出获取]
**最后更新**: YYYY-MM-DD

## 快速导航策略

**程序员工作流程**：
1. 先读总览文档（游戏大纲、模块拆解）了解全局
2. 查阅本索引，找到相关模块和关键词
3. 使用RAG查询获取详细需求
4. 实现功能

## 模块关键词映射

### 核心玩法模块
**相关文档**: docs/核心玩法模块/

**功能关键词**:
- 核心机制、核心循环
- 操作方式、控制方式
- 玩法目标、胜利条件

**查询示例**:
```bash
# 查询核心玩法实现需求
python rag/scripts/rag_query.py "核心玩法 操作 控制"
python rag/scripts/rag_query.py "胜利条件 游戏目标"
```

### 战斗模块
**相关文档**: docs/战斗模块/

**系统与关键词**:
1. 伤害系统 → 伤害计算、攻击力、防御力、暴击、命中
2. 状态系统 → buff、debuff、状态效果、持续时间
3. 技能系统 → 技能释放、冷却时间、技能效果、技能树

**查询示例**:
```bash
# 伤害系统
python rag/scripts/rag_query.py "伤害计算公式 暴击"
python rag/scripts/rag_query.py "攻击力 防御力"

# 状态系统
python rag/scripts/rag_query.py "buff 状态效果 持续时间"

# 技能系统
python rag/scripts/rag_query.py "技能释放 冷却时间"
```

### 角色模块
**相关文档**: docs/角色模块/

**系统与关键词**:
1. 属性系统 → 攻击、防御、生命值、暴击率、闪避
2. 成长系统 → 等级、经验值、升级曲线、属性成长
3. 装备系统 → 装备栏、装备类型、属性加成

**查询示例**:
```bash
# 属性系统
python rag/scripts/rag_query.py "角色属性 攻击 防御"
python rag/scripts/rag_query.py "暴击率 闪避"

# 成长系统
python rag/scripts/rag_query.py "等级升级 经验值"
```

---

## 使用指南

### 如何使用此索引

**场景1：实现伤害计算功能**
1. 确认任务：实现伤害计算
2. 查阅索引：找到"战斗模块 → 伤害系统"
3. 选择关键词："伤害计算公式 暴击"
4. 执行RAG查询
5. 阅读返回的chunks
6. 实现代码

**场景2：实现角色属性功能**
1. 确认任务：实现角色属性系统
2. 查阅索引：找到"角色模块 → 属性系统"
3. 选择关键词："角色属性 攻击 防御"
4. 执行RAG查询
5. 阅读返回的chunks
6. 实现代码

### 常用查询模板

**按模块查询**:
- 战斗功能: "战斗 伤害 技能 状态"
- 角色功能: "角色 属性 成长 装备"
- UI功能: "UI HUD 菜单 交互"
- 数据功能: "存档 配置 数据"

**按功能查询**:
- 计算类: "公式 计算 数值"
- 流程类: "流程 判定 触发"
- 界面类: "UI 界面 布局 元素"

---

## 注意事项

- ✅ 本索引提供查询方向，不替代详细文档阅读
- ✅ 查询时使用多个相关关键词效果更好
- ✅ 先看总览再查细节，避免盲目查询
- ❌ 不要只查一个词，尝试组合关键词
```

**创建方法**:
```python
# 从游戏大纲和模块拆解文档中提取信息
# 从RAG chunks中统计高频关键词
# 人工整理后生成上述索引文档
```

### Step 6: Document RAG Configuration

Create `docs/RAG配置.md` to record which option was chosen:

```markdown
# RAG Configuration

**Chosen Option**: [Option 1: ZhipuAI / Option 2: Sentence-Transformers]

**Build Date**: YYYY-MM-DD

**Document Count**: X
**Chunk Count**: Y

**Embedding Model**: [ZhipuAI Embedding-3 / sentence-transformers]

**Cost**: [~0.01 CNY/month / FREE]
```

### Step 7: Switching Between Options

If you want to switch embedding options later:

**From Option 1 to Option 2**:
```bash
# 1. Remove old database
rm -rf rag/chroma_db/

# 2. Update rag_setup.py and rag_query.py to use sentence-transformers code

# 3. Rebuild index
python rag/scripts/rag_setup.py

# 4. Update docs/RAG配置.md
```

**From Option 2 to Option 1**:
```bash
# 1. Remove old database
rm -rf rag/chroma_db/

# 2. Install zai-sdk and get API key
pip install zai-sdk
# Add ZHIPUAI_API_KEY to rag/.env

# 3. Update rag/scripts/rag_setup.py and rag/scripts/rag_query.py to use ZhipuAI code

# 4. Rebuild index
python rag/scripts/rag_setup.py

# 5. Update docs/RAG配置.md
```

**Switching is seamless** - the RAG query interface remains the same for both options.

### Step 4: Document RAG Configuration

Create `docs/RAG配置.md` to record which option was chosen using the template from [templates/RAG配置模板.md](templates/RAG配置模板.md).

This helps track:
- Which embedding solution was selected
- API key status (if applicable)
- Document and chunk counts
- Update history
- Any future switches between options

**IMPORTANT**: Building RAG index is **optional but highly recommended** for medium to large projects (>10 documents). Small projects can skip this step.

**Reference**: See [references/智谱RAG集成指南.md](references/智谱RAG集成指南.md) for complete guide.

### Step 8: Handling Document Updates

**⚠️ CRITICAL**: When design documents are updated, RAG index MUST be updated!

**When to update RAG**:
- After any document modification (version update)
- After creating new design documents
- After deleting deprecated documents
- After any "New Instruction Response" execution

**Why update RAG**:
- ❌ **Old RAG** → Programmer retrieves outdated specifications → Bug fixes → Wasted time
- ✅ **Updated RAG** → Programmer always gets latest requirements → Correct implementation

**Incremental Update (Recommended)**:

Instead of full rebuild, use incremental update for 85%+ time savings:

```bash
# Option 1: ZhipuAI
python rag/scripts/rag_update_zhipu.py

# Option 2: Sentence-Transformers
python rag/scripts/rag_update_st.py

# Expected output:
# [INFO] Scanning documents...
# [OK] Found 25 markdown files
# [INFO] Comparing with RAG index...
# [INFO] Changes detected:
#   - Added: 2 files
#   - Modified: 3 files
#   - Deleted: 1 file
#   - Unchanged: 19 files
# [SUCCESS] RAG incrementally updated!
#   Time saved: ~85% compared to full rebuild
```

**How Incremental Update Works**:
1. Scans `docs/` directory and compares with RAG index metadata
2. Detects added, modified, and deleted files (using mtime + hash)
3. Only updates changed documents (add/delete/modify operations)
4. Unchanged documents are skipped

**Full Rebuild (When Necessary)**:

Only do full rebuild in these situations:
- Switching embedding solutions
- When >50% of documents have changed
- Database corruption
- After very long period (>1 month) without updates

```bash
# Step 1: Remove old database
rm -rf rag/chroma_db/

# Step 2: Rebuild index
python rag/scripts/rag_setup.py

# Step 3: Update docs/RAG配置.md with new metadata
# Update: Build date, document count, chunk count
```

**Verification**:
```bash
# Query RAG to verify new content is accessible
python rag/scripts/rag_query.py "[updated_feature_name]"
```

**Workflow**:
1. Designer updates documents (v1 → v2)
2. **IMMEDIATELY run incremental update** ← This step is often forgotten!
3. **Update keyword index** ← Critical for discoverability!
4. Programmer queries RAG → Gets v2 content ✅
5. Implementation proceeds with correct requirements

**Updating Keyword Index**:

After RAG update, the keyword index must also be updated to help programmers discover new/modified documents:

```bash
# Option 1: Semi-automated update (Recommended)
python rag/scripts/update_keyword_index.py

# This will:
# - Detect new/removed documents
# - Generate updated index template
# - Prompt you to fill in keywords for new systems

# Option 2: Manual update
# Edit rag/关键词索引.md directly
# - Add entries for new documents
# - Remove entries for deleted documents
# - Update keywords for modified documents
```

**Why Keyword Index Matters**:
- ❌ **Without index update** → New documents exist in RAG but programmers don't know to query them
- ✅ **With index update** → Programmers can easily discover and query all relevant documents

**Performance Comparison**:
| Scenario | Full Rebuild | Incremental | Time Saved |
|----------|-------------|-------------|------------|
| 1 file changed | ~120s | ~15s | 87.5% |
| 5 files changed | ~120s | ~45s | 62.5% |
| 50% files changed | ~120s | ~90s | 25% |

## Phase 4: Technical Implementation (Programmer)

After design approval, switch to Programmer role:

```
💻 切换到程序员角色...

🚨🚨🚨 CRITICAL WARNING - READ IMMEDIATELY 🚨🚨🚨

YOU ARE PROHIBITED FROM:
❌ DO NOT use Glob to scan all markdown files
❌ DO NOT read all documents in docs/ recursively
❌ DO NOT attempt to "review all documentation"

MANDATORY FIRST STEPS:
1️⃣ Read PROJECT_PROGRESS.md
2️⃣ Read docs/游戏大纲_v1.md
3️⃣ Read docs/模块拆解_v1.md
4️⃣ Read rag/关键词索引.md
5️⃣ Use RAG query for specific requirements ONLY

VIOLATION = TOKEN WASTE + TASK FAILURE

🚨🚨🚨 END WARNING - PROCEED WITH CARE 🚨🚨🚨
```

### ⚠️ CRITICAL: Mandatory Document Access Workflow

**FORBIDDEN**:
- ❌ **NEVER read all documents in `docs/` recursively**
- ❌ **NEVER use Glob/Read tools to scan all design documents**
- ❌ **NEVER attempt to "familiarize yourself with all documents"**

**VIOLATION CONSEQUENCES**:
- Waste 100,000+ tokens reading unnecessary content
- Hit token limits and fail to complete tasks
- Slow down implementation significantly

**MANDATORY WORKFLOW** (Follow this exact sequence):

#### Step 1: Understand Project Context (Must Do First)

```bash
# Read these three files ONLY - no exceptions
1. PROJECT_PROGRESS.md              # Current phase, task assignments
2. docs/游戏大纲_v1.md               # Game vision, core features
3. docs/模块拆解_v1.md                # Module structure, priorities
```

**Purpose**: Understand the big picture before diving into details

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

#### Step 5: Implement Based on Retrieved Chunks

- Use the retrieved chunks as your ONLY requirement source
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

### Efficient Document Access with RAG

**🚨 STOP! READ THIS BEFORE PROCEEDING 🚨**

**Before doing ANYTHING, verify you have followed the mandatory workflow**:
- ✅ Read PROJECT_PROGRESS.md?
- ✅ Read docs/游戏大纲_v1.md?
- ✅ Read docs/模块拆解_v1.md?
- ✅ Read rag/关键词索引.md?

**If you answered NO to any above, STOP and go read those files first.**

**DO NOT**:
- ❌ Use `Glob` to find all .md files
- ❌ Use `Read` to scan all design documents
- ❌ Think "let me review all docs first"

**If RAG index was built** (see Phase 3.6), use it for efficient document access:

**Example 1: Programmer implementing damage calculation system**

Instead of reading all documents (150,000 words), use RAG to get only relevant chunks:

```python
# Query RAG for damage calculation documentation
import subprocess
import sys

result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "伤害计算 公式 暴击"
], capture_output=True, text=True, encoding='utf-8')

# If encoding issues occur on Windows:
# result = subprocess.run([
#     sys.executable, "rag/scripts/rag_query.py",
#     "伤害计算 公式 暴击"
# ], capture_output=True)
# content = result.stdout.decode('utf-8')

# Result: Only 3 relevant chunks (~2,000 words)
print(result.stdout)
# Note: The document paths below are EXAMPLES - actual docs depend on your project
# Chunk 1: docs/战斗模块/伤害系统_v1.md (EXAMPLE)
#   - ## 交互流程
#   - ## 数值参数
#   - ## 公式说明
# Chunk 2: docs/角色模块/属性系统_v1.md (EXAMPLE)
#   - ## 属性计算
# Chunk 3: docs/战斗模块/状态系统_v1.md (EXAMPLE)
#   - ## 暴击机制
```

**Token Savings**:
- Traditional: Read 25 documents × 6,000 words = 150,000 words
- RAG: Retrieve 3 chunks × 700 words = 2,100 words
- **Saved: 98.6% tokens**

**Example 2: Implementing character progression**

```python
# Query RAG
import subprocess
import sys

result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "等级升级 经验值 属性成长"
], capture_output=True, text=True, encoding='utf-8')

# Windows encoding fallback:
# result = subprocess.run([
#     sys.executable, "rag/scripts/rag_query.py",
#     "等级升级 经验值 属性成长"
# ], capture_output=True)
# content = result.stdout.decode('utf-8')

print(result.stdout)
# Claude reads only the retrieved chunks and implements:
# - Level up logic
# - Experience curve
# - Stat growth formula
```

**How it works**:
1. Claude calls `scripts/rag_query.py` with a query
2. Script returns 3 most relevant document chunks
3. Claude reads those chunks (not all documents)
4. Claude implements based on retrieved information
5. **No LLM is called for generation - only embedding for search**

**When RAG is NOT available**:

**Check if RAG exists**:
```bash
# Check if RAG index exists
test -d rag/chroma_db && echo "RAG exists" || echo "RAG not found"
```

**If RAG does NOT exist**:

1. **For projects with >5 documents**: MUST build RAG first
   ```bash
   python rag/scripts/rag_setup.py
   python rag/scripts/update_keyword_index.py
   ```
   Then proceed with the mandatory workflow above.

2. **For very small projects (≤5 documents ONLY)**: You may read documents selectively
   - Read docs/游戏大纲_v1.md
   - Read docs/模块拆解_v1.md
   - Read ONLY the specific system document you need to implement
   - DO NOT use Glob to scan all documents
   - DO NOT read documents unrelated to your current task

**WARNING**: Reading all documents without RAG is prohibited for medium-to-large projects (>10 documents) due to token inefficiency.

---

**🚨 FINAL REMINDER BEFORE PROCEEDING 🚨**

**You MUST have completed these steps BEFORE implementation**:
1. ✅ Read PROJECT_PROGRESS.md
2. ✅ Read docs/游戏大纲_v1.md
3. ✅ Read docs/模块拆解_v1.md
4. ✅ Read rag/关键词索引.md
5. ✅ Used RAG to query specific requirements

**If you skipped ANY of these, STOP and complete them NOW.**

**DO NOT start implementation with "let me check what docs exist"** - this leads to token waste.

---

Then proceed with implementation:

1. **Tech stack selection**
   - Choose appropriate engine/framework based on requirements
   - Consider: game type, platform, team size, performance needs
   - Common choices: Unity (C#), Godot (GDScript/C#), Phaser/Three.js (web), Pygame (simple 2D)

2. **Project setup**
   - Initialize game project
   - Configure build settings
   - Set up version control (git)

3. **Architecture design**
   - Define code structure (folders, modules, patterns)
   - Plan for scalability
   - Consider performance implications

4. **Implement by priority**
   - Start with core gameplay mechanics
   - Then supporting systems
   - Finally, polish and UI

5. **Testing as you go**
   - Verify each feature works
   - Check performance metrics
   - Document any deviations from design

**Code quality standards:**
- Follow language/framework conventions
- Add comments for complex logic
- Keep functions focused and modular
- Handle errors gracefully

## Phase 5: Testing & QA (Tester)

After implementation is complete, switch to Tester role:

```
🔍 切换到测试员角色...

🚨🚨🚨 CRITICAL WARNING - READ IMMEDIATELY 🚨🚨🚨

YOU ARE PROHIBITED FROM:
❌ DO NOT use Glob to scan all markdown files
❌ DO NOT read all documents in docs/ recursively

MANDATORY FIRST STEPS:
1️⃣ Read PROJECT_PROGRESS.md
2️⃣ Use RAG query for test requirements ONLY

VIOLATION = TOKEN WASTE + INCOMPLETE TESTING

🚨🚨🚨 END WARNING - PROCEED WITH CARE 🚨🚨🚨
```

### ⚠️ CRITICAL: Mandatory Document Access Workflow

**FORBIDDEN**:
- ❌ **NEVER read all documents in `docs/` recursively**
- ❌ **NEVER use Glob/Read tools to scan all design documents**

**MANDATORY WORKFLOW**:

#### Step 1: Understand What to Test
- Read PROJECT_PROGRESS.md to identify completed features
- Read implementation notes if available

#### Step 2: Use RAG for Test Requirements
```python
# Query RAG with targeted keywords
import subprocess
import sys

result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "feature you're testing"
], capture_output=True, text=True, encoding='utf-8')

# Windows fallback for encoding issues:
# result = subprocess.run([
#     sys.executable, "rag/scripts/rag_query.py",
#     "feature you're testing"
# ], capture_output=True)
# content = result.stdout.decode('utf-8')

print(result.stdout)
# Verify implementation against retrieved chunks
```

#### Step 3: Cross-Reference Systems
```python
# Query related systems to check consistency
result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "related system keywords"
], capture_output=True, text=True, encoding='utf-8')

print(result.stdout)
```

**When RAG is NOT available**:
- Follow same rules as Programmer (see Phase 4)
- Build RAG if project has >5 documents
- For small projects, read only relevant documents selectively

### Efficient Testing with RAG

**If RAG index was built** (see Phase 3.6), use it to quickly locate relevant test requirements:

**Example 1: Testing damage calculation bugs**

Instead of reading all design documents to verify formulas:

```python
# Query RAG for damage calculation specs
import subprocess
import sys

result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "伤害 暴击 计算公式"
], capture_output=True, text=True, encoding='utf-8')

# Windows encoding fallback:
# result = subprocess.run([
#     sys.executable, "rag/scripts/rag_query.py",
#     "伤害 暴击 计算公式"
# ], capture_output=True)
# content = result.stdout.decode('utf-8')

print(result.stdout)
# Result: Specific chunks with formulas
# Claude can now verify:
# - Is the damage formula implemented correctly?
# - Is the crit multiplier correct?
# - Are edge cases handled?
```

**Example 2: Testing character progression**

```python
# Query RAG for progression system
import subprocess
import sys

result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "升级 经验值 属性成长"
], capture_output=True, text=True, encoding='utf-8')

# Windows fallback:
# result = subprocess.run([
#     sys.executable, "rag/scripts/rag_query.py",
#     "升级 经验值 属性成长"
# ], capture_output=True)
# content = result.stdout.decode('utf-8')

print(result.stdout)
# Retrieved chunks show:
# - Level up requirements
# - XP curve formula
# - Stat increases per level

# Tester can verify implementation matches design
```

**Example 3: Cross-referencing related systems**

```python
# Check consistency across combat systems
result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "战斗 状态效果 buff 机制"
], capture_output=True, text=True, encoding='utf-8')

print(result.stdout)
# Returns chunks from multiple documents:
# - Damage system
# - Status system
# - Buff mechanics

# Tester can verify:
# - No contradictions between systems
# - Consistent terminology
# - Proper integration
```

**Benefits for Tester**:
- ✅ Quick access to design specifications
- ✅ Verify implementation against requirements
- ✅ Cross-reference multiple systems efficiently
- ✅ **90%+ reduction in tokens needed**

Conduct systematic testing:

1. **Functional testing**
   - Verify all features work as specified in design docs
   - Test edge cases and error conditions
   - Check cross-system interactions

2. **UX evaluation**
   - Assess game feel and responsiveness
   - Identify confusing interactions
   - Evaluate difficulty progression

3. **Bug reporting**
   - Document each bug with: description, reproduction steps, severity
   - Categorize issues: critical, major, minor
   - Report to Programmer with clear details

4. **Improvement suggestions**
   - Identify optimization opportunities
   - Suggest quality-of-life improvements
   - Note potential design refinements

**Use [checklist/测试检查清单.md](checklist/测试检查清单.md)** to ensure thoroughness.

Present findings in a structured test report and coordinate fixes with the Programmer role.

## Reference Materials

Load these references when needed:

- **[references/游戏开发流程.md](references/游戏开发流程.md)** - Detailed workflow explanations and role responsibilities
- **[checklist/主策划检查清单.md](checklist/主策划检查清单.md)** - Lead Designer phase verification checklist
- **[checklist/开发检查清单.md](checklist/开发检查清单.md)** - Development phase verification checklist

## Key Principles

1. **Lead Designer strategizes, Designer executes** - Clear separation between breakdown and detailed design
2. **Design first, code second** - Never implement without clear design documentation
3. **Version control** - Update document version numbers when modifying designs
4. **Confirm at checkpoints** - Get user approval before moving to next phase
5. **Complete documentation** - Design docs must be implementation-ready
6. **Proactive communication** - Both Lead Designer and Designer should confirm with user when uncertain
7. **Iterative quality** - Tester feedback drives refinement cycles
8. **🚨 CRITICAL: Never scan all documents** - Programmer/Tester MUST follow RAG workflow:
   - ✅ Read 3 overview files (PROJECT_PROGRESS.md + 游戏大纲 + 模块拆解)
   - ✅ Use RAG queries for specific requirements
   - ❌ NEVER use Glob/Read to scan all docs
   - **Violation = Token waste + task failure**

## Common Patterns

**When user says "主策划：我想要xxx"**:
→ Immediately switch to Lead Designer role → Analyze request → Break down into modules/systems → Plan execution approach

**When user says "Make me a game like X":**
→ Enter Lead Designer role → Analyze reference game → Ask clarifying questions → Break down into modules

**When user provides only a vague concept:**
→ Enter Lead Designer role → Guide through structured questioning → Build out the vision → Break down into structured modules

**When user wants to add features mid-development:**
→ Switch to Lead Designer → Analyze new feature → Break down into modules/systems → Switch to Designer → Create detailed docs → Hand off to Programmer

**When bugs are found:**
→ Tester documents and reports → Programmer implements fix → Tester verifies → Close issue or re-report

**When details are unclear during design:**
→ Designer or Lead Designer should proactively ask user → Get clarification → Continue with design

**When Programmer starts implementation** (CRITICAL - Follow this exact sequence):
→ Read PROJECT_PROGRESS.md → Read 游戏大纲_v1.md → Read 模块拆解_v1.md → Read 关键词索引.md → Query RAG for specific requirements → Implement based on retrieved chunks ONLY
→ 🚨 **DO NOT** use Glob/Read to scan all documents → 🚨 **DO NOT** "review all docs first"

**When Tester starts testing**:
→ Read PROJECT_PROGRESS.md → Query RAG for test requirements → Verify implementation → Cross-reference related systems with RAG queries
→ 🚨 **DO NOT** read all design documents
