"""
招式路由
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional, List

from app.database import get_db
from app.crud import move_crud
from app.utils.serializer import model_to_dict, models_to_list, serialize_response

router = APIRouter()

# 模拟招式数据
MOVES_DATA = [
    {
        "id": 1,
        "move_id": 1,
        "name": "拍击",
        "japanese_name": "はたく",
        "english_name": "Pound",
        "type": "一般",
        "category": "物理",
        "power": 40,
        "accuracy": 100,
        "pp": 35,
        "description": "使用长长的尾巴或手等拍打对手进行攻击。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 2,
        "move_id": 2,
        "name": "空手劈",
        "japanese_name": "からてチョップ",
        "english_name": "Karate Chop",
        "type": "格斗",
        "category": "物理",
        "power": 50,
        "accuracy": 100,
        "pp": 25,
        "description": "用锋利的手刀劈向对手进行攻击。容易击中要害。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 3,
        "move_id": 3,
        "name": "火焰拳",
        "japanese_name": "ほのおのパンチ",
        "english_name": "Fire Punch",
        "type": "火",
        "category": "物理",
        "power": 75,
        "accuracy": 100,
        "pp": 15,
        "description": "用充满火焰的拳头攻击对手。有时会让对手陷入灼伤状态。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 4,
        "move_id": 4,
        "name": "十万伏特",
        "japanese_name": "１０まんボルト",
        "english_name": "Thunderbolt",
        "type": "电",
        "category": "特殊",
        "power": 90,
        "accuracy": 100,
        "pp": 15,
        "description": "向对手发出强力电击进行攻击。有时会让对手陷入麻痹状态。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    },
    {
        "id": 5,
        "move_id": 5,
        "name": "喷射火焰",
        "japanese_name": "かえんほうしゃ",
        "english_name": "Flamethrower",
        "type": "火",
        "category": "特殊",
        "power": 90,
        "accuracy": 100,
        "pp": 15,
        "description": "向对手发射烈焰进行攻击。有时会让对手陷入灼伤状态。",
        "generation": "第一世代",
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-01T00:00:00"
    }
]


@router.get("/", response_model=dict)
async def get_moves_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    type: Optional[str] = Query(None, description="按属性筛选"),
    category: Optional[str] = Query(None, description="按分类筛选（物理/特殊/变化）"),
    db: Session = Depends(get_db)
):
    """获取招式列表"""
    try:
        skip = (page - 1) * page_size
        data = move_crud.get_with_filters(
            db=db,
            skip=skip,
            limit=page_size,
            type_name=type,
            category=category
        )
        total = move_crud.get_count_with_filters(
            db=db,
            type_name=type,
            category=category
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


@router.get("/{move_id_or_name}", response_model=dict)
async def get_move(
    move_id_or_name: str,
    db: Session = Depends(get_db)
):
    """获取单个招式详情"""
    try:
        move = None
        # 尝试按招式ID查找
        try:
            move_id = int(move_id_or_name)
            move = move_crud.get_by_move_id(db=db, move_id=move_id)
        except ValueError:
            pass
        
        # 如果未找到，按中文名查找
        if not move:
            move = move_crud.get_by_name(db=db, name=move_id_or_name)
        
        # 如果未找到，按英文名查找
        if not move:
            move = move_crud.get_by_english_name(db=db, english_name=move_id_or_name)
        
        if not move:
            raise HTTPException(status_code=404, detail="招式不存在")
        
        return serialize_response(data=model_to_dict(move))
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"获取失败: {str(e)}",
            "data": None
        }


@router.get("/type/{type_name}", response_model=dict)
async def get_moves_by_type(
    type_name: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """按属性获取招式"""
    try:
        skip = (page - 1) * page_size
        data = move_crud.get_by_type(
            db=db,
            type_name=type_name,
            skip=skip,
            limit=page_size
        )
        total = move_crud.get_count_by_type(db=db, type_name=type_name)
        
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
async def create_move(
    move_in: dict,
    db: Session = Depends(get_db)
):
    """创建招式"""
    try:
        move = move_crud.create(db=db, obj_in=move_in)
        return serialize_response(data=model_to_dict(move))
    except Exception as e:
        return {
            "success": False,
            "message": f"创建失败: {str(e)}",
            "data": None
        }


@router.put("/{move_id}", response_model=dict)
async def update_move(
    move_id: int,
    move_in: dict,
    db: Session = Depends(get_db)
):
    """更新招式"""
    try:
        move = move_crud.get(db=db, id=move_id)
        if not move:
            raise HTTPException(status_code=404, detail="招式不存在")
        
        move = move_crud.update(db=db, db_obj=move, obj_in=move_in)
        return serialize_response(data=model_to_dict(move))
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"更新失败: {str(e)}",
            "data": None
        }


@router.delete("/{move_id}", response_model=dict)
async def delete_move(
    move_id: int,
    db: Session = Depends(get_db)
):
    """删除招式"""
    try:
        move = move_crud.get(db=db, id=move_id)
        if not move:
            raise HTTPException(status_code=404, detail="招式不存在")
        
        move_crud.remove(db=db, id=move_id)
        return serialize_response(data=model_to_dict(None))
    except HTTPException:
        raise
    except Exception as e:
        return {
            "success": False,
            "message": f"删除失败: {str(e)}",
            "data": None
        }