#!/usr/bin/env python3
"""
数据库初始化和种子数据脚本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, Base, SessionLocal, init_db
from app.models.pokemon import Pokemon, Move, Ability, Item
from datetime import datetime
from sqlalchemy.orm import Session


def seed_pokemon_data(db: Session):
    """填充宝可梦数据"""
    print("填充宝可梦数据...")
    
    pokemon_data = [
        Pokemon(
            national_dex=1,
            name="妙蛙种子",
            japanese_name="フシギダネ",
            english_name="Bulbasaur",
            type1="草",
            type2=None,
            classification="种子宝可梦",
            height=0.7,
            weight=6.9,
            hp=45,
            attack=49,
            defense=49,
            sp_attack=65,
            sp_defense=65,
            speed=45,
            total_stats=318,
            catch_rate=45,
            experience_type="中等偏慢",
            gender_ratio="雄性87.5% 雌性12.5%",
            egg_groups=["怪獣", "植物"],
            abilities=["茂盛", "叶绿素"]
        ),
        Pokemon(
            national_dex=4,
            name="小火龙",
            japanese_name="ヒトカゲ",
            english_name="Charmander",
            type1="火",
            type2=None,
            classification="蜥蜴宝可梦",
            height=0.6,
            weight=8.5,
            hp=39,
            attack=52,
            defense=43,
            sp_attack=60,
            sp_defense=50,
            speed=65,
            total_stats=309,
            catch_rate=45,
            experience_type="中等偏慢",
            gender_ratio="雄性87.5% 雌性12.5%",
            egg_groups=["怪獣", "龙"],
            abilities=["猛火"]
        ),
        Pokemon(
            national_dex=7,
            name="杰尼龟",
            japanese_name="ゼニガメ",
            english_name="Squirtle",
            type1="水",
            type2=None,
            classification="小龟宝可梦",
            height=0.5,
            weight=9.0,
            hp=44,
            attack=48,
            defense=65,
            sp_attack=50,
            sp_defense=64,
            speed=43,
            total_stats=314,
            catch_rate=45,
            experience_type="中等偏慢",
            gender_ratio="雄性87.5% 雌性12.5%",
            egg_groups=["怪獣", "水中1"],
            abilities=["激流"]
        )
    ]
    
    db.bulk_save_objects(pokemon_data)
    db.commit()
    print(f"  成功插入 {len(pokemon_data)} 个宝可梦")


def seed_move_data(db: Session):
    """填充招式数据"""
    print("填充招式数据...")
    
    move_data = [
        Move(
            move_id=1,
            name="拍击",
            japanese_name="はたく",
            english_name="Pound",
            type="一般",
            category="物理",
            power=40,
            accuracy=100,
            pp=35,
            description="使用长长的尾巴或手等拍打对手进行攻击。"
        ),
        Move(
            move_id=2,
            name="空手劈",
            japanese_name="からてチョップ",
            english_name="Karate Chop",
            type="格斗",
            category="物理",
            power=50,
            accuracy=100,
            pp=25,
            description="用锋利的手刀劈向对手进行攻击。容易击中要害。"
        ),
        Move(
            move_id=3,
            name="火焰拳",
            japanese_name="ほのおのパンチ",
            english_name="Fire Punch",
            type="火",
            category="物理",
            power=75,
            accuracy=100,
            pp=15,
            description="用充满火焰的拳头攻击对手。有时会让对手陷入灼伤状态。"
        ),
        Move(
            move_id=4,
            name="十万伏特",
            japanese_name="１０まんボルト",
            english_name="Thunderbolt",
            type="电",
            category="特殊",
            power=90,
            accuracy=100,
            pp=15,
            description="向对手发出强力电击进行攻击。有时会让对手陷入麻痹状态。"
        ),
        Move(
            move_id=5,
            name="喷射火焰",
            japanese_name="かえんほうしゃ",
            english_name="Flamethrower",
            type="火",
            category="特殊",
            power=90,
            accuracy=100,
            pp=15,
            description="向对手发射烈焰进行攻击。有时会让对手陷入灼伤状态。"
        )
    ]
    
    db.bulk_save_objects(move_data)
    db.commit()
    print(f"  成功插入 {len(move_data)} 个招式")


def seed_ability_data(db: Session):
    """填充特性数据"""
    print("填充特性数据...")
    
    ability_data = [
        Ability(
            ability_id=1,
            name="茂盛",
            japanese_name="しんりょく",
            english_name="Overgrow",
            description="HP减少的时候，草属性的招式威力会提高。",
            common_count=28,
            hidden_count=2,
            generation="第三世代"
        ),
        Ability(
            ability_id=2,
            name="猛火",
            japanese_name="もうか",
            english_name="Blaze",
            description="HP减少的时候，火属性的招式威力会提高。",
            common_count=28,
            hidden_count=2,
            generation="第三世代"
        ),
        Ability(
            ability_id=3,
            name="激流",
            japanese_name="げきりゅう",
            english_name="Torrent",
            description="HP减少的时候，水属性的招式威力会提高。",
            common_count=28,
            hidden_count=2,
            generation="第三世代"
        ),
        Ability(
            ability_id=4,
            name="静电",
            japanese_name="せいでんき",
            english_name="Static",
            description="身上带有静电，有时会让接触到的对手麻痹。",
            common_count=19,
            hidden_count=1,
            generation="第三世代"
        ),
        Ability(
            ability_id=5,
            name="威吓",
            japanese_name="いかく",
            english_name="Intimidate",
            description="出场时威吓对手，让其退缩，降低对手的攻击。",
            common_count=34,
            hidden_count=7,
            generation="第三世代"
        )
    ]
    
    db.bulk_save_objects(ability_data)
    db.commit()
    print(f"  成功插入 {len(ability_data)} 个特性")


def seed_item_data(db: Session):
    """填充道具数据"""
    print("填充道具数据...")
    
    item_data = [
        Item(
            name="除虫喷雾",
            japanese_name="むしよけスプレー",
            english_name="Repel",
            category="野外使用",
            description="使用后，在较短时间内，弱小的野生宝可梦将完全不会出现。",
            generation="第一世代"
        ),
        Item(
            name="精灵球",
            japanese_name="モンスターボール",
            english_name="Poké Ball",
            category="精灵球",
            description="用于捕捉野生宝可梦的基础精灵球。",
            generation="第一世代"
        ),
        Item(
            name="超级球",
            japanese_name="ハイパーボール",
            english_name="Ultra Ball",
            category="精灵球",
            description="比精灵球更容易捕捉野生宝可梦。",
            generation="第一世代"
        ),
        Item(
            name="伤药",
            japanese_name="キズぐすり",
            english_name="Potion",
            category="回复道具",
            description="回复宝可梦20点HP。",
            generation="第一世代"
        ),
        Item(
            name="好伤药",
            japanese_name="いいきずぐすり",
            english_name="Super Potion",
            category="回复道具",
            description="回复宝可梦60点HP。",
            generation="第一世代"
        )
    ]
    
    db.bulk_save_objects(item_data)
    db.commit()
    print(f"  成功插入 {len(item_data)} 个道具")


def init_database():
    """初始化数据库"""
    print("=" * 50)
    print("  数据库初始化脚本")
    print("=" * 50)
    print()
    
    try:
        print("1. 创建数据库表...")
        Base.metadata.create_all(bind=engine)
        print("  数据库表创建成功")
        print()
        
        print("2. 连接数据库...")
        db = SessionLocal()
        print("  数据库连接成功")
        print()
        
        print("3. 检查数据...")
        pokemon_count = db.query(Pokemon).count()
        move_count = db.query(Move).count()
        ability_count = db.query(Ability).count()
        item_count = db.query(Item).count()
        
        print(f"  宝可梦: {pokemon_count}")
        print(f"  招式: {move_count}")
        print(f"  特性: {ability_count}")
        print(f"  道具: {item_count}")
        print()
        
        if pokemon_count == 0:
            seed_pokemon_data(db)
        else:
            print("宝可梦数据已存在，跳过")
            print()
        
        if move_count == 0:
            seed_move_data(db)
        else:
            print("招式数据已存在，跳过")
            print()
        
        if ability_count == 0:
            seed_ability_data(db)
        else:
            print("特性数据已存在，跳过")
            print()
        
        if item_count == 0:
            seed_item_data(db)
        else:
            print("道具数据已存在，跳过")
            print()
        
        db.close()
        
        print("=" * 50)
        print("  数据库初始化完成！")
        print("=" * 50)
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    init_database()
