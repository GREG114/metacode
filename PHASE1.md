# 阶段一：数据模型编辑器

## 目标
让用户能创建、编辑、删除数据模型定义。

## 核心功能
1. **模型管理**
   - 创建新数据模型
   - 编辑现有模型
   - 删除模型
   - 查看模型列表

2. **字段管理**
   - 为模型添加字段
   - 编辑字段属性
   - 删除字段
   - 调整字段顺序

3. **字段类型支持**
   - 文本 (text)
   - 整数 (integer)
   - 小数 (decimal)
   - 日期 (date)
   - 布尔值 (boolean)
   - 下拉选择 (select)
   - 文件上传 (file)

## 技术实现

### 后端 (Django)
1. **数据库表**
   ```sql
   -- 数据模型表
   CREATE TABLE data_model (
     id SERIAL PRIMARY KEY,
     name VARCHAR(100) NOT NULL UNIQUE,
     description TEXT,
     schema JSONB NOT NULL DEFAULT '{"fields": []}',
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW()
   );
   ```

2. **Django 模型**
   ```python
   class DataModel(models.Model):
       name = models.CharField(max_length=100, unique=True)
       description = models.TextField(blank=True)
       schema = models.JSONField(default=dict)  # {fields: [...], version: 1}
       created_at = models.DateTimeField(auto_now_add=True)
       updated_at = models.DateTimeField(auto_now=True)
   ```

3. **API 端点**
   - `GET /api/models/` - 模型列表
   - `POST /api/models/` - 创建模型
   - `GET /api/models/{id}/` - 模型详情
   - `PUT /api/models/{id}/` - 更新模型
   - `DELETE /api/models/{id}/` - 删除模型

### 前端 (Vue 3)
1. **页面结构**
   - `/models` - 模型列表页
   - `/models/new` - 创建模型页
   - `/models/{id}/edit` - 编辑模型页

2. **组件**
   - `ModelList.vue` - 模型列表
   - `ModelEditor.vue` - 模型编辑器
   - `FieldEditor.vue` - 字段属性编辑器

3. **状态管理**
   - Pinia 存储模型状态
   - API 服务层封装

## 开发步骤
1. 创建 Django 项目
2. 安装 DRF 并配置
3. 实现 DataModel 模型和序列化器
4. 创建视图集和路由
5. Vue 项目初始化
6. 前端页面开发
7. API 对接
8. 测试和验证

## 测试用例
### 后端测试
1. 模型 CRUD 操作
2. 字段 Schema 验证
3. 权限控制（暂无）
4. 输入验证

### 前端测试
1. 页面渲染正确
2. 表单提交
3. 错误处理
4. 用户交互流程

### 集成测试
1. 完整创建模型流程
2. 编辑模型更新字段
3. 删除模型

## 验收标准
- [ ] 用户能创建包含字段的模型
- [ ] 字段类型选择正常
- [ ] 模型数据持久化到数据库
- [ ] 前端 UI 响应流畅
- [ ] 所有测试用例通过
- [ ] 错误日志记录完整

## 日志要求
- 每个 API 调用记录请求/响应
- 测试失败时记录详细错误原因
- 用户操作日志（脱敏）
- 性能指标（响应时间）

## 预估时间
- 后端开发：2-3 天
- 前端开发：3-4 天
- 测试：1-2 天
- 总计：6-9 个工作日

## 风险与缓解
1. **Schema 设计变更**: 使用 JSONB 灵活存储
2. **前端复杂状态**: 使用 Pinia 管理状态
3. **数据库迁移**: 初期就设计好字段结构
4. **测试覆盖率**: 制定最小测试覆盖率目标 (80%)