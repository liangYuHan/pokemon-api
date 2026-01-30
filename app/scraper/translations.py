"""
中英文映射表
"""

# 宝可梦属性
TYPE_MAP = {
    "normal": "一般",
    "fire": "火",
    "water": "水",
    "grass": "草",
    "electric": "电",
    "ice": "冰",
    "fighting": "格斗",
    "poison": "毒",
    "ground": "地面",
    "flying": "飞行",
    "psychic": "超能力",
    "bug": "虫",
    "rock": "岩石",
    "ghost": "幽灵",
    "dragon": "龙",
    "dark": "恶",
    "steel": "钢",
    "fairy": "妖精"
}

# 宝可梦分类
GENUS_MAP = {
    "Seed Pokémon": "种子宝可梦",
    "Lizard Pokémon": "蜥蜴宝可梦",
    "Turtle Pokémon": "小龟宝可梦",
    "Worm Pokémon": "虫宝可梦",
    "Cocoon Pokémon": "蛹宝可梦",
    "Moth Pokémon": "飞蛾宝可梦",
    "Bee Pokémon": "蜜蜂宝可梦",
    "Tiny Bird Pokémon": "小鸟宝可梦",
    "Bird Pokémon": "鸟类宝可梦",
    "Flying Pokémon": "飞行宝可梦",
    "Mouse Pokémon": "老鼠宝可梦",
    "Cat Pokémon": "猫宝可梦",
    "Fox Pokémon": "狐狸宝可梦",
    "Bat Pokémon": "蝙蝠宝可梦",
    "Snake Pokémon": "蛇宝可梦",
    "Fish Pokémon": "鱼宝可梦",
    "Shellfish Pokémon": "甲壳宝可梦",
    "Dragon Pokémon": "龙宝可梦",
    "Monster Pokémon": "怪兽宝可梦",
    "Fairy Pokémon": "妖精宝可梦",
    "Fossil Pokémon": "化石宝可梦",
    "Baby Pokémon": "幼年宝可梦",
    "Mythical Pokémon": "神话宝可梦",
    "Legendary Pokémon": "传说宝可梦",
    "Unknown Pokémon": "未知宝可梦",
    "Shadow Pokémon": "影子宝可梦"
}

# 招式分类
MOVE_CATEGORY_MAP = {
    "physical": "物理",
    "special": "特殊",
    "status": "变化"
}

# 经验类型
GROWTH_RATE_MAP = {
    "slow": "慢",
    "medium-slow": "中慢",
    "medium": "中等",
    "medium-fast": "中快",
    "fast": "快",
    "erratic": "不定",
    "fluctuating": "波动"
}

# 道具分类
ITEM_CATEGORY_MAP = {
    "stat-boosts": "能力提升",
    "medicine": "药品",
    "healing": "回复",
    "all-machines": "所有学习装置",
    "berries": "树果",
    "plot-advancement": "剧情推进",
    "keys": "钥匙",
    "collectibles": "收集品",
    "evolution": "进化",
    "spoils": "战利品",
    "hold-items": "携带物品",
    "usable-in-battle": "战斗中使用",
    "usable-outside-battle": "场外使用",
    "all-mail": "所有信件",
    "vitamins": "维生素",
    "catching": "捕捉",
    "pp-recovery": "PP回复",
    "revival": "复活",
    "unused": "未使用",
    "competition": "比赛",
    "picn": "图片",
    "data-cards": "数据卡"
}

# 世代
GENERATION_MAP = {
    "generation-i": "第一世代",
    "generation-ii": "第二世代",
    "generation-iii": "第三世代",
    "generation-iv": "第四世代",
    "generation-v": "第五世代",
    "generation-vi": "第六世代",
    "generation-vii": "第七世代",
    "generation-viii": "第八世代",
    "generation-ix": "第九世代"
}


def get_chinese_type(english_type: str) -> str:
    """获取中文属性名称"""
    return TYPE_MAP.get(english_type.lower(), english_type)


def get_chinese_category(english_category: str) -> str:
    """获取中文分类名称（招式）"""
    return MOVE_CATEGORY_MAP.get(english_category.lower(), english_category)


def get_chinese_growth_rate(english_rate: str) -> str:
    """获取中文经验类型"""
    return GROWTH_RATE_MAP.get(english_rate.lower(), english_rate)


def get_chinese_generation(english_gen: str) -> str:
    """获取中文世代名称"""
    return GENERATION_MAP.get(english_gen.lower(), english_gen)


def get_chinese_item_category(english_category: str) -> str:
    """获取中文道具分类"""
    return ITEM_CATEGORY_MAP.get(english_category.lower(), english_category)
