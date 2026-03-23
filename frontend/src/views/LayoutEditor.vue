<template>
  <div class="layout-editor">
    <div class="header">
      <el-button @click="handleBack">
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
        :selected-parent-index="selectedParentIndex"
        :selected-child-index="selectedChildIndex"
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
import { ArrowLeft } from '@element-plus/icons-vue'
import { useLayoutEditor } from '../composables/useLayoutEditor'

// 导入组件
import WidgetPanel from '../components/layout/WidgetPanel.vue'
import LayoutCanvas from '../components/layout/LayoutCanvas.vue'
import PropsPanel from '../components/layout/PropsPanel.vue'
import LayoutList from '../components/layout/LayoutList.vue'
import PreviewDialog from '../components/layout/PreviewDialog.vue'

// 使用组合式函数
const {
  modelName,
  availableFields,
  layouts,
  layoutItems,
  selectedIndex,
  selectedParentIndex,
  selectedChildIndex,
  selectedItem,
  showPreview,
  onWidgetClick,
  onWidgetDrop,
  updateItems,
  onMoveToContainer,
  onChildDropOut,
  onChildDragStart,
  onChildDragEnd,
  handleSelect,
  removeItem,
  updateSelectedItem,
  loadLayout,
  createNewLayout,
  handleSave,
  activateLayout,
  deleteLayout,
  handleBack
} = useLayoutEditor()
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