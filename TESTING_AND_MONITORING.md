# Context Engineering v5.0 - 测试和监控

> **用途**: 验证智能加载系统的准确性和性能

---

## 🎯 测试目标

### 核心指标

| 指标 | 目标 | 当前 | 状态 |
|------|------|------|------|
| **任务识别准确率** | >90% | 待测试 | ⏳ |
| **平均 Context 使用** | <50KB | 预估 35KB | ✅ |
| **Free Context 比例** | >60% | 预估 82% | ✅ |
| **文档查找时间** | <2秒 | 预估 <1秒 | ✅ |

---

## 🧪 测试用例

### 测试 1: 浏览器自动化

**输入**:
```
"帮我写一个 Playwright 脚本，打开 Google 并搜索"
```

**预期识别**: `browser-automation`

**预期加载**:
- CLAUDE.md (7.7KB)
- rules/core/work-mode.md (5KB)
- rules/core/blocking-rules.md (5KB)
- rules/domain/coding.md (5KB)
- capabilities/browser-automation/decision-tree.md (8KB)

**预期 Context**: ~31KB (16%)

**测试结果**: ⏳ 待测试

---

### 测试 2: 视频创作

**输入**:
```
"做一个30秒的产品介绍视频，科技风格"
```

**预期识别**: `video-creation`

**预期加载**:
- CLAUDE.md (7.7KB)
- rules/core/work-mode.md (5KB)
- rules/core/blocking-rules.md (5KB)
- rules/domain/coding.md (5KB)
- rules/remotion-auto-production.md (12KB)
- capabilities/PROCESSING_SKILL.md (8KB)

**预期 Context**: ~47KB (24%)

**测试结果**: ⏳ 待测试

---

### 测试 3: 数据分析

**输入**:
```
"查询最近7天的用户增长数据，生成图表"
```

**预期识别**: `data-analysis`

**预期加载**:
- CLAUDE.md (7.7KB)
- rules/core/work-mode.md (5KB)
- rules/core/blocking-rules.md (5KB)
- rules/domain/coding.md (5KB)
- capabilities/data-analysis-guide.md (10KB)
- capabilities/sql-patterns.md (8KB)

**预期 Context**: ~46KB (23%)

**测试结果**: ⏳ 待测试

---

### 测试 4: UI 设计

**输入**:
```
"设计一个登录页面，现代简约风格"
```

**预期识别**: `ui-design`

**预期加载**:
- CLAUDE.md (7.7KB)
- rules/core/work-mode.md (5KB)
- design/DESIGN_MASTER_PERSONA.md (15KB)
- design/UI_DESIGN_STYLES_REFERENCE.md (20KB)

**预期 Context**: ~48KB (24%)

**测试结果**: ⏳ 待测试

---

### 测试 5: 营销内容

**输入**:
```
"写一篇 SEO 优化的博客文章，关于 AI 工具"
```

**预期识别**: `marketing`

**预期加载**:
- CLAUDE.md (7.7KB)
- rules/core/work-mode.md (5KB)
- vibe-marketing/VIBE_MARKETING_GUIDE.md (20KB)
- capabilities/MARKETING_SKILLS_GUIDE.md (15KB)

**预期 Context**: ~48KB (24%)

**测试结果**: ⏳ 待测试

---

### 测试 6: 代码开发

**输入**:
```
"实现一个用户认证系统，包含登录和注册"
```

**预期识别**: `coding`

**预期加载**:
- CLAUDE.md (7.7KB)
- rules/core/work-mode.md (5KB)
- rules/core/blocking-rules.md (5KB)
- rules/domain/coding.md (5KB)
- rules/domain/testing.md (5KB)
- rules/domain/git.md (5KB)

**预期 Context**: ~37KB (19%)

**测试结果**: ⏳ 待测试

---

### 测试 7: 错误调试

**输入**:
```
"我的代码有个 bug，异步操作很慢"
```

**预期识别**: `debugging`

**预期加载**:
- CLAUDE.md (7.7KB)
- rules/core/work-mode.md (5KB)
- rules/core/blocking-rules.md (5KB)
- rules/domain/coding.md (5KB)
- errors/top-5-errors.md (5.9KB)

**预期 Context**: ~34KB (17%)

**预期提示**: E001 异步未并行

**测试结果**: ⏳ 待测试

---

### 测试 8: 安全审计

**输入**:
```
"审查这个 API 端点的安全性"
```

**预期识别**: `security`

**预期加载**:
- CLAUDE.md (7.7KB)
- rules/core/work-mode.md (5KB)
- rules/core/blocking-rules.md (5KB)
- rules/domain/security.md (5KB)
- capabilities/security-best-practices.md (10KB)

**预期 Context**: ~38KB (19%)

**测试结果**: ⏳ 待测试

---

## 📊 性能基准测试

### Context 使用统计

| 任务类型 | 预期 Context | 实际 Context | 差异 | 状态 |
|---------|-------------|-------------|------|------|
| 浏览器自动化 | 31KB (16%) | ⏳ | ⏳ | ⏳ |
| 视频创作 | 47KB (24%) | ⏳ | ⏳ | ⏳ |
| 数据分析 | 46KB (23%) | ⏳ | ⏳ | ⏳ |
| UI 设计 | 48KB (24%) | ⏳ | ⏳ | ⏳ |
| 营销内容 | 48KB (24%) | ⏳ | ⏳ | ⏳ |
| 代码开发 | 37KB (19%) | ⏳ | ⏳ | ⏳ |
| 错误调试 | 34KB (17%) | ⏳ | ⏳ | ⏳ |
| 安全审计 | 38KB (19%) | ⏳ | ⏳ | ⏳ |

**平均预期**: ~41KB (21%)
**vs Before**: 120KB (60%)
**节省**: ~79KB (39%)

---

## 🔍 任务识别准确率测试

### 关键词测试

| 关键词 | 预期识别 | 实际识别 | 准确 |
|--------|---------|---------|------|
| "playwright", "浏览器", "自动化" | browser-automation | ⏳ | ⏳ |
| "视频", "remotion", "动画" | video-creation | ⏳ | ⏳ |
| "数据", "SQL", "查询" | data-analysis | ⏳ | ⏳ |
| "设计", "UI", "界面" | ui-design | ⏳ | ⏳ |
| "营销", "SEO", "文案" | marketing | ⏳ | ⏳ |
| "开发", "代码", "功能" | coding | ⏳ | ⏳ |
| "bug", "错误", "调试" | debugging | ⏳ | ⏳ |
| "安全", "漏洞", "审计" | security | ⏳ | ⏳ |

**目标准确率**: >90%
**实际准确率**: ⏳ 待测试

---

## 🎯 边界情况测试

### 模糊任务

**测试 9: 模糊描述**
```
输入: "优化网站"
问题: 前端？后端？数据库？
期望: 询问用户具体方向
```

**测试 10: 多任务组合**
```
输入: "做一个视频，包含数据图表"
识别: video-creation + data-analysis
加载: 两个任务的并集
```

**测试 11: 无明确关键词**
```
输入: "帮我做个东西"
识别: general
操作: 询问具体需求
```

---

## 📈 监控指标

### 实时监控

```typescript
interface ContextMetrics {
  task_type: string;              // 识别的任务类型
  documents_loaded: string[];     // 实际加载的文档
  total_context_kb: number;       // 总 Context 大小
  context_percentage: number;     // Context 使用百分比
  identification_time_ms: number; // 任务识别时间
  loading_time_ms: number;        // 文档加载时间
  accuracy: boolean;              // 识别是否准确
}
```

### 日志格式

```
[2026-02-05 14:30:00] TASK_IDENTIFIED
  Type: browser-automation
  Keywords: ["playwright", "自动化"]
  Confidence: 0.95

[2026-02-05 14:30:00] DOCUMENTS_LOADED
  - CLAUDE.md (7.7KB)
  - rules/core/work-mode.md (5KB)
  - rules/core/blocking-rules.md (5KB)
  - rules/domain/coding.md (5KB)
  - capabilities/browser-automation/decision-tree.md (8KB)
  Total: 31KB (16%)

[2026-02-05 14:30:01] TASK_COMPLETED
  Duration: 1.2s
  Context Used: 31KB / 200KB (16%)
  Free Context: 169KB (84%)
```

---

## 🔄 持续优化流程

### 反馈循环

```
任务完成
  ↓
记录实际使用的文档
  ↓
与预加载的文档对比
  ↓
识别问题:
  - 过度加载（加载了但未使用）
  - 加载不足（需要但未加载）
  ↓
更新 CONTEXT_MANAGER.md 映射表
  ↓
下次任务使用新映射
```

### 优化触发条件

- **识别错误率 >10%** → 更新关键词映射
- **Context 超过 50KB** → 精简加载内容
- **加载不足 >5%** → 添加缺失文档到映射

---

## 📝 测试执行计划

### Phase 1: 基础测试（本周）

```
[ ] 执行 8 个核心任务测试
[ ] 记录 Context 使用情况
[ ] 验证任务识别准确率
[ ] 记录性能指标
```

### Phase 2: 边界测试（下周）

```
[ ] 测试模糊任务处理
[ ] 测试多任务组合
[ ] 测试错误识别的恢复
[ ] 测试极端情况
```

### Phase 3: 性能优化（持续）

```
[ ] 分析过度加载的情况
[ ] 分析加载不足的情况
[ ] 优化映射表
[ ] 更新文档大小预估
```

---

## 🎓 测试方法

### 手动测试

```bash
# 1. 开始新对话
# 2. 输入测试用例
# 3. 观察系统行为
# 4. 记录结果
```

### 自动化测试（未来）

```typescript
// 测试框架（未来实现）
async function testTaskIdentification(input: string, expected: string) {
  const identified = identifyTaskType(input);
  assert.equal(identified, expected);
}

// 运行所有测试
runTests([
  { input: "写 Playwright 脚本", expected: "browser-automation" },
  { input: "做视频", expected: "video-creation" },
  // ...
]);
```

---

## 📊 结果报告模板

### 测试报告

```markdown
## Context Engineering v5.0 测试报告

**日期**: 2026-02-XX
**测试人**: [Name]
**测试范围**: 8个核心任务类型

### 结果摘要

- **识别准确率**: XX% (目标 >90%)
- **平均 Context 使用**: XXkB (目标 <50KB)
- **Free Context**: XX% (目标 >60%)
- **文档查找时间**: XX秒 (目标 <2秒)

### 详细结果

[插入测试用例结果表格]

### 问题和建议

1. [问题1]
2. [问题2]

### 优化建议

1. [建议1]
2. [建议2]
```

---

## 🔗 相关文档

- `CONTEXT_MANAGER.md` - 智能加载规则
- `CONTEXT_ENGINEERING_PLAN.md` - 完整设计方案
- `IMPLEMENTATION_SUMMARY.md` - 实施总结

---

**版本**: v1.0
**创建**: 2026-02-05
**状态**: 测试计划制定完成，待执行
