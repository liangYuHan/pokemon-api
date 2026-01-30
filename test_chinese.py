#!/usr/bin/env python3
"""
测试中文名称获取
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.scraper.base import PokemonScraper

print("=" * 60)
print("  测试中文名称获取")
print("=" * 60)
print()

scraper = PokemonScraper(delay=0.5)

# 测试第一个宝可梦（妙蛙种子）
print("测试宝可梦 #1 (妙蛙种子)...")
data = scraper.scrape_pokemon_by_id(1)

if data:
    print("\n✅ 爬取成功！")
    print("\n宝可梦信息:")
    print(f"  全国图鉴: {data.get('national_dex')}")
    print(f"  中文名: {data.get('name')}")
    print(f"  日文名: {data.get('japanese_name')}")
    print(f"  英文名: {data.get('english_name')}")
    print(f"  属性1: {data.get('type1')}")
    print(f"  属性2: {data.get('type2')}")
    print(f"  分类: {data.get('classification')}")
    print(f"  身高: {data.get('height')}m")
    print(f"  体重: {data.get('weight')}kg")
    print(f"  经验类型: {data.get('experience_type')}")
    print(f"  性别比例: {data.get('gender_ratio')}")
    print(f"  特性: {data.get('abilities')}")
    print()
else:
    print("❌ 爬取失败")

# 测试多个宝可梦
print("\n测试更多宝可梦...")
test_ids = [1, 4, 7, 25, 133]

for pokemon_id in test_ids:
    data = scraper.scrape_pokemon_by_id(pokemon_id)
    if data:
        print(f"  #{data['national_dex']} - {data['name']} ({data.get('type1')})")

print()
print("=" * 60)
print("  测试完成")
print("=" * 60)
