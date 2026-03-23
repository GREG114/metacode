<template>
  <div class="model-edit">
    <div class="header">
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>{{ isEdit ? '编辑模型' : '新建模型' }}</h2>
      <el-button type="primary" @click="handleSave">保存</el-button>
    </div>

    <el-card>
      <el-form :model="form" label-width="100px">
        <el-form-item label="模型名称">
          <el-input v-model="form.name" placeholder="请输入模型名称" />
        </el-form-item>
        <el-form-item label="模型描述">
          <el-input v-model="form.description" type="textarea" rows="2" placeholder="请输入模型描述" />
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="fields-card">
      <template #header>
        <div class="card-header">
          <span>字段列表</span>
          <el-button type="primary" size="small" @click="addField">
            <el-icon><Plus /></el-icon>
            添加字段
          </el-button>
        </div>
      </template>

      <el-table :data="form.schema.fields" border>
        <el-table-column label="字段名" width="150">
          <template #default="{ row, $index }">
            <el-input v-model="row.name" placeholder="字段名" size="small" />
          </template>
        </el-table-column>
        <el-table-column label="显示名称" width="150">
          <template #default="{ row }">
            <el-input v-model="row.label" placeholder="显示名称" size="small" />
          </template>
        </el-table-column>
        <el-table-column label="类型" width="150">
          <template #default="{ row }">
            <el-select v-model="row.type" size="small">
              <el-option label="文本" value="text" />
              <el-option label="整数" value="integer" />
              <el-option label="小数" value="decimal" />
              <el-option label="日期" value="date" />
              <el-option label="布尔" value="boolean" />
              <el-option label="下拉选择" value="select" />
              <el-option label="文本域" value="textarea" />
            </el-select>
          </template>
        </el-table-column>
        <el-table-column label="选项" width="150">
          <template #default="{ row }">
            <el-input 
              v-if="row.type === 'select'" 
              v-model="row.options" 
              placeholder="选项用逗号分隔" 
              size="small" 
            />
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column label="必填" width="80">
          <template #default="{ row }">
            <el-checkbox v-model="row.required" size="small" />
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ $index }">
            <el-button type="danger" size="small" @click="removeField($index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { modelApi } from '../api'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)

const form = ref({
  name: '',
  description: '',
  schema: {
    fields: []
  }
})

const addField = () => {
  form.value.schema.fields.push({
    name: '',
    label: '',
    type: 'text',
    required: false,
    options: ''
  })
}

const removeField = (index) => {
  form.value.schema.fields.splice(index, 1)
}

const handleSave = async () => {
  if (!form.value.name) {
    return ElMessage.warning('请输入模型名称')
  }
  
  // 处理字段选项
  const fields = form.value.schema.fields.map(f => ({
    ...f,
    options: f.type === 'select' ? f.options : undefined
  })).filter(f => f.name)

  const data = {
    ...form.value,
    schema: { fields }
  }

  try {
    if (isEdit.value) {
      await modelApi.update(route.params.id, data)
      ElMessage.success('更新成功')
    } else {
      await modelApi.create(data)
      ElMessage.success('创建成功')
    }
    router.push('/models')
  } catch (err) {
    ElMessage.error(err.response?.data?.error || '保存失败')
  }
}

const fetchData = async () => {
  if (!isEdit.value) return
  
  try {
    const res = await modelApi.get(route.params.id)
    form.value = res.data
  } catch (err) {
    ElMessage.error('获取模型失败')
    router.push('/models')
  }
}

onMounted(fetchData)
</script>

