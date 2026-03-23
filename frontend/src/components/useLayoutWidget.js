// frontend/src/components/useLayoutWidget.js
import { ref, computed, watch, toRaw } from 'vue'

export function useLayoutWidget(props, emit) {
  const expanded = ref(true)

  // 生成唯一ID
  const generateId = () => {
    return `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
  }

  // 判断是否为容器
  const isContainer = computed(() => {
    return ['panel', 'container'].includes(props.item.widgetType)
  })

  // 获取容器标签
  const containerLabel = computed(() => {
    if (props.item.widgetType === 'panel') {
      return props.item.label || '面板'
    }
    if (props.item.widgetType === 'container') {
      return props.item.direction === 'row' ? '横向容器' : '纵向容器'
    }
    return ''
  })

  // 获取容器方向
  const containerDirection = computed(() => {
    return props.item.direction || 'column'
  })

  // 获取子控件列表
  const children = computed(() => props.item.children || [])

  // 本地子控件列表
  const localChildren = ref([])

  // 控件标签映射
  const widgetLabels = {
    text: '单行文本',
    textarea: '文本域',
    number: '数字',
    date: '日期',
    switch: '开关',
    select: '下拉选择'
  }

  // 获取控件标签
  const widgetLabel = computed(() => {
    return widgetLabels[props.item.widgetType] || props.item.widgetType
  })

  // 同步子控件
  watch(() => props.item.children, (newChildren) => {
    localChildren.value = (newChildren || []).map(child => ({
      ...child,
      id: child.id || generateId()
    }))
  }, { immediate: true, deep: true })

  // 触发子控件更新
  const emitChildUpdate = () => {
    const cleanChildren = localChildren.value.map(({ isNew, ...rest }) => rest)
    emit('update', { ...toRaw(props.item), children: cleanChildren })
  }

  // 处理新添加的子控件
  const processNewChild = (newItem) => {
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
  }

  // 子控件添加完成
  const onChildAdded = (evt) => {
    const newItem = localChildren.value[evt.newIndex]
    
    if (newItem && newItem.isNew) {
      localChildren.value[evt.newIndex] = processNewChild(newItem)
      emitChildUpdate()
    } else {
      emitChildUpdate()
    }
  }

  // 子控件拖拽结束
  const onChildDragEnd = () => {
    emitChildUpdate()
  }

  // 切换面板展开/收起
  const toggleExpand = () => {
    if (props.item.widgetType === 'panel') {
      expanded.value = !expanded.value
      emit('update', { ...props.item, expanded: expanded.value })
    }
  }

  // 子控件点击
  const onChildClick = (event, index, child) => {
    event.stopPropagation()
    emit('select', { parentIndex: index, child: child })
  }

  // 更新子控件
  const updateChild = (index, newVal) => {
    const newChildren = [...children.value]
    newChildren[index] = newVal
    emit('update', { ...props.item, children: newChildren })
  }

  // 删除子控件
  const removeChild = (index) => {
    const newChildren = children.value.filter((_, i) => i !== index)
    emit('update', { ...props.item, children: newChildren })
  }

  // 判断子控件是否选中
  const isChildSelected = (index) => {
    return props.selectedChildIndex === index
  }

  // 获取子控件样式（用于横向布局）
  const getChildStyle = (element) => {
    if (containerDirection.value === 'row') {
      return {
        flex: element.span ? `0 0 ${(element.span / 24) * 100}%` : '1',
        minWidth: '0'
      }
    }
    return {}
  }

  // 获取子控件栅格宽度（用于纵向布局）
  const getChildSpan = (element) => {
    return element.span || 6
  }

  return {
    expanded,
    isContainer,
    containerLabel,
    containerDirection,
    children,
    localChildren,
    widgetLabel,
    onChildAdded,
    onChildDragEnd,
    toggleExpand,
    onChildClick,
    updateChild,
    removeChild,
    isChildSelected,
    getChildStyle,
    getChildSpan
  }
}