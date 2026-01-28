"""
RAG Query Script - ZhipuAI Embedding-3
查询RAG索引 - 使用智谱AI Embedding-3

用法:
    python rag_query.py "查询关键词"

示例:
    python rag_query.py "伤害计算 公式"
    python rag_query.py "角色升级 经验值"
"""
from langchain_chroma import Chroma
from zai import ZhipuAiClient
import os
import sys
from dotenv import load_dotenv

# 🔧 修复Windows控制台UTF-8编码问题
# 这确保在Windows环境下print输出中文不会乱码
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

load_dotenv("rag/.env")

# 检查API密钥
if not os.getenv("ZHIPUAI_API_KEY"):
    print("[ERROR] ZHIPUAI_API_KEY not found in rag/.env")
    print("[INFO] Please create rag/.env with: ZHIPUAI_API_KEY=your_key_here")
    sys.exit(1)

client = ZhipuAiClient(api_key=os.getenv("ZHIPUAI_API_KEY"))

class ZhipuEmbeddings:
    """智谱AI Embedding-3 包装类"""
    def __init__(self, client, dimensions=1024):
        self.client = client
        self.dimensions = dimensions

    def embed_query(self, text):
        """嵌入查询文本"""
        response = self.client.embeddings.create(
            model="embedding-3",
            input=[text],
            dimensions=self.dimensions
        )
        return response.data[0].embedding

    def embed_documents(self, texts):
        """批量嵌入（本脚本不需要）"""
        pass

# 加载向量数据库
print("[INFO] 正在加载向量数据库...")
try:
    embeddings = ZhipuEmbeddings(client, dimensions=1024)
    vectordb = Chroma(
        persist_directory="rag/chroma_db",
        embedding_function=embeddings
    )
    print("[OK] 向量数据库加载成功")
except Exception as e:
    print(f"[ERROR] 向量数据库加载失败: {e}")
    print("[INFO] 请确保已经运行: python rag/scripts/rag_setup.py")
    sys.exit(1)

# 获取查询参数
query = sys.argv[1] if len(sys.argv) > 1 else "移动控制"

# 执行查询
print(f"\n[查询] {query}\n")
print("=" * 60)

try:
    docs = vectordb.similarity_search(query, k=3)
except Exception as e:
    print(f"[ERROR] 查询失败: {e}")
    sys.exit(1)

# 输出结果
for i, doc in enumerate(docs, 1):
    print(f"\n[结果 {i}/{len(docs)}] 来源: {doc.metadata.get('source', 'unknown')}")
    print("-" * 60)

    content = doc.page_content

    # 限制输出长度，避免终端滚动过长
    if len(content) > 800:
        content = content[:800] + f"\n... (内容过长，已截断，完整内容{len(content)}字符)"
    print(content)
    print("-" * 60)

print(f"\n[完成] 检索到 {len(docs)} 个相关文档片段")
print(f"[提示] 嵌入维度: 1024 (ZhipuAI Embedding-3)")
