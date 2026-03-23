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
      >
        <!-- 纵向布局 -->
        <template v-if="containerDirection === 'column'">
          <draggable
            v-model="localChildren"
            item-key="id"
            ghost-class="ghost"
            :animation="200"
            :group="{ name: 'layout', pull: true, put: true }"
            @add="onChildAdded"
            @end="onChildDragEnd"
          >
            <template #item="{ element, index }">
              <el-col
                :span="element.span || 6"
                class="child-col"
                :class="{ active: selectedChildIndex === index }"
                :data-idx="index"
                :data-sci="selectedChildIndex"
                :data-issel="selected"
                @click.stop="(event) => onChildClick(event, index, element)"
              >
                <LayoutWidget
                  :item="element"
                  :fields="fields"
                  :selected="selectedChildIndex === index"
                  @update="(newVal) => updateChild(index, newVal)"
                  @remove="removeChild(index)"
                  @select="(info) => emit('select', { parentIndex: index, child: info })"
                  @child-dragstart="(info) => emit('child-dragstart', { ...info })"
                  @child-dragend="(info) => emit('child-dragend', info)"
                  @child-drop-out="(info) => emit('child-drop-out', { ...info })"
                />
              </el-col>
            </template>
            <template #footer>
              <div v-if="children.length === 0" class="empty-tip">
                拖拽控件到此处
              </div>
            </template>
          </draggable>
        </template>

        <!-- 横向布局 -->
        <template v-else>
          <draggable
            v-model="localChildren"
            item-key="id"
            ghost-class="ghost"
            :animation="200"
            :group="{ name: 'layout', pull: true, put: true }"
            class="row-container"
            @add="onChildAdded"
            @end="onChildDragEnd"
          >
            <template #item="{ element, index }">
              <div 
                class="horizontal-item" 
                :class="{ active: selectedChildIndex === index }"
                :style="{ flex: element.span ? `0 0 ${(element.span/24)*100}%` : '1', minWidth: '0' }"
                @click.stop="(event) => onChildClick(event, index, element)"
              >
                <LayoutWidget
                  :item="element"
                  :fields="fields"
                  :selected="selectedChildIndex === index"
                  @update="(newVal) => updateChild(index, newVal)"
                  @remove="removeChild(index)"
                  @select="(info) => emit('select', { parentIndex: index, child: info })"
                  @child-dragstart="(info) => emit('child-dragstart', { ...info })"
                  @child-dragend="(info) => emit('child-dragend', info)"
                  @child-drop-out="(info) => emit('child-drop-out', { ...info })"
                />
              </div>
            </template>
            <template #footer>
              <div v-if="children.length === 0" class="empty-tip">
                拖拽控件到此处
              </div>
            </template>
          </draggable>
        </template>
      </div>
    </template>
    
    <!-- 普通控件 -->
    <template v-else>
      <div class="widget-body" @click.stop="emit('select', item)">
        <div class="widget-header">
          <span>{{ widgetLabel }}</span>
          <el-icon @click.stop="emit('remove')"><Close /></el-icon>
        </div>
        <div class="widget-content">
          {{ item.label || item.fieldName || '未绑定' }}
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { ref, computed, watch, toRaw } from 'vue'
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
  },
  selectedChildIndex: {
    type: Number,
    default: null
  }
})

const emit = defineEmits(['update', 'remove', 'child-add', 'dragenter', 'select', 'move-to-container', 'child-dragstart', 'child-dragend', 'child-drop-out'])

const expanded = ref(true)

// 调试用
const isChildActive = computed(() => {
  console.log('[LayoutWidget]', props.item?.widgetType, 'selectedChildIndex:', props.selectedChildIndex)
  return props.selectedChildIndex !== null && props.selectedChildIndex !== undefined
})

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

const localChildren = ref([])

// 同步 children，不再添加 __index__ 等元数据
watch(() => props.item.children, (newChildren) => {
  localChildren.value = (newChildren || []).map(child => ({
    ...child,
    id: child.id || `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }))
}, { immediate: true, deep: true })

const onChildAdded = (evt) => {
  const newItem = localChildren.value[evt.newIndex]
  
  if (newItem && newItem.isNew) {
    const widgetType = newItem.type || newItem.widgetType
    const canHaveChildren = newItem.isContainer
    
    if (canHaveChildren) {
      localChildren.value[evt.newIndex] = {
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
      localChildren.value[evt.newIndex] = {
        id: newItem.id,
        widgetType: widgetType,
        label: newItem.label || '',
        fieldName: '',
        span: 12,
        props: {
          visible: true,
          required: false,
          readonly: false,
          default: ''
        },
        isNew: false
      }
    }
    emitChildUpdate()
  } else {
    emitChildUpdate()
  }
}

const onChildDragEnd = () => {
  emitChildUpdate()
}

const emitChildUpdate = () => {
  const cleanChildren = localChildren.value.map(({ isNew, ...rest }) => rest)
  emit('update', { ...toRaw(props.item), children: cleanChildren })
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

const onChildClick = (event, idx, child) => {
  event.stopPropagation()
  emit('select', { parentIndex: idx, child: child })
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

