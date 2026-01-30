"""
招式CRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pokemon import Move
from app.schemas import MoveCreate, MoveUpdate


class CRUDMove(CRUDBase[Move, MoveCreate, MoveUpdate]):
    def get_by_move_id(self, db: Session, *, move_id: int) -> Optional[Move]:
        return db.query(Move).filter(Move.move_id == move_id).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[Move]:
        return db.query(Move).filter(Move.name == name).first()

    def get_by_english_name(self, db: Session, *, english_name: str) -> Optional[Move]:
        return db.query(Move).filter(Move.english_name == english_name).first()

    def get_by_type(
        self,
        db: Session,
        *,
        type_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Move]:
        return db.query(Move).filter(Move.type == type_name).offset(skip).limit(limit).all()

    def get_count_by_type(self, db: Session, *, type_name: str) -> int:
        return db.query(Move).filter(Move.type == type_name).count()

    def get_by_category(
        self,
        db: Session,
        *,
        category: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Move]:
        return db.query(Move).filter(Move.category == category).offset(skip).limit(limit).all()

    def get_count_by_category(self, db: Session, *, category: str) -> int:
        return db.query(Move).filter(Move.category == category).count()

    def get_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        type_name: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Move]:
        query = db.query(Move)

        if type_name:
            query = query.filter(Move.type == type_name)

        if category:
            query = query.filter(Move.category == category)

        return query.offset(skip).limit(limit).all()

    def get_count_with_filters(
        self,
        db: Session,
        *,
        type_name: Optional[str] = None,
        category: Optional[str] = None
    ) -> int:
        query = db.query(Move)

        if type_name:
            query = query.filter(Move.type == type_name)

        if category:
            query = query.filter(Move.category == category)

        return query.count()


move_crud = CRUDMove(Move)
