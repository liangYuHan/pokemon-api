#!/bin/bash

# Docker镜像构建和推送脚本

set -e

# 配置变量
IMAGE_NAME="pokemon-api"
IMAGE_TAG=${1:-latest}
REGISTRY=${2:-""}

echo "========================================="
echo "  Pokemon API Docker镜像构建工具"
echo "========================================="
echo ""

# 如果提供了registry，添加前缀
if [ -n "$REGISTRY" ]; then
    FULL_IMAGE_NAME="${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
else
    FULL_IMAGE_NAME="${IMAGE_NAME}:${IMAGE_TAG}"
fi

echo "构建配置:"
echo "  镜像名称: $FULL_IMAGE_NAME"
echo "  标签: $IMAGE_TAG"
echo ""

# 选择Dockerfile
echo "选择Dockerfile:"
echo "  1. Dockerfile (标准)"
echo "  2. Dockerfile.optimized (优化版，更小)"
read -p "请选择 (1或2，默认1): " dockerfile_choice
dockerfile_choice=${dockerfile_choice:-1}

if [ "$dockerfile_choice" = "2" ]; then
    DOCKERFILE="Dockerfile.optimized"
else
    DOCKERFILE="Dockerfile"
fi

echo ""
echo "开始构建镜像..."

# 构建镜像
docker build -f $DOCKERFILE -t $FULL_IMAGE_NAME .

echo ""
echo "✅ 镜像构建成功！"
echo ""

# 显示镜像信息
echo "镜像信息:"
docker images | grep $IMAGE_NAME || true
echo ""

# 是否推送到仓库
if [ -n "$REGISTRY" ]; then
    read -p "是否推送到仓库 $REGISTRY? (y/n): " push_choice
    if [ "$push_choice" = "y" ]; then
        echo "推送镜像..."
        docker push $FULL_IMAGE_NAME
        echo "✅ 镜像推送成功！"
    fi
fi

echo ""
echo "========================================="
echo "  构建完成！"
echo "========================================="
echo ""
echo "运行命令:"
echo "  docker run -d -p 8000:8000 $FULL_IMAGE_NAME"
echo ""
echo "查看镜像:"
echo "  docker images | grep $IMAGE_NAME"
echo ""
