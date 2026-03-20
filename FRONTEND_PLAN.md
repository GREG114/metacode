# 前端开发计划

## 技术栈
- Vue 3 + Element Plus
- Vite 构建
- Vue Router + Pinia（可选）

## 项目结构
```
frontend/src/
├── api/                 # API 接口
├── components/         # 公共组件
│   └── layout/         # 布局相关组件
├── views/              # 页面组件
├── router/             # 路由配置
└── main.js             # 入口
```

---

## 开发进度

### ✅ 已完成

#### 阶段一：数据模型
| 页面 | 路由 | 功能 |
|------|------|------|
| 模型列表 | /models | 查看所有数据模型 |
| 创建模型 | /models/new | 新建数据模型 |
| 编辑模型 | /models/:id/edit | 编辑模型+字段 |

#### 阶段二：表单
| 页面 | 路由 | 功能 |
|------|------|------|
| 填写表单 | /forms/:modelId | 根据模型填表单 |
| 数据列表 | /forms/:modelId/data | 查看已提交数据 |

#### 阶段三：布局编辑器
| 页面 | 路由 | 功能 |
|------|------|------|
| 布局编辑器 | /layouts/:modelId | 拖拽调整布局 |

**布局编辑器 - 功能清单：**
- ✅ 三栏布局：左侧控件列表 + 中间画布 + 右侧属性面板
- ✅ 拖拽添加控件到画布
- ✅ 控件属性配置（标签、绑定字段、控件类型、栅格、可见/必填/只读/默认值）
- ✅ 布局管理（加载/新建/保存/激活/删除）
- ✅ 预览功能
- ⚠️ 表单联动（部分支持）
- ✅ 容器组件（面板/横向/纵向容器）
- ✅ 子控件选中与编辑
- ✅ 控件拖拽排序（画布内）
- ✅ 控件拖入/拖出容器

**组件拆分（已完成）：**
- `components/layout/WidgetPanel.vue` - 左侧控件列表
- `components/layout/LayoutCanvas.vue` - 中间画布区域
- `components/layout/LayoutWidget.vue` - 画布内单个控件
- `components/layout/PropsPanel.vue` - 右侧属性面板
- `components/layout/LayoutList.vue` - 布局列表
- `components/layout/PreviewDialog.vue` - 预览弹窗

---

### ⏳ 待开发

#### 优先级：高
- [ ] 撤销/重做功能
- [ ] 响应式布局预览
- [ ] 表单验证增强（后端）

#### 优先级：中
- [ ] 布局版本管理 UI
- [ ] 栅格布局支持（更细粒度的 span 配置）
- [ ] 控件属性增强（placeholder、max、min 等）

#### 优先级：低
- [ ] 多语言支持
- [ ] 主题切换
- [ ] 组件复用池
- [ ] 用户权限管理

---

## 页面结构
```
/                     - 首页/跳转
/models               - 模型列表
/models/new           - 创建模型
/models/:id/edit      - 编辑模型+字段
/forms/:modelId       - 填写表单
/forms/:modelId/data  - 查看数据
/layouts/:modelId     - 拖拽布局编辑器
```

---

## 代码质量

### 清理记录 (2026-03-18)
- ✅ 清理残留 debugger 语句
- ⚠️ 10 处 console.log 待清理（仅开发环境用）
- ⚠️ 前端构建产物需清理旧版本

### 已知问题
- 无撤销/重做
- 响应式预览缺失
- 容器嵌套编辑体验待优化

---

**更新日期**: 2026-03-18 19:42