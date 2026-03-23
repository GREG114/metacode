<template>
  <el-card class="widget-panel">
    <template #header>控件列表</template>
    
    <div class="widget-section">
      <div class="section-title">字段</div>
      <draggable
        v-model="widgets"
        :group="{ name: 'layout', pull: 'clone', put: false }"
        :sort="false"
        :clone="cloneWidget"
        item-key="id"
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

// 生成唯一 ID
const generateId = () => `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

// 克隆时添加唯一 ID 并标记为新控件
const cloneWidget = (widget) => ({
  ...widget,
  id: generateId(),
  isNew: true, // 明确标记为新控件
  isContainer: widget.canHaveChildren,
  direction: widget.direction || 'column'
})

const widgets = ref([
  { type: 'panel', label: '面板', icon: 'FolderOpened', canHaveChildren: true },
  { type: 'text', label: '单行文本', icon: 'Edit', compatibleTypes: ['text', 'textarea'] },
  { type: 'textarea', label: '文本域', icon: 'Document', compatibleTypes: ['text'] },
  { type: 'number', label: '数字', icon: 'Odometer', compatibleTypes: ['integer', 'decimal'] },
  { type: 'date', label: '日期', icon: 'Calendar', compatibleTypes: ['date'] },
  { type: 'switch', label: '开关', icon: 'Switch', compatibleTypes: ['boolean'] },
  { type: 'select', label: '下拉选择', icon: 'ArrowDown', compatibleTypes: ['select'] },
])

const onDragStart = (event, widget) => {
  const widgetData = {
    ...widget,
    isContainer: widget.canHaveChildren,
    direction: widget.direction || 'column'
  }
  event.dataTransfer.setData('widget', JSON.stringify(widgetData))
  emit('drag-start', widget)
}

const onWidgetClick = (widget) => {
  emit('widget-click', {
    ...widget,
    id: generateId(),
    isNew: true,
    isContainer: widget.canHaveChildren,
    direction: widget.direction || 'column'
  })
}
</script>

