# Context Engineering 重组方案

> **目标**: 释放 CLAUDE.md context，实现智能按需加载，建立清晰的 Subagent 架构

---

## 🎯 核心问题

### 当前状态
- **CLAUDE.md**: ~20KB（v4.2），仍包含大量详细内容
- **规则文件**: 全局和项目级重复
- **加载方式**: 静态全量加载
- **上下文腐烂**: 大量不相关内容被加载
- **缺少架构**: 没有清晰的 agent 职责边界

### 目标状态
- **CLAUDE.md**: <5KB，纯索引 + 核心原则
- **按需加载**: 根据任务类型智能加载相关文档
- **清晰分层**: 4层信息架构
- **Subagent 系统**: 明确的职责分工
- **Context 优化**: 保持 >50% free context

---

## 🏗️ 新架构设计

### 四层信息架构

```
Layer 0: 主索引层 (CLAUDE.md)
  ↓ 任务识别
Layer 1: 决策树层 (快速路由)
  ↓ 领域定位
Layer 2: 专题指南层 (深度内容)
  ↓ 按需加载
Layer 3: 案例库层 (具体示例)
  ↓ 精确匹配
```

### 目录结构

```
~/.claude/
├── CLAUDE.md                    # Layer 0: 主索引 (5KB)
├── CONTEXT_MANAGER.md           # Context 加载规则
│
├── index/                       # Layer 1: 快速决策树
│   ├── task-router.md          # 任务路由决策树
│   ├── capabilities-index.md   # 能力索引
│   ├── error-patterns-index.md # 错误模式索引
│   ├── tools-index.md          # 工具索引
│   └── workflow-index.md       # 工作流索引
│
├── rules/                       # 规则库
│   ├── core/                   # 核心规则（总是加载）
│   │   ├── work-mode.md        # 4步工作模式
│   │   └── blocking-rules.md   # 4种致命阻塞
│   ├── domain/                 # 领域规则（按需加载）
│   │   ├── coding.md
│   │   ├── testing.md
│   │   ├── security.md
│   │   └── git.md
│   └── context/                # 上下文管理
│       └── loading-rules.md    # 加载策略
│
├── capabilities/                # Layer 2: 能力库（按需加载）
│   ├── browser-automation/
│   ├── video-creation/
│   ├── data-analysis/
│   ├── design/
│   └── marketing/
│
├── errors/                      # Layer 3: 错误库（按需加载）
│   └── ERROR_CATALOG.md
│
├── templates/                   # 模板库（按需加载）
│   ├── remotion/
│   ├── processing/
│   └── code/
│
└── agents/                      # Subagent 定义
    ├── context-manager-agent.md
    ├── task-router-agent.md
    ├── execution-agents/
    └── verification-agent.md
```

---

## 🤖 Subagent 架构

### Agent 职责矩阵

| Agent | 职责 | 触发时机 | 输出 |
|-------|------|---------|------|
| **Context Manager** | 决定加载哪些文档 | 每个任务开始 | 文档列表 |
| **Task Router** | 识别任务类型，路由到专题 agent | 收到用户需求 | Agent + 参数 |
| **Execution Agents** | 执行具体任务 | 路由后 | 任务结果 |
| **Verification Agent** | 验证结果质量 | 任务完成时 | 通过/失败 |

### Context Manager Agent 工作流

```typescript
function context_manager(user_request: string) {
  // 1. 任务分类
  const task_type = classify_task(user_request);

  // 2. 识别所需能力
  const required_capabilities = identify_capabilities(task_type);

  // 3. 加载核心规则（总是加载）
  const core_rules = ["rules/core/work-mode.md", "rules/core/blocking-rules.md"];

  // 4. 按需加载领域规则
  const domain_rules = map_domain_rules(task_type);

  // 5. 按需加载能力文档
  const capability_docs = map_capability_docs(required_capabilities);

  // 6. 构建最小化 context
  return {
    core: core_rules,
    domain: domain_rules,
    capabilities: capability_docs,
    estimated_size: calculate_size([...core_rules, ...domain_rules, ...capability_docs])
  };
}
```

### Task Router Agent 决策树

```
用户请求
  ↓
任务类型识别
  ├─ 浏览器自动化 → browser-automation agent
  ├─ 视频创作 → video-creation agent
  ├─ 数据分析 → data-analysis agent
  ├─ UI 设计 → design agent
  ├─ 营销内容 → marketing agent
  ├─ 代码开发 → coding agent
  └─ 其他 → general-purpose agent
```

---

## 📋 实施步骤

### Phase 1: 重组目录结构 ✅
1. 创建新目录结构
2. 移动现有文件到新位置
3. 建立索引文件

### Phase 2: 创建极简 CLAUDE.md
1. 提取核心原则（4步工作模式 + 4种阻塞）
2. 创建能力索引表
3. 添加智能加载机制说明
4. 目标大小：<5KB

### Phase 3: 建立决策树层
1. 创建 task-router.md（任务路由）
2. 创建各个索引文件
3. 每个索引 <3KB

### Phase 4: 实现 Context Manager
1. 编写 CONTEXT_MANAGER.md
2. 定义加载规则
3. 创建任务类型映射表

### Phase 5: 设计 Subagent 系统
1. 定义各个 agent 的职责
2. 建立 agent 协作协议
3. 创建 agent 配置文件

### Phase 6: 测试和优化
1. 测试不同任务类型的 context 加载
2. 测量 context 使用率
3. 优化加载策略

---

## 🎯 成功指标

| 指标 | 当前 | 目标 | 测量方式 |
|------|------|------|---------|
| CLAUDE.md 大小 | ~20KB | <5KB | 文件大小 |
| 平均 context 加载 | ~120KB | <50KB | 按任务类型测量 |
| Free context 比例 | ~40% | >60% | 200K 总量计算 |
| 任务识别准确率 | N/A | >90% | 人工评估 |
| 文档查找时间 | N/A | <2秒 | 从问题到找到文档 |

---

## 📚 智能加载映射表

### 任务类型 → 必需文档

| 任务类型 | 核心规则 | 领域规则 | 能力文档 | 预估大小 |
|---------|---------|---------|---------|---------|
| **浏览器自动化** | work-mode | coding | browser-automation-decision-tree | 15KB |
| **视频创作** | work-mode | coding | remotion-guide + processing-skill | 25KB |
| **数据分析** | work-mode | coding | data-analysis-guide + sql-patterns | 20KB |
| **UI 设计** | work-mode | - | design-master-persona + ui-styles | 30KB |
| **营销内容** | work-mode | - | vibe-marketing + marketing-skills | 35KB |
| **代码开发** | work-mode | coding + testing + git | - | 12KB |
| **错误调试** | work-mode + blocking | coding | error-catalog (按需) | 10KB |
| **安全审计** | work-mode + blocking | security | security-best-practices | 15KB |

---

## 🔄 迁移计划

### 现有文件映射

| 当前位置 | 新位置 | 操作 |
|---------|--------|------|
| `CLAUDE.md` (20KB) | `CLAUDE.md` (5KB) + `index/*.md` | 拆分 |
| `capabilities/*.md` | `capabilities/*/` | 按领域分组 |
| `rules/delegator/*.md` | `capabilities/gpt-experts/` | 重组为能力 |
| `errors/ERROR_CATALOG.md` | `errors/catalog/` | 按错误类型分文件 |
| `design/*.md` | `capabilities/design/` | 保持不变 |
| `vibe-marketing/*.md` | `capabilities/marketing/` | 重组 |

---

## ⚡ 快速开始（新用户）

### 3 分钟了解系统

1. **阅读 CLAUDE.md** (5KB) - 核心原则 + 索引
2. **查看 index/task-router.md** - 快速找到你需要的能力
3. **按需阅读专题文档** - 只读相关的

### 示例：我想做浏览器自动化

```
1. 打开 CLAUDE.md → 看到能力索引
2. 点击"浏览器自动化" → 跳转到 index/tools-index.md
3. 找到决策树链接 → capabilities/browser-automation/decision-tree.md
4. 开始工作！
```

---

## 📊 Context 使用优化

### Before (当前)
```
CLAUDE.md: 20KB
+ 所有 rules: 30KB
+ 部分 capabilities: 70KB
= 总计: 120KB (60% context 占用)
```

### After (目标)
```
CLAUDE.md: 5KB
+ index/task-router.md: 3KB
+ rules/core: 5KB
+ 按需加载 1-2 个能力文档: 20-30KB
= 总计: 33-43KB (17-22% context 占用)
```

**节省**: ~80KB context (40% → 60%+ free context)

---

## 🚀 下一步行动

1. [ ] 创建新目录结构
2. [ ] 编写新的 CLAUDE.md (极简版)
3. [ ] 创建 task-router.md
4. [ ] 创建 CONTEXT_MANAGER.md
5. [ ] 重组现有文档
6. [ ] 测试加载机制
7. [ ] 优化和迭代

---

**开始时间**: 2026-02-05
**预计完成**: 2026-02-05 (同一天)
**负责人**: Claude + User
