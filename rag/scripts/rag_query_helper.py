"""
RAG查询辅助工具类
提供简洁的API查询RAG，自动处理编码问题
"""

import subprocess
import sys
from typing import Optional


class RAGQueryHelper:
    """RAG查询辅助类"""

    def __init__(self, use_zhipu: bool = True):
        """
        初始化RAG查询助手

        Args:
            use_zhipu: True使用ZhipuAI，False使用Sentence-Transformers
        """
        self.script = "rag/scripts/rag_query.py" if use_zhipu else "rag/scripts/rag_query_st.py"

    def query(self, keywords: str, timeout: int = 30) -> Optional[str]:
        """
        查询RAG

        Args:
            keywords: 查询关键词
            timeout: 超时时间（秒）

        Returns:
            查询结果文本，失败返回None
        """
        try:
            result = subprocess.run([
                sys.executable,
                self.script,
                keywords
            ], capture_output=True, text=True, encoding='utf-8', timeout=timeout)

            if result.returncode == 0:
                return result.stdout
            else:
                print(f"[ERROR] {result.stderr}")
                return None
        except subprocess.TimeoutExpired:
            print(f"[ERROR] Query timeout after {timeout}s")
            return None
        except Exception as e:
            print(f"[ERROR] Query failed: {e}")
            return None

    def query_and_print(self, keywords: str) -> bool:
        """
        查询并打印结果

        Args:
            keywords: 查询关键词

        Returns:
            成功返回True，失败返回False
        """
        content = self.query(keywords)
        if content:
            print(content)
            return True
        else:
            print(f"[ERROR] Failed to query: {keywords}")
            return False


# 使用示例
if __name__ == "__main__":
    # 使用ZhipuAI版本
    print("=== 测试ZhipuAI版本 ===")
    helper = RAGQueryHelper(use_zhipu=True)
    helper.query_and_print("伤害计算 公式")

    print("\n=== 测试Sentence-Transformers版本 ===")
    # 或使用Sentence-Transformers版本
    helper_st = RAGQueryHelper(use_zhipu=False)
    helper_st.query_and_print("等级升级 经验值")
