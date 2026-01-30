@echo off
chcp 65001
cls
echo ==========================================
echo   Pokemon API - Windows安装脚本
echo ==========================================
echo.

echo 检查Python版本...
python --version

echo.
echo 创建虚拟环境...
python -m venv venv

echo.
echo 激活虚拟环境...
venv\Scripts\activate

echo.
echo 升级pip...
python -m pip install --upgrade pip

echo.
echo 安装项目依赖...
pip install -r requirements.txt

echo.
echo ==========================================
echo   安装完成！
echo ==========================================
echo.
echo 使用方法：
echo   1. 激活虚拟环境: venv\Scripts\activate
echo   2. 启动开发服务器: python -m app.main
echo   3. 访问API文档: http://localhost:8000/docs
echo   4. 访问管理后台: http://localhost:8000/admin (admin/admin)
echo.
echo 配置说明：
echo   1. 复制.env.example为.env
echo   2. 修改.env文件中的数据库连接信息
echo   3. 如果需要MySQL，先创建数据库
echo.

pause