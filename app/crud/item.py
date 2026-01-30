"""
道具CRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pokemon import Item
from app.schemas import ItemCreate, ItemUpdate


class CRUDItem(CRUDBase[Item, ItemCreate, ItemUpdate]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Item]:
        return db.query(Item).filter(Item.name == name).first()

    def get_by_english_name(self, db: Session, *, english_name: str) -> Optional[Item]:
        return db.query(Item).filter(Item.english_name == english_name).first()

    def get_by_category(
        self,
        db: Session,
        *,
        category: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        return db.query(Item).filter(Item.category == category).offset(skip).limit(limit).all()

    def get_count_by_category(self, db: Session, *, category: str) -> int:
        return db.query(Item).filter(Item.category == category).count()

    def get_by_generation(
        self,
        db: Session,
        *,
        generation: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Item]:
        return db.query(Item).filter(Item.generation == generation).offset(skip).limit(limit).all()

    def get_count_by_generation(self, db: Session, *, generation: str) -> int:
        return db.query(Item).filter(Item.generation == generation).count()

    def get_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        category: Optional[str] = None,
        generation: Optional[str] = None
    ) -> List[Item]:
        query = db.query(Item)

        if category:
            query = query.filter(Item.category == category)

        if generation:
            query = query.filter(Item.generation == generation)

        return query.offset(skip).limit(limit).all()

    def get_count_with_filters(
        self,
        db: Session,
        *,
        category: Optional[str] = None,
        generation: Optional[str] = None
    ) -> int:
        query = db.query(Item)

        if category:
            query = query.filter(Item.category == category)

        if generation:
            query = query.filter(Item.generation == generation)

        return query.count()


item_crud = CRUDItem(Item)
