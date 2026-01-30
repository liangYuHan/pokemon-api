# Pokemon API

基于FastAPI的宝可梦数据查询API，提供宝可梦、招式、特性、道具等数据的查询接口。

## 功能特性

- 🎯 **RESTful API**: 标准的REST API设计
- 📚 **分页支持**: 所有列表接口都支持分页查询
- 🔍 **高级搜索**: 支持模糊搜索和多条件筛选
- 📊 **自动文档**: Swagger UI自动生成API文档
- 🌐 **跨域支持**: 完整的CORS配置
- ⚡ **高性能**: 基于FastAPI的异步支持

## 技术栈

- **框架**: FastAPI 0.104.1
- **数据库**: MySQL + SQLAlchemy ORM
- **管理后台**: FastAPI Admin
- **爬取**: BeautifulSoup4 + requests
- **API文档**: Swagger UI

## 快速开始

### 1. 安装依赖

```bash
cd pokemon-api
pip install -r requirements.txt
```

### 2. 配置环境

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，设置数据库连接信息
# MYSQL_HOST=localhost
# MYSQL_PORT=3306
# MYSQL_USER=your_username
# MYSQL_PASSWORD=your_password
# MYSQL_DATABASE=pokemon_api
```

### 3. 启动服务

```bash
# 开发模式（自动重载）
python -m app.main

# 生产模式
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### 4. 初始化数据库

首次运行前需要初始化数据库并填充种子数据：

```bash
# 初始化数据库表并填充种子数据
python init_db.py
```

### 5. 访问API文档

启动服务后，访问以下地址：
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **管理后台**: http://localhost:8000/admin

管理后台默认账号：
- 用户名: admin
- 密码: admin

> 注意：生产环境中请修改admin.py中的认证方式

### Docker 部署

使用Docker Compose快速部署：

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止服务并删除数据卷
docker-compose down -v
```

服务启动后，访问地址与上述相同。

## API接口

### 宝可梦相关

- `GET /api/pokemon/` - 获取宝可梦列表
- `GET /api/pokemon/{id_or_name}` - 获取单个宝可梦详情
- `GET /api/pokemon/type/{type}` - 按属性筛选宝可梦
- `GET /api/pokemon/search/{query}` - 搜索宝可梦
- `POST /api/pokemon/` - 创建宝可梦
- `PUT /api/pokemon/{id}` - 更新宝可梦
- `DELETE /api/pokemon/{id}` - 删除宝可梦

### 招式相关

- `GET /api/moves/` - 获取招式列表
- `GET /api/moves/{id_or_name}` - 获取单个招式详情
- `GET /api/moves/type/{type}` - 按属性筛选招式
- `POST /api/moves/` - 创建招式
- `PUT /api/moves/{id}` - 更新招式
- `DELETE /api/moves/{id}` - 删除招式

### 特性相关

- `GET /api/abilities/` - 获取特性列表
- `GET /api/abilities/{id_or_name}` - 获取单个特性详情
- `POST /api/abilities/` - 创建特性
- `PUT /api/abilities/{id}` - 更新特性
- `DELETE /api/abilities/{id}` - 删除特性

### 道具相关

- `GET /api/items/` - 获取道具列表
- `GET /api/items/{name}` - 获取单个道具详情
- `GET /api/items/category/{category}` - 按分类获取道具
- `POST /api/items/` - 创建道具
- `PUT /api/items/{name}` - 更新道具
- `DELETE /api/items/{name}` - 删除道具

### 宝可梦相关

- `GET /api/pokemon/` - 获取宝可梦列表
- `GET /api/pokemon/{id_or_name}` - 获取单个宝可梦详情
- `GET /api/pokemon/type/{type}` - 按属性筛选宝可梦
- `GET /api/pokemon/search/{query}` - 搜索宝可梦

### 招式相关

- `GET /api/moves/` - 获取招式列表
- `GET /api/moves/{id_or_name}` - 获取单个招式详情
- `GET /api/moves/type/{type}` - 按属性筛选招式

### 特性相关

- `GET /api/abilities/` - 获取特性列表
- `GET /api/abilities/{id_or_name}` - 获取单个特性详情

### 道具相关

- `GET /api/items/` - 获取道具列表
- `GET /api/items/{name}` - 获取单个道具详情
- `GET /api/items/category/{category}` - 按分类获取道具

## 数据爬取

项目提供了数据爬取功能，可以从PokeAPI获取数据并保存到数据库：

```bash
# 运行爬虫脚本
python scraper.py
```

爬虫脚本支持以下选项：
- 1. 宝可梦数据爬取
- 2. 招式数据爬取
- 3. 特性数据爬取
- 4. 道具数据爬取
- 5. 全部数据爬取

### 爬取功能

项目包含了从PokeAPI爬取数据的模块：

- 宝可梦数据爬取（从PokeAPI）
- 招式数据爬取（从PokeAPI）
- 特性数据爬取（从PokeAPI）
- 道具数据爬取（从PokeAPI）

## 项目结构

```
pokemon-api/
├── app/
│   ├── main.py              # FastAPI应用入口
│   ├── config.py             # 配置管理
│   ├── database.py           # 数据库连接
│   ├── models/              # 数据库模型
│   ├── schemas/             # Pydantic模型
│   ├── routers/              # API路由
│   ├── crud/                 # 数据库CRUD操作
│   └── scraper/             # 数据爬取模块
├── admin/                    # 管理后台配置
├── requirements.txt          # Python依赖
├── .env.example             # 环境变量模板
└── README.md               # 项目说明
```

## 分页参数

所有列表接口都支持以下分页参数：

- `page`: 页码（从1开始）
- `page_size`: 每页数量（1-100，默认20）

## 筛选参数

- `type`: 按属性筛选
- `category`: 按分类筛选
- `generation`: 按世代筛选
- `search`: 搜索查询

## 开发计划

- [x] 基础API框架搭建
- [x] API路由设计
- [x] 数据模型定义
- [x] 网页爬取模块
- [x] MySQL数据库集成
- [x] CRUD操作实现
- [x] 管理后台完善

## 许可证

MIT License

## 联系方式

如有问题或建议，欢迎提交Issue。