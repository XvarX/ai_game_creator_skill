# Scripts

本文件夹包含游戏开发实用工具脚本。

## 可用脚本

### config_loader.py - 配置表加载工具

**用途**：加载 `planner_config/` 下的 CSV 配置表文件

**功能**：
- `ConfigLoader` - 基础CSV加载器，支持类型转换和缓存
- `GameConfig` - 高级配置管理器，预加载所有配置并提供便捷访问接口

**使用方法**：

1. 将 `config_loader.py` 复制到你项目的 `code/common/` 目录
2. 根据你的实际配置表调整 `GameConfig` 类中的加载逻辑
3. 在游戏代码中导入使用：

```python
from code.common.config_loader import GameConfig

# 初始化（加载所有配置表）
config = GameConfig()

# 访问配置数据
level_3_attrs = config.get_character_attributes(level=3)
print(f"HP: {level_3_attrs['HP']}")
```

**详细文档**：参见脚本文件内的文档字符串

---

## 脚本使用指南

### 对于程序员

1. **复制脚本到项目**：
   - 将需要的脚本复制到 `code/common/` 或 `code/utils/`
   - 根据项目需求调整脚本

2. **参考实现**：
   - 脚本包含完整的使用示例
   - 可作为参考实现你自己的配置加载逻辑

3. **注意事项**：
   - 脚本使用 UTF-8 编码读取CSV
   - 第一行为列名，从第二行开始读取数据
   - 支持 `#` 开头的注释行

### 对于维护者

这些脚本是参考实现，可以根据实际项目需求调整：

- **修改加载逻辑**：根据你的配置表结构调整
- **添加新功能**：扩展配置管理器支持更多表类型
- **优化性能**：添加缓存、延迟加载等优化
