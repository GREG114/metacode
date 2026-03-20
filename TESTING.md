# 测试方法论

## 概述
每个开发阶段都需要有验证步骤，测试结果必须包含错误原因并写入日志。

## 测试目录结构
```
TEST/
├── phase1/              # 阶段一测试
│   ├── unit/           # 单元测试
│   ├── integration/    # 集成测试
│   ├── e2e/           # E2E 测试
│   └── performance/    # 性能测试
├── phase2/              # 阶段二测试
├── phase3/              # 阶段三测试
├── logs/                # 测试日志
│   ├── phase1_2026-03-18.json
│   ├── phase2_2026-03-20.json
│   └── phase3_2026-03-25.json
├── reports/             # 测试报告
└── fixtures/            # 测试数据
    ├── models.json
    ├── forms.json
    └── layouts.json
```

## 测试类型

### 1. 单元测试
**范围:** 单个函数、类、组件
**工具:** 
- 后端: Django Test Framework + coverage
- 前端: Vitest + Testing Library
**要求:**
- 每个可测试单元至少有一个测试用例
- 覆盖边界条件和异常情况
- 测试与外部依赖隔离（使用 mock）

### 2. 集成测试
**范围:** 模块间交互、API 调用、数据库操作
**工具:** 
- 后端: Django Test Framework (测试数据库)
- 前端: Vitest + MSW (Mock Service Worker)
**要求:**
- 测试前后端数据流
- 验证 API 响应格式
- 测试数据库读写操作

### 3. E2E 测试
**范围:** 完整的用户操作流程
**工具:** Playwright
**要求:**
- 模拟真实用户操作
- 跨浏览器测试（可选）
- 测试关键业务路径

### 4. 性能测试
**范围:** 关键路径性能指标
**工具:** 
- 后端: Django Test Framework (time metrics)
- 前端: Chrome DevTools + Lighthouse
**要求:**
- 记录响应时间
- 测试并发性能
- 监控内存泄漏

## 日志规范

### 日志文件命名
```
{phase}_{date}_{test_type}.json
示例: phase1_2026-03-18_unit.json
```

### 日志格式
```json
{
  "metadata": {
    "timestamp": "2026-03-18T15:30:00+08:00",
    "phase": "phase1",
    "test_type": "unit",
    "test_suite": "DataModelAPITest",
    "environment": "development"
  },
  "summary": {
    "total_tests": 15,
    "passed": 14,
    "failed": 1,
    "skipped": 0,
    "duration_ms": 2450
  },
  "test_cases": [
    {
      "name": "test_create_model_success",
      "status": "PASS",
      "duration_ms": 120,
      "assertions": 5
    },
    {
      "name": "test_create_model_duplicate_name",
      "status": "FAIL",
      "duration_ms": 85,
      "error": {
        "type": "IntegrityError",
        "message": "duplicate key value violates unique constraint",
        "detail": "Key (name)=(test_model) already exists.",
        "stack_trace": "..."
      },
      "context": {
        "request": {"name": "test_model", "description": "测试"},
        "response": null
      }
    }
  ],
  "recommendations": [
    "增加数据清理步骤",
    "优化数据库索引"
  ]
}
```

### 错误记录要求
1. **错误类型**: 明确分类（验证错误、数据库错误、网络错误等）
2. **错误详情**: 包含具体错误消息和堆栈信息
3. **上下文数据**: 请求参数、系统状态、用户操作
4. **重现步骤**: 如何重现该错误
5. **建议修复**: 可能的解决方案或优化建议

## 测试执行流程

### 开发阶段测试
```bash
# 后端测试
cd /root/.openclaw/workspace/metacode
python manage.py test --verbosity=2

# 前端测试
cd /root/.openclaw/workspace/metacode/frontend
npm run test:unit

# E2E 测试
npm run test:e2e
```

### 持续集成测试
```yaml
# 伪代码示例
test:
  stage: test
  script:
    - python manage.py test --coverage
    - npm run test:unit
    - npm run test:e2e
  artifacts:
    paths:
      - TEST/logs/
      - coverage/
```

### 测试报告生成
1. **覆盖率报告**: HTML 格式，包含代码行覆盖详情
2. **性能报告**: 关键路径性能图表
3. **缺陷报告**: 按优先级和严重程度分类
4. **趋势分析**: 测试通过率趋势图

## 验收标准
- [ ] 单元测试覆盖率 > 80%
- [ ] 集成测试覆盖所有关键路径
- [ ] E2E 测试覆盖核心用户流程
- [ ] 性能测试满足预设指标
- [ ] 所有测试失败都有详细错误日志
- [ ] 测试结果可重现

## 工具配置

### 后端测试配置 (pytest.ini)
```ini
[pytest]
DJANGO_SETTINGS_MODULE = metacode.settings
python_files = test_*.py
addopts = --tb=short --strict-markers
log_cli = true
log_cli_level = INFO
```

### 前端测试配置 (vitest.config.js)
```js
export default {
  test: {
    environment: 'jsdom',
    reporters: ['verbose'],
    coverage: {
      reporter: ['text', 'json', 'html'],
      exclude: ['node_modules/']
    }
  }
}
```

## 常见问题处理
1. **测试数据污染**: 使用事务回滚或测试数据库
2. **测试执行慢**: 并行执行测试，使用缓存
3. **测试不稳定性**: 增加重试机制，隔离外部依赖
4. **日志过大**: 轮转日志，只保留最近N天

## 测试负责人职责
1. 编写和维护测试用例
2. 执行定期测试
3. 分析测试结果和错误日志
4. 提出优化建议
5. 维护测试环境和工具链