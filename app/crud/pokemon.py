"""
宝可梦CRUD操作
"""
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.crud.base import CRUDBase
from app.models.pokemon import Pokemon
from app.schemas import PokemonCreate, PokemonUpdate


class CRUDPokemon(CRUDBase[Pokemon, PokemonCreate, PokemonUpdate]):
    def get_by_national_dex(self, db: Session, *, national_dex: int) -> Optional[Pokemon]:
        return db.query(Pokemon).filter(Pokemon.national_dex == national_dex).first()

    def get_by_name(self, db: Session, *, name: str) -> Optional[Pokemon]:
        return db.query(Pokemon).filter(Pokemon.name == name).first()

    def get_by_english_name(self, db: Session, *, english_name: str) -> Optional[Pokemon]:
        return db.query(Pokemon).filter(Pokemon.english_name == english_name).first()

    def get_by_type(
        self,
        db: Session,
        *,
        type_name: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Pokemon]:
        return db.query(Pokemon).filter(
            or_(Pokemon.type1 == type_name, Pokemon.type2 == type_name)
        ).offset(skip).limit(limit).all()

    def get_count_by_type(self, db: Session, *, type_name: str) -> int:
        return db.query(Pokemon).filter(
            or_(Pokemon.type1 == type_name, Pokemon.type2 == type_name)
        ).count()

    def search_pokemon(
        self,
        db: Session,
        *,
        query: str,
        skip: int = 0,
        limit: int = 100
    ) -> List[Pokemon]:
        return db.query(Pokemon).filter(
            or_(
                Pokemon.name.ilike(f"%{query}%"),
                Pokemon.english_name.ilike(f"%{query}%"),
                Pokemon.japanese_name.ilike(f"%{query}%")
            )
        ).offset(skip).limit(limit).all()

    def get_search_count(self, db: Session, *, query: str) -> int:
        return db.query(Pokemon).filter(
            or_(
                Pokemon.name.ilike(f"%{query}%"),
                Pokemon.english_name.ilike(f"%{query}%"),
                Pokemon.japanese_name.ilike(f"%{query}%")
            )
        ).count()

    def get_with_filters(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        type_name: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Pokemon]:
        query = db.query(Pokemon)

        if type_name:
            query = query.filter(
                or_(Pokemon.type1 == type_name, Pokemon.type2 == type_name)
            )

        if search:
            query = query.filter(
                or_(
                    Pokemon.name.ilike(f"%{search}%"),
                    Pokemon.english_name.ilike(f"%{search}%"),
                    Pokemon.japanese_name.ilike(f"%{search}%")
                )
            )

        return query.offset(skip).limit(limit).all()

    def get_count_with_filters(
        self,
        db: Session,
        *,
        type_name: Optional[str] = None,
        search: Optional[str] = None
    ) -> int:
        query = db.query(Pokemon)

        if type_name:
            query = query.filter(
                or_(Pokemon.type1 == type_name, Pokemon.type2 == type_name)
            )

        if search:
            query = query.filter(
                or_(
                    Pokemon.name.ilike(f"%{search}%"),
                    Pokemon.english_name.ilike(f"%{search}%"),
                    Pokemon.japanese_name.ilike(f"%{search}%")
                )
            )

        return query.count()


pokemon_crud = CRUDPokemon(Pokemon)
