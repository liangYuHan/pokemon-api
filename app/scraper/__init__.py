"""
宝可梦数据爬取模块 - 从神奇宝贝百科爬取数据
"""
import requests
from bs4 import BeautifulSoup
import time
import random
from typing import List, Dict, Any


class PokemonScraper:
    """宝可梦数据爬取器"""
    
    BASE_URL = "https://wiki.52poke.com"
    
    def __init__(self, delay=1.0, max_retries=3, timeout=30):
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _fetch_page(self, url: str, retries: int = 0) -> Optional[str]:
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
            print(f"  获取失败: {url}")
            return None
    
    def scrape_pokemon_list(self, max_count: int = None) -> List[Dict[str, Any]]:
        """爬取宝可梦列表"""
        print("开始爬取宝可梦列表...")
        
        # 爬取全国图鉴列表页面
        url = f"{self.BASE_URL}/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%E5%8F%B7%E3%E7%BC%96%E5%8F%B7%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%E3%E7%BC%96%E5%8F%B7%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%E3%E7%BC%96%E5%8F%B7%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%E3%E7%BC%96%E5%8F%B7%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%E3%7%BC%96%E8%BF%9E0%E7%B5%AE%E9%98%A7%E8%AF%B1%E9%A1%98%E5%8F%7%90%E7%9D%BA%E5%8F%B7%E3%E7%BC%96%E5%8F%B7%EF%BC%88%E6%8C%89%E5%85%A8%E5%9B%BD%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%E3%7%BC%96%E8%BF%9E0%E7%B5%AE%E9%98%A7%E8%AF%B1%E9%A1%98%E5%8F%7%90%E7%9D%BA"
        
        html = self._fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        pokemon_list = []
        
        # 解析宝可梦数据（需要根据实际网页结构调整）
        # 这里需要根据实际网页结构来解析
        # 示例：解析表格中的宝可梦信息
        
        # 找到所有宝可梦表格行
        rows = soup.find_all('table')[0].find_all('tr')[1:]  # 假设第一个表格是宝可梦列表
        
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 3:  # 至少包含：编号、名称、链接
                try:
                    # 解析数据
                    link = cols[1].find('a') if len(cols) > 1 else None
                    if link:
                        name = link.text.strip()
                        detail_url = f"{self.BASE_URL}{link.get('href', '')}"
                        
                        pokemon_list.append({
                            'name': name,
                            'detail_url': detail_url
                        })
                except Exception as e:
                    print(f"  解析行失败: {e}")
        
        print(f"  发现 {len(pokemon_list)} 个宝可梦")
        return pokemon_list
    
    def scrape_pokemon_detail(self, detail_url: str) -> Dict[str, Any]:
        """爬取宝可梦详情页面"""
        print(f"  爬取宝可梦详情: {detail_url}")
        
        html = self._fetch_page(detail_url)
        if not html:
            return {}
        
        soup = BeautifulSoup(html, 'html.parser')
        pokemon_data = {}
        
        # 解析宝可梦详情页面
        # 需要根据实际页面结构调整解析逻辑
        
        # 示例：解析基本信息表
        info_table = soup.find('table', {'class': ['roundy'])
        if info_table:
            rows = info_table.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 2:
                    label = cols[0].text.strip()
                    value = cols[1].text.strip()
                    pokemon_data[label] = value
        
        # 解析种族值
        stats_table = soup.find('table', {'class': ['roundy', 'background-color': '#A0A8A8'})  # 假设种族值表的样式
        if stats_table:
            rows = stats_table.find_all('tr')
            for row in rows[1:]:  # 跳过表头
                cols = row.find_all('td')
                if len(cols) >= 2:
                    stat_name = cols[0].text.strip()
                    stat_value = cols[1].text.strip()
                    pokemon_data[stat_name] = stat_value
        
        time.sleep(self.delay)  # 避免请求过快
        return pokemon_data


class MoveScraper:
    """招式数据爬取器"""
    
    BASE_URL = "https://wiki.52poke.com"
    
    def __init__(self, delay=1.0, max_retries=3, timeout=30):
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _fetch_page(self, url: str, retries: int = 0) -> Optional[str]:
        """获取网页内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status_code()
            return response.text
        except Exception as e:
            if retries < self.max_retries:
                print(f"  重试获取 {url} (尝试 {retries + 1}/{self.max_retries})")
                time.sleep(self.delay * (retries + 1))
                return self._fetch_page(url, retries + 1)
            print(f"  获取失败: {url}")
            return None
    
    def scrape_moves_list(self, generation: str = None) -> List[Dict[str, Any]]:
        """爬取招式列表"""
        print(f"开始爬取招式列表...")
        
        url = f"{self.BASE_URL}/wiki/%E6%8B%9B%E5%BC%8F%E5%88%97%E8%A1%A8"
        
        html = self._fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        moves_list = []
        
        # 解析招式表格
        tables = soup.find_all('table')
        if tables:
            main_table = tables[0]  # 假设第一个表格是招式列表
            rows = main_table.find_all('tr')[1:]  # 跳过表头
            
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:  # 编号、名称、属性等
                    try:
                        move_data = {}
                        for i, col in enumerate(cols):
                            text = col.get_text(strip=True).strip()
                            if text:
                                if i == 0:
                                    move_data['move_id'] = int(text) if text.isdigit() else None
                                elif i == 1:
                                    move_data['name'] = text
                                elif i == 2:
                                    move_data['japanese_name'] = text
                                elif i == 3:
                                    move_data['english_name'] = text
                                elif i == 4:
                                    move_data['type'] = text
                                elif i == 5:
                                    move_data['category'] = text
                                elif i == 6:
                                    move_data['power'] = int(text) if text.isdigit() else None
                                elif i == 7:
                                    move_data['accuracy'] = int(text) if text.isdigit() else None
                                elif i == 8:
                                    move_data['pp'] = int(text) if text.isdigit() else None
                                elif i == 9:
                                    move_data['description'] = text
                        
                        if 'name' in move_data:
                            moves_list.append(move_data)
                    except Exception as e:
                        print(f"  解析招式行失败: {e}")
        
        print(f"  发现 {len(moves_list)} 个招式")
        return moves_list


class AbilityScraper:
    """特性数据爬取器"""
    
    BASE_URL = "https://wiki.52poke.com"
    
    def __init__(self, delay=1.0, max_retries=3, timeout=30):
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _fetch_page(self, url: str, retries: int = 0) -> Optional[str]:
        """获取网页内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status_code()
            return response.text
        except Exception as e:
            if retries < self.max_retries:
                print(f"  重试获取 {url} (尝试 {retries + 1}/{self.max_retries})")
                time.sleep(self.delay * (retries + 1))
                return self._fetch_page(url, retries + 1)
            print(f"  获取失败: {url}")
            return None
    
    def scrape_abilities_list(self, generation: str = None) -> List[Dict[str, Any]]:
        """爬取特性列表"""
        print(f"开始爬取特性列表...")
        
        url = f"{self.BASE_URL}/wiki/%E7%89%B9%E6%80%A7%E5%88%97%E8%A1%A8"
        
        html = self._fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        abilities_list = []
        
        # 解析特性表格
        tables = soup.find_all('table')
        for table in tables:
            if '特性' in str(table.get('id', '')):
                rows = table.find_all('tr')[1:]  # 跳过表头
                
                for row in rows:
                    cols = row.find_all('td')
                    if len(cols) >= 3:
                        try:
                            ability_data = {}
                            for i, col in enumerate(cols):
                                text = col.get_text(strip=True).strip()
                                if text:
                                    if i == 0:
                                        ability_data['ability_id'] = int(text) if text.isdigit() else None
                                    elif i == 1:
                                        ability_data['name'] = text
                                    elif i == 2:
                                        ability_data['japanese_name'] = text
                                    elif i == 3:
                                        ability_data['english_name'] = text
                                    elif i == 4:
                                        ability_data['description'] = text
                                    elif i == 5:
                                        ability_data['common_count'] = int(text) if text.isdigit() else None
                                    elif i == 6:
                                        ability_data['hidden_count'] = int(text) if text.isdigit() else None
                                    elif i == 7:
                                        ability_data['generation'] = text
                            
                            if 'name' in ability_data:
                                abilities_list.append(ability_data)
                        except Exception as e:
                            print(f"  解析特性行失败: {e}")
        
        print(f"  发现 {len(abilities_list)} 个特性")
        return abilities_list


class ItemScraper:
    """道具数据爬取器"""
    
    BASE_URL = "https://wiki.52poke.com"
    
    def __init__(self, delay=1.0, max_retries=3, timeout=30):
        self.delay = delay
        self.max_retries = max_retries
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def _fetch_page(self, url: str, retries: int = 0) -> Optional[str]:
        """获取网页内容"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.raise_for_status_code()
            return response.text
        except Exception as e:
            if retries < self.max_retries:
                print(f"  重试获取 {url} (尝试 {retries + 1}/{self.max_retries})")
                time.sleep(self.delay * (retries + 1))
                return self._fetch_page(url, retries + 1)
            print(f"  获取失败: {url}")
            return None
    
    def scrape_items_list(self, category: str = None) -> List[Dict[str, Any]]:
        """爬取道具列表"""
        print(f"开始爬取道具列表...")
        
        url = f"{self.BASE_URL}/wiki/%E9%81%93%E5%85%B7%E5%88%97%E8%A1%A8"
        
        html = self._fetch_page(url)
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        items_list = []
        
        # 解析道具表格（需要根据实际网页结构调整）
        # 这里需要根据实际页面结构调整
        
        return items_list