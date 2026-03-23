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
            :span="getColSpan(element)"
            class="layout-col"
            :class="{ active: isSelected(index) }"
            @click.stop="emit('select', index)"
          >
            <LayoutWidget
              :item="element"
              :fields="fields"
              :selected="isSelected(index)"
              :selected-child-index="getSelectedChildIndex(index)"
              @update="(newVal) => updateItem(element.id, newVal)"
              @remove="() => removeItem(element.id)"
              @child-add="(widget) => addChildToContainer(element.id, widget)"
              @select="(info) => handleChildSelect(index, info)"
              @move-to-container="(info) => handleMoveToContainer(index, info)"
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
import { useLayoutCanvas } from '../useLayoutCanvas'  // 注意这里的路径

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

const emit = defineEmits([
  'update',
  'select',
  'move-to-container'
])

// 使用组合式函数
const {
  localItems,
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
} = useLayoutCanvas(props, emit)
</script>

<style scoped>
.canvas-panel {
  height: 100%;
  background: #fafafa;
}

.canvas-area {
  min-height: 400px;
  background: #f5f7fa;
  border-radius: 4px;
  padding: 12px;
}

.empty-tip {
  text-align: center;
  color: #909399;
  padding: 60px 0;
  font-size: 14px;
}

.layout-col {
  transition: all 0.3s;
  padding: 4px;
}

.layout-col.active {
  outline: 2px solid #409eff;
  outline-offset: 2px;
}

.ghost {
  opacity: 0.5;
  background: #c8e6ff;
}

.dragging {
  cursor: move;
}
</style>