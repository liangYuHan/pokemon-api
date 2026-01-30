"""
招式数据库模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base


class Move(Base):
    """招式表"""
    __tablename__ = "moves"
    
    id = Column(Integer, primary_key=True, index=True)
    move_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    japanese_name = Column(String(100), nullable=False)
    english_name = Column(String(100), nullable=False, index=True)
    type = Column(String(20), nullable=False, index=True)
    category = Column(String(20), nullable=False)  # 物理/特殊/变化
    power = Column(Integer)
    accuracy = Column(Integer)
    pp = Column(Integer)
    description = Column(Text, nullable=False)
    generation = Column(String(20), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)