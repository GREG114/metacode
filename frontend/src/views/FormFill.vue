<template>
  <div class="form-fill">
    <div class="header">
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>{{ modelName }} - 填写表单</h2>
      <el-button type="success" @click="$router.push(`/forms/${modelId}/data`)">
        查看数据
      </el-button>
    </div>

    <el-card v-loading="loading">
      <el-alert
        v-if="layoutId"
        :title="`当前布局: ${layoutName}`"
        type="info"
        :closable="false"
        show-icon
        style="margin-bottom: 20px"
      />
      
      <el-form :model="formData" label-width="120px" ref="formRef">
        <el-row :gutter="16">
          <el-col
            v-for="field in orderedFields"
            :key="field.name"
            :span="field.span || 6"
            v-show="field.customReadonly !== true"
          >
            <el-form-item
              :label="field.customLabel || field.title || field.name"
              :required="field.customRequired || field.required"
            >
              <!-- 文本输入 -->
              <el-input
                v-if="field.component === 'el-input' || field.component === undefined"
                v-model="formData[field.name]"
                :disabled="field.customReadonly"
                :placeholder="field.customDefault || `请输入${field.customLabel || field.name}`"
              />
              
              <!-- 文本域 -->
              <el-input
                v-else-if="field.component === 'el-input' && field.type === 'string'"
                v-model="formData[field.name]"
                type="textarea"
                :disabled="field.customReadonly"
                :placeholder="field.customDefault"
              />
              
              <!-- 数字输入 -->
              <el-input-number
                v-else-if="field.component === 'el-input-number'"
                v-model="formData[field.name]"
                :disabled="field.customReadonly"
                :min="field.minimum"
                :max="field.maximum"
                :placeholder="field.customDefault"
              />
              
              <!-- 日期选择 -->
              <el-date-picker
                v-else-if="field.component === 'el-date-picker'"
                v-model="formData[field.name]"
                type="date"
                value-format="YYYY-MM-DD"
                :disabled="field.customReadonly"
              />
              
              <!-- 布尔开关 -->
              <el-switch
                v-else-if="field.component === 'el-switch'"
                v-model="formData[field.name]"
                :disabled="field.customReadonly"
              />
              
              <!-- 下拉选择 -->
              <el-select
                v-else-if="field.component === 'el-select'"
                v-model="formData[field.name]"
                :disabled="field.customReadonly"
                placeholder="请选择"
              >
                <el-option
                  v-for="opt in field.options"
                  :key="opt"
                  :label="opt"
                  :value="opt"
                />
              </el-select>
              
              <!-- 默认 -->
              <el-input
                v-else
                v-model="formData[field.name]"
                :disabled="field.customReadonly"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button type="primary" @click="handleSubmit">提交</el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { modelApi, formDataApi } from '../api'

const route = useRoute()
const router = useRouter()

const modelId = route.params.modelId
const modelName = ref('')
const loading = ref(false)
const fields = ref([])
const formData = ref({})
const formRef = ref(null)
const layoutId = ref(null)
const layoutName = ref('默认')
const layout = ref({})

// 递归提取布局中的所有控件
const extractFieldsFromItems = (items) => {
  const fieldMap = new Map(fields.value.map(f => [f.name, f]))
  const result = []
  
  for (const item of items) {
    // 容器类型：递归处理子控件
    if (['panel', 'row', 'column'].includes(item.widgetType)) {
      if (item.children && item.children.length > 0) {
        result.push(...extractFieldsFromItems(item.children))
      }
      continue
    }
    
    // 普通控件
    if (item.props?.visible === false) continue
    
    const field = fieldMap.get(item.fieldName)
    if (field) {
      result.push({
        ...field,
        span: item.span || 6,
        customLabel: item.label,
        customRequired: item.props?.required,
        customReadonly: item.props?.readonly,
        customDefault: item.props?.default
      })
    }
  }
  
  return result
}

// 根据布局顺序排列字段
const orderedFields = computed(() => {
  const layoutItems = layout.value?.items || []
  if (layoutItems.length === 0) {
    return fields.value.map(f => ({ ...f, span: 6 }))
  }
  
  return extractFieldsFromItems(layoutItems)
})

const fetchForm = async () => {
  loading.value = true
  try {
    const [modelRes, formRes] = await Promise.all([
      modelApi.get(modelId),
      modelApi.getForm(modelId)
    ])
    modelName.value = modelRes.data.name
    
    const schema = formRes.data
    fields.value = Object.entries(schema.properties || {}).map(([name, prop]) => ({
      name,
      ...prop
    }))
    
    layout.value = schema.layout || {}
    layoutId.value = schema.layout_id
    layoutName.value = schema.layout_name
  } catch (err) {
    ElMessage.error('获取表单失败')
    router.push('/models')
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  try {
    await formDataApi.create({
      model: modelId,
      data: formData.value,
      submitted_by: 'admin'
    })
    ElMessage.success('提交成功')
    handleReset()
  } catch (err) {
    ElMessage.error(err.response?.data?.error || '提交失败')
  }
}

const handleReset = () => {
  formData.value = {}
}

onMounted(fetchForm)
</script>

