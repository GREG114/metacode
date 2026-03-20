<template>
  <div class="layout-editor">
    <div class="header">
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>{{ modelName }} - 布局编辑</h2>
      <el-button type="primary" @click="handleSave">保存布局</el-button>
      <el-button type="success" @click="showPreview = true">预览</el-button>
    </div>

    <div class="editor-container">
      <WidgetPanel @widget-click="onWidgetClick" />
      
      <LayoutCanvas 
        :items="layoutItems"
        :selected-index="selectedIndex"
        :fields="availableFields"
        @drop="onWidgetDrop"
        @select="handleSelect"
        @remove="removeItem"
        @update="updateItems"
        @move-to-container="onMoveToContainer"
        @child-dragstart="(event, info) => onChildDragStart(event, info)"
        @child-dragend="(event, info) => onChildDragEnd(event, info)"
        @child-drop-out="onChildDropOut"
      />
      
      <PropsPanel 
        :item="selectedItem"
        :fields="availableFields"
        @update="updateSelectedItem"
      />
    </div>

    <PreviewDialog v-model="showPreview" :items="layoutItems" />
    
    <LayoutList 
      :layouts="layouts"
      @load="loadLayout"
      @activate="activateLayout"
      @delete="deleteLayout"
      @create="createNewLayout"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { modelApi, layoutApi } from '../api'

import WidgetPanel from '../components/layout/WidgetPanel.vue'
import LayoutCanvas from '../components/layout/LayoutCanvas.vue'
import PropsPanel from '../components/layout/PropsPanel.vue'
import LayoutList from '../components/layout/LayoutList.vue'
import PreviewDialog from '../components/layout/PreviewDialog.vue'

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
      direction: widget.direction || 'column',  // 支持方向属性
      isMain: isFirstContainer,  // 第一个容器标记为 main
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

// 点击控件添加到画布
const onWidgetClick = (widget) => {
  onWidgetDrop(widget)
}

// 将控件移动到容器中
const onMoveToContainer = (info) => {
  const { fromIndex, toContainer, toChildren } = info
  
  // 获取要移动的控件
  const movedItem = layoutItems.value[fromIndex]
  if (!movedItem) return
  
  // 添加到目标容器
  const updatedContainer = {
    ...toContainer,
    children: [...toChildren, movedItem]
  }
  
  // 更新 layoutItems：移除原控件，替换容器
  const newItems = layoutItems.value.filter((_, idx) => idx !== fromIndex)
  const containerIndex = newItems.findIndex(item => item === toContainer || item.widgetType === toContainer.widgetType && item.children === toChildren)
  
  if (containerIndex !== -1) {
    newItems[containerIndex] = updatedContainer
  }
  
  layoutItems.value = newItems
  selectedIndex.value = null
}

// 子控件从容器拖出到画布
const onChildDropOut = (info) => {
  const { fromContainerIndex, childIndex } = info
  
  const container = layoutItems.value[fromContainerIndex]
  if (!container || !container.children) return
  
  // 获取要移动的子控件
  const movedChild = container.children[childIndex]
  if (!movedChild) return
  
  // 从容器中移除
  const newChildren = container.children.filter((_, idx) => idx !== childIndex)
  container.children = newChildren
  
  // 添加到画布末尾
  layoutItems.value = [...layoutItems.value, movedChild]
  
  // 触发更新
  const newItems = [...layoutItems.value]
  newItems[fromContainerIndex] = { ...container }
  layoutItems.value = newItems
}

// 子控件拖拽开始
const onChildDragStart = (event, info) => {
  // 仅记录日志，dataTransfer 在 LayoutWidget 中已设置
}

// 子控件拖拽结束
const onChildDragEnd = (event, info) => {
  // 可以在这里处理拖拽结束后的清理
}

const selectedChildIndex = ref(null)
const selectedParentIndex = ref(null)

const handleSelect = (info) => {
  console.log('[LayoutEditor] handleSelect:', info)
  if (typeof info === 'number') {
    // 顶层选中
    selectedIndex.value = info
    selectedChildIndex.value = null
    selectedParentIndex.value = null
    console.log('[LayoutEditor] top select, index:', info)
  } else if (info && typeof info === 'object' && info.childIndex !== undefined) {
    // 容器内控件选中
    console.log('[LayoutEditor] setting parentIndex:', info.containerIndex, 'childIndex:', info.childIndex)
    selectedParentIndex.value = info.containerIndex
    selectedChildIndex.value = info.childIndex
    selectedIndex.value = null
    console.log('[LayoutEditor] after set, selectedParentIndex:', selectedParentIndex.value, 'selectedChildIndex:', selectedChildIndex.value)
    // 找到对应的 item
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
  // 子控件更新
  if (selectedParentIndex.value !== null && selectedChildIndex.value !== null) {
    const parent = layoutItems.value[selectedParentIndex.value]
    if (parent && parent.children) {
      parent.children[selectedChildIndex.value] = updatedItem
      // 触发响应式更新
      layoutItems.value = [...layoutItems.value]
    }
    return
  }
  // 顶层更新
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

// 兼容转换：把旧的 row/column 转换成新的 container + direction
const convertToNewFormat = (items) => {
  if (!items || !Array.isArray(items)) return items
  
  return items.map(item => {
    const newItem = { ...item }
    
    // 旧的 row -> container(row)
    if (newItem.widgetType === 'row') {
      newItem.widgetType = 'container'
      newItem.direction = 'row'
    }
    // 旧的 column -> container(column)
    else if (newItem.widgetType === 'column') {
      newItem.widgetType = 'container'
      newItem.direction = 'column'
    }
    
    // 递归转换子控件
    if (newItem.children && Array.isArray(newItem.children)) {
      newItem.children = convertToNewFormat(newItem.children)
    }
    
    return newItem
  })
}

// 生成默认布局模板
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
  
  // 兼容三种格式: items(新) / sections(旧) / fields(最旧)
  if (layout.layout?.items && layout.layout.items.length > 0) {
    // 新格式：编辑器直接使用的 items（需转换旧 row/column）
    layoutItems.value = convertToNewFormat(layout.layout.items)
  } else if (layout.layout?.sections && layout.layout.sections.length > 0) {
    // 旧格式：sections 数组
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
    // 最旧格式：只有 fields 数组，转成单面板
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
    // 兜底：使用默认模板
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

onMounted(fetchData)
</script>

<style scoped>
.layout-editor {
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 20px;
}

.header h2 {
  margin: 0;
  flex: 1;
}

.editor-container {
  display: grid;
  grid-template-columns: 180px 1fr 280px;
  gap: 16px;
  margin-bottom: 20px;
  min-height: 450px;
}
</style>