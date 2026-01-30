"""
道具路由
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.crud import item_crud

router = APIRouter()
from app.utils.serializer import model_to_dict, models_to_list, serialize_response

# 模拟道具数据
ITEMS_DATA = [
    {
        "id": 1,
        "name": "除虫喷雾",
        "japanese_name": "むしよけスプレー",
        "english_name": "Repel",
        "category": "野外使用",
        "description": "使用后，在较短时间内，弱小的野生宝可梦将完全不会出现。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 2,
        "name": "精灵球",
        "japanese_name": "モンスターボール",
        "english_name": "Poké Ball",
        "category": "精灵球",
        "description": "用于捕捉野生宝可梦的基础精灵球。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 3,
        "name": "超级球",
        "japanese_name": "ハイパーボール",
        "english_name": "Ultra Ball",
        "category": "精灵球",
        "description": "比精灵球更容易捕捉野生宝可梦。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 4,
        "name": "伤药",
        "japanese_name": "キズぐすり",
        "english_name": "Potion",
        "category": "回复道具",
        "description": "回复宝可梦20点HP。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 5,
        "name": "好伤药",
        "japanese_name": "いいきずぐすり",
        "english_name": "Super Potion",
        "category": "回复道具",
        "description": "回复宝可梦60点HP。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
]


@router.get("/", response_model=dict)
async def get_items_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    category: Optional[str] = Query(None, description="按分类筛选"),
    generation: Optional[str] = Query(None, description="按世代筛选"),
    db: Session = Depends(get_db)
):
    """获取道具列表"""
    try:
        skip = (page - 1) * page_size
        data = item_crud.get_with_filters(
            db=db,
            skip=skip,
            limit=page_size,
            category=category,
            generation=generation
        )
        total = item_crud.get_count_with_filters(
            db=db,
            category=category,
            generation=generation
        )
        
        return serialize_response(data=models_to_list(data), total=total, page=page, page_size=page_size, message="获取成功")
    except Exception as e:
        return {
            "success": False,
            "message": f"获取失败: {str(e)}",
            "data": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }


@router.get("/{item_name}", response_model=dict)
async def get_item(
    item_name: str,
    db: Session = Depends(get_db)
):
    """获取单个道具详情"""
    try:
        item = None
        # 按中文名查找
        item = item_crud.get_by_name(db=db, name=item_name)
        
        # 如果未找到，按英文名查找
        if not item:
            item = item_crud.get_by_english_name(db=db, english_name=item_name)
        
        if not item:
            raise HTTPException(status_code=404, detail="道具不存在")
        
        return serialize_response(data=model_to_dict(item))
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"获取失败: {str(e)}",
            "data": None
        }


@router.get("/category/{category}", response_model=dict)
async def get_items_by_category(
    category: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """按分类获取道具"""
    try:
        skip = (page - 1) * page_size
        data = item_crud.get_by_category(
            db=db,
            category=category,
            skip=skip,
            limit=page_size
        )
        total = item_crud.get_count_by_category(db=db, category=category)
        
        return serialize_response(data=models_to_list(data), total=total, page=page, page_size=page_size, message="获取成功")
    except Exception as e:
        return {
            "success": False,
            "message": f"获取失败: {str(e)}",
            "data": [],
            "total": 0,
            "page": page,
            "page_size": page_size
        }


@router.post("/", response_model=dict)
async def create_item(
    item_in: dict,
    db: Session = Depends(get_db)
):
    """创建道具"""
    try:
        item = item_crud.create(db=db, obj_in=item_in)
        return serialize_response(data=model_to_dict(item))
    except Exception as e:
        return {
            "success": False,
            "message": f"创建失败: {str(e)}",
            "data": None
        }


@router.put("/{item_name}", response_model=dict)
async def update_item(
    item_name: str,
    item_in: dict,
    db: Session = Depends(get_db)
):
    """更新道具"""
    try:
        item = item_crud.get_by_name(db=db, name=item_name)
        if not item:
            raise HTTPException(status_code=404, detail="道具不存在")
        
        item = item_crud.update(db=db, db_obj=item, obj_in=item_in)
        return serialize_response(data=model_to_dict(item))
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"更新失败: {str(e)}",
            "data": None
        }


@router.delete("/{item_name}", response_model=dict)
async def delete_item(
    item_name: str,
    db: Session = Depends(get_db)
):
    """删除道具"""
    try:
        item = item_crud.get_by_name(db=db, name=item_name)
        if not item:
            raise HTTPException(status_code=404, detail="道具不存在")
        
        db.delete(item)
        db.commit()
        return serialize_response(data=model_to_dict(None))
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"删除失败: {str(e)}",
            "data": None
        }