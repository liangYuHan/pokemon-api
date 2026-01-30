"""
FastAPI主应用
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import Optional
import uvicorn

# 创建FastAPI应用
app = FastAPI(
    title="Pokemon API",
    description="宝可梦数据查询API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 添加CORS中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 自定义异常处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": str(exc),
            "data": None
        }
    )

# 根路径
@app.get("/")
async def root():
    return {
        "success": True,
        "message": "欢迎使用宝可梦数据API",
        "data": {
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc",
            "endpoints": {
                "pokemon": "/api/pokemon",
                "moves": "/api/moves", 
                "abilities": "/api/abilities",
                "items": "/api/items"
            }
        }
    }

# 健康检查
@app.get("/health")
async def health_check():
    return {
        "success": True,
        "message": "API运行正常",
        "data": {
            "status": "healthy"
        }
    }

# 导入路由
from app.routers import pokemon, move, ability, item

# 注册路由
app.include_router(pokemon.router, prefix="/api/pokemon", tags=["宝可梦"])
app.include_router(move.router, prefix="/api/moves", tags=["招式"])
app.include_router(ability.router, prefix="/api/abilities", tags=["特性"])
app.include_router(item.router, prefix="/api/items", tags=["道具"])

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)