<template>
  <el-dialog v-model="visible" title="表单预览" width="600px">
    <div class="preview-form">
      <el-form label-width="100px">
        <el-row :gutter="16">
        <template v-for="item in flatItems" :key="item.key">
          <el-col
            :span="item.span || 6"
            v-show="item.props?.visible !== false"
          >
            <el-form-item
              :label="item.label || item.fieldName || '未命名'"
              :required="item.props?.required"
            >
              <el-input
                v-if="item.widgetType === 'text'"
                :disabled="item.props?.readonly"
                :placeholder="item.props?.default"
              />
              <el-input-number
                v-else-if="item.widgetType === 'number'"
                :disabled="item.props?.readonly"
              />
              <el-date-picker
                v-else-if="item.widgetType === 'date'"
                :disabled="item.props?.readonly"
                type="date"
              />
              <el-switch
                v-else-if="item.widgetType === 'switch'"
                :disabled="item.props?.readonly"
              />
              <el-select
                v-else-if="item.widgetType === 'select'"
                :disabled="item.props?.readonly"
                placeholder="请选择"
              >
                <el-option label="选项1" value="1" />
                <el-option label="选项2" value="2" />
              </el-select>
              <el-input
                v-else-if="item.widgetType === 'field'"
                :disabled="item.props?.readonly"
                :placeholder="item.props?.default"
              />
              <el-input
                v-else
                :disabled="item.props?.readonly"
              />
            </el-form-item>
          </el-col>
        </template>
        </el-row>
      </el-form>
    </div>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: Boolean,
  items: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['update:modelValue'])

const visible = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

// 展平嵌套结构：处理 panel/row/column 及其 children
const flatItems = computed(() => {
  const result = []
  const flatten = (items, prefix = '') => {
    for (const item of items) {
      // 跳过容器类型，只渲染实际控件
      if (['panel', 'row', 'column', 'container'].includes(item.widgetType)) {
        if (item.children && item.children.length > 0) {
          flatten(item.children, prefix)
        }
        continue
      }
      // 添加 key 避免冲突
      result.push({
        ...item,
        key: prefix + item.fieldName || item.label || Math.random().toString(36).slice(2)
      })
    }
  }
  flatten(props.items || [])
  return result
})
</script>

<style scoped>
.preview-form {
  padding: 20px;
}
</style>