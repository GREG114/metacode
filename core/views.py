from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import DataModel, FormData, FormLayout
from .serializers import DataModelSerializer, FormDataSerializer, FormSchemaSerializer, FormLayoutSerializer


class DataModelViewSet(viewsets.ModelViewSet):
    """数据模型视图集"""

    queryset = DataModel.objects.all()
    serializer_class = DataModelSerializer

    @action(detail=True, methods=["get"])
    def form(self, request, pk=None):
        """获取模型的表单 Schema"""
        data_model = self.get_object()
        from .serializers import FormSchemaGenerator
        schema = FormSchemaGenerator.generate(data_model)
        
        # 获取当前激活的布局
        active_layout = data_model.layouts.filter(is_active=True).first()
        if active_layout:
            schema["layout"] = active_layout.layout
            schema["layout_id"] = active_layout.id
            schema["layout_name"] = active_layout.name
        else:
            schema["layout"] = {"items": []}
            schema["layout_id"] = None
            schema["layout_name"] = None
        
        return Response(schema)

    def create(self, request, *args, **kwargs):
        """创建数据模型"""
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "验证失败", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """更新数据模型"""
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if not serializer.is_valid():
            return Response(
                {"error": "验证失败", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """删除数据模型"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class FormDataViewSet(viewsets.ModelViewSet):
    """表单数据视图集"""

    serializer_class = FormDataSerializer

    def get_queryset(self):
        """按模型过滤"""
        model_id = self.request.query_params.get("model")
        if model_id:
            return FormData.objects.filter(model_id=model_id)
        return FormData.objects.all()

    def create(self, request, *args, **kwargs):
        """提交表单数据"""
        model_id = request.data.get("model")
        if not model_id:
            return Response(
                {"error": "缺少 model 字段"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证模型存在
        get_object_or_404(DataModel, pk=model_id)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "验证失败", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FormLayoutViewSet(viewsets.ModelViewSet):
    """表单布局视图集"""
    from rest_framework.permissions import AllowAny
    permission_classes = [AllowAny]
    
    serializer_class = FormLayoutSerializer

    def get_queryset(self):
        """按模型过滤"""
        model_id = self.request.query_params.get("model")
        if model_id:
            return FormLayout.objects.filter(model_id=model_id)
        return FormLayout.objects.all()

    @action(detail=True, methods=["post"])
    def activate(self, request, pk=None):
        """激活布局（同时停用其他布局）"""
        layout = self.get_object()
        model = layout.model

        with transaction.atomic():
            # 停用该模型的所有布局
            FormLayout.objects.filter(model=model).update(is_active=False)
            # 激活当前布局
            layout.is_active = True
            layout.save()

        serializer = self.get_serializer(layout)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def duplicate(self, request, pk=None):
        """复制布局"""
        layout = self.get_object()
        new_name = request.data.get("name", f"{layout.name} (副本)")

        new_layout = FormLayout.objects.create(
            model=layout.model,
            name=new_name,
            layout=layout.layout.copy(),
            is_active=False,
            version=1,
            created_by=request.data.get("created_by", "")
        )

        serializer = self.get_serializer(new_layout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        """创建布局"""
        model_id = request.data.get("model")
        if not model_id:
            return Response(
                {"error": "缺少 model 字段"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 验证模型存在
        get_object_or_404(DataModel, pk=model_id)

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {"error": "验证失败", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)