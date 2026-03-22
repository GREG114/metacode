#!/bin/bash

cd /root/.openclaw/workspace/metacode

# 杀旧进程
pkill -f "manage.py runserver" || true

# 更新代码
git pull

# 前端构建
cd frontend && rm -rf dist && npm run build && cd ..

# 复制前端到 Django templates
rm -rf templates/*
cp -r frontend/dist/* templates/

# 数据库迁移
python manage.py migrate --run-syncdb

# 启动
nohup python manage.py runserver 0.0.0.0:5001 > /tmp/metacode.log 2>&1 &

echo "Metacode deployed on port 5001"