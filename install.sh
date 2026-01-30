#!/bin/bash

echo "=========================================="
echo "  Pokemon API - 安装脚本"
echo "=========================================="
echo ""

# 检查Python版本
echo "检查Python版本..."
python3 --version

# 创建虚拟环境
echo ""
echo "创建虚拟环境..."
python3 -m venv venv

# 激活虚拟环境
echo ""
echo "激活虚拟环境..."
source venv/bin/activate

# 升级pip
echo ""
echo "升级pip..."
pip install --upgrade pip

# 安装依赖
echo ""
echo "安装项目依赖..."
pip install -r requirements.txt

echo ""
echo "=========================================="
echo "  安装完成！"
echo "=========================================="
echo ""
echo "使用方法："
echo "   激活虚拟环境: source venv/bin/activate"
echo "  启动开发服务器: python -m app.main"
echo "  访问API文档: http://localhost:8000/docs"
echo "  访问管理后台: http://localhost:8000/admin (admin/admin)"
echo ""
echo "配置说明："
echo "   1. 复制.env.example为.env"
echo "   2. 修改.env文件中的数据库连接信息"
echo "  3. 如果需要MySQL，先创建数据库"
echo ""