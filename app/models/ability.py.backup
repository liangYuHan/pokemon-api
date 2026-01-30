"""
特性数据库模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base


class Ability(Base):
    """特性表"""
    __tablename__ = "abilities"
    
    id = Column(Integer, primary_key=True, index=True)
    ability_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    japanese_name = Column(String(100), nullable=False)
    english_name = Column(String(100), nullable=False, index=True)
    description = Column(Text, nullable=False)
    common_count = Column(Integer)
    hidden_count = Column(Integer)
    generation = Column(String(20), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)