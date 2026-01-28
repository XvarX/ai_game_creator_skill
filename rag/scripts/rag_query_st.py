"""
RAG Query Script - Sentence-Transformers (免费离线版本)
查询RAG索引 - 使用Sentence-Transformers

用法:
    python rag_query_st.py "查询关键词"

示例:
    python rag_query_st.py "伤害计算 公式"
    python rag_query_st.py "角色升级 经验值"
"""
import chromadb
from sentence_transformers import SentenceTransformer
import sys
from chromadb.utils import embedding_functions

# 🔧 修复Windows控制台UTF-8编码问题
# 这确保在Windows环境下print输出中文不会乱码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 加载模型
print("[INFO] 正在加载sentence-transformers模型...")
try:
    model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
    print("[OK] 模型加载成功")
except Exception as e:
    print(f"[ERROR] 模型加载失败: {e}")
    print("[INFO] 请先安装: pip install sentence-transformers")
    sys.exit(1)

# 创建embedding函数
def embed_query(text):
    return model.encode(text, convert_to_numpy=True).tolist()

embedding_function = chromadb.utils.embedding_functions.CustomEmbeddingFunction(
    embedding_function=embed_query
)

# 连接数据库
print("[INFO] 正在连接向量数据库...")
try:
    client = chromadb.PersistentClient(path="rag/chroma_db")
    collection = client.get_collection(
        name="docs",
        embedding_function=embedding_function
    )
    print("[OK] 向量数据库连接成功")
except Exception as e:
    print(f"[ERROR] 向量数据库连接失败: {e}")
    print("[INFO] 请确保已经运行: python rag/scripts/rag_setup.py")
    sys.exit(1)

# 获取查询参数
query = sys.argv[1] if len(sys.argv) > 1 else "移动控制"

# 执行查询
print(f"\n[查询] {query}\n")
print("=" * 60)

try:
    results = collection.query(
        query_texts=[query],
        n_results=3
    )
except Exception as e:
    print(f"[ERROR] 查询失败: {e}")
    sys.exit(1)

# 输出结果
if results and results['documents'] and len(results['documents'][0]) > 0:
    docs = results['documents'][0]
    metadatas = results['metadatas'][0]

    for i, (doc_id, distance, metadata, document) in enumerate(
        zip(
            results['ids'][0],
            results['distances'][0],
            metadatas,
            docs
        ),
        1
    ):
        print(f"\n[结果 {i}/{len(docs)}] 来源: {metadata.get('source', 'unknown')}")
        print(f"[相似度] {1-distance:.2f}")  # 转换为相似度
        print("-" * 60)

        content = document

        # 限制输出长度
        if len(content) > 800:
            content = content[:800] + f"\n... (内容过长，已截断，完整内容{len(content)}字符)"
        print(content)
        print("-" * 60)

    print(f"\n[完成] 检索到 {len(docs)} 个相关文档片段")
    print(f"[提示] 嵌入维度: 384 (sentence-transformers)")
    print(f"[提示] 模型: paraphrase-multilingual-MiniLM-L12-v2")
else:
    print("[WARNING] 未找到相关文档")
    print(f"[INFO] 查询: {query}")
