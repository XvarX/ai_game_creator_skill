"""
RAG Setup Script - ZhipuAI Embedding-3
构建RAG索引 - 使用智谱AI Embedding-3

This script builds a RAG (Retrieval-Augmented Generation) index from markdown documents
using ZhipuAI's Embedding-3 model for high-quality Chinese semantic search.

Usage:
    python rag_setup_zhipu.py

Requirements:
    - ZHIPUAI_API_KEY in rag/.env
    - pip install langchain langchain-community langchain-chroma chromadb zai-sdk python-dotenv

Cost:
    - ~0.01 CNY/month for typical projects (15万字文档)
    - Pricing: https://open.bigmodel.cn/pricing
"""

from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from zai import ZhipuAiClient
import os
import sys
from dotenv import load_dotenv

# 🔧 修复Windows控制台UTF-8编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def load_documents(docs_dir="docs/"):
    """Load all markdown documents from docs/ directory"""
    print(f"[INFO] Loading documents from {docs_dir}...")

    if not os.path.exists(docs_dir):
        print(f"[ERROR] Directory '{docs_dir}' not found!")
        print("[INFO] Please create the directory and add design documents first.")
        sys.exit(1)

    documents = []
    for root, dirs, files in os.walk(docs_dir):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    # Store relative path as metadata
                    rel_path = os.path.relpath(filepath, docs_dir)
                    documents.append(Document(page_content=content, metadata={'source': rel_path}))
                except Exception as e:
                    print(f"[WARNING] Failed to read {filepath}: {e}")

    if not documents:
        print(f"[ERROR] No markdown files found in {docs_dir}")
        sys.exit(1)

    print(f"[OK] Loaded {len(documents)} documents")
    return documents

def split_documents(documents):
    """Split documents into chunks using markdown headers"""
    print("[INFO] Splitting documents into chunks...")

    text_splitter = MarkdownHeaderTextSplitter(
        headers_to_split_on=[("#", "Header 1"), ("##", "Header 2"), ("###", "Header 3")]
    )

    splits = []
    for doc in documents:
        try:
            docs = text_splitter.split_text(doc.page_content)
            for split_doc in docs:
                # Preserve original source metadata
                split_doc.metadata['source'] = doc.metadata.get('source', 'unknown')
            splits.extend(docs)
        except Exception as e:
            print(f"[WARNING] Failed to split {doc.metadata.get('source', 'unknown')}: {e}")

    print(f"[OK] Split into {len(splits)} chunks")
    return splits

def build_rag_index(splits, persist_directory="rag/chroma_db"):
    """Build and persist RAG index using ZhipuAI Embedding-3"""
    print("[INFO] Building RAG index with ZhipuAI Embedding-3...")

    # Initialize ZhipuAI client
    load_dotenv("rag/.env")

    if not os.getenv("ZHIPUAI_API_KEY"):
        print("[ERROR] ZHIPUAI_API_KEY not found in rag/.env")
        print("[INFO] Please create rag/.env with: ZHIPUAI_API_KEY=your_key_here")
        print("[INFO] Get free API key at: https://open.bigmodel.cn/")
        sys.exit(1)

    client = ZhipuAiClient(api_key=os.getenv("ZHIPUAI_API_KEY"))

    class ZhipuEmbeddings:
        """ZhipuAI Embedding-3 wrapper class"""
        def __init__(self, client, model="embedding-3", dimensions=1024):
            self.client = client
            self.model = model
            self.dimensions = dimensions

        def embed_documents(self, texts):
            """Embed multiple documents (batch processing)"""
            embeddings = []
            # ZhipuAI supports up to 64 texts per batch
            batch_size = 64
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                try:
                    response = self.client.embeddings.create(
                        model=self.model,
                        input=batch,
                        dimensions=self.dimensions
                    )
                    embeddings.extend([item.embedding for item in response.data])
                except Exception as e:
                    print(f"[WARNING] Batch {i//batch_size} failed: {e}")
                    # Add zero vectors as fallback
                    embeddings.extend([[0.0]*self.dimensions] * len(batch))
            return embeddings

        def embed_query(self, text):
            """Embed a single query text"""
            try:
                response = self.client.embeddings.create(
                    model=self.model,
                    input=[text],
                    dimensions=self.dimensions
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"[ERROR] Failed to embed query: {e}")
                return [0.0] * self.dimensions

    embeddings = ZhipuEmbeddings(client, dimensions=1024)

    # Build vector database
    try:
        vectordb = Chroma.from_documents(
            documents=splits,
            embedding=embeddings,
            persist_directory=persist_directory
        )

        # Calculate estimated cost
        total_chunks = len(splits)
        # ZhipuAI embedding-3 pricing: ~0.0001 CNY per 1K tokens (approximated)
        # Assuming ~500 tokens per chunk on average
        estimated_tokens = total_chunks * 500
        estimated_cost = (estimated_tokens / 1000) * 0.0001

        print(f"\n[SUCCESS] RAG index built successfully!")
        print(f"  - Chunks: {total_chunks}")
        print(f"  - Embedding: ZhipuAI Embedding-3 (1024 dimensions)")
        print(f"  - Storage: {persist_directory}")
        print(f"  - Estimated cost: ~{estimated_cost:.4f} CNY (one-time)")
        print(f"\n[INFO] You can now query RAG using:")
        print(f"  python rag/scripts/rag_query.py \"your query\"")

        return vectordb

    except Exception as e:
        print(f"[ERROR] Failed to build RAG index: {e}")
        sys.exit(1)

def main():
    """Main execution flow"""
    print("=" * 60)
    print("RAG Index Builder - ZhipuAI Embedding-3")
    print("=" * 60)

    # Step 1: Load documents
    documents = load_documents("docs/")

    # Step 2: Split documents
    splits = split_documents(documents)

    # Step 3: Build RAG index
    vectordb = build_rag_index(splits, "rag/chroma_db")

    print("\n" + "=" * 60)
    print("[INFO] Next steps:")
    print("  1. Update keyword index: python rag/scripts/update_keyword_index.py")
    print("  2. Test RAG query: python rag/scripts/rag_query.py \"test query\"")
    print("=" * 60)

if __name__ == "__main__":
    main()
