"""
数据库连接管理
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()

# 从环境变量获取数据库配置
DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('MYSQL_USER', 'root')}"
    f":{os.getenv('MYSQL_PASSWORD', 'password')}"
    f"@{os.getenv('MYSQL_HOST', 'localhost')}"
    f":{os.getenv('MYSQL_PORT', '3306')}"
    f"/{os.getenv('MYSQL_DATABASE', 'pokemon_api')}"
    f"?charset=utf8mb4"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基类
Base = declarative_base()

# 获取数据库会话
def get_db() -> Session:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 初始化数据库表
def init_db():
    """初始化数据库表"""
    from app.models.pokemon import Pokemon
    from app.models.move import Move
    from app.models.ability import Ability
    from app.models.item import Item
    
    Base.metadata.create_all(bind=engine)