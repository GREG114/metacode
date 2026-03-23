# metacode 低代码平台 - 项目详情报告

**生成时间**: 2026-03-22  
**分析人**: AI Assistant  

---

## 📋 一、项目概述

**项目名称**: metacode 低代码平台  
**一句话目标**: 让用户通过前端修改数据模型，根据模型生成表单，管理人员可拖拽调整布局。  
**技术栈**: Django + DRF (后端) + Vue 3 + Element Plus (前端)  
**端口**: 5001  
**数据库**: PostgreSQL (metacode)  

---

## 🎯 二、开发进度总览

### ✅ MVP 已完成（三个阶段）

| 阶段 | 功能 | API 端点 | 状态 |
|------|------|---------|------|
| **阶段一** | 数据模型 CRUD | `/api/models/` | ✅ 完成 |
| **阶段二** | 表单生成 + 数据存储 | `/api/models/{id}/form/`, `/api/form-data/` | ✅ 完成 |
| **阶段三** | 布局配置管理 | `/api/layouts/` | ✅ 完成 |

### 🏗️ 前端开发进度

#### ✅ 已完成功能

**布局编辑器核心能力：**
- 三栏布局：左侧控件列表 + 中间画布 + 右侧属性面板
- 拖拽添加控件到画布
- 控件属性配置（标签、绑定字段、控件类型、栅格、可见/必填/只读/默认值）
- 布局管理（加载/新建/保存/激活/删除）
- 预览功能
- 容器组件（面板/横向/纵向容器）
- 子控件选中与编辑
- 控件拖拽排序（画布内）
- 控件拖入/拖出容器

**页面路由：**
| 页面 | 路由 | 功能 |
|------|------|------|
| 模型列表 | `/models` | 查看所有数据模型 |
| 创建模型 | `/models/new` | 新建数据模型 |
| 编辑模型 | `/models/:id/edit` | 编辑模型 + 字段 |
| 填写表单 | `/forms/:modelId` | 根据模型填表单 |
| 数据列表 | `/forms/:modelId/data` | 查看已提交数据 |
| 布局编辑器 | `/layouts/:modelId` | 拖拽调整布局 |

#### ⏳ 待开发功能

**高优先级：**
- [ ] 撤销/重做功能
- [ ] 响应式布局预览
- [ ] 表单验证增强（后端）

**中优先级：**
- [ ] 布局版本管理 UI
- [ ] 栅格布局支持（更细粒度的 span 配置）
- [ ] 控件属性增强（placeholder、max、min 等）

**低优先级：**
- [ ] 多语言支持
- [ ] 主题切换
- [ ] 组件复用池
- [ ] 用户权限管理

---

## 🔍 三、架构问题

### 3.1 前后端分离但未完全分离
- 前端构建产物放在 `templates/assets/`
- Django 渲染 `templates/index.html` 加载静态资源
- **未配置** Django 的 STATICFILES_DIRS，开发/生产路径不一致

### 3.2 前端构建产物管理混乱
```bash
templates/assets/ 目录包含多个版本的 JS/CSS 文件：
- index-CSMl2glF.js (当前使用)
- index-C5qOtBDa.js (旧版本)
- index-D-jAhBIe.js (旧版本)
等 10+ 个旧文件
```

---

## 📝 四、代码质量

### 4.1 前端 - 待清理
| 文件 | 问题 |
|------|------|
| LayoutWidget.vue | 第 17 行残留 `debugger` 语句 |
| 多处 .vue | console.log 调试语句未清理（约 10 处） |

### 4.2 后端 - 基本正常
- 单元测试存在但覆盖有限
- 序列化器逻辑清晰
- API 设计 RESTful

---

## 🔒 五、安全风险

| 风险项 | 当前状态 | 建议措施 |
|--------|---------|---------|
| 用户认证/权限管理 | ❌ 无 | 添加 Django REST Framework 的认证机制 |
| CSRF 防护 | ❌ 未配置 | 配置 CSRF 中间件和 token |
| API 限流 | ❌ 无 | 添加基础限流规则 |
| HTTPS | ❌ 生产环境未配置 | 配置 SSL 证书 |

---

## 🛠️ 六、部署脚本 (deploy.sh)

```bash
#!/bin/bash

cd /root/.openclaw/workspace/metacode

# 杀旧进程
pkill -f "manage.py runserver" || true

# 更新代码
git pull

# 前端构建（已优化：构建前清理 dist）
cd frontend && rm -rf dist && npm run build && cd ..

# 复制前端到 Django templates
rm -rf templates/*
cp -r frontend/dist/* templates/

# 数据库迁移
python manage.py migrate --run-syncdb

# 启动
nohup python manage.py runserver 0.0.0.0:5001 > /tmp/metacode.log 2>&1 &

echo "Metacode deployed on port 5001"
```

**脚本特点：**
- ✅ 自动化全流程（杀进程 → git pull → build → copy → migrate → start）
- ✅ 已优化：构建前清理 dist 目录，避免新旧版本混用
- ⚠️ 风险：使用 `runserver` 而非 Gunicorn/uWSGI，生产环境建议改用 WSGI 服务器

---

## 📂 七、项目结构

```
metacode/
├── core/                 # Django 后端核心代码
├── frontend/             # Vue 前端项目（Vite 构建）
│   └── src/
│       ├── api/         # API 接口定义
│       ├── components/  # 公共组件
│       │   └── layout/  # 布局相关组件
│       ├── views/       # 页面组件
│       ├── router/      # 路由配置
│       └── main.js      # 入口文件
├── metacode/            # Django app
├── templates/           # Django 模板（含前端构建产物）
├── TEST/                # 测试代码
├── manage.py            # Django 管理脚本
├── deploy.sh            # 部署脚本
└── *.md                 # 文档文件
```

---

## 📚 八、详细文档索引

| 文档 | 位置 | 说明 |
|------|------|------|
| PLAN.md | `/root/.openclaw/workspace/metacode/PLAN.md` | 简洁版开发计划 |
| PHASE1.md | `/root/.openclaw/workspace/metacode/PHASE1.md` | 阶段一详情（数据模型） |
| PHASE2.md | `/root/.openclaw/workspace/metacode/PHASE2.md` | 阶段二详情（表单生成） |
| PHASE3.md | `/root/.openclaw/workspace/metacode/PHASE3.md` | 阶段三详情（布局配置） |
| FRONTEND_PLAN.md | `/root/.openclaw/workspace/metacode/FRONTEND_PLAN.md` | 前端开发计划 |
| TESTING.md | `/root/.openclaw/workspace/metacode/TESTING.md` | 测试方案 |
| MEMO.md | `/root/.openclaw/workspace/metacode/MEMO.md` | 开发备忘录 |
| AUDIT.md | `/root/.openclaw/workspace/metacode/AUDIT.md` | 项目审计报告 |

---

## ⚠️ 九、技术债务清单

1. **未配置 Django STATICFILES_DIRS** - 前后端分离不彻底
2. **前端构建产物管理混乱** - templates/assets/堆积旧版本
3. **无用户认证/权限** - 安全风险
4. **无撤销/重做功能** - 用户体验缺失
5. **响应式预览缺失** - 布局编辑器不完整
6. **代码质量需清理** - debugger/console.log残留

---

## 📊 十、Git 状态

- **分支**: main
- **与上游**: 一致（origin/main）
- **未提交变更**: ✅ 无（已提交 deploy.sh 优化改动）

---

## 🎯 十一、总结与建议

**整体评价**: MVP 已完成，基本可用  
**主要风险**: 
1. 前端构建产物管理混乱
2. 无安全防护
3. 代码质量需清理（console.log/debugger）

**建议优先级**:
1. ✅ **已处理**: deploy.sh 添加构建前清理指令
2. 🔧 **中优先级**: 清理调试代码、完善前后端分离部署
3. 🛡️ **高优先级**: 添加基础安全配置（认证/CSRF/限流）
4. ✨ **低优先级**: 补充功能（撤销/排序/响应式）

---

*本报告由 AI Assistant 自动生成，基于项目文档分析*
