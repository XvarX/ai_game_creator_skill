# RAG增量更新脚本说明

## 概述

当文档更新时，不需要完全重建RAG索引。增量更新只对变化的文档进行操作，大幅提升效率。

## 增量更新原理

### 文件变化检测

通过对比文件的**元数据**判断文件是否变化：

1. **文件路径** - 判断新增/删除
2. **修改时间（mtime）** - 判断是否修改
3. **文件哈希（MD5）** - 确认内容是否真的变化

### 操作分类

| 文件状态 | 检测方法 | 操作 |
|---------|---------|------|
| 新增 | 文件存在但数据库中没有 | `collection.add()` |
| 修改 | mtime或hash变化 | `collection.delete()` + `collection.add()` |
| 删除 | 数据库有但文件不存在 | `collection.delete()` |
| 未变化 | mtime和hash都相同 | 跳过 |

## 使用方法

### 创建增量更新脚本

根据你选择的方案，创建对应的更新脚本：

**方案1：ZhipuAI** - `rag/scripts/rag_update_zhipu.py`
**方案2：Sentence-Transformers** - `rag/scripts/rag_update_st.py`

### 执行增量更新

```bash
# 方案1：ZhipuAI
python rag/scripts/rag_update_zhipu.py

# 方案2：Sentence-Transformers
python rag/scripts/rag_update_st.py
```

### 输出示例

```bash
$ python rag/scripts/rag_update_zhipu.py

[INFO] Scanning documents in docs/...
[OK] Found 25 markdown files
[INFO] Comparing with RAG index...
[INFO] Changes detected:
  - Added: 2 files
  - Modified: 3 files
  - Deleted: 1 file
  - Unchanged: 19 files

[INFO] Processing changes...
[OK] Added: 新系统_v1.md (5 chunks)
[OK] Added: 另一个新系统_v1.md (3 chunks)
[OK] Modified: 伤害系统_v1.md → v2.md (8 chunks)
[OK] Modified: 属性系统_v2.md (6 chunks)
[OK] Deleted: 旧系统_v1.md (4 chunks removed)

[SUCCESS] RAG incrementally updated!
  - Total documents: 26
  - Total chunks: 195
  - Embedding cost: ~0.0002 CNY (only for changed files)
  - Time saved: ~85% compared to full rebuild

⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️
[重要提醒] 检测到文档变更，请更新关键词索引！
⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️ ⚠️

需要更新的文件: rag/关键词索引.md

变更详情:
  ➕ 新增文档 2 个: 请添加到索引
  🔄 修改文档 3 个: 请更新关键词
  🗑️  删除文档 1 个: 请从索引移除

快速更新方法:
  python rag/scripts/update_keyword_index.py

或手动编辑 rag/关键词索引.md 更新
```

## 性能对比

| 场景 | 完全重建 | 增量更新 | 节省 |
|------|---------|---------|------|
| 1个文件修改 | ~120秒 | ~15秒 | 87.5% |
| 5个文件修改 | ~120秒 | ~45秒 | 62.5% |
| 50%文件修改 | ~120秒 | ~90秒 | 25% |
| 所有文件修改 | ~120秒 | ~120秒 | 0% |

**建议**：当修改文件数超过50%时，考虑完全重建。

## 脚本实现要点

### 1. 元数据存储

在向量数据库的metadata中存储文件追踪信息：

```python
metadata = {
    "source": "伤害系统_v1.md",
    "mtime": "1704067200",  # 文件修改时间戳
    "hash": "abc123...",     # 文件内容MD5
    "chunk_id": 0           # chunk序号
}
```

### 2. 文件哈希计算

```python
import hashlib

def get_file_hash(filepath):
    """计算文件MD5哈希"""
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()
```

### 3. 增量更新逻辑

```python
def incremental_update():
    # 1. 扫描所有文档
    current_files = scan_docs()

    # 2. 获取数据库中的记录
    db_records = get_db_records()

    # 3. 对比差异
    added = current_files - db_records
    removed = db_records - current_files
    modified = check_mtime_and_hash(current_files & db_records)

    # 4. 执行增量操作
    for file in added:
        add_to_rag(file)

    for file in removed:
        delete_from_rag(file)

    for file in modified:
        delete_from_rag(file)
        add_to_rag(file)
```

## 集成到工作流程

### Phase 3.6: 构建RAG索引（首次）

```bash
python rag/scripts/rag_setup.py  # 完全构建
python rag/scripts/update_keyword_index.py  # 创建关键词索引
```

### Phase 3.5/文档更新后：增量更新

```bash
# Designer更新文档后
python rag/scripts/rag_update_zhipu.py  # 增量更新RAG
python rag/scripts/update_keyword_index.py  # 更新关键词索引
```

**关键点**：两个索引都需要更新！
- **向量数据库更新** → 确保能检索到新内容
- **关键词索引更新** → 确保程序员知道如何查询

### 何时完全重建

```bash
# 当以下情况时完全重建：
rm -rf rag/chroma_db/
python rag/scripts/rag_setup.py
```

重建时机：
- 切换embedding方案
- 文档变化超过50%
- 数据库损坏
- 长时间未更新（>1个月）

## 注意事项

1. **保持一致性**：文档更新后必须立即更新RAG和关键词索引
2. **双重更新**：
   - ✅ 向量数据库增量更新（自动检测变化）
   - ✅ 关键词索引更新（半自动辅助）
3. **验证更新**：更新后查询验证新内容可用
4. **定期清理**：删除的文档必须从RAG和索引移除
5. **元数据完整**：确保每个chunk都有正确的追踪元数据

## 为什么需要两个索引？

| 索引类型 | 作用 | 维护方式 |
|---------|------|---------|
| **向量数据库 (RAG)** | 存储文档内容，支持语义检索 | 自动增量更新 |
| **关键词索引** | 帮助程序员发现文档，指导查询 | 半自动辅助更新 |

**常见问题**：
- Q: 只有RAG更新不行吗？
- A: 不行。新文档在RAG中可检索，但程序员不知道它的存在，不知道该用什么关键词查询

**示例**：
```
场景: 新增了"装备强化系统_v1.md"

只更新RAG:
  ❌ 程序员: "有装备相关文档吗？" → 不知道查询什么关键词
  ❌ 结果: 新文档无人使用

同时更新关键词索引:
  ✅ 程序员查看索引 → 看到"装备模块 → 装备强化系统"
  ✅ 程序员: "python rag_query.py '装备强化 升级'"
  ✅ 结果: 成功检索并实现
```

## 完整实现示例

参见：
- `rag/scripts/rag_update_zhipu.py` - ZhipuAI增量更新实现
- `rag/scripts/rag_update_st.py` - Sentence-Transformers增量更新实现
