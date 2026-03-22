from django.urls import path, include, re_path  # 注意引入 re_path
from django.contrib import admin
from django.http import HttpResponse
from django.conf import settings  # 引入 settings 获取动态路径
import os

# 使用 settings 中的 BASE_DIR，而不是写死
INDEX_PATH = os.path.join(settings.BASE_DIR, "frontend", "dist", "index.html")

def serve_index(request):
    try:
        with open(INDEX_PATH, "r", encoding='utf-8') as f: # 建议加上编码
            return HttpResponse(f.read(), content_type="text/html")
    except FileNotFoundError:
        return HttpResponse("Frontend not built...", status=500)

urlpatterns = [
    # 1. 先定义具体的、优先匹配的路由
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
    
    # 2. (可选) 如果有静态文件配置，通常 Django 会自动处理，或者在这里定义
    
    # 3. 最后定义“兜底”路由：匹配任何未被上面捕获的路径
    # 正则 r'^.*$' 意思是：从开头到结尾的所有字符
    re_path(r'^.*$', serve_index), 
]