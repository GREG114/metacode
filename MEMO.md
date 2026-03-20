# 开发备忘录

**更新日期**: 2026-03-18

---

## 本次修复记录

### 2026-03-18
- **PropsPanel.vue**: 删除重复代码块（构建失败根源）
- **LayoutWidget.vue**: 子控件点击事件从 testClick 改为 onChildClick
- **LayoutCanvas.vue**: 清理 debugger
- **LayoutEditor.vue**: 支持子控件选中显示和更新
- **FormFill.vue**: 递归提取容器内子控件
- **拖拽功能**: 
  - 控件从画布拖入容器
  - 子控件从容器拖出到画布
  - 画布内控件排序

---

## 已知问题

1. **LayoutWidget.vue:17** - 残留 `debugger` 语句
2. 多处 `console.log` 调试语句待清理
3. `templates/assets/` 堆积旧版本构建产物

---

## 技术债务

1. 未配置 Django STATICFILES_DIRS
2. 前后端分离不彻底
3. 无用户认证/权限
4. 无撤销/重做
5. 响应式预览缺失

---

## 犯过的错误

### 2026-03-18
1. **未经允许提交代码** → 之后必须先问用户再提交
2. **拖拽事件传参错误** → 混淆了 event 和 info，导致 onChildDragStart 函数定义与调用不匹配
3. **构建产物覆盖问题** → 每次 build 后忘记更新 index.html 引用

---

## 下一步

见 FRONTEND_PLAN.md - 待开发功能列表