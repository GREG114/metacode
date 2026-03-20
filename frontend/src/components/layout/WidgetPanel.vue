<template>
  <el-card class="widget-panel">
    <template #header>控件列表</template>
    
    <div class="widget-section">
      <div class="section-title">容器</div>
      <div class="widget-list">
        <div
          v-for="c in containers"
          :key="c.type"
          class="widget-item container-item"
          draggable="true"
          @dragstart="onDragStart($event, { ...c, isContainer: true })"
        >
          <el-icon><component :is="c.icon" /></el-icon>
          <span>{{ c.label }}</span>
        </div>
      </div>
    </div>
    
    <div class="widget-section">
      <div class="section-title">字段</div>
      <div class="widget-list">
        <div
          v-for="widget in widgets"
          :key="widget.type"
          class="widget-item"
          draggable="true"
          @dragstart="onDragStart($event, widget)"
        >
          <el-icon><component :is="widget.icon" /></el-icon>
          <span>{{ widget.label }}</span>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script setup>
const emit = defineEmits(['drag-start'])

const containers = [
  { type: 'panel', label: '面板', icon: 'FolderOpened', canHaveChildren: true },
  { type: 'container', label: '容器', icon: 'Grid', canHaveChildren: true },
]
console.log('[WidgetPanel] containers:', containers)

const widgets = [
  { type: 'text', label: '单行文本', icon: 'Edit', compatibleTypes: ['text', 'textarea'] },
  { type: 'textarea', label: '文本域', icon: 'Document', compatibleTypes: ['text'] },
  { type: 'number', label: '数字', icon: 'Odometer', compatibleTypes: ['integer', 'decimal'] },
  { type: 'date', label: '日期', icon: 'Calendar', compatibleTypes: ['date'] },
  { type: 'switch', label: '开关', icon: 'Switch', compatibleTypes: ['boolean'] },
  { type: 'select', label: '下拉选择', icon: 'ArrowDown', compatibleTypes: ['select'] },
]

const onDragStart = (event, widget) => {
  // 容器需要额外传递属性
  const widgetData = {
    ...widget,
    isContainer: widget.canHaveChildren,
    direction: widget.direction || 'column'  // 传递方向属性
  }
  event.dataTransfer.setData('widget', JSON.stringify(widgetData))
  emit('drag-start', widget)
}
</script>

<style scoped>
.widget-panel {
  height: 450px;
  overflow-y: auto;
}

.widget-section {
  margin-bottom: 16px;
}

.section-title {
  font-size: 12px;
  color: #909399;
  margin-bottom: 8px;
  font-weight: 500;
}

.widget-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.widget-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: #f5f7fa;
  border-radius: 4px;
  cursor: move;
  transition: all 0.2s;
}

.widget-item:hover {
  background: #ecf5ff;
  border-color: #409eff;
}

.container-item {
  background: #f0f9eb;
}

.container-item:hover {
  background: #e1f3d8;
  border-color: #67c23a;
}
</style>