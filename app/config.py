"""
应用配置文件
"""
from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # 应用信息
    APP_NAME: str = "Pokemon API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # 数据库配置
    MYSQL_HOST: str
    MYSQL_PORT: int = 3306
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DATABASE: str = "pokemon_api"
    
    # 安全配置
    SECRET_KEY: str = "your-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 爬取配置
    SCRAPER_DELAY: float = 1.0
    SCRAPER_MAX_RETRIES: int = 3
    SCRAPER_TIMEOUT: int = 30
    
    # 分页配置
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # 跨域配置
    CORS_ORIGINS: list = ["*"]
    
    class Config:
        case_sensitive = True
    
    @property
    def DATABASE_URL(self) -> str:
        return (
            f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
            f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
            f"?charset=utf8mb4"
        )
    
    @property
    def SYNC_DATABASE_URL(self) -> str:
        return self.DATABASE_URL.replace("+pymysql", "")


settings = Settings()