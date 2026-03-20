from rest_framework import serializers
from .models import DataModel, FormData, FormLayout


class DataModelSerializer(serializers.ModelSerializer):
    """数据模型序列化器"""

    class Meta:
        model = DataModel
        fields = ["id", "name", "description", "schema", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_schema(self, value):
        """验证 Schema 格式"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("Schema 必须是 JSON 对象")
        if "fields" not in value:
            raise serializers.ValidationError("Schema 必须包含 fields 字段")
        return value

    def validate_name(self, value):
        """验证模型名称"""
        if not value:
            raise serializers.ValidationError("模型名称不能为空")
        if len(value) > 100:
            raise serializers.ValidationError("模型名称不能超过 100 个字符")
        return value


class FormSchemaGenerator:
    """表单 Schema 生成器"""

    # 字段类型映射
    FIELD_TYPE_MAP = {
        "text": {"type": "string", "component": "el-input"},
        "integer": {"type": "integer", "component": "el-input-number"},
        "decimal": {"type": "number", "component": "el-input-number"},
        "date": {"type": "string", "format": "date", "component": "el-date-picker"},
        "boolean": {"type": "boolean", "component": "el-switch"},
        "select": {"type": "string", "component": "el-select"},
        "textarea": {"type": "string", "component": "el-input"},
    }

    @classmethod
    def generate(cls, data_model: DataModel) -> dict:
        """将数据模型转换为表单 Schema"""
        schema = {
            "type": "object",
            "properties": {},
            "required": [],
            "ui": {
                "components": {},
                "order": []
            }
        }

        fields = data_model.schema.get("fields", [])
        for field in fields:
            field_name = field.get("name")
            if not field_name:
                continue

            field_type = field.get("type", "text")
            type_info = cls.FIELD_TYPE_MAP.get(field_type, cls.FIELD_TYPE_MAP["text"])

            field_schema = {
                "type": type_info["type"],
                "title": field.get("label", field_name),
                "description": field.get("description", ""),
                "component": type_info["component"],
            }

            # 添加验证规则
            if field.get("required"):
                schema["required"].append(field_name)
                field_schema["required"] = True

            # 处理选项（select 类型）
            if field_type == "select" and field.get("options"):
                field_schema["options"] = field.get("options").split(",") if isinstance(field.get("options"), str) else field.get("options")

            # 处理默认值
            if "default" in field:
                field_schema["default"] = field.get("default")

            # 处理数值范围
            if field_type in ("integer", "decimal"):
                if "min" in field:
                    field_schema["minimum"] = field.get("min")
                if "max" in field:
                    field_schema["maximum"] = field.get("max")

            schema["properties"][field_name] = field_schema
            schema["ui"]["components"][field_name] = {
                "component": type_info["component"],
                "props": field.get("props", {})
            }
            schema["ui"]["order"].append(field_name)

        return schema


class FormSchemaSerializer(serializers.Serializer):
    """表单 Schema 序列化器（只读）"""
    type = serializers.CharField()
    properties = serializers.DictField()
    required = serializers.ListField()
    ui = serializers.DictField()


class FormDataSerializer(serializers.ModelSerializer):
    """表单数据序列化器"""

    model_name = serializers.CharField(source="model.name", read_only=True)

    class Meta:
        model = FormData
        fields = ["id", "model", "model_name", "data", "submitted_by", "submitted_at"]
        read_only_fields = ["id", "submitted_at"]

    def validate_data(self, value):
        """验证表单数据"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("表单数据必须是 JSON 对象")
        return value


class FormLayoutSerializer(serializers.ModelSerializer):
    """表单布局序列化器"""

    model_name = serializers.CharField(source="model.name", read_only=True)

    class Meta:
        model = FormLayout
        fields = [
            "id", "model", "model_name", "name", "layout",
            "is_active", "version", "created_by", "created_at", "updated_at"
        ]
        read_only_fields = ["id", "version", "created_at", "updated_at"]

    def validate_layout(self, value):
        """验证布局配置"""
        if not isinstance(value, dict):
            raise serializers.ValidationError("布局配置必须是 JSON 对象")
        return value

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("布局名称不能为空")
        return value