# RAG方案快速切换指南

本文档说明如何在两种RAG方案之间切换。

## 两种方案对比

| 特性 | 方案1：智谱AI | 方案2：Sentence-Transformers |
|------|-------------|---------------------|
| **成本** | ~0.01元/月 | 完全免费 |
| **精度** | 高（专业优化） | 中等（开源模型） |
| **中文支持** | 专门优化 | 通用支持 |
| **网络要求** | 需要API调用 | 完全离线 |
| **本地计算** | 不需要 | 需要CPU/内存 |
| **首次使用** | 需API密钥 | 需下载模型(~400MB) |

## 从方案1切换到方案2

### 步骤

1. **卸载zai-sdk**（可选）
```bash
pip uninstall zai-sdk -y
```

2. **安装sentence-transformers**
```bash
pip install sentence-transformers
```

3. **更新scripts/rag_setup.py**

将整个文件替换为：

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
text_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[("#", "##", "###")]
)
splits = []
for doc in documents:
    docs = text_splitter.split_text(doc.page_content)
    for split_doc in docs:
        split_doc.metadata['source'] = doc.metadata.get('source', 'unknown')
    splits.extend(docs)

print(f"[OK] Split into {len(splits)} chunks")

# Load model
print("[INFO] Loading sentence-transformers model (first run may take a minute)...")
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# Embedding function
def embed_documents(texts):
    return model.encode(texts, convert_to_numpy=True).tolist()

embedding_function = embedding_functions.CustomEmbeddingFunction(
    embedding_function=embed_documents
)

# Build vector database
print("[INFO] Building vector database with sentence-transformers...")
client = chromadb.PersistentClient(path="./chroma_db")
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

print(f"\n[SUCCESS] RAG index built!")
print(f"  Documents: {len(documents)}")
print(f"  Chunks: {len(splits)}")
print(f"  Model: sentence-transformers")
print(f"  Cost: FREE")
```

4. **更新scripts/rag_query.py**

将整个文件替换为：

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
client = chromadb.PersistentClient(path="./chroma_db")
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
print(f"\n[RESULT] Found {len(results['ids'][0])} relevant chunks:\n")

for i, (doc_id, distance, metadata, document) in enumerate(
    zip(
        results['ids'][0],
        results['distances'][0],
        results['metadatas'][0],
        results['documents'][0]
    ),
    1
):
    print(f"[Chunk {i}]")
    print(f"Source: {metadata['source']}")
    print(f"Content:\n{document}\n")
    print("-" * 60)
```

5. **删除旧数据库**
```bash
rm -rf chroma_db/
```

6. **重建索引**
```bash
python scripts/rag_setup.py
```

7. **更新配置文档**
更新 `docs/RAG配置.md`，将方案改为"方案2"。

## 从方案2切换到方案1

### 步骤

1. **安装zai-sdk**
```bash
pip install zai-sdk
```

2. **获取API密钥**

访问 https://open.bigmodel.cn/ 注册并获取免费API密钥

3. **配置环境变量**

创建或更新 `.env` 文件：
```bash
ZHIPUAI_API_KEY=your_api_key_here
```

4. **更新scripts/rag_setup.py**

将整个文件替换为智谱AI版本（见本文档上方"方案1"部分）。

5. **更新scripts/rag_query.py**

将整个文件替换为智谱AI版本（见本文档上方"方案1"部分）。

6. **删除旧数据库**
```bash
rm -rf chroma_db/
```

7. **重建索引**
```bash
python scripts/rag_setup.py
```

8. **更新配置文档**
更新 `docs/RAG配置.md`，将方案改为"方案1"。

## 验证切换

无论哪种方案，验证方式相同：

```bash
# 测试查询
python scripts/rag_query.py "伤害计算"

# 应该返回3个相关chunks
```

## 注意事项

### 切换前备份

虽然切换过程很简单，但建议：
1. 备份当前的 `chroma_db/` 文件夹（可选）
2. 确保所有依赖都已安装

### 数据兼容性

**重要**：两种方案的向量格式不同：
- 智谱AI：1024维向量
- Sentence-Transformers：384维向量

因此**必须重新构建索引**，不能直接复用。

### 成本影响

- **切换到方案1**：开始产生API费用（但很少）
- **切换到方案2**：变为完全免费

## 推荐使用场景

### 使用方案1（智谱AI）如果你：
- ✅ 追求更高的检索精度
- ✅ 项目需要准确的中文语义理解
- ✅ 不在意每月<0.01元的成本
- ✅ 有稳定的网络连接

### 使用方案2（Sentence-Transformers）如果你：
- ✅ 需要完全离线工作
- ✅ 对成本敏感（即使是很少的费用）
- ✅ 数据隐私要求高
- ✅ 本地有足够的计算资源

## 总结

两种方案功能完全相同，区别仅在于：
- **精度**：智谱AI更高
- **成本**：Sentence-Transformers免费
- **便利性**：智谱AI不需要本地计算

**推荐**：大部分项目使用方案1（智谱AI），除非有特殊需求（离线、隐私等）。
