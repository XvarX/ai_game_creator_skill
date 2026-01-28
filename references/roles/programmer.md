# Programmer Role Guide

## 🎯 Role Responsibilities

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

## ⚠️ CRITICAL: Mandatory Document Access Workflow

### 🚨🚨🚨 READ THIS BEFORE STARTING ANY WORK 🚨🚨🚨

**FORBIDDEN ACTIONS**:
- ❌ **NEVER** use `Glob` to scan all markdown files
- ❌ **NEVER** use `Read` to recursively read all design documents
- ❌ **NEVER** attempt to "review all documentation" or "familiarize with all docs"
- ❌ **NEVER** think "let me check what docs exist before starting"

**VIOLATION CONSEQUENCES**:
- Waste 100,000+ tokens reading unnecessary content
- Hit token limits and fail to complete tasks
- Slow down implementation significantly
- **Violations = Task Failure**

---

### ✅ MANDATORY FIRST STEPS (Follow This Exact Sequence)

#### Step 1: Understand Project Context

Read these 3 files ONLY - no exceptions:

```bash
1. Read PROJECT_PROGRESS.md                      # Current phase, task assignments
2. Read docs/游戏大纲_v*.md (latest version)     # Game vision, core features
3. Read docs/模块拆解_v*.md (latest version)     # Module structure, priorities
```

**How to find latest version**:
```bash
# Use Glob ONLY for these specific files (do NOT scan all docs)
Glob: docs/游戏大纲_v*.md  # e.g., 游戏大纲_v1.md, 游戏大纲_v2.md - use highest number
Glob: docs/模块拆解_v*.md  # e.g., 模块拆解_v1.md, 模块拆解_v2.md - use highest number
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

⚠️ **CRITICAL WARNING**:
- ✅ Use the index ONLY to extract keywords for RAG queries
- ❌ **DO NOT read any documents listed in the index**
- ❌ **DO NOT attempt to read detailed design documents directly**
- ❌ **DO NOT use document paths shown in RAG results as an invitation to read them**

**Why This Matters**:
When RAG returns chunks like `[Chunk 1] 来源: docs\模块拆解_v2.md`, the path is **FOR REFERENCE ONLY**. Do NOT respond with "Let me read the full document from docs\模块拆解_v2.md". Instead:
- ✅ Query RAG again with different keywords if you need more details
- ✅ Ask the Designer for clarification if RAG doesn't provide enough information
- ❌ NEVER read the source document directly

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

If you see garbled text (乱码), use the helper function:
```bash
python rag/scripts/rag_query_helper.py "关键词"
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

---

## 🚨 FINAL REMINDER BEFORE PROCEEDING

**You MUST have completed these steps BEFORE implementation**:
1. ✅ Read PROJECT_PROGRESS.md
2. ✅ Read docs/游戏大纲_v*.md (latest version)
3. ✅ Read docs/模块拆解_v*.md (latest version)
4. ✅ Read rag/关键词索引.md
5. ✅ Used RAG to query specific requirements

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

- Define code structure (folders, modules, patterns)
- Plan for scalability
- Consider performance implications

### Step 4: Implement by Priority

- Start with core gameplay mechanics
- Then supporting systems
- Finally, polish and UI

### Step 5: Testing as You Go

- Verify each feature works
- Check performance metrics
- Document any deviations from design

---

## 🔧 RAG Setup (If Not Already Built)

**⚠️ CRITICAL**: RAG must be built in the **project root** where docs/ are located.

### RAG Directory Structure

Your project should have this structure:

```
your-game-project/
├── docs/                    # Design documents
├── rag/                     # ⭐ RAG directory (create here)
│   ├── scripts/             # RAG scripts (copy from skill)
│   │   ├── rag_setup_zhipu.py
│   │   ├── rag_setup_st.py
│   │   ├── rag_query.py
│   │   ├── rag_query_st.py
│   │   ├── rag_query_helper.py
│   │   ├── rag_update_zhipu.py
│   │   ├── rag_update_st.py
│   │   └── update_keyword_index.py
│   ├── chroma_db/           # Vector database (auto-created)
│   ├── .env                 # ZhipuAI API key (for ZhipuAI option)
│   └── 关键词索引.md         # Keyword index (auto-generated)
├── PROJECT_PROGRESS.md
└── SKILL.md
```

### Setup Steps

1. **Copy RAG scripts from skill to your project**:

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

   **Note**: Adjust the skill path `C:\Users\YourName\.claude\skills\ai_game_creator_skill` to your actual skill location.

2. **Choose embedding option and build**:

   **Option 1: ZhipuAI (Recommended)**
   ```bash
   # Create API key file
   echo "ZHIPUAI_API_KEY=your_key_here" > rag/.env

   # Build RAG index
   python rag/scripts/rag_setup_zhipu.py

   # Generate keyword index
   python rag/scripts/update_keyword_index.py
   ```

   **Option 2: Sentence-Transformers (Free)**
   ```bash
   # Build RAG index (first run downloads ~400MB model)
   python rag/scripts/rag_setup_st.py

   # Generate keyword index
   python rag/scripts/update_keyword_index.py
   ```

3. **Verify RAG is working and check encoding**:
   ```bash
   # Test with a Chinese keyword from your documents
   python rag/scripts/rag_query.py "伤害"  # ZhipuAI
   # or
   python rag/scripts/rag_query_st.py "伤害"  # Sentence-Transformers
   ```

   **⚠️ CRITICAL: Check output for encoding issues**:
   - ✅ If you see **normal Chinese text** → RAG is working correctly
   - ❌ If you see **garbled text (乱码)** like `À×Îö` or `æ± ä»`:

   ```bash
   # Use the helper script with encoding fix
   python rag/scripts/rag_query_helper.py "伤害"
   ```

   **Why this matters**:
   - Windows console often has UTF-8 encoding issues with Chinese
   - The helper script fixes encoding problems automatically
   - Test now to avoid problems during implementation
   - If encoding is broken, Claude cannot read the retrieved chunks

---

## 🔧 When RAG is NOT Available

**⚠️ Cross-platform solution** (Recommended - works on Windows, Linux, macOS):

```bash
# Check if RAG exists
python rag/scripts/rag_utils.py check

# Build RAG (choose one)
python rag/scripts/rag_utils.py setup_zhipu    # ZhipuAI
python rag/scripts/rag_utils.py setup_st       # Sentence-Transformers
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

1. **For projects with >5 documents**: MUST build RAG first (see setup above)
2. **For very small projects (≤5 documents ONLY)**: You may read documents selectively
   - Read docs/游戏大纲_v*.md (latest version)
   - Read docs/模块拆解_v*.md (latest version)
   - Read ONLY the specific system document you need to implement
   - DO NOT use Glob to scan all documents
   - DO NOT read documents unrelated to your current task

**WARNING**: Reading all documents without RAG is prohibited for medium-to-large projects (>10 documents) due to token inefficiency.

---

## 💻 Code Quality Standards

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

## 💡 Work Principles

1. **Follow specs** - Implement exactly as designed, avoid scope creep
2. **RAG-first** - Always use RAG queries, never scan all docs
3. **Token efficiency** - Every chunk read should be necessary
4. **Quality code** - Write clean, maintainable, performant code
5. **Test driven** - Verify as you build, don't defer testing
6. **Document deviations** - If design is infeasible, discuss before implementing workaround
