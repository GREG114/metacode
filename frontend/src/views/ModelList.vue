<template>
  <div class="model-list">
    <div class="header">
      <h2>数据模型</h2>
      <el-button type="primary" @click="$router.push('/models/new')">
        <el-icon><Plus /></el-icon>
        新建模型
      </el-button>
    </div>

    <el-table :data="models" v-loading="loading" stripe>
      <el-table-column prop="name" label="模型名称" width="200" />
      <el-table-column prop="description" label="描述" />
      <el-table-column prop="schema.fields" label="字段数" width="100">
        <template #default="{ row }">
          {{ row.schema?.fields?.length || 0 }}
        </template>
      </el-table-column>
      <el-table-column prop="updated_at" label="更新时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.updated_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="280" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="$router.push(`/models/${row.id}/edit`)">编辑</el-button>
          <el-button size="small" type="success" @click="$router.push(`/forms/${row.id}`)">表单</el-button>
          <el-button size="small" type="warning" @click="$router.push(`/layouts/${row.id}`)">布局</el-button>
          <el-button size="small" type="danger" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { modelApi } from '../api'

const models = ref([])
const loading = ref(false)

const fetchModels = async () => {
  loading.value = true
  try {
    const res = await modelApi.list()
    models.value = res.data
  } catch (err) {
    ElMessage.error('获取模型列表失败')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定删除模型 "${row.name}" 吗？`, '警告', {
      type: 'warning'
    })
    await modelApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchModels()
  } catch (err) {
    if (err !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (date) => {
  if (!date) return '-'
  return new Date(date).toLocaleString('zh-CN')
}

onMounted(fetchModels)
</script>

<style scoped>
.model-list {
  padding: 20px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.header h2 {
  margin: 0;
}
</style>