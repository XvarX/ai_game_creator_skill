# RAG配置

**项目名称**: [项目名称]

**配置日期**: YYYY-MM-DD

**选择方案**:
- [ ] 方案1：智谱AI Embedding-3（推荐）
- [ ] 方案2：Sentence-Transformers（免费）

## 方案详情

### 方案1：智谱AI Embedding-3

- **Embedding模型**: ZhipuAI Embedding-3
- **向量维度**: 1024
- **成本**: ~0.01 CNY/月
- **API密钥**: 已配置 / 未配置
- **首次构建时间**: ~2分钟（取决于文档大小）

### 方案2：Sentence-Transformers

- **Embedding模型**: paraphrase-multilingual-MiniLM-L12-v2
- **向量维度**: 384
- **成本**: 完全免费
- **API密钥**: 不需要
- **首次构建时间**: ~3分钟（首次需下载模型）

## 索引信息

- **文档数量**: [数量]
- **Chunks数量**: [数量]
- **向量数据库位置**: `./chroma_db/`
- **最后更新**: YYYY-MM-DD

## 使用说明

### 查询RAG

```bash
python scripts/rag_query.py "你的查询关键词"
```

### 更新索引

**推荐方法：增量更新（快85%）**

当策划文档更新后：
```bash
# 方案1：ZhipuAI
python rag/scripts/rag_update_zhipu.py

# 方案2：Sentence-Transformers
python rag/scripts/rag_update_st.py

# 验证
python rag/scripts/rag_query.py "测试查询"
```

**完全重建（必要时）**

仅在以下情况使用：
- 切换embedding方案
- 超过50%文档变更
- 数据库损坏
- 长时间未更新（>1个月）

```bash
# 删除旧索引
rm -rf rag/chroma_db/

# 重新构建
python rag/scripts/rag_setup.py

# 验证
python rag/scripts/rag_query.py "测试查询"
```

## 切换方案记录

**当前方案**: [方案1 / 方案2]

**切换历史**:
| 日期 | 从 | 到 | 原因 |
|------|-----|-----|------|
| YYYY-MM-DD | - | 方案1 | 初始配置 |
