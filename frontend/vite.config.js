import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

const version = new Date().toISOString().slice(0, 19).replace(/[-T:]/g, '')

export default defineConfig({
  plugins: [
    vue(),
    {
      name: 'inject-version',
      transform(code, id) {
        if (id.includes('LayoutEditor.vue')) {
          return code.replace('const VERSION = __VERSION__', `const VERSION = "${version}"`)
        }
      }
    }
  ],
  server: {
    host: '0.0.0.0',
    port: 5001,
    proxy: {
      '/api': {
        target: 'http://localhost:5002',
        changeOrigin: true
      }
    }
  }
})