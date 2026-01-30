"""
宝可梦路由
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.crud import pokemon_crud

router = APIRouter()

# 模拟数据（数据库连接前使用）
MOCK_POKEMON = [
    {
        "id": 1,
        "national_dex": 1,
        "name": "妙蛙种子",
        "japanese_name": "フシギダネ",
        "english_name": "Bulbasaur",
        "type1": "草",
        "type2": None,
        "classification": "种子宝可梦",
        "height": 0.7,
        "weight": 6.9,
        "hp": 45,
        "attack": 49,
        "defense": 49,
        "sp_attack": 65,
        "sp_defense": 65,
        "speed": 45,
        "total_stats": 318,
        "catch_rate": 45,
        "experience_type": "中等偏慢",
        "gender_ratio": "雄性87.5% 雌性12.5%",
        "egg_groups": ["怪獸", "植物"],
        "abilities": ["茂盛", "叶绿素"],
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 2,
        "national_dex": 4,
        "name": "小火龙",
        "japanese_name": "ヒトカゲ",
        "english_name": "Charmander",
        "type1": "火",
        "type2": None,
        "classification": "蜥蜴宝可梦",
        "height": 0.6,
        "weight": 8.5,
        "hp": 39,
        "attack": 52,
        "defense": 43,
        "sp_attack": 60,
        "sp_defense": 50,
        "speed": 65,
        "total_stats": 309,
        "catch_rate": 45,
        "experience_type": "中等偏慢",
        "gender_ratio": "雄性87.5% 雌性12.5%",
        "egg_groups": ["怪獸", "龙"],
        "abilities": ["猛火"],
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 3,
        "national_dex": 7,
        "name": "杰尼龟",
        "japanese_name": "ゼニガメ",
        "english_name": "Squirtle",
        "type1": "水",
        "type2": None,
        "classification": "小龟宝可梦",
        "height": 0.5,
        "weight": 9.0,
        "hp": 44,
        "attack": 48,
        "defense": 65,
        "sp_attack": 50,
        "sp_defense": 64,
        "speed": 43,
        "total_stats": 314,
        "catch_rate": 45,
        "experience_type": "中等偏慢",
        "gender_ratio": "雄性87.5% 雌性12.5%",
        "egg_groups": ["怪獸", "水中1"],
        "abilities": ["激流"],
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
]


@router.get("/", response_model=dict)
async def get_pokemon_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    type: Optional[str] = Query(None, description="按属性筛选"),
    search: Optional[str] = Query(None, description="搜索宝可梦名称"),
    db: Session = Depends(get_db)
):
    """获取宝可梦列表"""
    try:
        skip = (page - 1) * page_size
        data = pokemon_crud.get_with_filters(
            db=db,
            skip=skip,
            limit=page_size,
            type_name=type,
            search=search
        )
        total = pokemon_crud.get_count_with_filters(
            db=db,
            type_name=type,
            search=search
        )
        
        return {
            "success": True,
            "message": "获取成功",
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size,
            "has_next": skip + page_size < total
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取失败: {str(e)}",
            "data": [],
            "total": 0,
            "page": page,
            "page_size": page_size,
            "has_next": False
        }


@router.get("/{pokemon_id_or_name}", response_model=dict)
async def get_pokemon(
    pokemon_id_or_name: str,
    db: Session = Depends(get_db)
):
    """获取单个宝可梦详情"""
    try:
        pokemon = None
        # 尝试按全国图鉴编号查找
        try:
            pokemon_id = int(pokemon_id_or_name)
            pokemon = pokemon_crud.get_by_national_dex(db=db, national_dex=pokemon_id)
        except ValueError:
            pass
        
        # 如果未找到，按中文名查找
        if not pokemon:
            pokemon = pokemon_crud.get_by_name(db=db, name=pokemon_id_or_name)
        
        # 如果未找到，按英文名查找
        if not pokemon:
            pokemon = pokemon_crud.get_by_english_name(db=db, english_name=pokemon_id_or_name)
        
        if not pokemon:
            raise HTTPException(status_code=404, detail="宝可梦不存在")
        
        return {
            "success": True,
            "message": "获取成功",
            "data": pokemon
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"获取失败: {str(e)}",
            "data": None
        }


@router.get("/type/{type_name}", response_model=dict)
async def get_pokemon_by_type(
    type_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """按属性获取宝可梦"""
    try:
        skip = (page - 1) * page_size
        data = pokemon_crud.get_by_type(
            db=db,
            type_name=type_name,
            skip=skip,
            limit=page_size
        )
        total = pokemon_crud.get_count_by_type(db=db, type_name=type_name)
        
        return {
            "success": True,
            "message": "获取成功",
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"获取失败: {str(e)}",
            "data": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }


@router.get("/search/{query}", response_model=dict)
async def search_pokemon(
    query: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """搜索宝可梦"""
    try:
        skip = (page - 1) * page_size
        data = pokemon_crud.search_pokemon(
            db=db,
            query=query,
            skip=skip,
            limit=page_size
        )
        total = pokemon_crud.get_search_count(db=db, query=query)
        
        return {
            "success": True,
            "message": "搜索成功",
            "data": data,
            "total": total,
            "page": page,
            "page_size": page_size
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"搜索失败: {str(e)}",
            "data": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }


@router.post("/", response_model=dict)
async def create_pokemon(
    pokemon_in: dict,
    db: Session = Depends(get_db)
):
    """创建宝可梦"""
    try:
        pokemon = pokemon_crud.create(db=db, obj_in=pokemon_in)
        return {
            "success": True,
            "message": "创建成功",
            "data": pokemon
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"创建失败: {str(e)}",
            "data": None
        }


@router.put("/{pokemon_id}", response_model=dict)
async def update_pokemon(
    pokemon_id: int,
    pokemon_in: dict,
    db: Session = Depends(get_db)
):
    """更新宝可梦"""
    try:
        pokemon = pokemon_crud.get(db=db, id=pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="宝可梦不存在")
        
        pokemon = pokemon_crud.update(db=db, db_obj=pokemon, obj_in=pokemon_in)
        return {
            "success": True,
            "message": "更新成功",
            "data": pokemon
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"更新失败: {str(e)}",
            "data": None
        }


@router.delete("/{pokemon_id}", response_model=dict)
async def delete_pokemon(
    pokemon_id: int,
    db: Session = Depends(get_db)
):
    """删除宝可梦"""
    try:
        pokemon = pokemon_crud.get(db=db, id=pokemon_id)
        if not pokemon:
            raise HTTPException(status_code=404, detail="宝可梦不存在")
        
        pokemon_crud.remove(db=db, id=pokemon_id)
        return {
            "success": True,
            "message": "删除成功",
            "data": None
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"删除失败: {str(e)}",
            "data": None
        }