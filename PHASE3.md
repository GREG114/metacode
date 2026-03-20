# 阶段三：拖拽布局调试器

## 目标
让管理人员通过拖拽方式调整表单布局，提供实时预览和调试功能。

## 核心功能
1. **布局编辑器**
   - 拖拽调整字段位置
   - 修改字段分组和排版
   - 设置布局属性（列数、间距等）

2. **实时预览**
   - 布局变化实时反映到预览区
   - 同步表单渲染效果
   - 响应式布局预览

3. **布局配置管理**
   - 保存布局配置
   - 加载历史布局版本
   - 布局版本对比

4. **调试工具**
   - 字段属性实时编辑
   - 布局约束验证
   - 错误提示和建议

## 技术实现

### 后端 (Django)
1. **布局数据表**
   ```sql
   -- 表单布局配置表
   CREATE TABLE form_layout (
     id SERIAL PRIMARY KEY,
     model_id INTEGER REFERENCES data_model(id),
     name VARCHAR(100) NOT NULL,          -- 布局名称
     layout JSONB NOT NULL,                -- 布局配置
     is_active BOOLEAN DEFAULT FALSE,     -- 是否生效
     version INTEGER DEFAULT 1,
     created_by VARCHAR(100),
     created_at TIMESTAMP DEFAULT NOW(),
     updated_at TIMESTAMP DEFAULT NOW()
   );

   -- 布局版本表
   CREATE TABLE layout_version (
     id SERIAL PRIMARY KEY,
     layout_id INTEGER REFERENCES form_layout(id),
     layout JSONB NOT NULL,
     change_description TEXT,
     created_by VARCHAR(100),
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

2. **API 端点**
   - `GET /api/models/{id}/layouts/` - 布局列表
   - `POST /api/models/{id}/layouts/` - 创建布局
   - `PUT /api/models/{id}/layouts/{layout_id}/` - 更新布局
   - `DELETE /api/models/{id}/layouts/{layout_id}/` - 删除布局
   - `POST /api/layouts/{layout_id}/versions/` - 创建版本
   - `GET /api/layouts/{layout_id}/versions/` - 版本历史
   - `PUT /api/models/{id}/activate-layout/` - 激活布局

3. **布局 Schema 示例**
   ```json
   {
     "type": "grid",
     "columns": 2,
     "gap": "16px",
     "sections": [
       {
         "title": "基本信息",
         "fields": ["name", "age", "gender"],
         "layout": "grid",
         "columns": 3
       },
       {
         "title": "联系方式",
         "fields": ["email", "phone", "address"],
         "layout": "vertical"
       }
     ]
   }
   ```

### 前端 (Vue 3 + 拖拽库)
1. **组件架构**
   - `LayoutEditor.vue` - 布局编辑器主组件
   - `DraggableField.vue` - 可拖拽字段项
   - `LayoutPreview.vue` - 实时预览区
   - `LayoutToolbar.vue` - 布局工具栏
   - `SectionEditor.vue` - 分组编辑器

2. **拖拽库选择**
   - **Vue Draggable Next** (基于 Sortable.js)
   - 或 **dnd-kit** (现代拖拽库)
   - 或 **vue3-dnd** (React DnD 风格)

3. **布局状态管理**
   - 当前布局配置（响应式）
   - 字段拖拽状态
   - 预览同步状态
   - 版本管理状态

## 开发步骤
1. 创建布局数据模型和 API
2. 安装和配置拖拽库
3. 开发布局编辑器组件
4. 实现拖拽交互逻辑
5. 开发实时预览同步
6. 添加布局配置管理
7. 实现版本控制功能
8. 添加调试工具
9. 性能优化
10. 测试和验证

## 测试用例
### 后端测试
1. 布局 CRUD 操作
2. 布局版本控制
3. 布局激活/停用
4. 布局验证规则

### 前端测试
1. 拖拽操作流畅性
2. 布局配置保存/加载
3. 实时预览同步
4. 版本切换功能
5. 错误处理

### 性能测试
1. 拖拽性能（大量字段）
2. 预览渲染性能
3. 布局保存响应时间
4. 内存占用

### E2E 测试
1. 完整布局编辑流程
2. 多用户并发编辑
3. 布局版本回滚
4. 布局激活生效

## 验收标准
- [ ] 拖拽操作流畅，无卡顿
- [ ] 布局配置能正确保存/加载
- [ ] 实时预览与编辑器同步
- [ ] 布局版本管理正常
- [ ] 布局激活功能生效
- [ ] 响应式布局支持
- [ ] 测试覆盖率 > 80%
- [ ] 性能：拖拽响应 < 100ms

## 交互设计要点
1. **拖拽反馈**: 视觉提示、占位符
2. **撤销/重做**: 支持操作历史
3. **快捷键**: 常用操作快捷键
4. **冲突处理**: 并发编辑冲突解决
5. **引导提示**: 新手引导和工具提示

## 日志要求
- 拖拽操作日志（用于分析用户行为）
- 布局保存失败详情
- 版本变更记录
- 性能指标日志
- 用户调试操作记录

## 预估时间
- 后端开发：3-4 天
- 前端核心开发：5-6 天
- 交互优化：2-3 天
- 测试：3-4 天
- 总计：13-17 个工作日

## 风险与缓解
1. **拖拽性能**: 虚拟滚动、懒加载
2. **复杂布局**: 逐步支持，先实现简单网格
3. **同步冲突**: 乐观锁 + WebSocket 实时同步
4. **学习曲线**: 提供模板和预设布局
5. **浏览器兼容**: 明确支持的浏览器范围