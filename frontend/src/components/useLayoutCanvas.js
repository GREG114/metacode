// composables/useLayoutCanvas.js
import { ref, watch } from 'vue'

export function useLayoutCanvas(props, emit) {
  const localItems = ref([])

  // 生成唯一ID
  const generateId = () => {
    return `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  // 同步 props.items 到 localItems，确保 id 存在
  watch(() => props.items, (newItems) => {
    localItems.value = (newItems || []).map(item => ({
      ...item,
      id: item.id || generateId()
    }))
  }, { immediate: true, deep: true })

  // 触发更新事件
  const emitUpdate = () => {
    const cleanItems = localItems.value.map(({ isNew, ...rest }) => rest)
    emit('update', cleanItems)
  }

  // 处理新添加的控件
  const processNewItem = (newItem) => {
    const widgetType = newItem.type || newItem.widgetType
    const canHaveChildren = newItem.isContainer
    
    if (canHaveChildren) {
      return {
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
      return {
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
  }

  // 拖拽添加完成
  const onItemAdded = (evt) => {
    const newItem = localItems.value[evt.newIndex]
    
    // 检查是否是从左侧面板拖拽来的新控件
    if (newItem && newItem.isNew) {
      localItems.value[evt.newIndex] = processNewItem(newItem)
      emitUpdate()
    } else {
      // 内部移动，只更新数据
      emitUpdate()
    }
  }

  // 拖拽结束
  const onDragEnd = () => {
    emitUpdate()
  }

  // 更新单个控件
  const updateItem = (id, newVal) => {
    const index = localItems.value.findIndex(item => item.id === id)
    if (index !== -1) {
      localItems.value[index] = newVal
      emitUpdate()
    }
  }

  // 删除控件
  const removeItem = (id) => {
    const index = localItems.value.findIndex(item => item.id === id)
    if (index !== -1) {
      localItems.value.splice(index, 1)
      emitUpdate()
    }
  }

  // 添加子控件到容器
  const addChildToContainer = (parentId, widget) => {
    const parent = localItems.value.find(item => item.id === parentId)
    if (!parent) return
    
    const newChild = {
      id: generateId(),
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

  // 获取控件样式
  const getColSpan = (element) => {
    return element.span || (element.widgetType === 'panel' ? 24 : 6)
  }

  // 判断是否选中
  const isSelected = (index) => {
    return props.selectedIndex === index
  }

  // 获取子控件选中索引
  const getSelectedChildIndex = (index) => {
    return props.selectedParentIndex === index ? props.selectedChildIndex : null
  }

  // 处理子控件选择
  const handleChildSelect = (index, info) => {
    emit('select', { 
      containerIndex: index, 
      childIndex: info.parentIndex, 
      child: info.child 
    })
  }

  // 处理移动到容器
  const handleMoveToContainer = (fromIndex, info) => {
    emit('move-to-container', { fromIndex, ...info })
  }

  return {
    localItems,
    generateId,
    onItemAdded,
    onDragEnd,
    updateItem,
    removeItem,
    addChildToContainer,
    getColSpan,
    isSelected,
    getSelectedChildIndex,
    handleChildSelect,
    handleMoveToContainer
  }
}