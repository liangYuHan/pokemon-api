"""
应用配置文件（简化版）
"""

class Settings:
    """应用配置"""
    # 应用信息
    APP_NAME = "Pokemon API"
    APP_VERSION = "1.0.0"
    DEBUG = True
    
    # 服务器配置
    HOST = "0.0.0.0"
    PORT = 8000
    
    # 数据库配置
    MYSQL_HOST = "localhost"
    MYSQL_PORT = 3306
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "password"
    MYSQL_DATABASE = "pokemon_api"
    
    # 数据库URL
    @staticmethod
    def get_database_url():
        return f"mysql+pymysql://root:password@localhost:3306/pokemon_api?charset=utf8mb4"
    
    # 爬取配置
    SCRAPER_DELAY = 1.0
    SCRAPER_MAX_RETRIES = 3
    SCRAPER_TIMEOUT = 30
    
    # 分页配置
    DEFAULT_PAGE_SIZE = 20
    MAX_PAGE_SIZE = 100

settings = Settings()