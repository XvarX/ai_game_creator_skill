"""
RAG Utilities - Cross-platform helper functions
RAG工具集 - 跨平台辅助函数

This script provides cross-platform utilities for RAG management,
avoiding platform-specific shell commands.

Usage:
    python rag_utils.py check          # Check if RAG exists
    python rag_utils.py clean          # Delete RAG database
    python rag_utils.py setup_zhipu    # Setup ZhipuAI RAG
    python rag_utils.py setup_st       # Setup Sentence-Transformers RAG
"""

import os
import sys
import shutil
import subprocess

def check_rag_exists():
    """Check if RAG database exists"""
    rag_db_path = os.path.join("rag", "chroma_db")
    exists = os.path.isdir(rag_db_path)
    if exists:
        print(f"[OK] RAG database exists at {rag_db_path}")
        return True
    else:
        print(f"[INFO] RAG database not found at {rag_db_path}")
        return False

def clean_rag_db():
    """Delete RAG database"""
    rag_db_path = os.path.join("rag", "chroma_db")
    if os.path.exists(rag_db_path):
        print(f"[INFO] Deleting RAG database at {rag_db_path}...")
        try:
            shutil.rmtree(rag_db_path)
            print("[OK] RAG database deleted successfully")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to delete RAG database: {e}")
            return False
    else:
        print(f"[INFO] RAG database not found at {rag_db_path}, nothing to delete")
        return True

def setup_rag_zhipu():
    """Setup RAG with ZhipuAI"""
    print("[INFO] Setting up RAG with ZhipuAI Embedding-3...")
    script_path = os.path.join("rag", "scripts", "rag_setup_zhipu.py")
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"[ERROR] Script not found: {script_path}")

def setup_rag_st():
    """Setup RAG with Sentence-Transformers"""
    print("[INFO] Setting up RAG with Sentence-Transformers...")
    script_path = os.path.join("rag", "scripts", "rag_setup_st.py")
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"[ERROR] Script not found: {script_path}")

def update_rag_zhipu():
    """Incremental update with ZhipuAI"""
    print("[INFO] Incremental update with ZhipuAI...")
    script_path = os.path.join("rag", "scripts", "rag_update_zhipu.py")
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"[ERROR] Script not found: {script_path}")

def update_rag_st():
    """Incremental update with Sentence-Transformers"""
    print("[INFO] Incremental update with Sentence-Transformers...")
    script_path = os.path.join("rag", "scripts", "rag_update_st.py")
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"[ERROR] Script not found: {script_path}")

def update_keyword_index():
    """Update keyword index"""
    print("[INFO] Updating keyword index...")
    script_path = os.path.join("rag", "scripts", "update_keyword_index.py")
    if os.path.exists(script_path):
        subprocess.run([sys.executable, script_path])
    else:
        print(f"[ERROR] Script not found: {script_path}")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nAvailable commands:")
        print("  check          - Check if RAG database exists")
        print("  clean          - Delete RAG database (full rebuild)")
        print("  setup_zhipu    - Setup RAG with ZhipuAI")
        print("  setup_st       - Setup RAG with Sentence-Transformers")
        print("  update_zhipu   - Incremental update (ZhipuAI)")
        print("  update_st      - Incremental update (Sentence-Transformers)")
        print("  update_index   - Update keyword index")
        return

    command = sys.argv[1]

    if command == "check":
        check_rag_exists()
    elif command == "clean":
        clean_rag_db()
    elif command == "setup_zhipu":
        setup_rag_zhipu()
    elif command == "setup_st":
        setup_rag_st()
    elif command == "update_zhipu":
        update_rag_zhipu()
    elif command == "update_st":
        update_rag_st()
    elif command == "update_index":
        update_keyword_index()
    else:
        print(f"[ERROR] Unknown command: {command}")
        print("Run without arguments to see available commands")

if __name__ == "__main__":
    main()
