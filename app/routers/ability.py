"""
特性路由
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.crud import ability_crud

router = APIRouter()

# 模拟特性数据
ABILITIES_DATA = [
    {
        "id": 1,
        "ability_id": 1,
        "name": "茂盛",
        "japanese_name": "しんりょく",
        "english_name": "Overgrow",
        "description": "HP减少的时候，草属性的招式威力会提高。",
        "common_count": 28,
        "hidden_count": 2,
        "generation": "第三世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 2,
        "ability_id": 2,
        "name": "猛火",
        "japanese_name": "もうか",
        "english_name": "Blaze",
        "description": "HP减少的时候，火属性的招式威力会提高。",
        "common_count": 28,
        "hidden_count": 2,
        "generation": "第三世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 3,
        "ability_id": 3,
        "name": "激流",
        "japanese_name": "げきりゅう",
        "english_name": "Torrent",
        "description": "HP减少的时候，水属性的招式威力会提高。",
        "common_count": 28,
        "hidden_count": 2,
        "generation": "第三世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 4,
        "ability_id": 4,
        "name": "静电",
        "japanese_name": "せいでんき",
        "english_name": "Static",
        "description": "身上带有静电，有时会让接触到的对手麻痹。",
        "common_count": 19,
        "hidden_count": 1,
        "generation": "第三世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 5,
        "ability_id": 5,
        "name": "威吓",
        "japanese_name": "いかく",
        "english_name": "Intimidate",
        "description": "出场时威吓对手，让其退缩，降低对手的攻击。",
        "common_count": 34,
        "hidden_count": 7,
        "generation": "第三世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
]


@router.get("/", response_model=dict)
async def get_abilities_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    generation: Optional[str] = Query(None, description="按世代筛选"),
    db: Session = Depends(get_db)
):
    """获取特性列表"""
    try:
        skip = (page - 1) * page_size
        data = ability_crud.get_with_filters(
            db=db,
            skip=skip,
            limit=page_size,
            generation=generation
        )
        total = ability_crud.get_count_with_filters(
            db=db,
            generation=generation
        )
        
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


@router.get("/{ability_id_or_name}", response_model=dict)
async def get_ability(
    ability_id_or_name: str,
    db: Session = Depends(get_db)
):
    """获取单个特性详情"""
    try:
        ability = None
        # 尝试按特性ID查找
        try:
            ability_id = int(ability_id_or_name)
            ability = ability_crud.get_by_ability_id(db=db, ability_id=ability_id)
        except ValueError:
            pass
        
        # 如果未找到，按中文名查找
        if not ability:
            ability = ability_crud.get_by_name(db=db, name=ability_id_or_name)
        
        # 如果未找到，按英文名查找
        if not ability:
            ability = ability_crud.get_by_english_name(db=db, english_name=ability_id_or_name)
        
        if not ability:
            raise HTTPException(status_code=404, detail="特性不存在")
        
        return {
            "success": True,
            "message": "获取成功",
            "data": ability
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"获取失败: {str(e)}",
            "data": None
        }


@router.post("/", response_model=dict)
async def create_ability(
    ability_in: dict,
    db: Session = Depends(get_db)
):
    """创建特性"""
    try:
        ability = ability_crud.create(db=db, obj_in=ability_in)
        return {
            "success": True,
            "message": "创建成功",
            "data": ability
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"创建失败: {str(e)}",
            "data": None
        }


@router.put("/{ability_id}", response_model=dict)
async def update_ability(
    ability_id: int,
    ability_in: dict,
    db: Session = Depends(get_db)
):
    """更新特性"""
    try:
        ability = ability_crud.get(db=db, id=ability_id)
        if not ability:
            raise HTTPException(status_code=404, detail="特性不存在")
        
        ability = ability_crud.update(db=db, db_obj=ability, obj_in=ability_in)
        return {
            "success": True,
            "message": "更新成功",
            "data": ability
        }
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"更新失败: {str(e)}",
            "data": None
        }


@router.delete("/{ability_id}", response_model=dict)
async def delete_ability(
    ability_id: int,
    db: Session = Depends(get_db)
):
    """删除特性"""
    try:
        ability = ability_crud.get(db=db, id=ability_id)
        if not ability:
            raise HTTPException(status_code=404, detail="特性不存在")
        
        ability_crud.remove(db=db, id=ability_id)
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