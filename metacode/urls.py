from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

def serve_index(request):
    """返回前端首页（SPA fallback）"""
    index_path = "/root/.openclaw/workspace/metacode/frontend/dist/index.html"
    try:
        with open(index_path, "r") as f:
            return HttpResponse(f.read(), content_type="text/html")
    except FileNotFoundError:
        return HttpResponse("Frontend not built. Run 'npm run build' in frontend/", status=500)

urlpatterns = [
    path("", serve_index),  # 根路径返回前端首页（SPA fallback）
    path("admin/", admin.site.urls),
    path("api/", include("core.urls")),
]