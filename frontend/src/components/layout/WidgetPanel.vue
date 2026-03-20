<template>
  <el-card class="widget-panel">
    <template #header>控件列表</template>
    
    <div class="widget-section">
      <div class="section-title">字段</div>
      <draggable
        v-model="widgets"
        :group="{ name: 'layout', pull: 'clone', put: false }"
        :sort="false"
        item-key="type"
        class="widget-list"
      >
        <template #item="{ element }">
          <div
            class="widget-item"
            @click="onWidgetClick(element)"
          >
            <el-icon><component :is="element.icon" /></el-icon>
            <span>{{ element.label }}</span>
          </div>
        </template>
      </draggable>
    </div>
  </el-card>
</template>

<script setup>
import { ref } from 'vue'
import draggable from 'vuedraggable'

const emit = defineEmits(['drag-start', 'widget-click'])

const widgets = ref([
  { type: 'panel', label: '面板', icon: 'FolderOpened', canHaveChildren: true, isNew: true },
  { type: 'text', label: '单行文本', icon: 'Edit', compatibleTypes: ['text', 'textarea'], isNew: true },
  { type: 'textarea', label: '文本域', icon: 'Document', compatibleTypes: ['text'], isNew: true },
  { type: 'number', label: '数字', icon: 'Odometer', compatibleTypes: ['integer', 'decimal'], isNew: true },
  { type: 'date', label: '日期', icon: 'Calendar', compatibleTypes: ['date'], isNew: true },
  { type: 'switch', label: '开关', icon: 'Switch', compatibleTypes: ['boolean'], isNew: true },
  { type: 'select', label: '下拉选择', icon: 'ArrowDown', compatibleTypes: ['select'], isNew: true },
])

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

// 点击控件添加到画布（兼容点击添加）
const onWidgetClick = (widget) => {
  emit('widget-click', {
    ...widget,
    isContainer: widget.canHaveChildren,
    direction: widget.direction || 'column'
  })
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