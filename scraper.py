#!/usr/bin/env python3
"""
使用爬虫获取数据并保存到数据库
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models.pokemon import Pokemon, Move, Ability, Item
from app.scraper.base import PokemonScraper, MoveScraper, AbilityScraper, ItemScraper
from datetime import datetime


def scrape_and_save_pokemon(start_id: int = 1, end_id: int = 151):
    """爬取宝可梦数据并保存到数据库"""
    print(f"爬取宝可梦数据 (#{start_id} - #{end_id})...")
    
    db = SessionLocal()
    scraper = PokemonScraper(delay=1.0)
    
    try:
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for pokemon_id in range(start_id, end_id + 1):
            pokemon_data = scraper.scrape_pokemon_by_id(pokemon_id)
            if pokemon_data:
                # 检查是否已存在
                existing = db.query(Pokemon).filter(
                    Pokemon.national_dex == pokemon_data["national_dex"]
                ).first()
                
                if existing:
                    print(f"  ⏭️  宝可梦 #{pokemon_id} 已存在，跳过")
                    skip_count += 1
                else:
                    pokemon = Pokemon(**pokemon_data)
                    db.add(pokemon)
                    db.commit()
                    print(f"  ✅ 保存宝可梦 #{pokemon_id} 成功")
                    success_count += 1
            else:
                print(f"  ❌ 宝可梦 #{pokemon_id} 爬取失败")
                error_count += 1
        
        print(f"\n总结:")
        print(f"  ✅ 成功保存: {success_count} 个")
        print(f"  ⏭️  跳过已存在: {skip_count} 个")
        print(f"  ❌ 爬取失败: {error_count} 个")
        print(f"  总计处理: {end_id - start_id + 1} 个")
        
    except Exception as e:
        print(f"\n爬取失败: {e}")
        db.rollback()
    finally:
        db.close()


def scrape_and_save_moves(start_id: int = 1, end_id: int = 100):
    """爬取招式数据并保存到数据库"""
    print(f"爬取招式数据 (#{start_id} - #{end_id})...")
    
    db = SessionLocal()
    scraper = MoveScraper(delay=1.0)
    
    try:
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for move_id in range(start_id, end_id + 1):
            move_data = scraper.scrape_move_by_id(move_id)
            if move_data:
                # 检查是否已存在
                existing = db.query(Move).filter(
                    Move.move_id == move_data["move_id"]
                ).first()
                
                if existing:
                    print(f"  ⏭️  招式 #{move_id} 已存在，跳过")
                    skip_count += 1
                else:
                    move = Move(**move_data)
                    db.add(move)
                    db.commit()
                    print(f"  ✅ 保存招式 #{move_id} 成功")
                    success_count += 1
            else:
                print(f"  ❌ 招式 #{move_id} 爬取失败")
                error_count += 1
        
        print(f"\n总结:")
        print(f"  ✅ 成功保存: {success_count} 个")
        print(f"  ⏭️  跳过已存在: {skip_count} 个")
        print(f"  ❌ 爬取失败: {error_count} 个")
        print(f"  总计处理: {end_id - start_id + 1} 个")
        
    except Exception as e:
        print(f"\n爬取失败: {e}")
        db.rollback()
    finally:
        db.close()


def scrape_and_save_abilities(start_id: int = 1, end_id: int = 50):
    """爬取特性数据并保存到数据库"""
    print(f"爬取特性数据 (#{start_id} - #{end_id})...")
    
    db = SessionLocal()
    scraper = AbilityScraper(delay=1.0)
    
    try:
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for ability_id in range(start_id, end_id + 1):
            ability_data = scraper.scrape_ability_by_id(ability_id)
            if ability_data:
                # 检查是否已存在
                existing = db.query(Ability).filter(
                    Ability.ability_id == ability_data["ability_id"]
                ).first()
                
                if existing:
                    print(f"  ⏭️  特性 #{ability_id} 已存在，跳过")
                    skip_count += 1
                else:
                    ability = Ability(**ability_data)
                    db.add(ability)
                    db.commit()
                    print(f"  ✅ 保存特性 #{ability_id} 成功")
                    success_count += 1
            else:
                print(f"  ❌ 特性 #{ability_id} 爬取失败")
                error_count += 1
        
        print(f"\n总结:")
        print(f"  ✅ 成功保存: {success_count} 个")
        print(f"  ⏭️  跳过已存在: {skip_count} 个")
        print(f"  ❌ 爬取失败: {error_count} 个")
        print(f"  总计处理: {end_id - start_id + 1} 个")
        
    except Exception as e:
        print(f"\n爬取失败: {e}")
        db.rollback()
    finally:
        db.close()


def scrape_and_save_items(start_id: int = 1, end_id: int = 50):
    """爬取道具数据并保存到数据库"""
    print(f"爬取道具数据 (#{start_id} - #{end_id})...")
    
    db = SessionLocal()
    scraper = ItemScraper(delay=1.0)
    
    try:
        success_count = 0
        skip_count = 0
        error_count = 0
        
        for item_id in range(start_id, end_id + 1):
            item_data = scraper.scrape_item_by_id(item_id)
            if item_data:
                # 检查是否已存在（item表按name检查）
                existing = db.query(Item).filter(
                    Item.name == item_data["name"]
                ).first()
                
                if existing:
                    print(f"  ⏭️  道具 #{item_id} 已存在，跳过")
                    skip_count += 1
                else:
                    item = Item(**item_data)
                    db.add(item)
                    db.commit()
                    print(f"  ✅ 保存道具 #{item_id} 成功")
                    success_count += 1
            else:
                print(f"  ❌ 道具 #{item_id} 爬取失败")
                error_count += 1
        
        print(f"\n总结:")
        print(f"  ✅ 成功保存: {success_count} 个")
        print(f"  ⏭️  跳过已存在: {skip_count} 个")
        print(f"  ❌ 爬取失败: {error_count} 个")
        print(f"  总计处理: {end_id - start_id + 1} 个")
        
    except Exception as e:
        print(f"\n爬取失败: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    print("=" * 50)
    print("  宝可梦数据爬取脚本")
    print("=" * 50)
    print()
    print("选择要爬取的数据类型：")
    print("  1. 宝可梦")
    print("  2. 招式")
    print("  3. 特性")
    print("  4. 道具")
    print("  5. 全部")
    print()
    
    choice = input("请输入选项 (1-5): ").strip()
    
    if choice == "1":
        start_id = int(input("起始ID (默认1): ") or "1")
        end_id = int(input("结束ID (默认151): ") or "151")
        scrape_and_save_pokemon(start_id, end_id)
    elif choice == "2":
        start_id = int(input("起始ID (默认1): ") or "1")
        end_id = int(input("结束ID (默认100): ") or "100")
        scrape_and_save_moves(start_id, end_id)
    elif choice == "3":
        start_id = int(input("起始ID (默认1): ") or "1")
        end_id = int(input("结束ID (默认50): ") or "50")
        scrape_and_save_abilities(start_id, end_id)
    elif choice == "4":
        start_id = int(input("起始ID (默认1): ") or "1")
        end_id = int(input("结束ID (默认50): ") or "50")
        scrape_and_save_items(start_id, end_id)
    elif choice == "5":
        print("\n开始爬取所有数据...")
        scrape_and_save_pokemon(1, 151)
        scrape_and_save_moves(1, 100)
        scrape_and_save_abilities(1, 50)
        scrape_and_save_items(1, 50)
    else:
        print("无效的选项")
        sys.exit(1)
    
    print()
    print("=" * 50)
    print("  爬取完成！")
    print("=" * 50)
