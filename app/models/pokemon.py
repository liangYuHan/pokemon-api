"""
宝可梦数据库模型
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Pokemon(Base):
    """宝可梦表"""
    __tablename__ = "pokemon"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    national_dex = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    japanese_name = Column(String(100), nullable=False)
    english_name = Column(String(100), nullable=False, index=True)
    type1 = Column(String(20), nullable=False, index=True)
    type2 = Column(String(20))
    classification = Column(String(100))
    height = Column(Float)
    weight = Column(Float)
    hp = Column(Integer)
    attack = Column(Integer)
    defense = Column(Integer)
    sp_attack = Column(Integer)
    sp_defense = Column(Integer)
    speed = Column(Integer)
    total_stats = Column(Integer)
    catch_rate = Column(Integer)
    experience_type = Column(String(50))
    gender_ratio = Column(String(50))
    egg_groups = Column(JSON)
    abilities = Column(JSON)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    
    # 关联关系
    moves = relationship("PokemonMove", back_populates="pokemon")


class Move(Base):
    """招式表"""
    __tablename__ = "moves"
    __table_args__ = {'extend_existing': True}
    
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
    
    # 关联关系
    pokemon_moves = relationship("PokemonMove", back_populates="move")


class Ability(Base):
    """特性表"""
    __tablename__ = "abilities"
    __table_args__ = {'extend_existing': True}
    
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


class Item(Base):
    """道具表"""
    __tablename__ = "items"
    __table_args__ = {'extend_existing': True}
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, unique=True, index=True)
    japanese_name = Column(String(200), nullable=False)
    english_name = Column(String(200), nullable=False, index=True)
    category = Column(String(50), nullable=False, index=True)
    description = Column(Text, nullable=False)
    generation = Column(String(20), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class PokemonMove(Base):
    """宝可梦-招式关联表"""
    __tablename__ = "pokemon_moves"
    __table_args__ = (
        Index('idx_pokemon_id', 'pokemon_id'),
        Index('idx_move_id', 'move_id'),
        Index('idx_pokemon_move', 'pokemon_id', 'move_id'),
        {'extend_existing': True}
    )
    
    id = Column(Integer, primary_key=True, index=True)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'), nullable=False)
    move_id = Column(Integer, ForeignKey('moves.id'), nullable=False)
    learn_method = Column(String(50))  # 学习方式：升级、招式学习器、遗传等
    learn_level = Column(Integer)  # 学习等级
    
    # 关联关系
    pokemon = relationship("Pokemon", back_populates="moves")
    move = relationship("Move", back_populates="pokemon_moves")