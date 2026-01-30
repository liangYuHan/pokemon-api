# MySQL用户创建指南

## 方法一：一键自动化脚本（推荐）

```bash
cd /Users/user/pokemon-api

# 运行自动化脚本
./setup_mysql.sh
```

这个脚本会自动：
1. 启动MySQL容器
2. 创建数据库 `pokemon_api`
3. 创建用户 `pokemon_user`
4. 授予权限
5. 更新 `.env` 文件
6. 初始化数据库表

---

## 方法二：手动创建（使用Docker）

### 步骤1：启动MySQL

```bash
docker stop pokemon_mysql 2>/dev/null
docker rm pokemon_mysql 2>/dev/null

docker run -d \
  --name pokemon_mysql \
  -e MYSQL_ROOT_PASSWORD=root123456 \
  -p 3306:3306 \
  mysql:8.0

# 等待MySQL启动
sleep 15
```

### 步骤2：连接MySQL并创建用户

```bash
# 连接到MySQL
docker exec -it pokemon_mysql mysql -u root -proot123456
```

在MySQL提示符下执行：

```sql
-- 1. 创建数据库
CREATE DATABASE IF NOT EXISTS pokemon_api 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. 创建用户
CREATE USER IF NOT EXISTS 'pokemon_user'@'%' IDENTIFIED BY 'pokemon_pass123';

-- 3. 授予权限
GRANT ALL PRIVILEGES ON pokemon_api.* TO 'pokemon_user'@'%';

-- 4. 刷新权限
FLUSH PRIVILEGES;

-- 5. 查看用户
SELECT User, Host FROM mysql.user WHERE User = 'pokemon_user';

-- 6. 查看数据库
SHOW DATABASES;

-- 7. 退出
exit;
```

### 步骤3：更新.env文件

```bash
cd /Users/user/pokemon-api

cat > .env << 'EOF'
# MySQL数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=pokemon_user
MYSQL_PASSWORD=pokemon_pass123
MYSQL_DATABASE=pokemon_api

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
```

### 步骤4：初始化数据库表

```bash
python init_db.py
```

---

## 方法三：使用SQL脚本

### 步骤1：启动MySQL

```bash
docker stop pokemon_mysql 2>/dev/null
docker rm pokemon_mysql 2>/dev/null

docker run -d \
  --name pokemon_mysql \
  -e MYSQL_ROOT_PASSWORD=root123456 \
  -p 3306:3306 \
  mysql:8.0

sleep 15
```

### 步骤2：执行SQL脚本

```bash
# 执行SQL脚本创建用户和数据库
docker exec -i pokemon_mysql mysql -u root -proot123456 < create_user.sql
```

### 步骤3：更新.env并初始化

```bash
cd /Users/user/pokemon-api

# 更新.env
cat > .env << 'EOF'
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=pokemon_user
MYSQL_PASSWORD=pokemon_pass123
MYSQL_DATABASE=pokemon_api
EOF

# 初始化数据库
python init_db.py
```

---

## 验证安装

### 1. 测试用户连接

```bash
# 使用新用户连接
docker exec -it pokemon_mysql mysql -u pokemon_user -ppokemon_pass123 pokemon_api

# 在MySQL中执行
SHOW TABLES;

# 应该看到：
# pokemon
# moves
# abilities
# items
# pokemon_moves
```

### 2. 检查用户权限

```bash
docker exec -it pokemon_mysql mysql -u root -proot123656 -e "
SELECT User, Host, 
       Select_priv, Insert_priv, Update_priv, Delete_priv, 
       Create_priv, Drop_priv, Grant_priv
FROM mysql.user 
WHERE User = 'pokemon_user';
"
```

---

## 管理用户

### 查看所有用户

```bash
docker exec -it pokemon_mysql mysql -u root -proot123456 -e "SELECT User, Host FROM mysql.user;"
```

### 查看用户权限

```bash
docker exec -it pokemon_mysql mysql -u root -proot123456 -e "SHOW GRANTS FOR 'pokemon_user'@'%';"
```

### 修改用户密码

```bash
docker exec -it pokemon_mysql mysql -u root -proot123456 -e "
ALTER USER 'pokemon_user'@'%' IDENTIFIED BY 'new_password';
FLUSH PRIVILEGES;
"
```

### 删除用户

```bash
docker exec -it pokemon_mysql mysql -u root -proot123456 -e "
DROP USER IF EXISTS 'pokemon_user'@'%';
FLUSH PRIVILEGES;
"
```

### 撤销权限

```bash
docker exec -it pokemon_mysql mysql -u root -proot123456 -e "
REVOKE ALL PRIVILEGES ON pokemon_api.* FROM 'pokemon_user'@'%';
FLUSH PRIVILEGES;
"
```

---

## 远程MySQL配置

如果使用远程MySQL（如 192.168.50.202:33306）：

```bash
# SSH到MySQL服务器
ssh root@192.168.50.202

# 连接到MySQL
mysql -u root -p

# 创建数据库和用户
CREATE DATABASE IF NOT EXISTS pokemon_api CHARACTER SET utf8mb4;
CREATE USER IF NOT EXISTS 'pokemon_user'@'%' IDENTIFIED BY 'pokemon_pass123';
GRANT ALL PRIVILEGES ON pokemon_api.* TO 'pokemon_user'@'%';
FLUSH PRIVILEGES;

# 退出MySQL
exit

# 退出SSH
exit

# 在本地更新.env文件
cd /Users/user/pokemon-api
cat > .env << 'EOF'
MYSQL_HOST=192.168.50.202
MYSQL_PORT=33306
MYSQL_USER=pokemon_user
MYSQL_PASSWORD=pokemon_pass123
MYSQL_DATABASE=pokemon_api
EOF

# 测试连接
mysql -h 192.168.50.202 -P 33306 -u pokemon_user -ppokemon_pass123 pokemon_api -e "SHOW DATABASES;"

# 初始化数据库
python init_db.py
```

---

## 常见问题

### Q1: 提示"Access denied"
**A**: 检查密码是否正确，用户是否有权限。

### Q2: 提示"Can't connect to MySQL server"
**A**: 检查MySQL是否启动，端口是否正确。

### Q3: 提示"Unknown database"
**A**: 先创建数据库：
```sql
CREATE DATABASE pokemon_api CHARACTER SET utf8mb4;
```

### Q4: 如何限制用户权限？
**A**: 使用最小权限原则：
```sql
-- 只允许查询
GRANT SELECT ON pokemon_api.* TO 'pokemon_user'@'%';

-- 允许增删改查
GRANT SELECT, INSERT, UPDATE, DELETE ON pokemon_api.* TO 'pokemon_user'@'%';
```

---

## 安全建议

1. **不要使用弱密码** - 使用复杂密码
2. **限制访问IP** - 不要使用 `%`，使用具体IP
3. **最小权限原则** - 只授予必要的权限
4. **定期更换密码** - 定期更新数据库密码
5. **使用SSL连接** - 生产环境启用SSL
6. **备份用户信息** - 保存好用户名和密码

---

## 推荐配置

### 开发环境
```sql
CREATE USER 'pokemon_user'@'%' IDENTIFIED BY 'dev_password_123';
GRANT ALL PRIVILEGES ON pokemon_api.* TO 'pokemon_user'@'%';
```

### 生产环境
```sql
CREATE USER 'pokemon_user'@'192.168.x.x' IDENTIFIED BY 'strong_password_xyz!@#';
GRANT SELECT, INSERT, UPDATE, DELETE ON pokemon_api.* TO 'pokemon_user'@'192.168.x.x';
```

---

## 快速开始

```bash
cd /Users/user/pokemon-api

# 一键创建用户并初始化数据库
./setup_mysql.sh
```

就这么简单！
