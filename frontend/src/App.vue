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

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  height: 100vh;
}
.el-header {
  display: flex;
  align-items: center;
  padding: 0 20px;
  background: #fff;
  border-bottom: 1px solid #e6e6e6;
}
.logo {
  cursor: pointer;
  margin-right: 40px;
}
.logo h1 {
  margin: 0;
  font-size: 20px;
  color: #409eff;
}
.el-menu {
  border-bottom: none !important;
}
.el-main {
  background: #f5f7fa;
  min-height: calc(100vh - 60px);
}
</style>