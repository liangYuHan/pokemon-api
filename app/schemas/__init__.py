"""
Pydantic输入输出模型
"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime


class PokemonBase(BaseModel):
    """宝可梦基础模型"""
    name: str
    japanese_name: str
    english_name: str
    type1: str
    type2: Optional[str] = None
    classification: str
    height: Optional[float] = None
    weight: Optional[float] = None


class PokemonCreate(PokemonBase):
    """创建宝可梦模型"""
    pass


class PokemonUpdate(PokemonBase):
    """更新宝可梦模型"""
    pass


class Pokemon(PokemonBase):
    """宝可梦响应模型"""
    id: int
    national_dex: int
    hp: Optional[int] = None
    attack: Optional[int] = None
    defense: Optional[int] = None
    sp_attack: Optional[int] = None
    sp_defense: Optional[int] = None
    speed: Optional[int] = None
    total_stats: Optional[int] = None
    catch_rate: Optional[int] = None
    experience_type: Optional[str] = None
    gender_ratio: Optional[str] = None
    egg_groups: Optional[List[str]] = None
    abilities: Optional[List[str]] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class PokemonResponse(BaseModel):
    """API响应模型"""
    success: bool = True
    message: str = ""
    data: Optional[Pokemon] = None
    total: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


class PokemonListResponse(BaseModel):
    """宝可梦列表响应模型"""
    success: bool = True
    message: str = ""
    data: List[Pokemon] = []
    total: int
    page: int
    page_size: int


# 招式模型
class MoveBase(BaseModel):
    """招式基础模型"""
    name: str
    japanese_name: str
    english_name: str
    type: str
    category: str  # 物理/特殊/变化


class MoveCreate(MoveBase):
    """创建招式模型"""
    pass


class MoveUpdate(MoveBase):
    """更新招式模型"""
    pass


class Move(MoveBase):
    """招式响应模型"""
    id: int
    move_id: int
    power: Optional[int] = None
    accuracy: Optional[int] = None
    pp: Optional[int] = None
    description: str
    generation: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class MoveResponse(BaseModel):
    """招式API响应模型"""
    success: bool = True
    message: str = ""
    data: Optional[Move] = None
    total: Optional[int] = None


class MoveListResponse(BaseModel):
    """招式列表响应模型"""
    success: bool = True
    message: str = ""
    data: List[Move] = []
    total: int
    page: int
    page_size: int


# 特性模型
class AbilityBase(BaseModel):
    """特性基础模型"""
    name: str
    japanese_name: str
    english_name: str
    description: str


class AbilityCreate(AbilityBase):
    """创建特性模型"""
    pass


class AbilityUpdate(AbilityBase):
    """更新特性模型"""
    pass


class Ability(AbilityBase):
    """特性响应模型"""
    id: int
    ability_id: int
    common_count: Optional[int] = None
    hidden_count: Optional[int] = None
    generation: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class AbilityResponse(BaseModel):
    """特性API响应模型"""
    success: bool = True
    message: str = ""
    data: Optional[Ability] = None
    total: Optional[int] = None


class AbilityListResponse(BaseModel):
    """特性列表响应模型"""
    success: bool = True
    message: str = ""
    data: List[Ability] = []
    total: int
    page: int
    page_size: int


# 道具模型
class ItemBase(BaseModel):
    """道具基础模型"""
    name: str
    japanese_name: str
    english_name: str
    category: str
    description: str


class ItemCreate(ItemBase):
    """创建道具模型"""
    pass


class ItemUpdate(ItemBase):
    """更新道具模型"""
    pass


class Item(ItemBase):
    """道具响应模型"""
    id: int
    generation: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    """道具API响应模型"""
    success: bool = True
    message: str = ""
    data: Optional[Item] = None
    total: Optional[int] = None


class ItemListResponse(BaseModel):
    """道具列表响应模型"""
    success: bool = True
    message: str = ""
    data: List[Item] = []
    total: int
    page: int
    page_size: int


# 搜索和筛选模型
class SearchQuery(BaseModel):
    """搜索查询模型"""
    query: Optional[str] = None
    type: Optional[str] = None
    category: Optional[str] = None
    generation: Optional[str] = None
    limit: Optional[int] = 20


# 分页参数模型
class PaginationParams(BaseModel):
    """分页参数模型"""
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")