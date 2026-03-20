# 阶段二：表单生成器

## 目标
根据数据模型定义，自动生成表单供用户填写。

## 核心功能
1. **表单 Schema 生成**
   - 根据数据模型转换为表单 JSON Schema
   - 支持字段级验证规则
   - 布局建议（默认顺序）

2. **动态表单渲染**
   - 根据 Schema 渲染表单 UI
   - 支持不同字段类型组件
   - 实时表单验证

3. **表单数据处理**
   - 表单数据收集
   - 数据验证（前端+后端）
   - 提交到后端 API

4. **表单预览**
   - 预览生成的表单效果
   - 模拟用户填写
   - 查看验证效果

## 技术实现

### 后端 (Django)
1. **API 端点**
   - `GET /api/models/{id}/form/` - 获取表单 Schema
   - `POST /api/models/{id}/data/` - 提交表单数据
   - `GET /api/models/{id}/data/` - 获取表单数据列表

2. **表单 Schema 生成器**
   ```python
   def generate_form_schema(data_model):
       """将数据模型转换为表单 Schema"""
       schema = {
           "type": "object",
           "properties": {},
           "required": [],
           "ui": {"order": []}
       }
       
       for field in data_model.schema.get("fields", []):
           field_schema = {
               "type": field.get("type", "string"),
               "title": field.get("label", field["name"]),
               "description": field.get("description", ""),
           }
           
           # 添加验证规则
           if field.get("required"):
               schema["required"].append(field["name"])
               
           if field.get("options"):
               field_schema["enum"] = field["options"]
               
           schema["properties"][field["name"]] = field_schema
           schema["ui"]["order"].append(field["name"])
           
       return schema
   ```

3. **表单数据表**
   ```sql
   -- 表单数据表
   CREATE TABLE form_data (
     id SERIAL PRIMARY KEY,
     model_id INTEGER REFERENCES data_model(id),
     data JSONB NOT NULL,  -- 表单提交的数据
     submitted_by VARCHAR(100),
     submitted_at TIMESTAMP DEFAULT NOW()
   );
   ```

### 前端 (Vue 3)
1. **组件架构**
   - `FormRenderer.vue` - 核心表单渲染组件
   - `FieldComponents/` - 字段类型组件库
   - `FormPreview.vue` - 表单预览页
   - `DataList.vue` - 表单数据列表

2. **表单组件类型**
   - `TextField.vue` - 文本输入
   - `NumberField.vue` - 数字输入
   - `DateField.vue` - 日期选择
   - `SelectField.vue` - 下拉选择
   - `CheckboxField.vue` - 复选框
   - `FileUpload.vue` - 文件上传

3. **表单状态管理**
   - 表单数据响应式绑定
   - 验证状态管理
   - 提交状态管理

## 开发步骤
1. 扩展 DataModel 模型，支持表单配置
2. 实现表单 Schema 生成器
3. 创建表单数据存储表
4. 开发前端表单渲染组件
5. 实现字段类型组件库
6. 添加表单验证逻辑
7. 表单数据提交 API
8. 表单预览功能
9. 测试和验证

## 测试用例
### 后端测试
1. 表单 Schema 生成正确性
2. 表单数据验证
3. 表单数据存储/检索
4. 边界值测试

### 前端测试
1. 表单渲染正确性
2. 字段组件交互
3. 表单验证触发
4. 表单提交流程
5. 错误状态处理

### 集成测试
1. 从模型创建到表单生成全流程
2. 表单填写和提交
3. 表单数据查询
4. 多用户同时操作

## 验收标准
- [ ] 表单 Schema 能正确从模型生成
- [ ] 表单 UI 渲染与模型定义一致
- [ ] 表单验证规则生效
- [ ] 表单数据能提交和保存
- [ ] 表单预览功能正常
- [ ] 性能：表单加载 < 500ms
- [ ] 测试覆盖率 > 85%

## 表单 Schema 示例
```json
{
  "type": "object",
  "properties": {
    "name": {
      "type": "string",
      "title": "姓名",
      "minLength": 2,
      "maxLength": 50
    },
    "age": {
      "type": "integer",
      "title": "年龄",
      "minimum": 0,
      "maximum": 150
    }
  },
  "required": ["name"],
  "ui": {
    "order": ["name", "age"]
  }
}
```

## 日志要求
- 表单 Schema 生成日志
- 表单提交数据记录（脱敏）
- 验证错误详情
- 性能监控日志

## 预估时间
- 后端开发：3-4 天
- 前端开发：4-5 天
- 测试：2-3 天
- 总计：9-12 个工作日

## 风险与缓解
1. **表单复杂度**: 限制字段类型数量，逐步扩展
2. **性能问题**: 缓存表单 Schema，懒加载
3. **验证复杂性**: 使用成熟表单验证库
4. **数据安全**: 输入过滤，防 XSS