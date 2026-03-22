#!/bin/bash

cd /root/.openclaw/workspace/metacode

# 杀旧进程
pkill -f "manage.py runserver" || true

# 更新代码
git pull

# 前端构建（直接输出到 dist，Nginx 会从这里读取）
cd frontend && rm -rf dist && npm run build && cd ..

# 数据库迁移
python manage.py migrate --run-syncdb

# 启动 Django（处理 API 请求和动态路由）
nohup python manage.py runserver 0.0.0.0:5001 > /tmp/metacode.log 2>&1 &

echo "✅ Metacode deployed on port 5001"
echo "   - Nginx (80) → Django API + HTML routing"
echo "   - Static files served from frontend/dist/"