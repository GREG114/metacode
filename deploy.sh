#!/bin/bash

# 获取脚本所在目录（相对路径）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 杀旧进程
pkill -f "manage.py runserver" || true


# 前端构建（直接输出到 dist，Nginx 会从这里读取）
cd frontend && rm -rf dist && npm run build && cd ..

# 数据库迁移
python manage.py migrate --run-syncdb

# 启动 Django（处理所有请求，包括前端和 API）
nohup python manage.py runserver 0.0.0.0:5001 > /tmp/metacode.log 2>&1 &

echo "✅ Metacode deployed:"
echo "   - Frontend + API → http://...:5001/"
