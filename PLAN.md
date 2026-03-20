# metacode 低代码平台开发计划（简洁版）

## 一句话目标
让用户通过前端修改数据模型，根据模型生成表单，管理人员可拖拽调整布局。

## 核心功能（管理员后台）
- 定义数据模型（表结构）
- 自动生成表单
- 拖拽调整表单布局
- 测试填写/查看数据

## 技术栈
- 后端: Django + DRF (5001 端口)
- 前端: Vue 3 + Element Plus (见 [FRONTEND_PLAN.md](FRONTEND_PLAN.md))
- 数据库: PostgreSQL (现有 metacode)
- 部署: Django 服务前端静态文件（单一端口 5001）

## 开发进度

### ✅ 后端（已完成）
| 阶段 | 功能 | API 端点 | 状态 |
|------|------|---------|------|
| 阶段一 | 数据模型 CRUD | /api/models/ | ✅ 完成 |
| 阶段二 | 表单生成 + 数据存储 | /api/models/{id}/form/, /api/form-data/ | ✅ 完成 |
| 阶段三 | 布局配置管理 | /api/layouts/ | ✅ 完成 |

### ✅ 前端
详见 [FRONTEND_PLAN.md](FRONTEND_PLAN.md)

## 用户操作流程
1. 管理员创建/编辑数据模型
2. 系统自动生成表单
3. 管理员拖拽调整布局
4. 管理员测试填写/查看数据

## 测试规范
- 每个阶段在 TEST/ 目录有独立测试
- 日志格式: JSON，包含错误原因
- 测试类型: 单元、集成、E2E

## 详细文档
- 阶段一详情: [PHASE1.md](PHASE1.md)
- 阶段二详情: [PHASE2.md](PHASE2.md)
- 阶段三详情: [PHASE3.md](PHASE3.md)
- 测试方案: [TESTING.md](TESTING.md)
- 前端计划: [FRONTEND_PLAN.md](FRONTEND_PLAN.md)

---

**更新日期**: 2026-03-18