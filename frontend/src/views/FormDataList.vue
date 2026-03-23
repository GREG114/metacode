<template>
  <div class="form-data-list">
    <div class="header">
      <el-button @click="$router.back()">
        <el-icon><ArrowLeft /></el-icon>
        返回
      </el-button>
      <h2>{{ modelName }} - 数据列表</h2>
    </div>

    <el-table :data="dataList" v-loading="loading" stripe>
      <el-table-column type="index" label="序号" width="60" />
      <el-table-column
        v-for="field in fields"
        :key="field.name"
        :prop="`data.${field.name}`"
        :label="field.title || field.name"
      />
      <el-table-column prop="submitted_by" label="提交人" width="100" />
      <el-table-column prop="submitted_at" label="提交时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.submitted_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="100">
        <template #default="{ row }">
          <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { modelApi, formDataApi } from '../api'

const route = useRoute()
const router = useRouter()

const modelId = route.params.modelId
const modelName = ref('')
const fields = ref([])
const dataList = ref([])
const loading = ref(false)

const fetchData = async () => {
  loading.value = true
  try {
    const [modelRes, dataRes] = await Promise.all([
      modelApi.get(modelId),
      formDataApi.list(modelId)
    ])
    modelName.value = modelRes.data.name
    fields.value = modelRes.data.schema?.fields || []
    dataList.value = dataRes.data
  } catch (err) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除这条数据吗？', '警告', { type: 'warning' })
    await formDataApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchData()
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

onMounted(fetchData)
</script>

