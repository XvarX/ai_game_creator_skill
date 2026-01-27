# 智谱RAG集成指南

本文档指导游戏项目使用LangChain + ChromaDB + 智谱AI Embedding构建RAG系统。

## 为什么选择这个方案？

**核心优势**：
- ✅ **极低成本**：智谱embedding只需0.5元/百万tokens
- ✅ **纯检索模式**：不调用LLM生成答案，Claude自己理解检索结果
- ✅ **专业框架**：LangChain + ChromaDB工业级方案
- ✅ **中文优化**：智谱Embedding-3专门针对中文优化
- ✅ **本地存储**：向量数据库持久化本地，无需重复调用API
- ✅ **Token高效**：平均节省80-90% tokens

## 工作原理

```
用户提问
    ↓
智谱AI Embedding-3转向量（1024维）
    ↓
ChromaDB向量检索
    ↓
返回最相关的3个文档chunks
    ↓
Claude自己阅读并理解这些chunks
    ↓
Claude根据检索结果完成任务
```

**关键点**：只有embedding使用智谱API，Claude自己（不调用其他LLM）理解检索结果。

## 快速开始

### 1. 安装依赖

```bash
pip install langchain langchain-community langchain-chroma chromadb zai-sdk python-dotenv
```

### 2. 配置API密钥

创建 `.env` 文件：
```bash
ZHIPUAI_API_KEY=your_api_key_here
```

获取API密钥：https://open.bigmodel.cn/

### 3. 构建RAG索引

创建 `scripts/rag_setup.py`：

```python
from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from zai import ZhipuAiClient
import os
from dotenv import load_dotenv

load_dotenv()

# 配置
DOCS_DIR = "docs/"
PERSIST_DIR = "./chroma_db"

# 1. 加载文档
print("[INFO] Loading documents...")
documents = []
for filename in os.listdir(DOCS_DIR):
    if filename.endswith('.md'):
        with open(f"{DOCS_DIR}{filename}", 'r', encoding='utf-8') as f:
            content = f.read()
        documents.append(Document(page_content=content, metadata={'source': filename}))

print(f"[OK] Loaded {len(documents)} documents")

# 2. 按Markdown标题切分
print("[INFO] Splitting documents...")
text_splitter = MarkdownHeaderTextSplitter(
    headers_to_split_on=[
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ],
)

splits = []
for doc in documents:
    docs = text_splitter.split_text(doc.page_content)
    for split_doc in docs:
        split_doc.metadata['source'] = doc.metadata.get('source', 'unknown')
    splits.extend(docs)

print(f"[OK] Split into {len(splits)} chunks")

# 3. 使用智谱embedding
print("[INFO] Connecting to ZhipuAI...")
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

# 4. 创建向量数据库
print("[INFO] Building vector database with ZhipuAI Embedding-3...")
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory=PERSIST_DIR
)

print(f"\n[SUCCESS] RAG index built!")
print(f"  Documents: {len(documents)}")
print(f"  Chunks: {len(splits)}")
print(f"  Location: {PERSIST_DIR}")
print(f"  Cost: ~{len(splits) * 0.5 / 100000:.4f} CNY")
```

运行构建脚本：
```bash
python scripts/rag_setup.py

# 输出示例：
# [INFO] Loading documents...
# [OK] Loaded 25 documents
# [INFO] Splitting documents...
# [OK] Split into 187 chunks
# [INFO] Connecting to ZhipuAI...
# [INFO] Building vector database with ZhipuAI Embedding-3...
#
# [SUCCESS] RAG index built!
#   Documents: 25
#   Chunks: 187
#   Location: ./chroma_db
#   Cost: ~0.0009 CNY
```

### 4. 查询RAG

创建 `scripts/rag_query.py`：

```python
from langchain_chroma import Chroma
from zai import ZhipuAiClient
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Setup
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
    persist_directory="./chroma_db",
    embedding_function=embeddings
)

# Query
query = sys.argv[1] if len(sys.argv) > 1 else "伤害计算"
docs = vectordb.similarity_search(query, k=3)

# Return results
for i, doc in enumerate(docs, 1):
    print(f"\n{'='*60}")
    print(f"Chunk {i} from {doc.metadata['source']}")
    print(f"{'='*60}")
    print(doc.page_content)
```

查询示例：
```bash
# 查询伤害计算
python scripts/rag_query.py "伤害计算公式 暴击"

# 查询角色成长
python scripts/rag_query.py "等级升级 经验值"

# 查询战斗系统
python scripts/rag_query.py "战斗 伤害 状态"
```

## 实际使用场景

### 场景1：程序员实现功能

```python
import subprocess

# 程序员需要实现伤害计算系统
query_result = subprocess.run([
    "python", "scripts/rag_query.py",
    "伤害计算 公式 暴击"
], capture_output=True, text=True)

# 只获取相关的3个chunks，约2,000字
# 而不是全部文档150,000字
# 节省98.6% tokens

# Claude阅读query_result并实现代码
```

### 场景2：策划调整设计

```python
# 策划需要调整暴击机制
query_result = subprocess.run([
    "python", "scripts/rag_query.py",
    "暴击 伤害 装备 属性"
], capture_output=True, text=True)

# 获取相关的文档chunks
# 了解哪些系统需要同步更新
# 节省95% tokens
```

### 场景3：测试员验证实现

```python
# 测试员需要验证暴击伤害
query_result = subprocess.run([
    "python", "scripts/rag_query.py",
    "暴击 倍率 验证"
], capture_output=True, text=True)

# 获取设计规范
# 对比代码实现
# 节省99% tokens
```

## 成本估算

### 构建索引（一次性）

假设15万字文档，约1000个chunks：
- Embedding成本：1000 × 0.5 / 100000 = **0.005元**

### 查询（每次）

- Embedding查询：~0.000005元
- 月查询1000次：**0.005元**

### 总成本

- 初期：0.005元（一次性）
- 月度：<0.01元
- **几乎免费**

## 向量维度选择

智谱Embedding-3支持自定义维度（256-2048）：

| 维度 | 精度 | 适用场景 | 推荐 |
|------|------|----------|------|
| 2048维 | 最高 | 高精度需求 | ❌ 过度 |
| **1024维** | **高** | **通用场景** | **✅ 推荐** |
| 512维 | 中等 | 大规模部署 | 可选 |
| 256维 | 较高 | 实时检索 | 可选 |

**默认使用1024维**（性价比最优）。

## 更新索引

当策划文档更新后：

```bash
# 重新构建索引
python scripts/rag_setup.py

# ChromaDB会自动更新
```

## 故障排查

### 问题1：API密钥错误

```
Error: ZHIPUAI_API_KEY not found
```

解决：
1. 检查 `.env` 文件是否存在
2. 检查 `ZHIPUAI_API_KEY` 是否配置
3. 重新加载环境变量

### 问题2：向量数据库损坏

```
Error: Chroma DB persist failed
```

解决：
```bash
# 删除旧数据库
rm -rf chroma_db/

# 重新构建
python scripts/rag_setup.py
```

### 问题3：Python版本兼容性

推荐使用Python 3.10-3.12，避免使用3.13+（部分包可能不兼容）。

## 总结

使用智谱AI + ChromaDB构建RAG的优势：

- ✅ **成本极低**：几乎免费（<0.01元/月）
- ✅ **纯检索**：Claude自己理解，不依赖其他LLM
- ✅ **Token高效**：平均节省80-90% tokens
- ✅ **中文优化**：智谱Embedding-3专门优化
- ✅ **易于使用**：一行命令查询
- ✅ **本地存储**：向量数据库持久化

推荐所有中型到大型游戏项目使用！
