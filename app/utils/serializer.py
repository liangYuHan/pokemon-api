"""
序列化工具
"""
from typing import List, Any, Type, TypeVar
from pydantic import BaseModel
from sqlalchemy.orm import Session

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)


def model_to_dict(model: Any) -> dict:
    """将SQLAlchemy模型转换为字典"""
    if model is None:
        return None
    
    result = {}
    for column in model.__table__.columns:
        value = getattr(model, column.name)
        
        # 处理特殊类型
        if hasattr(value, 'isoformat'):
            value = value.isoformat()
        elif value is None:
            value = None
        
        result[column.name] = value
    
    return result


def models_to_list(models: List[Any]) -> List[dict]:
    """将SQLAlchemy模型列表转换为字典列表"""
    return [model_to_dict(model) for model in models]


def serialize_response(
    data: Any,
    success: bool = True,
    message: str = "操作成功",
    **kwargs
) -> dict:
    """序列化API响应"""
    response = {
        "success": success,
        "message": message,
        "data": data
    }
    
    # 添加额外字段
    response.update(kwargs)
    
    return response
