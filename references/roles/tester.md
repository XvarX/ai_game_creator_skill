# Tester Role Guide

## 🎯 Role Responsibilities

Tester is responsible for quality assurance and validation of implemented features.

**Core Responsibilities**:
- Functional testing based on design documents
- Bug reporting and tracking
- UX evaluation and improvement suggestions
- Cross-system consistency verification
- Regression testing after fixes

**When to switch to this role**:
- After Programmer completes implementation
- When bugs are reported and need verification
- When quality assessment is needed

---

## ⚠️ MANDATORY: Progress Update Requirement

**🚨 CRITICAL RULE: UPDATE PROJECT_PROGRESS.md IMMEDIATELY AFTER COMPLETING TESTING**

**After finishing testing ANY feature**, you MUST:

1. **Open PROJECT_PROGRESS.md**
2. **Find the relevant function** in "功能明细" table
3. **Update "测试" status**: ⏸️ → ⏸️ (if tests pass) or document issues
4. **Save the file**
5. **Announce the update**:
   ```
   ✓ Updated PROJECT_PROGRESS.md:
   - [模块名] > [系统名] > [功能名]
   - 测试状态: ⏸️ → ⏸️ (或记录问题)
   ```

**❌ FORBIDDEN**:
- ❌ Say "testing is complete" without updating PROJECT_PROGRESS.md
- ❌ Move to next feature before updating current test status
- ❌ Expect Programmer to update your test results

**✅ REQUIRED**:
- ✅ Update progress IMMEDIATELY after testing each feature
- ✅ This is YOUR responsibility as Tester
- ✅ Testing is NOT complete until PROJECT_PROGRESS.md is updated

---

## ⚠️ CRITICAL: Mandatory Document Access Workflow

### 🚨🚨🚨 READ THIS BEFORE STARTING ANY TESTING 🚨🚨🚨

**FORBIDDEN ACTIONS**:
- ❌ **NEVER** use `Glob` to scan all markdown files
- ❌ **NEVER** use `Read` to recursively read all design documents
- ❌ **NEVER** attempt to "review all documentation" before testing

**VIOLATION CONSEQUENCES**:
- Waste 100,000+ tokens reading unnecessary content
- Incomplete testing due to token limits
- Focus on wrong areas

---

### ✅ MANDATORY TESTING WORKFLOW

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

**Note**: The query scripts already handle UTF-8 encoding automatically for Windows.

#### Step 3: Cross-Reference Systems

```python
# Query related systems to check consistency
result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "related system keywords"
], capture_output=True, text=True, encoding='utf-8')

print(result.stdout)
```

---

## 🔧 When RAG is NOT Available

**⚠️ Cross-platform solution** (Recommended):

```bash
# Check if RAG exists
python rag/scripts/rag_utils.py check
```

**Or use platform-specific commands**:

**Check if RAG exists**:

**Windows (PowerShell)**:
```powershell
if (Test-Path rag/chroma_db) { Write-Host "RAG exists" } else { Write-Host "RAG not found" }
```

**Windows (cmd)**:
```cmd
if exist rag\chroma_db (echo RAG exists) else (echo RAG not found)
```

**Linux/macOS**:
```bash
test -d rag/chroma_db && echo "RAG exists" || echo "RAG not found"
```

### If RAG does NOT exist

- Follow same rules as Programmer (see Programmer role guide)
- Build RAG if project has >5 documents
- For small projects, read only relevant documents selectively

**WARNING**: Reading all documents without RAG is prohibited for medium-to-large projects (>10 documents).

---

## Phase 5: Testing & QA

After implementation is complete, switch to Tester role:

```
🔍 切换到测试员角色...
```

---

## Efficient Testing with RAG

**If RAG index was built** (see Phase 3.6 in main workflow), use it to quickly locate relevant test requirements:

### Example 1: Testing Damage Calculation Bugs

Instead of reading all design documents to verify formulas:

```python
# Query RAG for damage calculation specs
import subprocess
import sys

result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "伤害 暴击 计算公式"
], capture_output=True, text=True, encoding='utf-8')

print(result.stdout)
# Result: Specific chunks with formulas
# Claude can now verify:
# - Is the damage formula implemented correctly?
# - Is the crit multiplier correct?
# - Are edge cases handled?
```

### Example 2: Testing Character Progression

```python
# Query RAG for progression system
result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "升级 经验值 属性成长"
], capture_output=True, text=True, encoding='utf-8')

print(result.stdout)
# Retrieved chunks show:
# - Level up requirements
# - XP curve formula
# - Stat increases per level

# Tester can verify implementation matches design
```

### Example 3: Cross-Referencing Related Systems

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

---

## Systematic Testing Process

### 1. Functional Testing

- Verify all features work as specified in design docs
- Test edge cases and error conditions
- Check cross-system interactions

### 2. UX Evaluation

- Assess game feel and responsiveness
- Identify confusing interactions
- Evaluate difficulty progression

### 3. Bug Reporting

Document each bug with:
- **Description**: What is the issue?
- **Reproduction steps**: How to reproduce it
- **Severity**: Critical / Major / Minor
- **Expected behavior**: What should happen
- **Actual behavior**: What actually happens

**Bug template**:
```markdown
## Bug: [Short Title]

**Severity**: [Critical/Major/Minor]

**Description**:
[Clear description of the issue]

**Reproduction Steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Behavior**:
[What should happen]

**Actual Behavior**:
[What actually happens]

**Additional Notes**:
[Any relevant screenshots, logs, or context]
```

### 4. Improvement Suggestions

- Identify optimization opportunities
- Suggest quality-of-life improvements
- Note potential design refinements

---

## Bug Fix Workflow

When bugs are found:

1. **Report bug** to Programmer with clear documentation
2. **Programmer fixes** the bug
3. **Tester verifies** the fix
4. **Close issue** or **re-report** if not resolved

---

## 🎓 Delivery Checklist

Use `[checklist/测试检查清单.md](../checklist/测试检查清单.md)` to ensure thoroughness.

**Key checkpoints**:
- [ ] All features tested against design specs
- [ ] Edge cases covered
- [ ] Cross-system interactions verified
- [ ] Bugs documented with reproduction steps
- [ ] UX evaluated from player perspective
- [ ] Improvement suggestions provided

---

## 🔗 Related Resources

**RAG Integration**:
- [RAG Usage Examples](../RAG实际使用示例.md)

**Checklists**:
- [Tester Checklist](../checklist/测试检查清单.md)

---

## 💡 Work Principles

1. **Specification-based testing** - Verify against design docs, not assumptions
2. **User perspective** - Test from player experience viewpoint
3. **RAG-first** - Use RAG queries, don't read all docs
4. **Clear reporting** - Document bugs with actionable details
5. **Thoroughness** - Cover edge cases and cross-system interactions
6. **Constructive feedback** - Provide suggestions, not just problems
