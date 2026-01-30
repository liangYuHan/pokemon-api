-- 创建数据库和用户的SQL脚本

-- 创建数据库
CREATE DATABASE IF NOT EXISTS pokemon_api 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 创建新用户
CREATE USER IF NOT EXISTS 'pokemon_user'@'%' IDENTIFIED BY 'pokemon_pass123';

-- 授予权限（完全控制pokemon_api数据库）
GRANT ALL PRIVILEGES ON pokemon_api.* TO 'pokemon_user'@'%' WITH GRANT OPTION;

-- 授予全局权限（可选，如果需要创建其他数据库）
-- GRANT ALL PRIVILEGES ON *.* TO 'pokemon_user'@'%' WITH GRANT OPTION;

-- 刷新权限
FLUSH PRIVILEGES;

-- 显示用户信息
SELECT User, Host, Select_priv, Insert_priv, Update_priv, Delete_priv, Create_priv, Drop_priv 
FROM mysql.user 
WHERE User = 'pokemon_user';

-- 显示数据库
SHOW DATABASES LIKE 'pokemon_api';
