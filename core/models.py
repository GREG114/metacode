from django.db import models


class DataModel(models.Model):
    """数据模型定义"""

    name = models.CharField(max_length=100, unique=True, verbose_name="模型名称")
    description = models.TextField(blank=True, verbose_name="模型描述")
    schema = models.JSONField(default=dict, verbose_name="模型 Schema")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "data_model"
        verbose_name = "数据模型"
        verbose_name_plural = "数据模型"
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class FormData(models.Model):
    """表单数据存储"""

    model = models.ForeignKey(DataModel, on_delete=models.CASCADE, related_name="form_data")
    data = models.JSONField(default=dict, verbose_name="表单数据")
    submitted_by = models.CharField(max_length=100, blank=True, verbose_name="提交人")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "form_data"
        verbose_name = "表单数据"
        verbose_name_plural = "表单数据"
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"{self.model.name} - {self.id}"


class FormLayout(models.Model):
    """表单布局配置"""

    model = models.ForeignKey(DataModel, on_delete=models.CASCADE, related_name="layouts")
    name = models.CharField(max_length=100, verbose_name="布局名称")
    layout = models.JSONField(default=dict, verbose_name="布局配置")
    is_active = models.BooleanField(default=False, verbose_name="是否生效")
    version = models.IntegerField(default=1, verbose_name="版本号")
    created_by = models.CharField(max_length=100, blank=True, verbose_name="创建人")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "form_layout"
        verbose_name = "表单布局"
        verbose_name_plural = "表单布局"
        ordering = ["-updated_at"]
        unique_together = ["model", "name"]

    def __str__(self):
        return f"{self.model.name} - {self.name} (v{self.version})"