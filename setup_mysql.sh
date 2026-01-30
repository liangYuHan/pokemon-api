#!/bin/bash

# 自动化脚本：创建MySQL用户并初始化数据库

set -e

echo "========================================="
echo "  创建MySQL用户并初始化数据库"
echo "========================================="
echo ""

# 配置变量
MYSQL_ROOT_PASSWORD="root123456"
MYSQL_USER="pokemon_user"
MYSQL_PASSWORD="pokemon_pass123"
MYSQL_DATABASE="pokemon_api"
MYSQL_HOST="localhost"
MYSQL_PORT="3306"

echo "配置信息:"
echo "  MySQL主机: $MYSQL_HOST"
echo "  MySQL端口: $MYSQL_PORT"
echo "  新用户名: $MYSQL_USER"
echo "  新密码: $MYSQL_PASSWORD"
echo "  数据库名: $MYSQL_DATABASE"
echo ""

# 检查Docker是否运行
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker未运行，请先启动Docker"
    exit 1
fi

echo "✅ Docker环境检查通过"
echo ""

# 停止并删除旧的MySQL容器
echo "清理旧的MySQL容器..."
docker stop pokemon_mysql 2>/dev/null || true
docker rm pokemon_mysql 2>/dev/null || true
echo "✅ 清理完成"
echo ""

# 启动MySQL容器
echo "启动MySQL容器..."
docker run -d \
  --name pokemon_mysql \
  -e MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
  -p $MYSQL_PORT:3306 \
  mysql:8.0

echo "✅ MySQL容器启动成功"
echo ""

# 等待MySQL完全启动
echo "等待MySQL启动..."
for i in {1..30}; do
    if docker exec pokemon_mysql mysql -u root -p$MYSQL_ROOT_PASSWORD -e "SELECT 1" &> /dev/null; then
        echo "✅ MySQL已就绪"
        break
    fi
    echo "  等待中... ($i/30)"
    sleep 1
done

if [ $i -eq 30 ]; then
    echo "❌ MySQL启动超时"
    exit 1
fi

echo ""

# 创建数据库和用户
echo "创建数据库和用户..."
docker exec -i pokemon_mysql mysql -u root -p$MYSQL_ROOT_PASSWORD << EOF
-- 创建数据库
CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 创建新用户
CREATE USER IF NOT EXISTS '$MYSQL_USER'@'%' IDENTIFIED BY '$MYSQL_PASSWORD';

-- 授予权限
GRANT ALL PRIVILEGES ON $MYSQL_DATABASE.* TO '$MYSQL_USER'@'%';

-- 刷新权限
FLUSH PRIVILEGES;

-- 显示创建结果
SELECT 'Database created:' AS info;
SHOW DATABASES LIKE '$MYSQL_DATABASE';

SELECT 'User created:' AS info;
SELECT User, Host FROM mysql.user WHERE User = '$MYSQL_USER';
EOF

echo "✅ 数据库和用户创建成功"
echo ""

# 测试新用户连接
echo "测试新用户连接..."
if docker exec pokemon_mysql mysql -u $MYSQL_USER -p$MYSQL_PASSWORD -e "SELECT 1" &> /dev/null; then
    echo "✅ 新用户连接成功"
else
    echo "❌ 新用户连接失败"
    exit 1
fi

echo ""

# 创建.env文件
echo "创建.env文件..."
cat > .env << EOF
# MySQL数据库配置
MYSQL_HOST=$MYSQL_HOST
MYSQL_PORT=$MYSQL_PORT
MYSQL_USER=$MYSQL_USER
MYSQL_PASSWORD=$MYSQL_PASSWORD
MYSQL_DATABASE=$MYSQL_DATABASE

# 应用配置
APP_NAME=Pokemon API
APP_VERSION=1.0.0
DEBUG=True

# 服务器配置
HOST=0.0.0.0
PORT=8000

# 安全配置
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# 爬取配置
SCRAPER_DELAY=1.0
SCRAPER_MAX_RETRIES=3
SCRAPER_TIMEOUT=30

# 分页配置
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100

# 跨域配置
CORS_ORIGINS=*
EOF

echo "✅ .env文件创建成功"
echo ""

# 初始化数据库表
echo "初始化数据库表..."
python init_db.py

echo ""
echo "========================================="
echo "  完成！"
echo "========================================="
echo ""
echo "数据库连接信息:"
echo "  主机: $MYSQL_HOST:$MYSQL_PORT"
echo "  用户: $MYSQL_USER"
echo "  密码: $MYSQL_PASSWORD"
echo "  数据库: $MYSQL_DATABASE"
echo ""
echo "测试命令:"
echo "  docker exec -it pokemon_mysql mysql -u $MYSQL_USER -p$MYSQL_PASSWORD $MYSQL_DATABASE"
echo ""
