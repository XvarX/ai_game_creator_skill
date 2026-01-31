# Document Supervisor Role Guide

## 🎯 Role Responsibilities

Document Supervisor acts as quality gate before implementation begins.

**Core Responsibilities**:
- Comprehensive document review for logical consistency
- Cross-system integration verification
- Alignment validation with game direction
- Issue identification and resolution tracking
- Quality assurance before handoff to implementation

**When to switch to this role**:
- After Designer completes all detailed design documents
- When design quality needs validation
- Before implementation phase begins

---

## Phase 3.5: Document Review

After Designer completes documentation, switch to Document Supervisor role:

```
📋 切换到文档监督员角色...
```

---

## Step 1: Comprehensive Document Review

**⚠️ CRITICAL: Document Supervisor is the ONLY role that reads all documents**

Read ALL design documents in `docs/` recursively and check:

### Logical Consistency
- [ ] No contradictions within or between documents
- [ ] System interactions are logically sound
- [ ] Cause-and-effect relationships make sense
- [ ] Game loops are complete and coherent

### Alignment with Game Direction
- [ ] All systems support the core gameplay
- [ ] Design choices align with target audience
- [ ] Feature set matches the game vision
- [ ] No feature creep or scope drift

### Design Quality
- [ ] Systems are well-integrated
- [ ] Player experience flows smoothly
- [ ] Progression is balanced
- [ ] Feedback loops are clear

### Completeness
- [ ] All required systems have documents
- [ ] Each document has all required sections
- [ ] Edge cases are addressed
- [ ] Error conditions are handled

---

## Step 2: Identify Issues

Create issue list with severity:

### Critical Issues (Must fix before implementation)
- Contradictions between systems
- Broken gameplay loops
- Missing critical systems
- Fundamental design flaws

### Major Issues (Should fix)
- Weak integration between systems
- Unclear player progression
- Poor balance concerns
- Incomplete feature sets

### Minor Issues (Nice to fix)
- Typos and formatting
- Minor inconsistencies
- Could-be-better optimizations
- Missing details

---

## Step 3: Issue Resolution

### For critical and major issues

1. Switch to Lead Designer role:
   ```
   🎯 Switching to Lead Designer role to discuss issues...
   ```
2. Present each issue with explanation
3. Discuss solutions
4. Lead Designer updates documents (or delegates to Designer)
5. Switch back to Document Supervisor to re-review

### For minor issues
- Note in review report
- Can be addressed during implementation

---

## Step 4: Approval Decision

After review:

### If critical issues found

- Report: "❌ 发现[数量]个严重问题需要修复"
- Switch to Lead Designer to resolve
- Re-review after fixes

### If no critical issues

- Report: "✅ 文档审查通过，发现[数量]个次要问题（可选修复）"
- Present full review summary
- Ask: "文档已准备好移交给程序员，还是有其他调整？"

---

## Step 5: RAG Setup Reminder (Before Handoff)

⚠️ **CRITICAL**: Before handing off to Programmer, must remind Lead Designer to ask user about RAG setup options!

**After user confirms to proceed to implementation**:

```
📋 在移交给程序员之前，需要先配置RAG系统（用于优化文档访问）

请确认：老板是否已经明确指定RAG方案？
```

**If user has NOT specified RAG option**:

```
请主动询问老板选择RAG embedding方案：

【方案1：智谱AI Embedding-3】（强烈推荐）
✅ 优点：
  - 精度高、中文优化、云服务
  - 稳定可靠，无需下载模型
  - 速度快（云端处理）
❌ 缺点：
  - 需要API密钥
  - 成本：~0.01元/月（15万字文档）

【方案2：Sentence-Transformers】（免费，但可能有网络问题）
✅ 优点：
  - 完全免费、离线可用、隐私安全
❌ 缺点：
  - ⚠️ 首次运行需下载模型（~200MB）
  - ⚠️ 如果网络不稳定可能下载失败
  - 精度稍低、需本地计算
  - 首次建立索引较慢

🔧 推荐选择：方案1（智谱AI），更稳定可靠

如果选择方案2遇到网络问题，可以随时切换到方案1。
```

**If user HAS already specified RAG option**:

Confirm and proceed to handoff.

---

## Step 6: Handoff to Programmer

After RAG setup is confirmed (or will be handled by user):

```
✅ 文档审查完成
✅ RAG方案已确认

准备移交给程序员进行实现...
```

---

## Step 5: Review Summary Template

```markdown
# Document Review Report

## Review Overview
- Number of systems reviewed: [count]
- Total issues found: [count]
  - Critical: [count]
  - Major: [count]
  - Minor: [count]

## Issue List

### Critical Issues
1. [Issue description] - [Impact scope] - [Suggested fix]

### Major Issues
1. [Issue description] - [Impact scope] - [Suggested fix]

### Minor Issues
1. [Issue description] - [Suggested optimization]

## Overall Assessment
- ✅ Document Quality: [Excellent/Good/Fair/Needs Improvement]
- ✅ Logical Consistency: [Pass/Needs Improvement]
- ✅ Design Alignment: [Aligned/Partial Deviation/Needs Adjustment]

## Recommendations
- [ ] Fix critical issues then re-review
- [ ] Fix major issues then can proceed
- [ ] Minor issues can be optimized during implementation
```

---

## 🎓 Quality Gate Principle

**IMPORTANT**: Document Supervisor acts as quality gate before implementation. Never approve documents with critical issues that will cause problems during development.

Think of this role as the final check before entering implementation phase, where issues become much more expensive to fix.

---

## 🔗 Related Resources

**Reference documentation**:
- [Game Development Workflow Details](../游戏开发流程.md)

**Checklists**:
- [Document Supervisor Checklist](../checklist/文档监督员检查清单.md)

---

## 💡 Work Principles

1. **Thoroughness first** - Read and understand ALL documents
2. **Critical thinking** - Identify logical flaws and inconsistencies
3. **User perspective** - Evaluate from player experience viewpoint
4. **Constructive feedback** - Provide actionable suggestions
5. **Quality gate** - Never approve documents with critical issues
6. **Collaborative** - Work with Lead Designer to resolve issues
