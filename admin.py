"""
FastAPI Admin配置
"""
from app.main import app
from app.models.pokemon import Pokemon, Move, Ability, Item
from app.database import engine
from fastapi_admin.app import app as admin_app
from fastapi_admin import Admin
from fastapi_admin.resources import Field, Model
from fastapi_admin.widgets import displays, inputs

# 创建认证后台
class AdminAuth:
    async def login(self, username: str, password: str):
        # 简单认证：在生产环境中应该使用数据库或JWT
        if username == "admin" and password == "admin":
            return True
        return False
    
    async def logout(self):
        pass

# 创建Admin实例
admin = Admin(
    app,
    engine,
    authentication_backend=AdminAuth(),
    title="宝可梦数据管理后台",
    logo_url="https://media.52poke.com/wiki/4/4b/Wikilogo.png"
)

# 注册宝可梦模型
@admin.register
class PokemonAdmin(Model):
    label = "宝可梦"
    model = Pokemon
    page_size = 20

    fields = [
        "id",
        Field(name="national_dex", label="全国图鉴编号", display=displays.InputOnly()),
        Field(name="name", label="名称", input_=inputs.Input()),
        Field(name="japanese_name", label="日文名", input_=inputs.Input()),
        Field(name="english_name", label="英文名", input_=inputs.Input()),
        Field(name="type1", label="属性1", input_=inputs.Input()),
        Field(name="type2", label="属性2", input_=inputs.Input()),
        Field(name="classification", label="分类", input_=inputs.Input()),
        Field(name="height", label="身高(m)", input_=inputs.Input()),
        Field(name="weight", label="体重(kg)", input_=inputs.Input()),
        Field(name="hp", label="HP", input_=inputs.Input()),
        Field(name="attack", label="攻击", input_=inputs.Input()),
        Field(name="defense", label="防御", input_=inputs.Input()),
        Field(name="sp_attack", label="特攻", input_=inputs.Input()),
        Field(name="sp_defense", label="特防", input_=inputs.Input()),
        Field(name="speed", label="速度", input_=inputs.Input()),
        Field(name="total_stats", label="种族值总和", input_=inputs.Input()),
        Field(name="catch_rate", label="捕获率", input_=inputs.Input()),
        Field(name="experience_type", label="经验类型", input_=inputs.Input()),
        Field(name="gender_ratio", label="性别比例", input_=inputs.Input()),
    ]

# 注册招式模型
@admin.register
class MoveAdmin(Model):
    label = "招式"
    model = Move
    page_size = 20

    fields = [
        "id",
        Field(name="move_id", label="招式ID", display=displays.InputOnly()),
        Field(name="name", label="名称", input_=inputs.Input()),
        Field(name="japanese_name", label="日文名", input_=inputs.Input()),
        Field(name="english_name", label="英文名", input_=inputs.Input()),
        Field(name="type", label="属性", input_=inputs.Input()),
        Field(name="category", label="分类", input_=inputs.Input()),
        Field(name="power", label="威力", input_=inputs.Input()),
        Field(name="accuracy", label="命中率", input_=inputs.Input()),
        Field(name="pp", label="PP", input_=inputs.Input()),
        Field(name="description", label="描述", input_=inputs.TextArea()),
        Field(name="generation", label="世代", input_=inputs.Input()),
    ]

# 注册特性模型
@admin.register
class AbilityAdmin(Model):
    label = "特性"
    model = Ability
    page_size = 20

    fields = [
        "id",
        Field(name="ability_id", label="特性ID", display=displays.InputOnly()),
        Field(name="name", label="名称", input_=inputs.Input()),
        Field(name="japanese_name", label="日文名", input_=inputs.Input()),
        Field(name="english_name", label="英文名", input_=inputs.Input()),
        Field(name="description", label="描述", input_=inputs.TextArea()),
        Field(name="common_count", label="通常特性数量", input_=inputs.Input()),
        Field(name="hidden_count", label="隐藏特性数量", input_=inputs.Input()),
        Field(name="generation", label="世代", input_=inputs.Input()),
    ]

# 注册道具模型
@admin.register
class ItemAdmin(Model):
    label = "道具"
    model = Item
    page_size = 20

    fields = [
        "id",
        Field(name="name", label="名称", input_=inputs.Input()),
        Field(name="japanese_name", label="日文名", input_=inputs.Input()),
        Field(name="english_name", label="英文名", input_=inputs.Input()),
        Field(name="category", label="分类", input_=inputs.Input()),
        Field(name="description", label="描述", input_=inputs.TextArea()),
        Field(name="generation", label="世代", input_=inputs.Input()),
    ]