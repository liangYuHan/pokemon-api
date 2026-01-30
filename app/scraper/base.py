"""
基础爬虫类
"""
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any, Optional
from app.scraper.translations import (
    get_chinese_type,
    get_chinese_generation,
    GENERATION_MAP
)


class BaseScraper:
    """基础爬虫类"""
    
    def __init__(self, delay=1.0, max_retries=3, timeout=30):
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _fetch_page(self, url: str, retries: int = 0) -> str:
        """获取网页内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status()
            return response.text
        except Exception as e:
            if retries < self.max_retries:
                print(f"  重试获取 {url} (尝试 {retries + 1}/{self.max_retries})")
                time.sleep(self.delay * (retries + 1))
                return self._fetch_page(url, retries + 1)
            raise Exception(f"获取失败: {url} - {e}")
    
    def _sleep(self):
        """休眠"""
        time.sleep(self.delay)


class PokemonScraper(BaseScraper):
    """宝可梦数据爬取器（从PokeAPI）"""
    
    POKEAPI_BASE = "https://pokeapi.co/api/v2"
    
    def scrape_pokemon_by_id(self, pokemon_id: int) -> Optional[Dict[str, Any]]:
        """通过ID爬取宝可梦数据"""
        try:
            print(f"  正在爬取宝可梦 #{pokemon_id}...")
            
            url = f"{self.POKEAPI_BASE}/pokemon/{pokemon_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code != 200:
                print(f"  宝可梦 #{pokemon_id} 不存在")
                return None
            
            data = response.json()
            
            # 获取species信息（可能包含更多信息）
            species_data = None
            if data.get('species') and data['species'].get('url'):
                species_url = data['species']['url']
                try:
                    species_response = requests.get(species_url, timeout=self.timeout)
                    if species_response.status_code == 200:
                        species_data = species_response.json()
                except:
                    pass
            
            pokemon_data = {
                "national_dex": data["id"],
                "name": self._get_chinese_name(species_data) if species_data else data["name"],  # 中文名
                "japanese_name": self._get_japanese_name(species_data) if species_data else data["name"],  # 日文名
                "english_name": data["name"],  # 英文名
                "type1": get_chinese_type(data["types"][0]["type"]["name"]),  # 中文属性
                "type2": get_chinese_type(data["types"][1]["type"]["name"]) if len(data["types"]) > 1 else None,
                "classification": self._get_chinese_classification(species_data) if species_data else "",
                "height": data["height"] / 10,
                "weight": data["weight"] / 10,
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "sp_attack": data["stats"][3]["base_stat"],
                "sp_defense": data["stats"][4]["base_stat"],
                "speed": data["stats"][5]["base_stat"],
                "total_stats": sum(stat["base_stat"] for stat in data["stats"]),
                "catch_rate": self._get_catch_rate(species_data) if species_data else 0,
                "experience_type": self._get_chinese_growth_rate(species_data) if species_data else "未知",
                "gender_ratio": self._get_chinese_gender_rate(species_data) if species_data else "未知",
                "abilities": self._get_chinese_abilities(data.get("abilities", []))
            }
            
            self._sleep()
            return pokemon_data
            
        except Exception as e:
            print(f"  爬取宝可梦 #{pokemon_id} 失败: {e}")
            return None
    
    def _get_japanese_name(self, species_data: Dict) -> str:
        """从species数据中获取日文名"""
        if not species_data:
            return ""
        
        names = species_data.get("names", [])
        for name_obj in names:
            if name_obj.get("language", {}).get("name") == "ja-Hrkt":
                return name_obj.get("name", "")
        return ""
    
    def _get_chinese_name(self, species_data: Dict) -> str:
        """从species数据中获取中文名"""
        if not species_data:
            return ""
        
        names = species_data.get("names", [])
        # 优先使用简体中文
        for name_obj in names:
            if name_obj.get("language", {}).get("name") == "zh-Hans":
                return name_obj.get("name", "")
        # 其次使用繁体中文
        for name_obj in names:
            if name_obj.get("language", {}).get("name") == "zh-Hant":
                return name_obj.get("name", "")
        # 最后使用通用中文
        for name_obj in names:
            if name_obj.get("language", {}).get("name") == "zh":
                return name_obj.get("name", "")
        
        # 如果没有中文名，使用英文名
        for name_obj in names:
            if name_obj.get("language", {}).get("name") == "en":
                return name_obj.get("name", "")
        
        return ""
    
    def _get_chinese_classification(self, species_data: Dict) -> str:
        """从species数据中获取中文分类"""
        if not species_data:
            return ""
        
        genera = species_data.get("genera", [])
        # 查找中文分类
        for genus_obj in genera:
            language = genus_obj.get("language", {}).get("name")
            if language and "zh" in language:
                return genus_obj.get("genus", "")
        
        # 如果没有中文，使用英文并翻译
        for genus_obj in genera:
            if genus_obj.get("language", {}).get("name") == "en":
                genus = genus_obj.get("genus", "")
                # 英文翻译映射
                genus_map = {
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
                }
                return genus_map.get(genus, genus)
        
        return ""
    
    def _get_chinese_gender_rate(self, species_data: Dict) -> str:
        """获取中文性别比例"""
        if not species_data:
            return "未知"
        
        rate = species_data.get("gender_rate", None)
        if rate is None:
            return "无性别"
        elif rate == -1:
            return "无性别"
        elif rate == 8:
            return "雌性87.5% 雄性12.5%"
        elif rate == 0:
            return "雄性100%"
        elif rate == 1:
            return "雄性87.5% 雌性12.5%"
        elif rate == 2:
            return "雄性75% 雌性25%"
        elif rate == 4:
            return "雄性50% 雌性50%"
        elif rate == 6:
            return "雄性25% 雌性75%"
        elif rate == 7:
            return "雌性100%"
        else:
            return "未知"
    
    def _get_chinese_growth_rate(self, species_data: Dict) -> str:
        """获取中文经验类型"""
        if not species_data:
            return "未知"
        
        growth_rate = species_data.get("growth_rate", {})
        english_name = growth_rate.get("name", "未知")
        
        growth_rate_map = {
            "slow": "慢",
            "medium-slow": "中慢",
            "medium": "中等",
            "medium-fast": "中快",
            "fast": "快",
            "erratic": "不定",
            "fluctuating": "波动"
        }
        
        return growth_rate_map.get(english_name, english_name)
    
    def _get_chinese_abilities(self, abilities: List[Dict]) -> List[str]:
        """获取中文特性名称"""
        # 这里需要一个中英文映射
        # 简化处理：直接返回英文名称
        # 可以添加一个完整的特性中英文映射
        return [ability["ability"]["name"] for ability in abilities]
    
    def _get_catch_rate(self, species_data: Dict) -> int:
        """获取捕获率"""
        if not species_data:
            return 0
        return species_data.get("capture_rate", 0)
    
    def _get_growth_rate(self, species_data: Dict) -> str:
        """获取经验类型"""
        if not species_data:
            return "未知"
        return species_data.get("growth_rate", {}).get("name", "未知")
    
    def _get_gender_rate(self, species_data: Dict) -> str:
        """获取性别比例"""
        if not species_data:
            return "未知"
        
        rate = species_data.get("gender_rate", None)
        if rate is None:
            return "无性别"
        elif rate == -1:
            return "无性别"
        elif rate == 8:
            return "雌性:87.5% 雄性:12.5%"
        elif rate == 0:
            return "雄性:100%"
        elif rate == 1:
            return "雄性:87.5% 雌性:12.5%"
        elif rate == 2:
            return "雄性:75% 雌性:25%"
        elif rate == 4:
            return "雄性:50% 雌性:50%"
        elif rate == 6:
            return "雄性:25% 雌性:75%"
        elif rate == 7:
            return "雌性:100%"
        else:
            return "未知"
    
    def scrape_pokemon_list(self, start_id: int = 1, end_id: int = 151) -> List[Dict[str, Any]]:
        """爬取宝可梦列表"""
        print(f"开始爬取宝可梦列表 (#{start_id} - #{end_id})...")
        
        pokemon_list = []
        for pokemon_id in range(start_id, end_id + 1):
            pokemon_data = self.scrape_pokemon_by_id(pokemon_id)
            if pokemon_data:
                pokemon_list.append(pokemon_data)
        
        print(f"成功爬取 {len(pokemon_list)} 个宝可梦")
        return pokemon_list


class MoveScraper(BaseScraper):
    """招式数据爬取器（从PokeAPI）"""
    
    POKEAPI_BASE = "https://pokeapi.co/api/v2"
    
    def scrape_move_by_id(self, move_id: int) -> Optional[Dict[str, Any]]:
        """通过ID爬取招式数据"""
        try:
            print(f"  正在爬取招式 #{move_id}...")
            
            url = f"{self.POKEAPI_BASE}/move/{move_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code != 200:
                print(f"  招式 #{move_id} 不存在")
                return None
            
            data = response.json()
            
            move_data = {
                "move_id": data["id"],
                "name": data["name"],
                "type": data["type"]["name"],
                "power": data["power"],
                "accuracy": data["accuracy"],
                "pp": data["pp"],
                "description": data["flavor_text_entries"][0]["flavor_text"] if data["flavor_text_entries"] else "",
                "generation": data["generation"]["name"].replace("generation-", "")
            }
            
            self._sleep()
            return move_data
            
        except Exception as e:
            print(f"  爬取招式 #{move_id} 失败: {e}")
            return None
    
    def scrape_move_list(self, start_id: int = 1, end_id: int = 100) -> List[Dict[str, Any]]:
        """爬取招式列表"""
        print(f"开始爬取招式列表 (#{start_id} - #{end_id})...")
        
        move_list = []
        for move_id in range(start_id, end_id + 1):
            move_data = self.scrape_move_by_id(move_id)
            if move_data:
                move_list.append(move_data)
        
        print(f"成功爬取 {len(move_list)} 个招式")
        return move_list


class AbilityScraper(BaseScraper):
    """特性数据爬取器（从PokeAPI）"""
    
    POKEAPI_BASE = "https://pokeapi.co/api/v2"
    
    def scrape_ability_by_id(self, ability_id: int) -> Optional[Dict[str, Any]]:
        """通过ID爬取特性数据"""
        try:
            print(f"  正在爬取特性 #{ability_id}...")
            
            url = f"{self.POKEAPI_BASE}/ability/{ability_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code != 200:
                print(f"  特性 #{ability_id} 不存在")
                return None
            
            data = response.json()
            
            ability_data = {
                "ability_id": data["id"],
                "name": data["name"],
                "description": data["flavor_text_entries"][0]["flavor_text"] if data["flavor_text_entries"] else "",
                "generation": data["generation"]["name"].replace("generation-", "")
            }
            
            self._sleep()
            return ability_data
            
        except Exception as e:
            print(f"  爬取特性 #{ability_id} 失败: {e}")
            return None
    
    def scrape_ability_list(self, start_id: int = 1, end_id: int = 50) -> List[Dict[str, Any]]:
        """爬取特性列表"""
        print(f"开始爬取特性列表 (#{start_id} - #{end_id})...")
        
        ability_list = []
        for ability_id in range(start_id, end_id + 1):
            ability_data = self.scrape_ability_by_id(ability_id)
            if ability_data:
                ability_list.append(ability_data)
        
        print(f"成功爬取 {len(ability_list)} 个特性")
        return ability_list


class ItemScraper(BaseScraper):
    """道具数据爬取器（从PokeAPI）"""
    
    POKEAPI_BASE = "https://pokeapi.co/api/v2"
    
    def scrape_item_by_id(self, item_id: int) -> Optional[Dict[str, Any]]:
        """通过ID爬取道具数据"""
        try:
            print(f"  正在爬取道具 #{item_id}...")
            
            url = f"{self.POKEAPI_BASE}/item/{item_id}"
            response = requests.get(url, timeout=self.timeout)
            
            if response.status_code != 200:
                print(f"  道具 #{item_id} 不存在")
                return None
            
            data = response.json()
            
            item_data = {
                "name": data["name"],
                "category": data["category"]["name"],
                "description": data["flavor_text_entries"][0]["text"] if data["flavor_text_entries"] else "",
                "generation": data["generation"]["name"].replace("generation-", "")
            }
            
            self._sleep()
            return item_data
            
        except Exception as e:
            print(f"  爬取道具 #{item_id} 失败: {e}")
            return None
    
    def scrape_item_list(self, start_id: int = 1, end_id: int = 50) -> List[Dict[str, Any]]:
        """爬取道具列表"""
        print(f"开始爬取道具列表 (#{start_id} - #{end_id})...")
        
        item_list = []
        for item_id in range(start_id, end_id + 1):
            item_data = self.scrape_item_by_id(item_id)
            if item_data:
                item_list.append(item_data)
        
        print(f"成功爬取 {len(item_list)} 个道具")
        return item_list
