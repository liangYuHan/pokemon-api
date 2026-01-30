"""
特性CRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.pokemon import Ability
from app.schemas import AbilityCreate, AbilityUpdate


class CRUDAbility(CRUDBase[Ability, AbilityCreate, AbilityUpdate]):
    def get_by_ability_id(self, db: Session, *, ability_id: int) -> Optional[Ability]:
        return db.query(Ability).filter(Ability.ability_id == ability_id).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[Ability]:
        return db.query(Ability).filter(Ability.name == name).first()

    def get_by_english_name(self, db: Session, *, english_name: str) -> Optional[Ability]:
        return db.query(Ability).filter(Ability.english_name == english_name).first()

    def get_by_generation(
        self,
        db: Session,
        *,
        generation: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Ability]:
        return db.query(Ability).filter(Ability.generation == generation).offset(skip).limit(limit).all()

    def get_count_by_generation(self, db: Session, *, generation: str) -> int:
        return db.query(Ability).filter(Ability.generation == generation).count()

    def get_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        generation: Optional[str] = None
    ) -> List[Ability]:
        query = db.query(Ability)

        if generation:
            query = query.filter(Ability.generation == generation)

        return query.offset(skip).limit(limit).all()

    def get_count_with_filters(
        self,
        db: Session,
        *,
        generation: Optional[str] = None
    ) -> int:
        query = db.query(Ability)

        if generation:
            query = query.filter(Ability.generation == generation)

        return query.count()


ability_crud = CRUDAbility(Ability)
