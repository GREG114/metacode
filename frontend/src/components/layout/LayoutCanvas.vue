<template>
  <el-card class="canvas-panel">
    <template #header>
      <span>画布区域（拖拽控件到此处，12栅格）</span>
    </template>
    <div class="canvas-area">
      <div v-if="items.length === 0" class="empty-tip">
        从左侧拖拽控件到此处
      </div>
      
      <draggable
        v-model="localItems"
        item-key="__index__"
        ghost-class="ghost"
        drag-class="dragging"
        :animation="200"
        :group="{ name: 'layout', pull: true, put: true }"
        @add="onItemAdded"
        @end="onDragEnd"
      >
        <template #item="{ element, index }">
          <el-col
            :span="element.span || (element.widgetType === 'panel' ? 24 : 6)"
            class="layout-col"
            :class="{ active: selectedIndex === index }"
            @click="emit('select', index)"
          >
            <LayoutWidget
              :item="element"
              :fields="fields"
              :selected="selectedIndex === index"
              @update="(newVal) => updateItem(element.__selfIndex__, newVal)"
              @remove="emit('remove', index)"
              @child-add="(widget) => addChildToContainer(element.__selfIndex__, widget)"
              @select="(info) => emit('select', { containerIndex: element.__selfIndex__, childIndex: info.parentIndex, child: info.child })"
              @move-to-container="(info) => emit('move-to-container', { fromIndex: element.__selfIndex__, ...info })"
              @child-dragstart="(info) => emit('child-dragstart', { containerIndex: element.__selfIndex__, ...info })"
              @child-dragend="(info) => emit('child-dragend', { containerIndex: element.__selfIndex__, ...info })"
            />
          </el-col>
        </template>
      </draggable>
    </div>
  </el-card>
</template>

<script setup>
import { computed, ref, watch, toRaw } from 'vue'
import draggable from 'vuedraggable'
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

// vuedraggable 用的 items（用 watch 模式）
const localItems = ref([])

watch(() => props.items, (newItems) => {
  localItems.value = (newItems || []).map((item, idx) => ({ ...item, __index__: idx, __selfIndex__: idx }))
}, { immediate: true, deep: true })

// vuedraggable 接受新元素时触发（从工具箱拖入或从容器拖出）
const onItemAdded = (evt) => {
  const newItem = localItems.value[evt.newIndex]
  
  // 用 isNew 标记判断是否是从工具箱拖入的新控件
  if (newItem && newItem.isNew) {
    const widgetType = newItem.type || newItem.widgetType
    const canHaveChildren = newItem.canHaveChildren
    
    if (canHaveChildren) {
      // 容器控件
      localItems.value[evt.newIndex] = {
        widgetType: widgetType,
        direction: newItem.direction || 'column',
        label: widgetType === 'panel' ? '新面板' : '',
        children: [],
        expanded: true,
        span: 24,
        __index__: evt.newIndex,
        __selfIndex__: evt.newIndex
      }
    } else {
      // 普通控件
      localItems.value[evt.newIndex] = {
        widgetType: widgetType,
        label: newItem.label || '',
        fieldName: '',
        span: 6,
        props: {
          visible: true,
          required: false,
          readonly: false,
          default: ''
        },
        __index__: evt.newIndex,
        __selfIndex__: evt.newIndex
      }
    }
    
    // 立即触发更新
    const newItems = localItems.value.map(item => {
      const { __index__: i, __selfIndex__: s, isNew, ...rest } = item
      return rest
    })
    emit('update', newItems)
  } else {
    // 内部排序或从容器移动到画布，直接更新
    onDragEnd(evt)
  }
}

const onDragEnd = (evt) => {
  const newItems = localItems.value.map((item, idx) => {
    const { __index__: i, __selfIndex__: s, isNew, ...rest } = item
    return { ...rest, __index__: idx }
  })
  emit('update', newItems)
}

const onDrop = (event) => {
  const widgetData = event.dataTransfer.getData('widget')
  const dragSource = event.dataTransfer.getData('drag-source')
  const childIndex = event.dataTransfer.getData('child-index')
  const containerIndex = event.dataTransfer.getData('container-index')
  
  // 子控件从容器拖出到画布
  if (dragSource === 'child' && childIndex !== null && containerIndex !== null) {
    emit('child-drop-out', {
      fromContainerIndex: parseInt(containerIndex),
      childIndex: parseInt(childIndex)
    })
    return
  }
  
  // 拖拽新控件（从 WidgetPanel 拖入）
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

/* vuedraggable 拖拽占位符样式 */
.ghost {
  opacity: 0.5;
  background: #c8ebfb;
  border: 2px dashed #409eff;
}

.dragging {
  opacity: 0.8;
}
</style>