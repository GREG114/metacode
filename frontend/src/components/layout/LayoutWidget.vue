<template>
  <div class="layout-widget" :class="{ 
    'is-container': isContainer, 
    'is-panel': item.widgetType === 'panel',
    'is-selected': selected
  }">
    <!-- 容器类型 -->
    <template v-if="isContainer">
      <div class="container-header" @click.stop="toggleExpand">
        <el-icon v-if="item.widgetType === 'panel'">
          <ArrowDown v-if="expanded" />
          <ArrowRight v-else />
        </el-icon>
        <span class="container-title">{{ containerLabel }}</span>
        <div class="container-actions" @click.stop>
          <el-button link type="danger" size="small" @click="emit('remove')">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </div>
      
      <div v-if="item.widgetType !== 'panel' || expanded" 
           class="container-body"
           :class="{ 'row': containerDirection === 'row', 'column': containerDirection === 'column' }"
           @dragover.prevent
           @drop.stop="onContainerDrop"
      >
        <!-- 纵向布局 -->
        <template v-if="containerDirection === 'column'">
          <div v-if="children.length === 0" class="empty-tip" @dragover.prevent @drop.stop="onContainerDrop">
            拖拽控件到此处
          </div>
          <draggable
            v-else
            v-model="localChildren"
            item-key="__index__"
            ghost-class="ghost"
            :animation="200"
            group="layout"
            @end="onChildDragEnd"
          >
            <template #item="{ element, index }">
              <el-col
                :span="element.span || 6"
                class="child-col"
                @click.stop="(event) => onChildClick(event, index, element)"
              >
                <LayoutWidget
                  :item="element"
                  :fields="fields"
                  :selected="false"
                  @update="(newVal) => updateChild(index, newVal)"
                  @remove="removeChild(index)"
                  @select="(info) => emit('select', { parentIndex: index, child: info })"
                  @child-dragstart="(info) => emit('child-dragstart', { ...info, containerIndex: props.item.__parentIndex__ })"
                  @child-dragend="(info) => emit('child-dragend', info)"
                  @child-drop-out="(info) => emit('child-drop-out', { ...info, fromContainerIndex: props.item.__parentIndex__ })"
                />
              </el-col>
            </template>
          </draggable>
        </template>

        <!-- 横向布局 -->
        <template v-else>
          <div v-if="children.length === 0" class="empty-tip" @dragover.prevent @drop.stop="onContainerDrop">
            拖拽控件到此处
          </div>
          <draggable
            v-else
            v-model="localChildren"
            item-key="__index__"
            ghost-class="ghost"
            :animation="200"
            group="layout"
            class="horizontal-drag"
            @end="onChildDragEnd"
          >
            <template #item="{ element, index }">
              <div class="horizontal-item" @click.stop="(event) => onChildClick(event, index, element)">
                <LayoutWidget
                  :item="element"
                  :fields="fields"
                  :selected="false"
                  @update="(newVal) => updateChild(index, newVal)"
                  @remove="removeChild(index)"
                  @select="(info) => emit('select', { parentIndex: index, child: info })"
                  @child-dragstart="(info) => emit('child-dragstart', { ...info, containerIndex: props.item.__parentIndex__ })"
                  @child-dragend="(info) => emit('child-dragend', info)"
                  @child-drop-out="(info) => emit('child-drop-out', { ...info, fromContainerIndex: props.item.__parentIndex__ })"
                />
              </div>
            </template>
          </draggable>
        </template>
      </div>
    </template>
    
    <!-- 普通控件 -->
    <template v-else>
      <div class="widget-header">
        <span>{{ widgetLabel }}</span>
        <el-icon @click.stop="emit('remove')"><Close /></el-icon>
      </div>
      <div class="widget-content">
        {{ item.label || item.fieldName || '未绑定' }}
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import draggable from 'vuedraggable'

const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  fields: {
    type: Array,
    default: () => []
  },
  selected: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update', 'remove', 'child-add', 'dragenter', 'select', 'move-to-container', 'child-dragstart', 'child-dragend', 'child-drop-out'])

const expanded = ref(true)

const isContainer = computed(() => {
  return ['panel', 'container'].includes(props.item.widgetType)
})

const containerLabel = computed(() => {
  if (props.item.widgetType === 'panel') {
    return props.item.label || '面板'
  }
  if (props.item.widgetType === 'container') {
    return props.item.direction === 'row' ? '横向容器' : '纵向容器'
  }
  return ''
})

const containerDirection = computed(() => {
  return props.item.direction || 'column'
})

const children = computed(() => props.item.children || [])

// vuedraggable 用的带索引的 children
const localChildren = computed({
  get: () => children.value.map((child, idx) => ({ ...child, __index__: idx, __parentIndex__: props.item.__selfIndex__ })),
  set: (val) => {
    const newChildren = val.map(item => {
      const { __index__, __parentIndex__, ...rest } = item
      return rest
    })
    emit('update', { ...props.item, children: newChildren })
  }
})

const onChildDragEnd = (evt) => {
  console.log('[LayoutWidget] child drag end:', evt)
}

const widgetLabels = {
  text: '单行文本',
  textarea: '文本域',
  number: '数字',
  date: '日期',
  switch: '开关',
  select: '下拉选择'
}

const widgetLabel = computed(() => {
  return widgetLabels[props.item.widgetType] || props.item.widgetType
})

const toggleExpand = () => {
  if (props.item.widgetType === 'panel') {
    expanded.value = !expanded.value
    emit('update', { ...props.item, expanded: expanded.value })
  }
}

// 子控件拖拽开始
const onChildDragStart = (event, idx, child) => {
  event.dataTransfer.setData('drag-source', 'child')
  event.dataTransfer.setData('child-index', idx)
  emit('child-dragstart', { 
    index: idx, 
    child: child,
    parentItem: props.item
  })
}

const onContainerDrop = (event) => {
  const widgetData = event.dataTransfer.getData('widget')
  const itemIndex = event.dataTransfer.getData('item-index')
  const dragSource = event.dataTransfer.getData('drag-source')
  const currentChildren = props.item.children || []
  
  // 从画布拖拽已有控件到容器
  if (itemIndex !== null && dragSource === 'canvas') {
    // 需要通知父组件处理控件移动
    emit('move-to-container', {
      fromIndex: parseInt(itemIndex),
      toContainer: props.item,
      toChildren: currentChildren
    })
    return
  }
  
  if (!widgetData) return
  
  const widget = JSON.parse(widgetData)
  
  // 允许容器嵌套
  if (widget.isContainer) {
    const newChild = {
      widgetType: widget.type,
      direction: widget.direction || 'column',  // 新格式：使用 direction 属性
      label: widget.type === 'panel' ? '新面板' : '',
      children: [],
      expanded: true,
      span: 24
    }
    const newChildren = [...currentChildren, newChild]
    emit('update', { ...props.item, children: newChildren })
    return
  }
  
  // 添加普通控件
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
  
  const newChildren = [...(props.item.children || []), newChild]
  emit('update', { ...props.item, children: newChildren })
}

const onChildClick = (event, idx, child) => {
  event.stopPropagation()
  console.log('[LayoutWidget] onChildClick:', idx, child)
  emit('select', { parentIndex: idx, child: child })
}

const testClick = (idx) => {
  console.log('[LayoutWidget] testClick:', idx)
}

const updateChild = (index, newVal) => {
  const newChildren = [...children.value]
  newChildren[index] = newVal
  emit('update', { ...props.item, children: newChildren })
}

const removeChild = (index) => {
  const newChildren = children.value.filter((_, i) => i !== index)
  emit('update', { ...props.item, children: newChildren })
}
</script>

<style scoped>
.layout-widget {
  background: #ecf5ff;
  border: 2px solid transparent;
  border-radius: 4px;
  padding: 12px;
  cursor: pointer;
  transition: all 0.2s;
}

.layout-widget:hover {
  border-color: #409eff;
}

.layout-widget.is-selected {
  border-color: #409eff;
}

/* 容器样式 */
.layout-widget.is-container {
  background: #f0f9eb;
  border-color: #e1f3d8;
}

.layout-widget.is-panel {
  background: #fdf6ec;
  border-color: #faecd8;
}

.container-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 8px;
  border-bottom: 1px dashed #dcdfe6;
  margin-bottom: 8px;
  cursor: pointer;
}

.container-title {
  flex: 1;
  font-weight: 500;
}

.container-body {
  min-height: 60px;
}

.container-body.row {
  display: flex;
  gap: 16px;
}

.container-body.row .el-col {
  flex: 1;
}

.container-body.column {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.empty-tip {
  text-align: center;
  color: #909399;
  padding: 20px;
  font-size: 12px;
}

.child-col {
  cursor: pointer;
  pointer-events: auto;
}

.child-col:hover {
  opacity: 0.8;
}

/* 普通控件样式 */
.widget-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
  font-weight: 500;
}

.widget-content {
  color: #606266;
  font-size: 14px;
}
</style>