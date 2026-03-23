<template>
  <div class="layout-editor">
    <div class="header">
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>{{ modelName }} - 布局编辑</h2>
      <span class="version">v{{ VERSION }}</span>
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
        @child-dragstart="onChildDragStart"
        @child-dragend="onChildDragEnd"
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
import WidgetPanel from '../components/layout/WidgetPanel.vue'
import LayoutCanvas from '../components/layout/LayoutCanvas.vue'
import PropsPanel from '../components/layout/PropsPanel.vue'
import LayoutList from '../components/layout/LayoutList.vue'
import PreviewDialog from '../components/layout/PreviewDialog.vue'

import { useLayoutEditor } from '../composables/useLayoutEditor'

const VERSION = __VERSION__

const {
  modelName,
  availableFields,
  layouts,
  layoutItems,
  selectedIndex,
  currentLayoutId,
  showPreview,
  selectedItem,
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
  loadLayout,
  createNewLayout,
  handleSave,
  activateLayout,
  deleteLayout
} = useLayoutEditor()
</script>

