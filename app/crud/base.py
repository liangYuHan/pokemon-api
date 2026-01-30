"""
基础CRUD类
"""
from typing import TypeVar, Generic, Type, Optional, List, Any
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import select, func

ModelType = TypeVar("ModelType")
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    def get(self, db: Session, id: int) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    def get_count(self, db: Session) -> int:
        return db.query(func.count(self.model.id)).scalar()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.dict() if hasattr(obj_in, 'dict') else obj_in
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any]
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj

    def get_by_field(
        self, db: Session, *, field_name: str, field_value: Any
    ) -> Optional[ModelType]:
        return db.query(self.model).filter(
            getattr(self.model, field_name) == field_value
        ).first()

    def get_multi_by_field(
        self,
        db: Session,
        *,
        field_name: str,
        field_value: Any,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).filter(
            getattr(self.model, field_name) == field_value
        ).offset(skip).limit(limit).all()

    def search(
        self,
        db: Session,
        *,
        query: str,
        search_fields: List[str],
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        conditions = []
        for field in search_fields:
            conditions.append(
                getattr(self.model, field).ilike(f"%{query}%")
            )
        return db.query(self.model).filter(
            func.or_(*conditions)
        ).offset(skip).limit(limit).all()

    def get_count_by_field(
        self, db: Session, *, field_name: str, field_value: Any
    ) -> int:
        return db.query(func.count(self.model.id)).filter(
            getattr(self.model, field_name) == field_value
        ).scalar()

    def get_search_count(
        self, db: Session, *, query: str, search_fields: List[str]
    ) -> int:
        conditions = []
        for field in search_fields:
            conditions.append(
                getattr(self.model, field).ilike(f"%{query}%")
            )
        return db.query(func.count(self.model.id)).filter(
            func.or_(*conditions)
        ).scalar()
