#!/bin/bash

# 快速启动脚本 - 一键启动完整的Pokemon API环境

set -e

echo "========================================="
echo "  Pokemon API 快速启动脚本"
echo "========================================="
echo ""

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker未安装，请先安装Docker"
    exit 1
fi

# 检查Docker Compose是否安装
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose未安装，请先安装Docker Compose"
    exit 1
fi

echo "✅ Docker环境检查通过"
echo ""

# 选择启动模式
echo "请选择启动模式:"
echo "  1. 使用Docker Compose（推荐）"
echo "  2. 使用构建脚本"
echo "  3. 停止所有服务"
read -p "请选择 (1/2/3): " mode

case $mode in
    1)
        echo ""
        echo "🚀 使用Docker Compose启动..."
        
        # 检查.env文件
        if [ ! -f .env ]; then
            echo "⚠️  .env文件不存在，从.env.example复制..."
            cp .env.example .env
            echo "✅ 已创建.env文件，请根据需要修改配置"
        fi
        
        # 构建并启动
        docker-compose up -d --build
        
        echo ""
        echo "✅ 服务启动成功！"
        echo ""
        echo "访问地址:"
        echo "  - API文档: http://localhost:8000/docs"
        echo "  - API健康检查: http://localhost:8000/health"
        echo "  - 管理后台: http://localhost:8000/admin"
        echo ""
        echo "查看日志:"
        echo "  docker-compose logs -f"
        echo ""
        echo "停止服务:"
        echo "  docker-compose down"
        ;;
    
    2)
        echo ""
        echo "🔨 使用构建脚本..."
        chmod +x build.sh
        ./build.sh
        ;;
    
    3)
        echo ""
        echo "🛑 停止所有服务..."
        docker-compose down
        echo "✅ 服务已停止"
        ;;
    
    *)
        echo "❌ 无效的选择"
        exit 1
        ;;
esac

echo ""
echo "========================================="
echo "  完成！"
echo "========================================="
