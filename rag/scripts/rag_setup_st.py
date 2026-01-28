"""
RAG Setup Script - Sentence-Transformers (Free & Offline)
构建RAG索引 - 使用Sentence-Transformers（免费离线）

This script builds a RAG (Retrieval-Augmented Generation) index from markdown documents
using Sentence-Transformers for free, offline semantic search.

Usage:
    python rag_setup_st.py

Requirements:
    - pip install langchain langchain-community langchain-chroma chromadb sentence-transformers

Cost:
    - FREE (no API costs)
    - Runs locally on your machine
"""

from langchain_chroma import Chroma
from langchain_text_splitters import MarkdownHeaderTextSplitter
from langchain_core.documents import Document
from sentence_transformers import SentenceTransformer
import os
import sys
import chromadb
from chromadb.utils import embedding_functions

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
    """Build and persist RAG index using Sentence-Transformers"""
    print("[INFO] Building RAG index with Sentence-Transformers...")

    # Download/load model (first run downloads ~400MB)
    print("[INFO] Loading sentence-transformers model...")
    print("[INFO] (First run downloads ~400MB model file, please wait...)")

    try:
        model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
        print("[OK] Model loaded successfully")
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}")
        print("[INFO] Please check your internet connection (first run requires download)")
        sys.exit(1)

    # Create embedding function
    def embed_documents(texts):
        """Embed multiple documents"""
        return model.encode(texts, convert_to_numpy=True).tolist()

    def embed_query(text):
        """Embed a single query text"""
        return model.encode(text, convert_to_numpy=True).tolist()

    embedding_function = embedding_functions.CustomEmbeddingFunction(
        embedding_function=embed_documents
    )

    # Build vector database
    try:
        print("[INFO] Building vector database...")

        # Use ChromaDB directly with custom embedding
        client = chromadb.PersistentClient(path=persist_directory)
        collection = client.get_or_create_collection(
            name="docs",
            embedding_function=embedding_function
        )

        # Prepare data
        ids = [f"doc_{i}" for i in range(len(splits))]
        documents_text = [split.page_content for split in splits]
        metadatas = [split.metadata for split in splits]

        # Add to collection
        collection.add(
            ids=ids,
            documents=documents_text,
            metadatas=metadatas
        )

        print(f"\n[SUCCESS] RAG index built successfully!")
        print(f"  - Chunks: {len(splits)}")
        print(f"  - Embedding: sentence-transformers (384 dimensions)")
        print(f"  - Model: paraphrase-multilingual-MiniLM-L12-v2")
        print(f"  - Storage: {persist_directory}")
        print(f"  - Cost: FREE")
        print(f"\n[INFO] You can now query RAG using:")
        print(f"  python rag/scripts/rag_query_st.py \"your query\"")

        return collection

    except Exception as e:
        print(f"[ERROR] Failed to build RAG index: {e}")
        sys.exit(1)

def main():
    """Main execution flow"""
    print("=" * 60)
    print("RAG Index Builder - Sentence-Transformers (Free)")
    print("=" * 60)

    # Step 1: Load documents
    documents = load_documents("docs/")

    # Step 2: Split documents
    splits = split_documents(documents)

    # Step 3: Build RAG index
    collection = build_rag_index(splits, "rag/chroma_db")

    print("\n" + "=" * 60)
    print("[INFO] Next steps:")
    print("  1. Update keyword index: python rag/scripts/update_keyword_index.py")
    print("  2. Test RAG query: python rag/scripts/rag_query_st.py \"test query\"")
    print("=" * 60)

if __name__ == "__main__":
    main()
