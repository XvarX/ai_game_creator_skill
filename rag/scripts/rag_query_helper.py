# RAG查询辅助函数

## 问题：Windows环境中文乱码

在Windows环境下使用subprocess调用RAG查询时，可能遇到中文乱码问题。

## 解决方案

### 方案1：使用encoding参数（推荐）

```python
import subprocess
import sys

def query_rag(keywords):
    """查询RAG（推荐方式，支持中文）"""
    result = subprocess.run([
        sys.executable,
        "rag/scripts/rag_query.py",
        keywords
    ], capture_output=True, text=True, encoding='utf-8')

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return None

    return result.stdout

# 使用示例
content = query_rag("伤害计算 公式")
print(content)
```

### 方案2：手动解码（备用方案）

如果方案1在特殊环境下仍有问题，使用手动解码：

```python
import subprocess
import sys

def query_rag_fallback(keywords):
    """查询RAG（备用方案，手动解码）"""
    result = subprocess.run([
        sys.executable,
        "rag/scripts/rag_query.py",
        keywords
    ], capture_output=True)  # 不使用text=True

    if result.returncode != 0:
        print(f"Error: {result.stderr.decode('utf-8', errors='ignore')}")
        return None

    # 手动解码，忽略错误字符
    return result.stdout.decode('utf-8', errors='ignore')

# 使用示例
content = query_rag_fallback("伤害计算 公式")
print(content)
```

### 方案3：自动检测并处理

```python
import subprocess
import sys
import locale

def query_rag_auto(keywords):
    """查询RAG（自动检测编码）"""
    # 尝试方案1
    try:
        result = subprocess.run([
            sys.executable,
            "rag/scripts/rag_query.py",
            keywords
        ], capture_output=True, text=True, encoding='utf-8', timeout=30)

        if result.returncode == 0:
            return result.stdout
    except Exception as e:
        print(f"Method 1 failed: {e}")

    # 尝试方案2
    try:
        result = subprocess.run([
            sys.executable,
            "rag/scripts/rag_query.py",
            keywords
        ], capture_output=True, timeout=30)

        if result.returncode == 0:
            # 尝试多种编码
            for encoding in ['utf-8', 'gbk', 'cp936', locale.getpreferredencoding()]:
                try:
                    return result.stdout.decode(encoding)
                except:
                    continue
    except Exception as e:
        print(f"Method 2 failed: {e}")

    return None

# 使用示例
content = query_rag_auto("伤害计算 公式")
if content:
    print(content)
else:
    print("Failed to query RAG")
```

## 完整工具类

```python
import subprocess
import sys
from typing import Optional

class RAGQueryHelper:
    """RAG查询辅助类 - 处理编码问题"""

    @staticmethod
    def query(keywords: str, timeout: int = 30) -> Optional[str]:
        """
        查询RAG（自动处理编码）

        Args:
            keywords: 查询关键词
            timeout: 超时时间（秒）

        Returns:
            查询结果文本，失败返回None
        """
        # 方法1：使用encoding参数
        try:
            result = subprocess.run([
                sys.executable,
                "rag/scripts/rag_query.py",
                keywords
            ], capture_output=True, text=True, encoding='utf-8', timeout=timeout)

            if result.returncode == 0 and result.stdout:
                return result.stdout
        except Exception:
            pass

        # 方法2：手动解码
        try:
            result = subprocess.run([
                sys.executable,
                "rag/scripts/rag_query.py",
                keywords
            ], capture_output=True, timeout=timeout)

            if result.returncode == 0 and result.stdout:
                # 尝试多种编码
                for encoding in ['utf-8', 'gbk', 'cp936']:
                    try:
                        return result.stdout.decode(encoding)
                    except UnicodeDecodeError:
                        continue
        except Exception:
            pass

        return None

    @staticmethod
    def query_and_print(keywords: str) -> bool:
        """查询并打印结果"""
        content = RAGQueryHelper.query(keywords)
        if content:
            print(content)
            return True
        else:
            print(f"[ERROR] Failed to query RAG for: {keywords}")
            return False

# 使用示例
if __name__ == "__main__":
    # 简单查询
    content = RAGQueryHelper.query("伤害计算 公式")
    if content:
        print(content)

    # 查询并打印
    RAGQueryHelper.query_and_print("等级升级 经验值")
```

## Claude使用方式

在Programmer或Tester角色中，直接使用工具类：

```python
# 导入工具类
import sys
sys.path.insert(0, '.')
from rag_query_helper import RAGQueryHelper

# 查询需求文档
content = RAGQueryHelper.query("伤害计算 公式 暴击")
if content:
    # 基于返回的内容实现功能
    # ...
else:
    print("[ERROR] RAG查询失败，无法获取需求")
```

## 常见问题排查

### 问题1：返回乱码
**症状**：输出显示为 `���` 或其他乱码字符

**解决**：使用方案2的手动解码方法

### 问题2：返回空字符串
**症状**：`result.stdout` 为空

**解决**：
1. 检查RAG索引是否构建：`test -d rag/chroma_db`
2. 检查查询脚本是否存在：`test -f rag/scripts/rag_query.py`
3. 尝试手动运行：`python rag/scripts/rag_query.py "测试"`

### 问题3：超时
**症状**：查询卡住不动

**解决**：
1. 检查文档数量是否过大（>1000个文档）
2. 检查RAG数据库是否损坏
3. 重建RAG索引

## 最佳实践

1. **始终使用sys.executable**：不要硬编码"python"
2. **设置超时**：避免查询无限等待
3. **检查返回值**：验证result.returncode == 0
4. **使用工具类**：RAGQueryHelper处理所有边界情况
5. **打印调试信息**：遇到问题时打印result.stderr
