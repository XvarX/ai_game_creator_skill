# Game Development Collaboration Skill

**专业游戏开发协作skill** - 指导Claude以多角色协作模式完成游戏开发项目。

## 📖 简介

这是一个专业的游戏开发Agent Skill，模拟真实游戏开发团队的协作流程。Claude将扮演不同的团队角色（主策划、执行策划、文档监督员、程序员、测试员），通过标准化的工作流程完成从需求分析到技术实现的全过程。

**核心特点**：采用**渐进式披露**（Progressive Disclosure）架构，只加载当前工作所需的内容，大幅降低token消耗。

## 🎯 核心特性

### 1. 多角色协作系统
- 🎯 **主策划**：需求分析、模块拆解、流程规划
- 📝 **执行策划**：编写详细的游戏设计文档
- 👁️ **文档监督员**：审查文档质量、确保一致性
- 💻 **程序员**：技术实现、代码开发
- 🧪 **测试员**：功能验证、质量保证

### 2. 完整的开发流程
- Phase 1: 需求分析（主策划）
- Phase 2: 模块拆解（主策划）
- Phase 3: 详细设计（执行策划）
- Phase 3.5: 文档审查（文档监督员）
- Phase 3.6: RAG构建（程序员）⭐
- Phase 4: 技术实现（程序员）
- Phase 5: 质量保证（测试员）

### 3. RAG文档检索系统 ⭐

**重要特性**：集成RAG（Retrieval-Augmented Generation）系统，大幅降低token消耗！

- ✅ **双方案支持**：
  - 方案1：智谱AI Embedding-3（推荐，精度高，~0.01元/月）
  - 方案2：Sentence-Transformers（免费离线，本地计算）
- ✅ **纯检索模式**：不调用LLM生成答案，Claude直接阅读检索结果
- ✅ **Token节省**：平均节省80-90% tokens
- ✅ **增量更新**：文档变更后85%+时间节省的增量更新

**RAG工作流程**：
```
策划文档编写完成
    ↓
程序员构建RAG索引（Phase 3.6）
    ↓
程序员开发时使用RAG检索（Phase 4）
    ↓
测试员验证时使用RAG检索（Phase 5）
```

### 4. 渐进式披露架构 ⭐

**核心优化**：角色详细指导按需加载，避免一次性加载所有内容。

```
SKILL.md (274行 - 导航和约束)
    ↓ (当切换到角色时)
角色详细文档 (references/roles/*.md)
    ↓ (需要时)
参考文档、模板、检查清单
```

**收益**：
- ✅ SKILL.md从2,009行精简到274行（86%减少）
- ✅ 只加载当前角色的详细指导
- ✅ 节省80-90% tokens

## 📁 项目结构

```
ai_game_creator_skill/
├── SKILL.md                    # 核心skill文件（274行 - 导航和约束）
│
├── references/
│   ├── roles/                  # ⭐ 角色详细文档（按需加载）
│   │   ├── lead_designer.md    # 主策划详细指导
│   │   ├── designer.md         # 执行策划详细指导
│   │   ├── document_supervisor.md  # 文档监督员详细指导
│   │   ├── programmer.md       # 程序员详细指导
│   │   └── tester.md           # 测试员详细指导
│   │
│   ├── 游戏开发流程.md          # 详细流程说明
│   ├── 智谱RAG集成指南.md       # RAG方案1完整指南
│   ├── RAG方案切换指南.md       # 方案切换步骤
│   ├── RAG实际使用示例.md       # 实际场景示例
│   └── RAG增量更新示例.md       # 增量更新使用说明
│
├── checklist/                  # 角色检查清单
│   ├── 主策划检查清单.md
│   ├── 执行策划检查清单.md
│   ├── 文档监督员检查清单.md
│   ├── 开发检查清单.md
│   └── 测试检查清单.md
│
├── templates/                  # 文档模板
│   ├── 游戏大纲模板.md
│   ├── 模块拆解模板.md
│   ├── 策划文档模板.md
│   ├── RAG配置模板.md
│   └── 关键词索引模板.md        # ⭐ RAG关键词索引模板
│
├── rag/
│   └── scripts/                # ⭐ RAG脚本
│       ├── rag_utils.py             # ⭐ 跨平台工具（推荐）
│       ├── rag_setup_zhipu.py        # 智谱AI构建脚本
│       ├── rag_setup_st.py           # Sentence-Transformers构建脚本
│       ├── rag_query.py              # 智谱AI查询脚本
│       ├── rag_query_st.py           # Sentence-Transformers查询脚本
│       ├── rag_update_zhipu.py       # 智谱AI增量更新
│       ├── rag_update_st.py          # Sentence-Transformers增量更新
│       └── update_keyword_index.py   # 关键词索引更新脚本
│
├── scripts/                    # 工具脚本
│   └── generate_project_structure.py
│
└── assets/                     # 资源文件
```

### ⭐ 代码组织原则（重要）

**你的游戏项目结构**（由程序员在Phase 4创建）：

**⚠️ 关键原则**：`code/` 目录结构必须**镜像反映** `docs/模块拆解_v1.md` 的结构

```
your-game-project/
├── docs/                    # 设计文档（主策划+执行策划创建）
│   ├── 模块拆解_v1.md        # ⭐ 代码结构依据这个文档
│   └── 模块/
│       ├── 战斗模块/
│       │   ├── 伤害系统_v1.md
│       │   └── 状态系统_v1.md
│       └── 角色模块/
│           └── 成长系统_v1.md
│
├── code/                    # ⭐ 代码（程序员根据模块拆解创建）
│   ├── combat/              # 战斗模块 → combat/
│   │   ├── damage/          # 伤害系统
│   │   └── status/          # 状态系统
│   ├── character/           # 角色模块 → character/
│   │   └── progression/     # 成长系统
│   └── common/              # 通用工具（总是添加）
│
├── assets/                  # 美术、音频等资源
├── rag/                     # RAG系统
└── PROJECT_PROGRESS.md      # 项目进度追踪
```

**重要说明**：
- ❌ **不要使用固定模板** - 每个游戏的模块都不同
- ✅ **读取模块拆解文档** - `docs/模块拆解_v1.md` 决定代码目录
- ✅ **一一对应** - 每个模块文档 → 一个代码目录
- ✅ **遵循优先级** - 按模块拆解中的优先级顺序实现

---

## 🚀 使用方法

### 触发方式

使用以下任意方式触发此skill：

1. **直接描述游戏想法**：
   - "我想做一个XX游戏"
   - "帮我设计一个游戏"
   - "创建一个XX类型的游戏"

2. **使用角色前缀**：
   - "主策划：做一个RPG游戏"
   - "主策划：[你的游戏想法]"

3. **明确请求**：
   - "帮我开发一个新游戏"
   - "设计并实现一个游戏系统"

### 工作模式选择

skill启动时会询问选择工作模式：

**交互模式**（推荐新手）：
- 在每个关键检查点确认
- 遇到疑问会主动询问
- 确保对齐后再继续

**自动模式**（适合有经验用户）：
- 一次性完成所有阶段
- 跳过确认检查点
- 遇到不确定时做合理假设

### 工作量评估（动态）⭐

**重要更新**：工作量现在根据实际项目动态评估，不再使用固定模板。

skill会根据以下因素动态评估：
- 游戏类型和复杂度
- 玩法系统数量
- 角色和成长系统深度
- UI/UX模块数量
- 特色功能数量

**示例评估输出**：
```
基于你的需求，预估工作量如下：

模块数量：5个
系统文档数：18份
预估总字数：120,000字
预估时间：2.5-3小时

这个工作量是否符合预期？还是需要缩小范围？
```

## 📚 RAG系统使用

### 为什么使用RAG？

随着项目规模增长，文档可能达到10-30万字：
- ❌ **传统方式**：每次都要读取全部文档，token消耗巨大
- ✅ **RAG方式**：只加载相关章节，token消耗降低80-90%

### 构建时机

在文档监督员审查通过后、程序员开始实现前，由程序员构建RAG索引。

### RAG目录结构 ⭐

**⚠️ 重要**：RAG必须构建在**项目根目录**（docs/所在位置）：

```
your-game-project/
├── docs/                    # 游戏设计文档
├── rag/                     # ⭐ RAG目录（在这里创建）
│   ├── scripts/             # RAG脚本（从skill复制）
│   │   ├── rag_setup_zhipu.py
│   │   ├── rag_setup_st.py
│   │   ├── rag_query.py
│   │   ├── rag_query_st.py
│   │   ├── rag_update_zhipu.py
│   │   ├── rag_update_st.py
│   │   └── update_keyword_index.py
│   ├── chroma_db/           # 向量数据库（自动创建）
│   ├── .env                 # 智谱API密钥（仅智谱方案需要）
│   └── 关键词索引.md         # 关键词索引（自动生成）
├── PROJECT_PROGRESS.md
└── SKILL.md
```

**设置步骤**：
1. 从skill复制`rag/scripts/`到项目的`rag/`目录：

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

   **注意**：将路径 `C:\Users\YourName\.claude\skills\ai_game_creator_skill` 修改为你实际的skill安装路径。

2. 在**项目根目录**运行构建脚本
3. 向量数据库（`chroma_db/`）会自动在`rag/`中创建

### 方案选择

**方案1：智谱AI Embedding-3**（推荐）
- ✅ 精度高、中文优化、云服务
- ✅ 成本：~0.01元/月（15万字文档）
- ✅ 构建：`python rag/scripts/rag_setup_zhipu.py`
- ❌ 需要：智谱API密钥

**方案2：Sentence-Transformers**（免费离线）
- ✅ 完全免费、离线可用、隐私安全
- ❌ 精度稍低、需本地计算
- ✅ 构建：`python rag/scripts/rag_setup_st.py`
- ✅ 需要：无（首次运行自动下载模型）

### ⚠️ 重要：构建后必须测试编码 ⭐

**构建完RAG后立即测试**，确认输出编码正常：

```bash
# 使用你文档中的关键词进行测试
python rag/scripts/rag_query.py "伤害"  # 智谱AI
# 或
python rag/scripts/rag_query_st.py "伤害"  # Sentence-Transformers
```

**检查输出**：
- ✅ 如果看到**正常的中文** → RAG工作正常
- ❌ 如果看到**乱码**或错误信息：
  - 检查控制台是否支持UTF-8
  - 确认RAG是否构建成功
  - 尝试重新运行查询

**为什么这很重要**：
- 查询脚本已经自动处理UTF-8编码
- 现在测试可以在实现阶段避免问题
- 如果出现问题，可以及早发现并解决

### 使用示例

程序员实现功能时：
```python
import subprocess
import sys

# 传统方式：读取全部文档（150,000字）
# RAG方式：只检索相关chunks（2,000字）

result = subprocess.run([
    sys.executable, "rag/scripts/rag_query.py",
    "伤害计算 公式 暴击"
], capture_output=True, text=True, encoding='utf-8')

# RAG返回3个相关chunks
# Claude阅读这3个chunks后实现代码
# 节省98.6% tokens
```

### 增量更新 ⭐

文档变更后，使用增量更新代替完全重建：

**⚠️ 推荐：使用Python工具（跨平台兼容）**：
```bash
# 所有平台通用
python rag/scripts/rag_utils.py update_zhipu    # 智谱AI
python rag/scripts/rag_utils.py update_st       # Sentence-Transformers
python rag/scripts/rag_utils.py update_index    # 更新关键词索引
```

**或使用平台特定命令**：
```bash
# 增量更新（85%+时间节省）
python rag/scripts/rag_update_zhipu.py    # 智谱AI
python rag/scripts/rag_update_st.py       # Sentence-Transformers
python rag/scripts/update_keyword_index.py  # 更新关键词索引
```

**何时更新**：
- 文档修改（版本更新）
- 新文档创建
- 文档删除
- 任何新指令响应执行后

### 🔧 跨平台RAG工具 ⭐

**推荐使用** `rag_utils.py` **跨平台工具**，避免平台特定命令问题：

```bash
# 检查RAG是否存在
python rag/scripts/rag_utils.py check

# 删除RAG数据库（完全重建前）
python rag/scripts/rag_utils.py clean

# 构建RAG（选择其一）
python rag/scripts/rag_utils.py setup_zhipu    # 智谱AI
python rag/scripts/rag_utils.py setup_st       # Sentence-Transformers（免费）

# 增量更新
python rag/scripts/rag_utils.py update_zhipu   # 智谱AI
python rag/scripts/rag_utils.py update_st      # Sentence-Transformers
python rag/scripts/rag_utils.py update_index   # 更新关键词索引
```

**优势**：
- ✅ 在Windows、Linux、macOS上都能工作
- ✅ 避免Windows cmd/PowerShell命令兼容性问题
- ✅ 一个命令完成操作，不需要记忆平台特定语法
- ✅ 不会创建奇怪的文件名（如 `scripts&& cp...`）

## 📋 相关文档

### 核心文档
- [SKILL.md](SKILL.md) - Skill导航和核心约束（274行）
- [角色详细指导](references/roles/) - 5个角色的完整工作流程

### RAG文档
- [智谱RAG集成指南.md](references/智谱RAG集成指南.md) - 智谱AI方案详细指南
- [RAG方案切换指南.md](references/RAG方案切换指南.md) - 方案切换步骤
- [RAG实际使用示例.md](references/RAG实际使用示例.md) - 实际场景示例
- [RAG增量更新示例.md](references/RAG增量更新示例.md) - 增量更新使用说明

### 角色检查清单
- [主策划检查清单.md](checklist/主策划检查清单.md)
- [执行策划检查清单.md](checklist/执行策划检查清单.md)
- [文档监督员检查清单.md](checklist/文档监督员检查清单.md)
- [开发检查清单.md](checklist/开发检查清单.md)
- [测试检查清单.md](checklist/测试检查清单.md)

## 🎓 适用场景

### 适合使用此skill的场景

- ✅ 需要完整游戏设计方案的游戏项目
- ✅ 需要系统化设计文档的独立游戏开发者
- ✅ 游戏jam或原型开发
- ✅ 学习游戏开发流程
- ✅ 需要快速生成游戏设计文档

### 项目规模建议

**小规模项目**（适合新手）：
- 3-5个系统文档
- 总计30,000-50,000字
- 预计0.5-1小时完成

**中等规模项目**（推荐）：
- 10-20个系统文档
- 总计80,000-150,000字
- 预计1.5-3小时完成

**大规模项目**（完整）：
- 25-40个系统文档
- 总计150,000-250,000字
- 预计3-5小时完成

## 🔧 高级特性

### 新指令响应机制

当老板（用户）提供新指令或反馈时，skill会：
1. 全面审查所有现有文档
2. 识别变更范围和影响
3. 更新受影响的文档
4. 进行影响分析
5. 向老板展示变更摘要
6. 更新RAG索引（如已构建）

### RAG中途切换

支持在两种RAG方案之间切换：
- 详细的切换步骤见 [RAG方案切换指南.md](references/RAG方案切换指南.md)
- 切换过程无缝，查询接口保持一致

### 版本管理

严格的文档版本管理：
- 初始文档：`_v1.md`
- 修订文档：`_v2.md`, `_v3.md` 等
- **重要**：更新后删除旧版本（保持单一真相源）

## 💡 最佳实践

1. **从交互模式开始**：第一次使用建议选择交互模式，了解完整流程
2. **合理规划项目规模**：根据实际需求动态评估工作量
3. **充分利用RAG**：中等以上项目（>5个文档）强烈建议构建RAG索引
4. **遵循检查清单**：每个角色都有对应的检查清单，确保质量
5. **及时反馈**：遇到问题或需要调整时，及时提供反馈
6. **角色分离**：每个角色专注于自己的职责，Designer不写代码，Programmer不全读文档

## 🚨 重要约束

**Designer（执行策划）**：
- ❌ 永远不要写代码或实现逻辑
- ✅ 只描述要实现什么（WHAT），不描述如何实现（HOW）

**Programmer & Tester（程序员 & 测试员）**：
- 🚨 **永远不要使用Glob扫描所有文档**
- 🚨 **永远不要递归读取所有设计文档**
- ✅ **必须使用RAG工作流**：读概览文件 → 查关键词索引 → RAG查询 → 工作

**违反约束 = token浪费 + 任务失败**

## 📝 版本历史

### v2.0.0 (2026-01-28) - 重构版 ⭐
- ✅ **渐进式披露架构**：SKILL.md从2,009行精简到274行（86%减少）
- ✅ **角色文档分离**：5个角色的详细指导独立到`references/roles/`
- ✅ **RAG构建脚本**：新增2个独立的RAG构建脚本
- ✅ **动态工作量评估**：不再使用固定模板，根据实际项目评估
- ✅ **代码提取**：所有代码从文档中提取到可执行脚本

### v1.0.0 (2026-01-27)
- ✅ 完整的多角色协作系统
- ✅ 标准化的游戏开发流程
- ✅ RAG双方案集成（智谱AI + Sentence-Transformers）
- ✅ 完整的检查清单体系
- ✅ 丰富的文档模板
- ✅ 新指令响应机制

## 🤝 贡献

欢迎提出改进建议和反馈！

## 📄 许可

本skill遵循开源许可，可自由使用和修改。

---

**开始使用**：直接告诉Claude你的游戏想法，skill将自动启动！

示例：
- "主策划：我想做一个赛博朋克风格的RPG游戏"
- "帮我设计一个像素风的平台跳跃游戏"
- "创建一个多人在线的卡牌对战游戏"
