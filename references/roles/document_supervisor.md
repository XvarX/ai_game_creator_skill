# Document Supervisor Role Guide

## [TARGET] Role Responsibilities

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
[DOC_SUPERVISOR] 切换到文档监督员角色...
```

---

## Step 1: Comprehensive Document Review

**[CRITICAL]: Document Supervisor is the ONLY role that reads all documents**

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
   [TARGET] Switching to Lead Designer role to discuss issues...
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

- Report: "[FORBIDDEN] 发现[数量]个严重问题需要修复"
- Switch to Lead Designer to resolve
- Re-review after fixes

### If no critical issues

- Report: "[OK] 文档审查通过，发现[数量]个次要问题（可选修复）"
- Present full review summary
- Ask: "文档已准备好移交给程序员，还是有其他调整？"

---

## Step 5: RAG Setup and Build (REQUIRED)

[WARNING] **CRITICAL: Must build RAG before handing off to Programmer**

After document review passes, you MUST set up and build RAG system for efficient document access.

### 5.1 Check if RAG Already Exists

```bash
# Check if RAG is already configured
python rag/scripts/rag_utils.py check
```

**If RAG exists**: Update it (skip to 5.3)
**If RAG doesn't exist**: Setup new RAG (continue to 5.2)

### 5.2 Setup RAG (First Time Only)

**If user hasn't specified RAG option**:

[INPUT] **Required**: RAG embedding solution selection

```
[DOC_SUPERVISOR] 文档审查通过，需要配置RAG系统

RAG可节省80-90%的token消耗

[方案1: ZhipuAI Embedding-3] (推荐)
[OK] 精度高/中文优化/云服务 [FORBIDDEN] 需要API密钥/成本~0.01元/月

[方案2: Sentence-Transformers] (免费)
[OK] 完全免费/离线可用 [FORBIDDEN] 精度稍低/首次下载~200MB

用户选择 (1/2):
```

**After user input**, execute setup:

**Option 1 - ZhipuAI (Recommended)**:
```bash
# Create .env file with API key
echo "ZHIPUAI_API_KEY=your_key_here" > rag/.env

# Build RAG index
python rag/scripts/rag_setup_zhipu.py
```

**Option 2 - Sentence-Transformers (Free)**:
```bash
# Build RAG index (first run downloads model)
python rag/scripts/rag_setup_st.py
```

### 5.3 Update RAG (If Already Exists)

After document review changes:

```bash
# Incremental update (85% faster)
python rag/scripts/rag_update_zhipu.py    # or rag_update_st.py
python rag/scripts/update_keyword_index.py
```

### 5.4 Verify RAG

**ALWAYS test RAG before handoff**:

```bash
# Test query with a keyword from documents
python rag/scripts/rag_query.py "测试"    # ZhipuAI
# or
python rag/scripts/rag_query_st.py "测试" # Sentence-Transformers
```

**Check output**:
- [OK] Normal Chinese text → RAG working correctly
- [FORBIDDEN] Garbled text (乱码) → Encoding issue, fix before handoff

### 5.5 Confirm RAG Ready

After successful build/update:

```
[OK] 文档审查完成
[OK] RAG系统已构建/更新

RAG统计：
- 文档数量：X份
- 索引块数：Y个
- 查询命令：python rag/scripts/rag_query.py "关键词"

程序员现在可以使用RAG快速访问设计文档！
```

---

## Step 6: Handoff to Programmer

After RAG is successfully built and tested:

```
[OK] 文档审查通过
[OK] RAG系统就绪

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
- [OK] Document Quality: [Excellent/Good/Fair/Needs Improvement]
- [OK] Logical Consistency: [Pass/Needs Improvement]
- [OK] Design Alignment: [Aligned/Partial Deviation/Needs Adjustment]

## Recommendations
- [ ] Fix critical issues then re-review
- [ ] Fix major issues then can proceed
- [ ] Minor issues can be optimized during implementation
```

---

## [GUIDE] Quality Gate Principle

**IMPORTANT**: Document Supervisor acts as quality gate before implementation. Never approve documents with critical issues that will cause problems during development.

Think of this role as the final check before entering implementation phase, where issues become much more expensive to fix.

---

## 🔗 Related Resources

**Reference documentation**:
- [Game Development Workflow Details](../游戏开发流程.md)

**Checklists**:
- [Document Supervisor Checklist](../checklist/文档监督员检查清单.md)

---

## [PRINCIPLE] Work Principles

1. **Thoroughness first** - Read and understand ALL documents
2. **Critical thinking** - Identify logical flaws and inconsistencies
3. **User perspective** - Evaluate from player experience viewpoint
4. **Constructive feedback** - Provide actionable suggestions
5. **Quality gate** - Never approve documents with critical issues
6. **Collaborative** - Work with Lead Designer to resolve issues
