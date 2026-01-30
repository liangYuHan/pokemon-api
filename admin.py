"""
简单的管理后台
"""
from app.main import app
from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

# 管理后台路由
admin_router = APIRouter()

# 简单的认证检查
async def check_admin(request: Request):
    # 简单的session认证（生产环境应该使用JWT）
    session = request.cookies.get("admin_session")
    if session == "admin_logged_in":
        return True
    return False

@admin_router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """管理后台首页"""
    is_logged_in = await check_admin(request)
    if not is_logged_in:
        return RedirectResponse(url="/admin/login", status_code=303)
    
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>宝可梦数据管理后台</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; }
            .header { background: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
            .card { background: white; padding: 20px; margin-bottom: 20px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
            .card h2 { margin-top: 0; color: #3498db; }
            .menu { display: flex; gap: 10px; flex-wrap: wrap; }
            .menu-item { background: #3498db; color: white; padding: 10px 20px; border-radius: 5px; text-decoration: none; }
            .menu-item:hover { background: #2980b9; }
            .btn { background: #e74c3c; color: white; padding: 5px 15px; border: none; border-radius: 3px; cursor: pointer; }
            .btn:hover { background: #c0392b; }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎮 宝可梦数据管理后台</h1>
                <p>欢迎使用数据管理系统</p>
            </div>
            
            <div class="card">
                <h2>快速导航</h2>
                <div class="menu">
                    <a href="/docs" class="menu-item">📚 API文档</a>
                    <a href="/api/pokemon" class="menu-item">🐾 宝可梦管理</a>
                    <a href="/api/moves" class="menu-item">⚔️ 招式管理</a>
                    <a href="/api/abilities" class="menu-item">✨ 特性管理</a>
                    <a href="/api/items" class="menu-item">🎒 道具管理</a>
                    <a href="/admin/logout" class="btn">退出登录</a>
                </div>
            </div>
            
            <div class="card">
                <h2>数据统计</h2>
                <p>请使用API文档中的接口进行数据管理操作。</p>
                <p><strong>提示：</strong></p>
                <ul>
                    <li>使用 GET 方法查看数据</li>
                    <li>使用 POST 方法添加数据</li>
                    <li>使用 PUT 方法更新数据</li>
                    <li>使用 DELETE 方法删除数据</li>
                </ul>
            </div>
            
            <div class="card">
                <h2>快速链接</h2>
                <ul>
                    <li><a href="/docs">Swagger UI - 交互式API文档</a></li>
                    <li><a href="/redoc">ReDoc - 美观的API文档</a></li>
                    <li><a href="/health">健康检查</a></li>
                    <li><a href="/">API首页</a></li>
                </ul>
            </div>
        </div>
    </body>
    </html>
    """
    return html_content

@admin_router.get("/login", response_class=HTMLResponse)
async def admin_login():
    """登录页面"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>管理后台登录</title>
        <meta charset="utf-8">
        <style>
            body { font-family: Arial, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; background: #f5f5f5; margin: 0; }
            .login-box { background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 300px; }
            h2 { text-align: center; color: #3498db; margin-bottom: 30px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 5px; color: #333; }
            input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; box-sizing: border-box; }
            button { width: 100%; padding: 10px; background: #3498db; color: white; border: none; border-radius: 5px; cursor: pointer; font-size: 16px; }
            button:hover { background: #2980b9; }
        </style>
    </head>
    <body>
        <div class="login-box">
            <h2>🔐 管理后台登录</h2>
            <form action="/admin/auth" method="POST">
                <div class="form-group">
                    <label>用户名：</label>
                    <input type="text" name="username" required>
                </div>
                <div class="form-group">
                    <label>密码：</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">登录</button>
            </form>
            <p style="text-align: center; margin-top: 20px; color: #666; font-size: 14px;">
                默认账号：admin / admin
            </p>
        </div>
    </body>
    </html>
    """
    return html_content

from fastapi import Form

@admin_router.post("/auth")
async def admin_authenticate(request: Request, username: str = Form(...), password: str = Form(...)):
    """认证处理"""
    # 简单的硬编码认证（生产环境应该使用数据库）
    if username == "admin" and password == "admin":
        response = RedirectResponse(url="/admin", status_code=303)
        response.set_cookie(key="admin_session", value="admin_logged_in", max_age=3600)
        return response
    
    # 认证失败
    return RedirectResponse(url="/admin/login?error=1", status_code=303)

@admin_router.get("/logout")
async def admin_logout(request: Request):
    """退出登录"""
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("admin_session")
    return response

# 挂载管理后台路由
app.include_router(admin_router, prefix="/admin", tags=["管理后台"])

print("✅ 管理后台路由已注册到 /admin")
print("   登录地址: http://localhost:8000/admin/login")
print("   默认账号: admin / admin")