<template>
  <el-card class="layout-list">
    <template #header>
      <div class="card-header">
        <span>布局列表</span>
        <el-button size="small" @click="emit('create')">新建布局</el-button>
      </div>
    </template>
    
    <el-table :data="layouts" border>
      <el-table-column prop="name" label="布局名称" />
      <el-table-column prop="is_active" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'info'">
            {{ row.is_active ? '生效中' : '未生效' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200">
        <template #default="{ row }">
          <el-button size="small" @click="emit('load', row)">加载</el-button>
          <el-button 
            size="small" 
            type="success" 
            :disabled="row.is_active" 
            @click="emit('activate', row)"
          >
            激活
          </el-button>
          <el-button size="small" type="danger" @click="emit('delete', row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
defineProps({
  layouts: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['load', 'activate', 'delete', 'create'])
</script>

