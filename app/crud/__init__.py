"""
CRUD包初始化
"""
from app.crud.pokemon import pokemon_crud
from app.crud.move import move_crud
from app.crud.ability import ability_crud
from app.crud.item import item_crud

__all__ = ["pokemon_crud", "move_crud", "ability_crud", "item_crud"]
