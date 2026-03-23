<template>
  <!-- 面板类型（容器） -->
  <template v-if="isContainer">
    <div class="panel-widget" :class="{ selected: selected }">
      <div class="panel-header" @click="toggleExpand">
        <el-icon class="panel-header-icon" :class="{ expanded: expanded }">
          <ArrowRight />
        </el-icon>
        <span class="panel-title">{{ containerLabel }}</span>
        <div class="panel-actions" @click.stop>
          <el-button link type="danger" size="small" @click="emit('remove')">
            <el-icon><Close /></el-icon>
          </el-button>
        </div>
      </div>
      
      <div v-if="item.widgetType !== 'panel' || expanded" 
           class="panel-body"
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
                :span="getChildSpan(element)"
                class="panel-child-col"
                :class="{ active: isChildSelected(index) }"
                @click.stop="(event) => onChildClick(event, index, element)"
              >
                <LayoutWidget
                  :item="element"
                  :fields="fields"
                  :selected="isChildSelected(index)"
                  @update="(newVal) => updateChild(index, newVal)"
                  @remove="() => removeChild(index)"
                  @select="(info) => emit('select', { parentIndex: index, child: info })"
                />
              </el-col>
            </template>
            <template #footer>
              <div v-if="children.length === 0" class="panel-empty-tip">
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
            class="panel-row-container"
            @add="onChildAdded"
            @end="onChildDragEnd"
          >
            <template #item="{ element, index }">
              <div 
                class="panel-horizontal-item" 
                :class="{ active: isChildSelected(index) }"
                :style="getChildStyle(element)"
                @click.stop="(event) => onChildClick(event, index, element)"
              >
                <LayoutWidget
                  :item="element"
                  :fields="fields"
                  :selected="isChildSelected(index)"
                  @update="(newVal) => updateChild(index, newVal)"
                  @remove="() => removeChild(index)"
                  @select="(info) => emit('select', { parentIndex: index, child: info })"
                />
              </div>
            </template>
            <template #footer>
              <div v-if="children.length === 0" class="panel-empty-tip">
                拖拽控件到此处
              </div>
            </template>
          </draggable>
        </template>
      </div>
    </div>
  </template>
  
  <!-- 普通控件 - 单行文本 -->
  <template v-else>
    <div 
      class="text-widget" 
      :class="{ selected: selected }"
      @click.stop="emit('select', item)"
    >
      <div class="text-widget-header">
        <span class="text-widget-title">{{ widgetLabel }}</span>
        <el-icon class="text-widget-remove" @click.stop="emit('remove')">
          <Close />
        </el-icon>
      </div>
      <div class="text-widget-content">
        {{ item.label || item.fieldName || '未绑定' }}
      </div>
    </div>
  </template>
</template>

<script setup>
import draggable from 'vuedraggable'
import { useLayoutWidget } from '../useLayoutWidget'
import '../WidgetStyle/FieldWidget.css'
import '../WidgetStyle/PanelWidget.css'

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

const emit = defineEmits(['update', 'remove', 'select'])

const {
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
} = useLayoutWidget(props, emit)
</script>