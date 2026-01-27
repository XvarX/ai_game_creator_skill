# RAG实际使用示例

## 场景1：程序员角色实现伤害计算系统

### 传统方式（不使用RAG）

```
💻 切换到程序员角色...

[程序员] 我需要实现伤害计算系统，让我先阅读相关文档...

读取 docs/战斗模块/伤害系统_v1.md (6,000字)
读取 docs/角色模块/属性系统_v1.md (5,000字)
读取 docs/战斗模块/状态系统_v1.md (4,000字)
读取 docs/战斗模块/技能系统_v1.md (5,000字)

总计读取：20,000字
消耗token：~27,000 tokens
```

### RAG方式（使用RAG）

```
💻 切换到程序员角色...

[程序员] 我需要实现伤害计算系统，让我查询相关文档...

执行：python scripts/rag_query.py "伤害计算 公式 暴击"

返回：
=== Chunk 1 from 伤害系统_v1.md ===
## 数值参数
- 基础伤害：攻击力 - 防御力
- 暴击倍率：2.0
- 暴击率：暴击属性 / 100

## 公式说明
final_damage = base_damage * crit_multiplier

=== Chunk 2 from 属性系统_v1.md ===
## 攻击力计算
total_attack = base_attack + weapon_attack

=== Chunk 3 from 状态系统_v1.md ===
## 暴击状态
暴击时伤害 × 2

总计读取：3个chunks，约1,500字
消耗token：~2,000 tokens
节省：92.6%
```

### 实现代码

```python
class DamageSystem:
    def calculate_damage(self, attacker, defender):
        # 基于RAG检索到的文档实现
        base_attack = attacker.base_attack + attacker.weapon.attack
        base_defense = defender.base_defense + defender.armor.defense

        base_damage = max(0, base_attack - base_defense)

        # 暴击检测（来自Chunk 1和3）
        if random.random() * 100 < attacker.crit_rate:
            base_damage *= 2.0  # 暴击倍率

        return base_damage
```

---

## 场景2：策划角色调整平衡性

### 传统方式

```
📝 切换到执行策划角色...

[策划] 老板要求调整暴击机制，让我看看受影响的系统...

读取 docs/战斗模块/伤害系统_v1.md
读取 docs/战斗模块/状态系统_v1.md
读取 docs/角色模块/属性系统_v1.md
读取 docs/战斗模块/技能系统_v1.md
读取 docs/装备模块/装备系统_v1.md

总计：25,000字
```

### RAG方式

```
📝 切换到执行策划角色...

[策划] 老板要求调整暴击机制，让我看看受影响的系统...

执行：python scripts/rag_query.py "暴击 伤害 装备 属性"

返回：
=== Chunk 1 from 伤害系统_v1.md ===
暴击倍率：2.0

=== Chunk 2 from 属性系统_v1.md ===
暴击属性来源：装备、天赋、buff

=== Chunk 3 from 装备系统_v1.md ===
装备提供暴击率加成

[策划] 分析：需要同步更新伤害系统、属性系统和装备系统的暴击相关参数。
只读取了3个chunks，约1,200字，节省90%
```

---

## 场景3：测试员验证实现

### 传统方式

```
🔍 切换到测试员角色...

[测试员] 需要验证暴击伤害是否正确，让我查看设计文档...

读取所有战斗相关文档（30,000字）
逐一对比代码实现
```

### RAG方式

```
🔍 切换到测试员角色...

[测试员] 需要验证暴击伤害是否正确...

执行：python scripts/rag_query.py "暴击 倍率 验证"

返回：
=== Chunk 1 from 伤害系统_v1.md ===
暴击倍率：2.0
暴击伤害 = 基础伤害 × 2.0

[测试员] 验证：
1. 代码中是否使用2.0作为倍率？✓
2. 暴击伤害计算是否正确？✓

只读取了1个chunk，约400字，节省98%
```

---

## Token消耗对比

| 操作 | 传统方式 | RAG方式 | 节省 |
|------|---------|---------|------|
| 程序员实现伤害系统 | 27,000 tokens | 2,000 tokens | 92.6% |
| 策划调整暴击机制 | 33,000 tokens | 1,200 tokens | 96.4% |
| 测试员验证实现 | 40,000 tokens | 400 tokens | 99.0% |
| **平均节省** | - | - | **~95%** |

---

## 实际使用流程

### 1. 构建RAG索引（一次性）

```bash
# 在Phase 3.6由程序员角色执行
python scripts/rag_setup.py

# 输出：
# [SUCCESS] RAG index built with 187 chunks
# Cost: ~0.0009 CNY
```

### 2. 各角色使用RAG

```python
# 任何角色都可以调用
import subprocess

def query_docs(question):
    """查询策划文档"""
    result = subprocess.run([
        "python", "scripts/rag_query.py", question
    ], capture_output=True, text=True)
    return result.stdout

# 使用示例
relevant_docs = query_docs("伤害计算公式")
print(relevant_docs)
# Claude现在只需要阅读这3个chunks，而不是全部文档
```

### 3. Claude基于检索结果工作

```
Claude的工作流程：
1. 接收任务
2. 调用RAG查询相关文档
3. 阅读返回的3个chunks（不是全部文档）
4. 基于检索结果完成任务
5. 消耗token减少90-95%
```

---

## 核心优势总结

✅ **极低成本**：智谱embedding，0.5元/百万tokens
✅ **纯检索模式**：不调用LLM生成答案，Claude自己理解
✅ **语义搜索**：理解查询意图，不是简单关键词
✅ **Token高效**：平均节省95% tokens
✅ **易于使用**：一行命令查询，返回可读文档chunks
