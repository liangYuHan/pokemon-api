# Docker 部署指南

## 快速开始

### 1. 使用 Docker Compose（最简单）

```bash
# 启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down

# 停止并删除数据卷
docker-compose down -v
```

服务将在 `http://localhost:8000` 启动。

### 2. 使用构建脚本（推荐）

```bash
# 给脚本添加执行权限（如果还没有）
chmod +x build.sh

# 构建最新版本
./build.sh

# 构建特定版本
./build.sh v1.0.0

# 构建并推送到Docker Hub
./build.sh latest your-dockerhub-username
```

### 3. 手动构建

#### 使用标准Dockerfile
```bash
# 构建镜像
docker build -t pokemon-api:latest .

# 运行容器
docker run -d -p 8000:8000 pokemon-api:latest
```

#### 使用优化版Dockerfile（镜像更小）
```bash
# 构建镜像
docker build -f Dockerfile.optimized -t pokemon-api:latest .

# 运行容器
docker run -d -p 8000:8000 pokemon-api:latest
```

## 配置选项

### 环境变量

在 `docker-compose.yml` 中配置，或者使用 `-e` 参数传递：

| 变量 | 说明 | 默认值 |
|------|------|--------|
| MYSQL_HOST | MySQL主机地址 | mysql |
| MYSQL_PORT | MySQL端口 | 3306 |
| MYSQL_USER | MySQL用户名 | pokemon_user |
| MYSQL_PASSWORD | MySQL密码 | pokemon_password |
| MYSQL_DATABASE | MySQL数据库名 | pokemon_api |
| DEBUG | 调试模式 | True |

### 端口映射

| 内部端口 | 外部端口 | 说明 |
|---------|---------|------|
| 8000 | 8000 | API服务 |
| 3306 | 3306 | MySQL数据库 |

## 高级用法

### 连接到外部MySQL数据库

修改 `docker-compose.yml` 中的 `api` 服务：

```yaml
api:
  build: .
  environment:
    MYSQL_HOST: your-external-mysql-host
    MYSQL_PORT: 3306
    MYSQL_USER: your_user
    MYSQL_PASSWORD: your_password
    MYSQL_DATABASE: pokemon_db
  # 移除 depends_on
```

### 自定义端口

```bash
# 映射到8080端口
docker run -d -p 8080:8000 pokemon-api:latest
```

### 数据持久化

数据卷已配置在 `docker-compose.yml` 中：

```yaml
volumes:
  mysql_data:
```

### 查看容器日志

```bash
# 查看特定容器日志
docker logs pokemon_api

# 实时查看日志
docker logs -f pokemon_api

# 查看最近100行
docker logs --tail 100 pokemon_api
```

### 进入容器

```bash
# 进入运行中的容器
docker exec -it pokemon_api bash

# 运行命令
docker exec pokemon_api python init_db.py
```

## 镜像大小对比

| Dockerfile | 镜像大小 | 说明 |
|------------|---------|------|
| Dockerfile | ~800MB | 标准构建，包含编译工具 |
| Dockerfile.optimized | ~400MB | 多阶段构建，优化后 |

## 推送到镜像仓库

### Docker Hub

```bash
# 登录Docker Hub
docker login

# 标记镜像
docker tag pokemon-api:latest yourusername/pokemon-api:latest

# 推送
docker push yourusername/pokemon-api:latest
```

### 阿里云容器镜像服务

```bash
# 登录阿里云
docker login --username=your_username registry.cn-hangzhou.aliyuncs.com

# 标记镜像
docker tag pokemon-api:latest registry.cn-hangzhou.aliyuncs.com/your_namespace/pokemon-api:latest

# 推送
docker push registry.cn-hangzhou.aliyuncs.com/your_namespace/pokemon-api:latest
```

### GitHub Container Registry (ghcr.io)

```bash
# 登录GitHub Container Registry
echo $GITHUB_TOKEN | docker login ghcr.io -u USERNAME --password-stdin

# 标记镜像
docker tag pokemon-api:latest ghcr.io/username/pokemon-api:latest

# 推送
docker push ghcr.io/username/pokemon-api:latest
```

## 部署到云平台

### 部署到云服务器

```bash
# 1. 保存镜像为tar文件
docker save -o pokemon-api.tar pokemon-api:latest

# 2. 上传到服务器
scp pokemon-api.tar user@server:/path/

# 3. 在服务器上加载镜像
docker load -i pokemon-api.tar

# 4. 运行容器
docker run -d -p 8000:8000 pokemon-api:latest
```

### 使用Kubernetes部署

创建 `k8s-deployment.yaml`：

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: pokemon-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: pokemon-api
  template:
    metadata:
      labels:
        app: pokemon-api
    spec:
      containers:
      - name: pokemon-api
        image: pokemon-api:latest
        ports:
        - containerPort: 8000
        env:
        - name: MYSQL_HOST
          value: "mysql-service"
        - name: MYSQL_PASSWORD
          valueFrom:
            secretKeyRef:
              name: mysql-secret
              key: password
---
apiVersion: v1
kind: Service
metadata:
  name: pokemon-api-service
spec:
  selector:
    app: pokemon-api
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8000
  type: LoadBalancer
```

部署：

```bash
kubectl apply -f k8s-deployment.yaml
```

## 故障排查

### 容器无法启动

```bash
# 查看日志
docker logs pokemon_api

# 检查容器状态
docker ps -a | grep pokemon_api

# 进入容器调试
docker exec -it pokemon_api bash
```

### 数据库连接失败

1. 检查MySQL容器是否运行：
```bash
docker ps | grep mysql
```

2. 检查网络连接：
```bash
docker network ls
docker network inspect pokemon_api_default
```

3. 测试数据库连接：
```bash
docker exec -it pokemon_mysql mysql -u pokemon_user -p
```

### 端口被占用

```bash
# 查看端口占用
lsof -i :8000

# 使用不同端口
docker run -d -p 8080:8000 pokemon-api:latest
```

## 安全建议

1. **不要在镜像中包含敏感信息**
   - 不要复制 `.env` 文件到镜像
   - 使用 Docker secrets 或环境变量传递密码

2. **使用非root用户运行**
   - 优化版Dockerfile已配置非root用户

3. **定期更新基础镜像**
   ```bash
   docker pull python:3.11-slim
   docker build --no-cache -t pokemon-api:latest .
   ```

4. **扫描镜像漏洞**
   ```bash
   docker scan pokemon-api:latest
   ```

## 性能优化

1. **使用多阶段构建** - 减小镜像大小
2. **启用Docker BuildKit** - 加速构建
   ```bash
   DOCKER_BUILDKIT=1 docker build -t pokemon-api:latest .
   ```
3. **使用健康检查**
   ```yaml
   healthcheck:
     test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
     interval: 30s
     timeout: 10s
     retries: 3
   ```
