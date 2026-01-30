"""
基础爬虫类
"""
import requests
from bs4 import BeautifulSoup
import time
from typing import List, Dict, Any, Optional


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
            
            pokemon_data = {
                "national_dex": data["id"],
                "name": data["name"],
                "type1": data["types"][0]["type"]["name"],
                "type2": data["types"][1]["type"]["name"] if len(data["types"]) > 1 else None,
                "height": data["height"] / 10,
                "weight": data["weight"] / 10,
                "hp": data["stats"][0]["base_stat"],
                "attack": data["stats"][1]["base_stat"],
                "defense": data["stats"][2]["base_stat"],
                "sp_attack": data["stats"][3]["base_stat"],
                "sp_defense": data["stats"][4]["base_stat"],
                "speed": data["stats"][5]["base_stat"],
                "total_stats": sum(stat["base_stat"] for stat in data["stats"]),
                "abilities": [ability["ability"]["name"] for ability in data["abilities"]]
            }
            
            self._sleep()
            return pokemon_data
            
        except Exception as e:
            print(f"  爬取宝可梦 #{pokemon_id} 失败: {e}")
            return None
    
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
