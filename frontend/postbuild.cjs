const fs = require('fs')
const path = require('path')

const distHtml = fs.readFileSync('dist/index.html', 'utf-8')
const templatesDir = path.join(__dirname, '..', 'templates')
const targetHtml = path.join(templatesDir, 'index.html')

// 同时复制 assets 目录
const srcAssets = path.join(__dirname, 'dist', 'assets')
const destAssets = path.join(templatesDir, 'assets')

// 清空目标 assets 目录
if (fs.existsSync(destAssets)) {
  fs.rmSync(destAssets, { recursive: true })
}
// 复制新的 assets
fs.cpSync(srcAssets, destAssets, { recursive: true })

// 复制 index.html
fs.writeFileSync(targetHtml, distHtml)

console.log('✓ Synced dist/index.html and assets to templates/')