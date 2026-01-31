"""
配置表加载工具 (通用版本)
Config Loader Utility

用途：提供通用的 CSV 配置表加载功能
使用：程序员根据项目需求调用工具函数

依赖：Python 3.6+
"""

import csv
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional, Callable, TypeVar

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

T = TypeVar('T')


def load_csv(
    relative_path: str,
    config_root: str = "planner_config",
    skip_comments: bool = True,
    encoding: str = "utf-8"
) -> List[Dict[str, str]]:
    """
    加载单个CSV配置文件

    Args:
        relative_path: 相对于 config_root 的文件路径，例如 "balance/角色属性表.csv"
        config_root: 配置表根目录，默认为 "planner_config"
        skip_comments: 是否跳过注释行（以 # 开头的行）
        encoding: 文件编码，默认为 utf-8

    Returns:
        包含所有行数据的字典列表，每行是一个字典，键为列名

    Raises:
        FileNotFoundError: 配置文件不存在
        ValueError: CSV格式错误

    Example:
        >>> data = load_csv("balance/角色属性表.csv")
        >>> print(data[0]["HP"])
    """
    csv_path = Path(config_root) / relative_path

    if not csv_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {csv_path}")

    logger.info(f"正在加载配置表: {csv_path}")

    try:
        with open(csv_path, 'r', encoding=encoding) as f:
            # 读取所有行
            lines = f.readlines()

            # 跳过注释行
            if skip_comments:
                data_start = 0
                for i, line in enumerate(lines):
                    if line.strip() and not line.strip().startswith('#'):
                        data_start = i
                        break

                # 重新构造文件内容用于解析
                content = ''.join(lines[data_start:])
            else:
                content = ''.join(lines)

            # 解析CSV
            reader = csv.DictReader(content.splitlines())
            data = list(reader)

        logger.info(f"✓ 加载成功: {len(data)} 行数据")
        return data

    except Exception as e:
        raise ValueError(f"CSV解析失败 ({csv_path}): {e}")


def load_csv_typed(
    relative_path: str,
    type_mapping: Dict[str, Callable[[str], T]],
    config_root: str = "planner_config",
    skip_comments: bool = True
) -> List[Dict[str, Any]]:
    """
    加载CSV并自动转换数据类型

    Args:
        relative_path: CSV文件相对路径
        type_mapping: 列名到转换函数的映射，例如 {"等级": int, "HP": int, "暴击率": float}
        config_root: 配置表根目录
        skip_comments: 是否跳过注释行

    Returns:
        数据类型已转换的字典列表

    Example:
        >>> type_map = {"等级": int, "HP": int, "攻击力": int, "暴击率": float}
        >>> data = load_csv_typed("balance/角色属性表.csv", type_map)
        >>> print(f"等级1的HP: {data[0]['HP']}, 类型: {type(data[0]['HP'])}")
    """
    raw_data = load_csv(relative_path, config_root, skip_comments)

    # 转换数据类型
    converted_data = []
    for row in raw_data:
        converted_row = {}
        for key, value in row.items():
            if key in type_mapping:
                try:
                    converted_row[key] = type_mapping[key](value)
                except (ValueError, TypeError) as e:
                    logger.warning(f"类型转换失败: {key}={value} ({e})")
                    converted_row[key] = value
            else:
                converted_row[key] = value
        converted_data.append(converted_row)

    return converted_data


def load_all_in_dir(
    dir_path: str,
    config_root: str = "planner_config",
    pattern: str = "*.csv"
) -> Dict[str, List[Dict[str, str]]]:
    """
    加载指定目录下的所有CSV文件

    Args:
        dir_path: 相对于 config_root 的目录路径，例如 "balance/"
        config_root: 配置表根目录
        pattern: 文件匹配模式，默认为 "*.csv"

    Returns:
        字典，键为文件名（不含扩展名），值为CSV数据

    Example:
        >>> balance_configs = load_all_in_dir("balance/")
        >>> print(list(balance_configs.keys()))  # ["角色属性表", "伤害系数表"]
    """
    result = {}
    dir_full_path = Path(config_root) / dir_path

    if not dir_full_path.exists():
        logger.warning(f"目录不存在: {dir_full_path}")
        return result

    csv_files = list(dir_full_path.glob(pattern))
    logger.info(f"在 {dir_path} 中发现 {len(csv_files)} 个CSV文件")

    for csv_file in csv_files:
        file_name = csv_file.stem  # 不含扩展名的文件名
        relative_path = f"{dir_path}/{csv_file.name}"
        try:
            result[file_name] = load_csv(relative_path, config_root)
        except Exception as e:
            logger.error(f"加载失败: {csv_file.name}: {e}")

    return result


def index_by_field(
    data: List[Dict[str, Any]],
    key_field: str
) -> Dict[Any, Dict[str, Any]]:
    """
    将数据列表按指定字段索引

    Args:
        data: 数据列表
        key_field: 作为索引的字段名

    Returns:
        以字段值为键的字典

    Example:
        >>> data = [{"ID": "W001", "名称": "木剑"}, {"ID": "W002", "名称": "铁剑"}]
        >>> indexed = index_by_field(data, "ID")
        >>> print(indexed["W001"]["名称"])  # "木剑"
    """
    return {row[key_field]: row for row in data}


def find_by_field(
    data: List[Dict[str, Any]],
    key_field: str,
    value: Any
) -> Optional[Dict[str, Any]]:
    """
    在数据列表中查找指定字段值等于给定值的行

    Args:
        data: 数据列表
        key_field: 字段名
        value: 要查找的值

    Returns:
        找到的行，如果未找到则返回 None

    Example:
        >>> data = [{"等级": 1, "HP": 100}, {"等级": 2, "HP": 120}]
        >>> row = find_by_field(data, "等级", 2)
        >>> print(row["HP"])  # 120
    """
    for row in data:
        if row.get(key_field) == value:
            return row
    return None


# ========================================
# 使用示例
# ========================================

def example_basic_usage():
    """基础使用示例"""
    print("\n" + "=" * 50)
    print("示例 1: 加载单个配置表")
    print("=" * 50)

    # 加载配置表
    data = load_csv("balance/角色属性表.csv")
    print(f"加载了 {len(data)} 行数据")
    print(f"第1行: {data[0]}")

    # 带类型转换的加载
    type_map = {"等级": int, "HP": int, "攻击力": int}
    typed_data = load_csv_typed("balance/角色属性表.csv", type_map)
    print(f"等级1的HP: {typed_data[0]['HP']}, 类型: {type(typed_data[0]['HP'])}")


def example_index_and_find():
    """索引和查找示例"""
    print("\n" + "=" * 50)
    print("示例 2: 索引和查找")
    print("=" * 50)

    # 加载装备表
    equipment = load_csv("items/装备配置表_武器.csv")

    # 按ID索引
    equipment_by_id = index_by_field(equipment, "ID")
    sword = equipment_by_id.get("W001")
    if sword:
        print(f"装备W001: {sword['名称']}")

    # 查找特定等级的装备
    type_map = {"等级": int}
    typed_equipment = load_csv_typed("items/装备配置表_武器.csv", type_map)
    level_5_sword = find_by_field(typed_equipment, "等级", 5)
    if level_5_sword:
        print(f"等级5武器: {level_5_sword['名称']}")


def example_batch_load():
    """批量加载示例"""
    print("\n" + "=" * 50)
    print("示例 3: 批量加载目录")
    print("=" * 50)

    # 加载整个目录
    balance_configs = load_all_in_dir("balance/")
    for name, data in balance_configs.items():
        print(f"配置表: {name}, 行数: {len(data)}")


def example_game_config():
    """
    游戏配置管理器示例
    展示如何根据项目需求创建自己的配置管理器
    """
    print("\n" + "=" * 50)
    print("示例 4: 自定义游戏配置管理器")
    print("=" * 50)

    # 定义类型转换映射
    ATTR_TYPES = {"等级": int, "HP": int, "MP": int, "攻击力": int, "暴击率": float}
    EQUIP_TYPES = {"等级": int, "攻击力": int, "售价": int}
    PARAM_TYPES = {}  # 参数保持字符串

    # 加载配置表
    attributes = load_csv_typed("balance/角色属性表.csv", ATTR_TYPES)
    equipment = load_csv("items/装备配置表_武器.csv")
    params = load_csv("gameplay/游戏参数表.csv")

    # 创建索引
    attributes_by_level = index_by_field(attributes, "等级")
    equipment_by_id = index_by_field(equipment, "ID")

    # 访问数据
    level_3 = attributes_by_level.get(3)
    if level_3:
        print(f"等级3: HP={level_3['HP']}, 攻击力={level_3['攻击力']}")

    sword = equipment_by_id.get("W001")
    if sword:
        print(f"木剑: 攻击力={sword['攻击力']}")

    # 或者按需要使用 find_by_field 查找
    level_5_sword = find_by_field(
        load_csv_typed("items/装备配置表_武器.csv", EQUIP_TYPES),
        "等级",
        5
    )
    if level_5_sword:
        print(f"等级5武器: {level_5_sword['名称']}")


def example_custom_config_manager():
    """
    自定义配置管理器完整示例
    根据你的项目需求调整此类
    """
    print("\n" + "=" * 50)
    print("示例 5: 完整的配置管理器模板")
    print("=" * 50)

    class MyGameConfig:
        """
        你的游戏配置管理器
        根据项目需求添加配置表和访问方法
        """

        def __init__(self, config_root: str = "planner_config"):
            self.config_root = config_root

            # 在这里添加你需要加载的所有配置表
            self._load_configs()

        def _load_configs(self):
            """加载所有配置表"""
            logger.info("正在加载游戏配置...")

            # 示例：加载角色属性
            try:
                attr_types = {"等级": int, "HP": int, "MP": int, "攻击力": int}
                self.attributes = load_csv_typed("balance/角色属性表.csv", attr_types)
                self.attributes_by_level = index_by_field(self.attributes, "等级")
                logger.info(f"✓ 角色属性: {len(self.attributes)} 个等级")
            except FileNotFoundError:
                self.attributes = []
                self.attributes_by_level = {}
                logger.warning("角色属性表不存在")

            # 示例：加载装备
            try:
                equip_types = {"等级": int, "攻击力": int, "售价": int}
                self.weapons = load_csv_typed("items/装备配置表_武器.csv", equip_types)
                self.weapons_by_id = index_by_field(self.weapons, "ID")
                logger.info(f"✓ 武器: {len(self.weapons)} 件")
            except FileNotFoundError:
                self.weapons = []
                self.weapons_by_id = {}
                logger.warning("武器表不存在")

            # TODO: 添加更多配置表...

        def get_attribute(self, level: int):
            """获取指定等级的属性"""
            return self.attributes_by_level.get(level)

        def get_weapon(self, weapon_id: str):
            """根据ID获取武器"""
            return self.weapons_by_id.get(weapon_id)

        def find_weapons_by_level(self, level: int):
            """查找指定等级的所有武器"""
            return [w for w in self.weapons if w.get("等级") == level]

    # 使用示例
    try:
        config = MyGameConfig()
        attrs = config.get_attribute(3)
        if attrs:
            print(f"✓ 等级3属性: HP={attrs['HP']}")

        sword = config.get_weapon("W001")
        if sword:
            print(f"✓ 武器W001: {sword['名称']}")
    except Exception as e:
        print(f"配置初始化失败（预期行为，因为配置表不存在）: {e}")


if __name__ == "__main__":
    # 运行所有示例
    example_basic_usage()
    example_index_and_find()
    example_batch_load()
    example_game_config()
    example_custom_config_manager()

    print("\n" + "=" * 60)
    print("使用指南")
    print("=" * 60)
    print("""
1. 将此脚本复制到你的项目的 code/common/ 目录
2. 根据项目需求创建自己的配置管理器类
3. 参考示例 5 (MyGameConfig) 的结构
4. 在游戏初始化时创建配置管理器实例
5. 通过配置管理器访问游戏数据

提示：
- 使用 load_csv() 加载字符串类型的数据
- 使用 load_csv_typed() 加载需要类型转换的数据
- 使用 index_by_field() 创建快速访问索引
- 使用 find_by_field() 查找特定条件的行
    """)
