<template>
  <el-card class="canvas-panel">
    <template #header>
      <span>画布区域（拖拽控件到此处，12栅格）</span>
    </template>
    <div
      class="canvas-area"
      @dragover.prevent
      @drop="onDrop"
    >
      <div v-if="items.length === 0" class="empty-tip">
        从左侧拖拽控件到此处
      </div>
      
      <el-row :gutter="16">
        <el-col
          v-for="(item, index) in items"
          :key="index"
          :span="item.span || (item.widgetType === 'panel' ? 24 : 6)"
          class="layout-col"
          :class="{ active: selectedIndex === index }"
          draggable="true"
          @click="emit('select', index)"
          @dragstart="(e) => onItemDragStart(e, index)"
        >
            <LayoutWidget
            :item="item"
            :fields="fields"
            :selected="selectedIndex === index"
            @update="(newVal) => updateItem(index, newVal)"
            @remove="emit('remove', index)"
            @child-add="(widget) => addChildToContainer(index, widget)"
            @select="(info) => emit('select', { containerIndex: index, childIndex: info.parentIndex, child: info.child })"
            @move-to-container="(info) => emit('move-to-container', { fromIndex: index, ...info })"
            @child-dragstart="(info) => emit('child-dragstart', { containerIndex: index, ...info })"
            @child-dragend="(info) => emit('child-dragend', { containerIndex: index, ...info })"
          />
        </el-col>
      </el-row>
    </div>
  </el-card>
</template>

<script setup>
import LayoutWidget from './LayoutWidget.vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  selectedIndex: {
    type: Number,
    default: null
  },
  fields: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['drop', 'select', 'remove', 'update', 'move-to-container', 'child-dragstart', 'child-dragend', 'child-drop-out'])

const widgets = [
  { type: 'text', label: '单行文本' },
  { type: 'textarea', label: '文本域' },
  { type: 'number', label: '数字' },
  { type: 'date', label: '日期' },
  { type: 'switch', label: '开关' },
  { type: 'select', label: '下拉选择' },
]

let draggedIndex = null

const onItemDragStart = (event, index) => {
  draggedIndex = index
  event.dataTransfer.setData('item-index', index)
  event.dataTransfer.setData('drag-source', 'canvas')
}

const onDrop = (event) => {
  const widgetData = event.dataTransfer.getData('widget')
  const itemIndex = event.dataTransfer.getData('item-index')
  const dragSource = event.dataTransfer.getData('drag-source')
  const childIndex = event.dataTransfer.getData('child-index')
  const containerIndex = event.dataTransfer.getData('container-index')
  
  // 子控件从容器拖出到画布
  if (dragSource === 'child' && childIndex !== null && containerIndex !== null) {
    emit('child-drop-out', {
      fromContainerIndex: parseInt(containerIndex),
      childIndex: parseInt(childIndex)
    })
    draggedIndex = null
    return
  }
  
  // 拖拽已有控件重新排序
  if (draggedIndex !== null && dragSource === 'canvas') {
    const fromIndex = draggedIndex
    const toIndex = props.items.length - 1 // 默认放到末尾
    
    if (fromIndex !== toIndex) {
      const newItems = [...props.items]
      const [movedItem] = newItems.splice(fromIndex, 1)
      newItems.splice(toIndex, 0, movedItem)
      emit('update', newItems)
    }
    
    draggedIndex = null
    return
  }
  
  // 拖拽新控件
  if (!widgetData) return
  
  const widget = JSON.parse(widgetData)
  
  // 如果是容器，直接添加
  if (widget.isContainer) {
    emit('drop', {
      widgetType: widget.type,
      direction: 'column',  // 默认纵向
      label: widget.type === 'panel' ? '新面板' : '',
      children: [],
      expanded: true,
      span: 24
    })
  } else {
    // 普通控件
    emit('drop', {
      widgetType: widget.type,
      label: widget.label,
      fieldName: '',
      span: 6,
      props: {
        visible: true,
        required: false,
        readonly: false,
        default: ''
      }
    })
  }
}

const updateItem = (index, newVal) => {
  const newItems = [...props.items]
  newItems[index] = newVal
  emit('update', newItems)
}

const onChildDrop = (parentIndex, payload) => {
  // 处理子控件添加到容器
  const widget = payload.widget
  const newItem = {
    widgetType: widget.type,
    label: widget.label,
    fieldName: '',
    span: 12,
    props: {
      visible: true,
      required: false,
      readonly: false,
      default: ''
    }
  }
  
  const parent = props.items[parentIndex]
  const children = [...(parent.children || []), newItem]
  
  updateItem(parentIndex, { ...parent, children })
}

const addChildToContainer = (parentIndex, widget) => {
  const newChild = {
    widgetType: widget.type,
    label: widget.label,
    fieldName: '',
    span: 12,
    props: {
      visible: true,
      required: false,
      readonly: false,
      default: ''
    }
  }
  
  const parent = props.items[parentIndex]
  const children = [...(parent.children || []), newChild]
  updateItem(parentIndex, { ...parent, children })
}
</script>

<style scoped>
.canvas-panel {
  min-height: 450px;
}

.canvas-area {
  min-height: 350px;
  border: 2px dashed #dcdfe6;
  border-radius: 4px;
  padding: 16px;
}

.empty-tip {
  text-align: center;
  color: #909399;
  padding: 40px;
}

.layout-col {
  margin-bottom: 16px;
  cursor: move;
}

.layout-col.active :deep(.layout-widget) {
  border-color: #409eff;
}
</style>