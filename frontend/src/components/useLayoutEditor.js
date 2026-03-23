// composables/useLayoutEditor.js
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { modelApi, layoutApi } from '../api'

export function useLayoutEditor() {
  const route = useRoute()
  const router = useRouter()
  
  const modelId = route.params.modelId
  const modelName = ref('')
  const availableFields = ref([])
  const layouts = ref([])
  const layoutItems = ref([])
  const selectedIndex = ref(null)
  const currentLayoutId = ref(null)
  const showPreview = ref(false)
  const selectedChildIndex = ref(null)
  const selectedParentIndex = ref(null)
  
  const selectedItem = computed(() => {
    // 子控件选中优先
    if (selectedParentIndex.value !== null && selectedChildIndex.value !== null) {
      const parent = layoutItems.value[selectedParentIndex.value]
      if (parent && parent.children) {
        return parent.children[selectedChildIndex.value]
      }
    }
    // 顶层选中
    if (selectedIndex.value === null) return null
    return layoutItems.value[selectedIndex.value]
  })
  
  const onWidgetDrop = (widget) => {
    // 检查是否是容器 (支持旧的 row/column 和新的 container)
    if (['panel', 'row', 'column', 'container'].includes(widget.widgetType)) {
      // 只有第一个根容器才标记为 main
      const isFirstContainer = layoutItems.value.filter(item => 
        ['panel', 'container', 'row', 'column'].includes(item.widgetType)
      ).length === 0
      
      layoutItems.value.push({
        widgetType: widget.widgetType,
        direction: widget.direction || 'column',
        isMain: isFirstContainer,
        label: widget.widgetType === 'panel' ? '新面板' : '',
        children: [],
        expanded: true,
        span: 24
      })
    } else {
      // 普通控件
      layoutItems.value.push({
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
  
  const updateItems = (newItems) => {
    layoutItems.value = newItems
  }
  
  const onWidgetClick = (widget) => {
    onWidgetDrop(widget)
  }
  
  const onMoveToContainer = (info) => {
    const { fromIndex, toContainer, toChildren } = info
    
    const movedItem = layoutItems.value[fromIndex]
    if (!movedItem) return
    
    const updatedContainer = {
      ...toContainer,
      children: [...toChildren, movedItem]
    }
    
    const newItems = layoutItems.value.filter((_, idx) => idx !== fromIndex)
    const containerIndex = newItems.findIndex(item => item === toContainer || item.widgetType === toContainer.widgetType && item.children === toChildren)
    
    if (containerIndex !== -1) {
      newItems[containerIndex] = updatedContainer
    }
    
    layoutItems.value = newItems
    selectedIndex.value = null
  }
  
  const onChildDropOut = (info) => {
    const { fromContainerIndex, childIndex } = info
    
    const container = layoutItems.value[fromContainerIndex]
    if (!container || !container.children) return
    
    const movedChild = container.children[childIndex]
    if (!movedChild) return
    
    const newChildren = container.children.filter((_, idx) => idx !== childIndex)
    container.children = newChildren
    
    layoutItems.value = [...layoutItems.value, movedChild]
    
    const newItems = [...layoutItems.value]
    newItems[fromContainerIndex] = { ...container }
    layoutItems.value = newItems
  }
  
  const onChildDragStart = (event, info) => {
    // 仅记录日志，dataTransfer 在 LayoutWidget 中已设置
  }
  
  const onChildDragEnd = (event, info) => {
    // 可以在这里处理拖拽结束后的清理
  }
  
  const handleSelect = (info) => {
    console.log('[LayoutEditor] handleSelect:', info)
    if (typeof info === 'number') {
      selectedIndex.value = info
      selectedChildIndex.value = null
      selectedParentIndex.value = null
      console.log('[LayoutEditor] top select, index:', info)
    } else if (info && typeof info === 'object' && info.childIndex !== undefined) {
      console.log('[LayoutEditor] setting parentIndex:', info.containerIndex, 'childIndex:', info.childIndex)
      selectedParentIndex.value = info.containerIndex
      selectedChildIndex.value = info.childIndex
      selectedIndex.value = null
      console.log('[LayoutEditor] after set, selectedParentIndex:', selectedParentIndex.value, 'selectedChildIndex:', selectedChildIndex.value)
      const parentItem = layoutItems.value[info.containerIndex]
      console.log('[LayoutEditor] parentItem:', parentItem)
      if (parentItem && parentItem.children) {
        const childItem = parentItem.children[info.childIndex]
        console.log('[LayoutEditor] childItem:', childItem)
      }
    }
  }
  
  const removeItem = (index) => {
    layoutItems.value.splice(index, 1)
    if (selectedIndex.value === index) {
      selectedIndex.value = null
    }
  }
  
  const updateSelectedItem = (updatedItem) => {
    if (selectedParentIndex.value !== null && selectedChildIndex.value !== null) {
      const parent = layoutItems.value[selectedParentIndex.value]
      if (parent && parent.children) {
        parent.children[selectedChildIndex.value] = updatedItem
        layoutItems.value = [...layoutItems.value]
      }
      return
    }
    if (selectedIndex.value !== null) {
      layoutItems.value[selectedIndex.value] = updatedItem
    }
  }
  
  const fetchData = async () => {
    try {
      const [modelRes, layoutRes] = await Promise.all([
        modelApi.get(modelId),
        layoutApi.list(modelId)
      ])
      modelName.value = modelRes.data.name
      availableFields.value = modelRes.data.schema?.fields || []
      layouts.value = layoutRes.data
      const activeLayout = layouts.value.find(l => l.is_active)
      if (activeLayout) {
        loadLayout(activeLayout)
      }
    } catch (err) {
      ElMessage.error('获取数据失败')
    }
  }
  
  const convertToNewFormat = (items) => {
    if (!items || !Array.isArray(items)) return items
    
    return items.map(item => {
      const newItem = { ...item }
      
      if (newItem.widgetType === 'row') {
        newItem.widgetType = 'container'
        newItem.direction = 'row'
      } else if (newItem.widgetType === 'column') {
        newItem.widgetType = 'container'
        newItem.direction = 'column'
      }
      
      if (newItem.children && Array.isArray(newItem.children)) {
        newItem.children = convertToNewFormat(newItem.children)
      }
      
      return newItem
    })
  }
  
  const generateDefaultLayout = (fields) => {
    if (!fields || fields.length === 0) {
      return [{
        widgetType: 'panel',
        label: '默认面板',
        isMain: true,
        direction: 'column',
        children: [],
        expanded: true,
        span: 24
      }]
    }
    
    return [{
      widgetType: 'panel',
      label: '基本信息',
      isMain: true,
      direction: 'column',
      children: fields.slice(0, 6).map(f => ({
        widgetType: 'field',
        label: f.name,
        fieldName: f.name,
        span: 8,
        props: {
          visible: true,
          required: false,
          readonly: false,
          default: ''
        }
      })),
      expanded: true,
      span: 24
    }]
  }
  
  const loadLayout = (layout) => {
    currentLayoutId.value = layout.id
    
    if (layout.layout?.items && layout.layout.items.length > 0) {
      layoutItems.value = convertToNewFormat(layout.layout.items)
    } else if (layout.layout?.sections && layout.layout.sections.length > 0) {
      layoutItems.value = layout.layout.sections.map(section => ({
        widgetType: 'panel',
        label: section.title || '新面板',
        direction: 'column',
        children: (section.fields || []).map(fieldName => ({
          widgetType: 'field',
          label: fieldName,
          fieldName: fieldName,
          span: 12,
          props: {
            visible: true,
            required: false,
            readonly: false,
            default: ''
          }
        })),
        expanded: true,
        span: 24
      }))
    } else if (layout.layout?.fields && layout.layout.fields.length > 0) {
      layoutItems.value = [{
        widgetType: 'panel',
        label: '字段',
        direction: 'column',
        children: layout.layout.fields.map(fieldName => ({
          widgetType: 'field',
          label: fieldName,
          fieldName: fieldName,
          span: 12,
          props: {
            visible: true,
            required: false,
            readonly: false,
            default: ''
          }
        })),
        expanded: true,
        span: 24
      }]
    } else {
      layoutItems.value = generateDefaultLayout(availableFields.value)
    }
  }
  
  const createNewLayout = async () => {
    try {
      const { value: name } = await ElMessageBox.prompt('请输入布局名称', '新建布局', {
        confirmButtonText: '确定',
        cancelButtonText: '取消'
      })
      if (!name) return
      
      await layoutApi.create({
        model: modelId,
        name,
        layout: { items: [] },
        created_by: 'admin'
      })
      ElMessage.success('创建成功')
      fetchData()
    } catch (err) {
      if (err !== 'cancel') {
        ElMessage.error('创建失败')
      }
    }
  }
  
  const handleSave = async () => {
    if (!currentLayoutId.value) {
      return ElMessage.warning('请先加载一个布局')
    }
    
    try {
      await layoutApi.update(currentLayoutId.value, {
        model: modelId,
        name: layouts.value.find(l => l.id === currentLayoutId.value)?.name,
        layout: {
          items: layoutItems.value
        }
      })
      ElMessage.success('保存成功')
      fetchData()
    } catch (err) {
      ElMessage.error('保存失败')
    }
  }
  
  const activateLayout = async (layout) => {
    try {
      await layoutApi.activate(layout.id)
      ElMessage.success('激活成功')
      fetchData()
    } catch (err) {
      ElMessage.error('激活失败')
    }
  }
  
  const deleteLayout = async (layout) => {
    try {
      await ElMessageBox.confirm(`确定删除布局 "${layout.name}" 吗？`, '警告', { type: 'warning' })
      await layoutApi.delete(layout.id)
      ElMessage.success('删除成功')
      fetchData()
    } catch (err) {
      if (err !== 'cancel') {
        ElMessage.error('删除失败')
      }
    }
  }
  
  const handleBack = () => {
    router.back()
  }
  
  onMounted(fetchData)
  
  return {
    // 响应式数据
    modelId,
    modelName,
    availableFields,
    layouts,
    layoutItems,
    selectedIndex,
    currentLayoutId,
    showPreview,
    selectedChildIndex,
    selectedParentIndex,
    selectedItem,
    
    // 方法
    onWidgetDrop,
    updateItems,
    onWidgetClick,
    onMoveToContainer,
    onChildDropOut,
    onChildDragStart,
    onChildDragEnd,
    handleSelect,
    removeItem,
    updateSelectedItem,
    createNewLayout,
    handleSave,
    activateLayout,
    deleteLayout,
    handleBack
  }
}