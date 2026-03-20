<template>
  <el-dialog v-model="visible" title="表单预览" width="600px">
    <div class="preview-form">
      <el-form label-width="100px">
        <el-row :gutter="16">
          <el-col
            v-for="item in items"
            :key="item.fieldName"
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
                v-else
                :disabled="item.props?.readonly"
              />
            </el-form-item>
          </el-col>
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
</script>

<style scoped>
.preview-form {
  padding: 20px;
}
</style>