<template>
  <el-card class="canvas-panel">
    <template #header>
      <span>画布区域（拖拽控件到此处，12 栅格）</span>
    </template>
    <div class="canvas-area">
      <div v-if="items.length === 0" class="empty-tip">
        从左侧拖拽控件到此处
      </div>
      
      <draggable
        v-model="localItems"
        item-key="id"
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
            @click.stop="emit('select', index)"
          >
            <LayoutWidget
              :item="element"
              :fields="fields"
              :selected="selectedIndex === index"
              :selected-child-index="selectedParentIndex === index ? selectedChildIndex : null"
              @update="(newVal) => updateItem(element.id, newVal)"
              @remove="removeItem(element.id)"
              @child-add="(widget) => addChildToContainer(element.id, widget)"
              @select="(info) => emit('select', { containerIndex: index, childIndex: info.parentIndex, child: info.child })"
              @move-to-container="(info) => emit('move-to-container', { fromIndex: index, ...info })"
              @child-dragstart="(info) => emit('child-dragstart', { containerIndex: index, ...info })"
              @child-dragend="(info) => emit('child-dragend', { containerIndex: index, ...info })"
            />
          </el-col>
        </template>
      </draggable>
    </div>
  </el-card>
</template>

<script setup>
import { ref, watch } from 'vue'
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
  selectedParentIndex: {
    type: Number,
    default: null
  },
  selectedChildIndex: {
    type: Number,
    default: null
  },
  fields: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['drop', 'select', 'remove', 'update', 'move-to-container', 'child-dragstart', 'child-dragend', 'child-drop-out'])

const localItems = ref([])

// 同步 props.items 到 localItems，确保 id 存在
watch(() => props.items, (newItems) => {
  localItems.value = (newItems || []).map(item => ({
    ...item,
    id: item.id || `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }))
}, { immediate: true, deep: true })

const onItemAdded = (evt) => {
  const newItem = localItems.value[evt.newIndex]
  
  // 只有标记为 isNew 的控件才需要初始化结构
  if (newItem && newItem.isNew) {
    const widgetType = newItem.type || newItem.widgetType
    const canHaveChildren = newItem.isContainer
    
    if (canHaveChildren) {
      localItems.value[evt.newIndex] = {
        id: newItem.id,
        widgetType: widgetType,
        direction: newItem.direction || 'column',
        label: widgetType === 'panel' ? '新面板' : '',
        children: [],
        expanded: true,
        span: 24,
        isNew: false
      }
    } else {
      localItems.value[evt.newIndex] = {
        id: newItem.id,
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
        isNew: false
      }
    }
    emitUpdate()
  } else {
    // 非新控件（移动操作），直接触发更新以同步状态
    emitUpdate()
  }
}

const onDragEnd = () => {
  emitUpdate()
}

const emitUpdate = () => {
  const cleanItems = localItems.value.map(({ isNew, ...rest }) => rest)
  emit('update', cleanItems)
}

const updateItem = (id, newVal) => {
  const index = localItems.value.findIndex(item => item.id === id)
  if (index !== -1) {
    localItems.value[index] = newVal
    emitUpdate()
  }
}

const removeItem = (id) => {
  const index = localItems.value.findIndex(item => item.id === id)
  if (index !== -1) {
    localItems.value.splice(index, 1)
    emitUpdate()
  }
}

const addChildToContainer = (parentId, widget) => {
  const parent = localItems.value.find(item => item.id === parentId)
  if (!parent) return
  
  const newChild = {
    id: `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
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
  
  const updatedParent = {
    ...parent,
    children: [...(parent.children || []), newChild]
  }
  
  updateItem(parentId, updatedParent)
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