<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="logo" @click="$router.push('/')">
          <h1>Metacode 低代码平台</h1>
        </div>
        <el-menu
          mode="horizontal"
          :default-active="$route.path"
          router
        >
          <el-menu-item index="/models">数据模型</el-menu-item>
        </el-menu>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
</script>

