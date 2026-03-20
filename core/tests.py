from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from .models import DataModel, FormData, FormLayout
from .serializers import FormSchemaGenerator


class FormSchemaGeneratorTest(TestCase):
    """表单 Schema 生成器测试"""

    def test_generate_simple_schema(self):
        """测试生成简单表单 Schema"""
        model = DataModel.objects.create(
            name="test_model",
            schema={
                "fields": [
                    {"name": "username", "type": "text", "label": "用户名", "required": True},
                    {"name": "age", "type": "integer", "label": "年龄"}
                ]
            }
        )
        schema = FormSchemaGenerator.generate(model)

        self.assertEqual(schema["type"], "object")
        self.assertIn("username", schema["properties"])
        self.assertIn("age", schema["properties"])
        self.assertIn("username", schema["required"])
        self.assertNotIn("age", schema["required"])

    def test_generate_select_field(self):
        """测试生成下拉选择字段"""
        model = DataModel.objects.create(
            name="select_model",
            schema={
                "fields": [
                    {"name": "gender", "type": "select", "options": "male,female,other"}
                ]
            }
        )
        schema = FormSchemaGenerator.generate(model)

        self.assertEqual(schema["properties"]["gender"]["type"], "string")
        self.assertEqual(schema["properties"]["gender"]["options"], ["male", "female", "other"])

    def test_generate_empty_fields(self):
        """测试空字段列表"""
        model = DataModel.objects.create(name="empty_model", schema={"fields": []})
        schema = FormSchemaGenerator.generate(model)

        self.assertEqual(schema["properties"], {})
        self.assertEqual(schema["required"], [])

    def test_field_type_mapping(self):
        """测试字段类型映射"""
        model = DataModel.objects.create(
            name="type_test",
            schema={
                "fields": [
                    {"name": "text_field", "type": "text"},
                    {"name": "date_field", "type": "date"},
                    {"name": "boolean_field", "type": "boolean"}
                ]
            }
        )
        schema = FormSchemaGenerator.generate(model)

        self.assertEqual(schema["properties"]["text_field"]["component"], "el-input")
        self.assertEqual(schema["properties"]["date_field"]["component"], "el-date-picker")
        self.assertEqual(schema["properties"]["boolean_field"]["component"], "el-switch")


class DataModelAPITest(APITestCase):
    """数据模型 API 测试"""

    def setUp(self):
        """测试前准备"""
        self.model_data = {
            "name": "test_model",
            "description": "测试模型",
            "schema": {
                "fields": [
                    {"name": "username", "type": "text", "required": True},
                    {"name": "age", "type": "integer", "required": False}
                ]
            }
        }

    def test_create_model_success(self):
        """测试创建模型成功"""
        response = self.client.post("/api/models/", self.model_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "test_model")
        self.assertIn("id", response.data)
        # 验证数据库
        self.assertEqual(DataModel.objects.count(), 1)

    def test_create_model_duplicate_name(self):
        """测试创建重复名称的模型应失败"""
        # 先创建一个模型
        self.client.post("/api/models/", self.model_data, format="json")
        # 再创建一个同名的
        response = self.client.post("/api/models/", self.model_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_model_empty_name(self):
        """测试空名称应失败"""
        data = self.model_data.copy()
        data["name"] = ""
        response = self.client.post("/api/models/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_model_without_schema(self):
        """测试缺少 schema 时使用默认值"""
        data = {"name": "no_schema_model", "description": "无 schema"}
        response = self.client.post("/api/models/", data, format="json")
        # schema 有默认值，缺少时应自动使用空 dict
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["schema"], {})

    def test_list_models(self):
        """测试模型列表"""
        # 创建两个模型
        self.client.post("/api/models/", self.model_data, format="json")
        self.client.post("/api/models/", {
            "name": "model_2",
            "description": "第二个模型",
            "schema": {"fields": []}
        }, format="json")

        response = self.client.get("/api/models/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_model_detail(self):
        """测试获取模型详情"""
        # 创建模型
        create_response = self.client.post("/api/models/", self.model_data, format="json")
        model_id = create_response.data["id"]

        # 获取详情
        response = self.client.get(f"/api/models/{model_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "test_model")

    def test_update_model(self):
        """测试更新模型"""
        # 创建模型
        create_response = self.client.post("/api/models/", self.model_data, format="json")
        model_id = create_response.data["id"]

        # 更新
        update_data = create_response.data.copy()
        update_data["description"] = "更新后的描述"
        response = self.client.put(f"/api/models/{model_id}/", update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "更新后的描述")

    def test_partial_update_model(self):
        """测试部分更新模型"""
        # 创建模型
        create_response = self.client.post("/api/models/", self.model_data, format="json")
        model_id = create_response.data["id"]

        # 部分更新
        response = self.client.patch(f"/api/models/{model_id}/", {"description": "部分更新"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "部分更新")
        # 其他字段保持不变
        self.assertEqual(response.data["name"], "test_model")

    def test_delete_model(self):
        """测试删除模型"""
        # 创建模型
        create_response = self.client.post("/api/models/", self.model_data, format="json")
        model_id = create_response.data["id"]

        # 删除
        response = self.client.delete(f"/api/models/{model_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # 验证已删除
        self.assertEqual(DataModel.objects.count(), 0)

    def test_delete_nonexistent_model(self):
        """测试删除不存在的模型"""
        response = self.client.delete("/api/models/99999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_schema_validation_invalid(self):
        """测试无效 schema 应失败"""
        data = {
            "name": "invalid_schema",
            "description": "测试",
            "schema": "not_a_dict"  # 应该是 dict
        }
        response = self.client.post("/api/models/", data, format="json")
        # 序列化器会验证失败
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FormDataAPITest(APITestCase):
    """表单数据 API 测试"""

    def setUp(self):
        """测试前准备"""
        self.model = DataModel.objects.create(
            name="form_test_model",
            description="表单测试模型",
            schema={
                "fields": [
                    {"name": "username", "type": "text", "required": True},
                    {"name": "age", "type": "integer", "required": False}
                ]
            }
        )

    def test_get_form_schema(self):
        """测试获取表单 Schema"""
        response = self.client.get(f"/api/models/{self.model.id}/form/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("properties", response.data)
        self.assertIn("username", response.data["properties"])

    def test_submit_form_data(self):
        """测试提交表单数据"""
        data = {
            "model": self.model.id,
            "data": {"username": "testuser", "age": 25},
            "submitted_by": "admin"
        }
        response = self.client.post("/api/form-data/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["data"]["username"], "testuser")
        # 验证数据库
        self.assertEqual(FormData.objects.count(), 1)

    def test_submit_form_data_without_model(self):
        """测试缺少 model 字段应失败"""
        data = {"data": {"username": "testuser"}, "submitted_by": "admin"}
        response = self.client.post("/api/form-data/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_submit_form_data_invalid_model(self):
        """测试无效模型 ID"""
        data = {"model": 99999, "data": {}, "submitted_by": "admin"}
        response = self.client.post("/api/form-data/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_form_data(self):
        """测试表单数据列表"""
        # 创建两条数据
        FormData.objects.create(model=self.model, data={"username": "user1"}, submitted_by="admin")
        FormData.objects.create(model=self.model, data={"username": "user2"}, submitted_by="admin")

        response = self.client.get(f"/api/form-data/?model={self.model.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_form_data_by_model(self):
        """测试按模型过滤表单数据"""
        model2 = DataModel.objects.create(name="model2", schema={"fields": []})
        FormData.objects.create(model=self.model, data={"username": "user1"})
        FormData.objects.create(model=model2, data={"username": "user2"})

        response = self.client.get(f"/api/form-data/?model={self.model.id}")
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["data"]["username"], "user1")


class FormLayoutAPITest(APITestCase):
    """表单布局 API 测试"""

    def setUp(self):
        """测试前准备"""
        self.model = DataModel.objects.create(
            name="layout_test_model",
            schema={
                "fields": [
                    {"name": "username", "type": "text"},
                    {"name": "age", "type": "integer"}
                ]
            }
        )
        self.layout_data = {
            "model": self.model.id,
            "name": "测试布局",
            "layout": {
                "type": "grid",
                "columns": 2,
                "sections": [
                    {"title": "基本信息", "fields": ["username", "age"]}
                ]
            },
            "created_by": "admin"
        }

    def test_create_layout(self):
        """测试创建布局"""
        response = self.client.post("/api/layouts/", self.layout_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "测试布局")
        self.assertEqual(response.data["is_active"], False)
        # 验证数据库
        self.assertEqual(FormLayout.objects.count(), 1)

    def test_list_layouts(self):
        """测试布局列表"""
        FormLayout.objects.create(model=self.model, name="布局1", layout={})
        FormLayout.objects.create(model=self.model, name="布局2", layout={})

        response = self.client.get(f"/api/layouts/?model={self.model.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_activate_layout(self):
        """测试激活布局"""
        # 创建两个布局
        layout1 = FormLayout.objects.create(model=self.model, name="布局1", layout={})
        layout2 = FormLayout.objects.create(model=self.model, name="布局2", layout={})

        # 激活 layout1
        response = self.client.post(f"/api/layouts/{layout1.id}/activate/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["is_active"], True)

        # 验证 layout2 已自动停用
        layout2.refresh_from_db()
        self.assertEqual(layout2.is_active, False)

    def test_duplicate_layout(self):
        """测试复制布局"""
        layout = FormLayout.objects.create(
            model=self.model,
            name="原始布局",
            layout={"type": "grid", "columns": 2}
        )

        response = self.client.post(
            f"/api/layouts/{layout.id}/duplicate/",
            {"name": "新布局"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "新布局")
        self.assertEqual(response.data["layout"], layout.layout)
        # 验证原始布局未被修改
        layout.refresh_from_db()
        self.assertEqual(layout.name, "原始布局")

    def test_update_layout(self):
        """测试更新布局"""
        layout = FormLayout.objects.create(
            model=self.model,
            name="原始布局",
            layout={"type": "grid"}
        )

        response = self.client.put(
            f"/api/layouts/{layout.id}/",
            {"model": self.model.id, "name": "更新后布局", "layout": {"type": "flex"}},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "更新后布局")

    def test_delete_layout(self):
        """测试删除布局"""
        layout = FormLayout.objects.create(model=self.model, name="布局", layout={})

        response = self.client.delete(f"/api/layouts/{layout.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(FormLayout.objects.count(), 0)

    def test_layout_without_model(self):
        """测试缺少 model 应失败"""
        data = {"name": "布局", "layout": {}}
        response = self.client.post("/api/layouts/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)