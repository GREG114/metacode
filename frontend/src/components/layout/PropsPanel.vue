<template>
  <el-card class="props-panel">
    <template #header>控件属性</template>
    
    <div :class="item ? 'props-form' : 'no-selection'">
      <div style="color: green; margin-bottom: 10px;">✅ 选中了: {{ item?.widgetType }} - {{ item?.label || item?.fieldName }}</div>
      <div style="color: #999; font-size: 12px;">JSON: {{ JSON.stringify(item) }}</div>
      <el-form v-if="item" label-width="80px" size="small">
        <!-- 容器通用属性 -->
        <template v-if="isContainer">
          <el-form-item label="容器类型">
            <el-tag>{{ containerTypeLabel }}</el-tag>
          </el-form-item>
          
          <el-form-item v-if="item.widgetType === 'panel'" label="面板标题">
            <el-input v-model="localItem.label" placeholder="输入面板标题" @input="emitUpdate" />
          </el-form-item>
          
          <el-form-item v-if="item.widgetType === 'panel'" label="默认展开">
            <el-switch v-model="localItem.expanded" @change="emitUpdate" />
          </el-form-item>
          
          <el-form-item label="排列方向">
            <el-radio-group v-model="localItem.direction" @update:modelValue="emitUpdate">
              <el-radio-button value="column">纵向</el-radio-button>
              <el-radio-button value="row">横向</el-radio-button>
            </el-radio-group>
          </el-form-item>
          
          <el-divider>栅格设置</el-divider>
          
          <el-form-item label="宽度(列)">
            <el-slider 
              v-model="localItem.span" 
              :min="1" 
              :max="24" 
              :marks="{1:1, 12:12, 24:24}"
              @change="emitUpdate"
            />
          </el-form-item>
        </template>
        
        <!-- 普通控件属性 -->
        <template v-else>
          <el-form-item label="控件标签">
            <el-input v-model="localItem.label" placeholder="如：姓名" @input="emitUpdate" />
          </el-form-item>
          
          <el-form-item label="绑定字段">
            <el-select v-model="localItem.fieldName" placeholder="选择字段" @change="emitUpdate">
              <el-option
                v-for="f in fields"
                :key="f.name"
                :label="f.label || f.name"
                :value="f.name"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="控件类型">
            <el-select v-model="localItem.widgetType" @change="emitUpdate">
              <el-option
                v-for="w in compatibleWidgets"
                :key="w.type"
                :label="w.label"
                :value="w.type"
              />
            </el-select>
          </el-form-item>
          
          <el-form-item label="栅格(列)">
            <el-slider 
              v-model="localItem.span" 
              :min="1" 
              :max="12" 
              :marks="{1:1, 6:6, 12:12}"
              @change="emitUpdate"
            />
          </el-form-item>
          
          <el-divider>基础属性</el-divider>
          
          <el-form-item label="可见">
            <el-switch v-model="localItem.props.visible" @change="emitUpdate" />
          </el-form-item>
          
          <el-form-item label="必填">
            <el-switch v-model="localItem.props.required" @change="emitUpdate" />
          </el-form-item>
          
          <el-form-item label="只读">
            <el-switch v-model="localItem.props.readonly" @change="emitUpdate" />
          </el-form-item>
          
          <el-form-item label="默认值">
            <el-input v-model="localItem.props.default" @input="emitUpdate" />
          </el-form-item>
        </template>
      </el-form>
    </div>
    
    <div v-if="!item" class="no-selection">
      <div style="color: red;">❌ 未选中任何控件</div>
      <div style="color: #999; font-size: 12px;">props.item 是空的</div>
    </div>
  </el-card>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  item: {
    type: Object,
    default: null
  },
  fields: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update'])

const localItem = ref(null)

const containerTypes = {
  panel: '面板（可折叠）',
  container: '容器',
  row: '横向容器',
  column: '纵向容器'
}

const isContainer = computed(() => {
  if (!localItem.value) return false
  return ['panel', 'container', 'row', 'column'].includes(localItem.value.widgetType)
})

const containerTypeLabel = computed(() => {
  if (!localItem.value) return ''
  return containerTypes[localItem.value.widgetType] || ''
})

const widgets = [
  { type: 'text', label: '单行文本', compatibleTypes: ['text', 'textarea'] },
  { type: 'textarea', label: '文本域', compatibleTypes: ['text'] },
  { type: 'number', label: '数字', compatibleTypes: ['integer', 'decimal'] },
  { type: 'date', label: '日期', compatibleTypes: ['date'] },
  { type: 'switch', label: '开关', compatibleTypes: ['boolean'] },
  { type: 'select', label: '下拉选择', compatibleTypes: ['select'] },
]

const compatibleWidgets = computed(() => {
  if (!localItem.value?.fieldName) return widgets
  const field = props.fields.find(f => f.name === localItem.value.fieldName)
  if (!field) return widgets
  return widgets.filter(w => w.compatibleTypes.includes(field.type))
})

watch(() => props.item, (newItem) => {
  console.log('[PropsPanel] item changed:', newItem)
  if (!newItem) {
    localItem.value = null
    return
  }
  
  // 深拷贝，区分容器和普通控件
  if (['panel', 'row', 'column'].includes(newItem.widgetType)) {
    localItem.value = { 
      ...newItem, 
      children: [...(newItem.children || [])] 
    }
  } else {
    localItem.value = { 
      ...newItem, 
      props: { ...newItem.props } 
    }
  }
}, { immediate: true, deep: true })

const emitUpdate = () => {
  emit('update', localItem.value)
}
</script>

<style scoped>
.props-panel {
  height: 450px;
  overflow-y: auto;
}

.props-form {
  padding: 10px;
}

.no-selection {
  text-align: center;
  color: #909399;
  padding: 40px;
}
</style>