---
name: game-dev-collaboration
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
   - Delete deprecated documents
   - Update code if implementation phase
   - Ensure all changes are consistent

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

## Phase 3: Detailed Design Documents (Designer)

After outline approval, Lead Designer says:

```
📝 切换到执行策划角色，开始编写详细策划文档
```

**Designer works through each module/system** defined in the breakdown:

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

## Phase 4: Technical Implementation (Programmer)

After design approval, switch to Programmer role:

```
💻 切换到程序员角色...
```

Read all design documents in `docs/` recursively. If anything is unclear, communicate with Designer (simulate internal team communication).

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
```

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
