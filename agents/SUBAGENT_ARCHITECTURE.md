# Subagent 架构

> **设计原则**: 明确的职责分工，独立的上下文，清晰的协作协议

---

## 🎯 架构概览

```
用户请求
  ↓
Context Manager Agent (识别 + 加载)
  ↓
Task Router Agent (路由 + 分发)
  ↓
Execution Agents (执行任务)
  ├─ Browser Automation Agent
  ├─ Video Creation Agent
  ├─ Data Analysis Agent
  ├─ UI Design Agent
  ├─ Coding Agent
  └─ ...
  ↓
Verification Agent (验证结果)
  ↓
返回给用户
```

---

## 🤖 Agent 职责矩阵

| Agent | 职责 | 输入 | 输出 | Context |
|-------|------|------|------|---------|
| **Context Manager** | 决定加载哪些文档 | 用户请求 | 文档列表 | 最小（只需任务类型） |
| **Task Router** | 识别任务类型并路由 | 用户请求 | Agent + 参数 | 最小（只需决策树） |
| **Execution Agents** | 执行具体任务 | 任务参数 | 任务结果 | 中等（加载相关能力文档） |
| **Verification Agent** | 验证结果质量 | 执行结果 | 通过/失败 + 建议 | 最小（只需验证规则） |

---

## 1️⃣ Context Manager Agent

### 职责
- 分析用户请求，识别任务类型
- 决定加载哪些文档
- 构建最小化 context
- 监控 context 使用率

### 输入
```typescript
interface ContextManagerInput {
  user_request: string;          // 用户的原始请求
  current_context_size: number;  // 当前已使用的 context
}
```

### 输出
```typescript
interface ContextManagerOutput {
  task_type: string;                  // 识别的任务类型
  documents_to_load: string[];        // 需要加载的文档路径
  estimated_size: number;             // 预估加载大小（KB）
  loading_strategy: "eager" | "lazy"; // 加载策略
}
```

### 工作流程

```
1. 接收用户请求
   ↓
2. 提取关键词
   ↓
3. 匹配任务类型
   ↓
4. 查询映射表
   ↓
5. 构建加载计划
   ↓
6. 检查 context 预算
   ↓ (如果超过阈值)
7. 优化加载内容
   ↓
8. 返回加载计划
```

### Context 需求
- **核心**: `CONTEXT_MANAGER.md` (~10KB)
- **其他**: 不需要其他文档

---

## 2️⃣ Task Router Agent

### 职责
- 基于任务类型选择合适的 Execution Agent
- 提取任务参数
- 配置 agent 环境
- 处理多任务场景

### 输入
```typescript
interface TaskRouterInput {
  task_type: string;         // Context Manager 识别的任务类型
  user_request: string;      // 原始请求
  loaded_documents: string[]; // 已加载的文档
}
```

### 输出
```typescript
interface TaskRouterOutput {
  agent_type: string;            // 选择的 agent 类型
  agent_config: AgentConfig;     // Agent 配置
  task_parameters: object;       // 提取的任务参数
  execution_mode: "single" | "parallel"; // 执行模式
}
```

### 决策树

```
任务类型识别
  ├─ browser-automation
  │  └─ Browser Automation Agent
  │     ├─ tool: playwright / agent-browser
  │     └─ context: decision-tree.md
  │
  ├─ video-creation
  │  └─ Video Creation Agent
  │     ├─ tools: Remotion + Processing
  │     └─ context: remotion-guide + processing-skill
  │
  ├─ data-analysis
  │  └─ Data Analysis Agent
  │     ├─ tools: SQL + Charts
  │     └─ context: data-analysis-guide
  │
  ├─ ui-design
  │  └─ UI Design Agent
  │     ├─ skills: ui-ux-pro-max
  │     └─ context: design-master-persona
  │
  ├─ coding
  │  └─ Coding Agent
  │     ├─ tools: Edit, Write, Bash
  │     └─ context: coding + testing + git
  │
  └─ 其他类型...
```

### Context 需求
- **核心**: `index/task-router.md` (~8KB)
- **其他**: 不需要其他文档

---

## 3️⃣ Execution Agents

### 通用接口

所有 Execution Agent 都实现这个接口：

```typescript
interface ExecutionAgent {
  name: string;
  capabilities: string[];
  required_context: string[];

  // 执行任务
  execute(task: TaskDefinition): Promise<TaskResult>;

  // 验证结果
  self_verify?(result: TaskResult): Promise<boolean>;

  // 错误处理
  handle_error?(error: Error): Promise<void>;
}
```

### 具体 Agent 示例

#### Browser Automation Agent

```yaml
name: Browser Automation Agent
capabilities:
  - 网页自动化操作
  - 网页爬取
  - UI 测试
  - 截图和录制

required_context:
  - capabilities/browser-automation/decision-tree.md
  - rules/domain/coding.md

tools:
  - playwright (MCP) - 交互式操作
  - agent-browser (CLI) - 批量/脚本化

execution_pattern:
  1. 分析需求
  2. 选择工具（playwright vs agent-browser）
  3. 生成操作序列
  4. 执行操作
  5. 处理错误
  6. 返回结果

context_size: ~15KB
```

#### Video Creation Agent

```yaml
name: Video Creation Agent
capabilities:
  - Remotion 视频生成
  - 自动风格匹配
  - 配色方案设计
  - 场景分镜设计
  - 素材生成指令

required_context:
  - rules/remotion-auto-production.md
  - capabilities/PROCESSING_SKILL.md
  - capabilities/REMOTION_TEMPLATES_LIBRARY.md (可选)

tools:
  - Remotion
  - Processing Creative Skill
  - Nano Banana Pro

execution_pattern:
  1. 分析需求（目的、时长、风格）
  2. 匹配设计风格
  3. 选择模板或从零生成
  4. 生成代码
  5. 生成素材指令
  6. 提供渲染命令

context_size: ~25KB
```

#### Data Analysis Agent

```yaml
name: Data Analysis Agent
capabilities:
  - SQL 查询设计
  - 数据可视化
  - 报表生成
  - 趋势分析

required_context:
  - capabilities/data-analysis-guide.md
  - capabilities/sql-patterns.md

tools:
  - bytebase (MCP) - MySQL
  - PostgreSQL 直连
  - chart (MCP) - 图表生成
  - honeycomb (MCP) - 监控数据

execution_pattern:
  1. 理解分析目标
  2. 设计查询逻辑
  3. 优化查询性能（CTE）
  4. 执行查询
  5. 生成可视化
  6. 解释结果

context_size: ~20KB
```

---

## 4️⃣ Verification Agent

### 职责
- 验证任务执行结果
- 检查质量标准
- 提供改进建议
- 决定是否需要重试

### 输入
```typescript
interface VerificationInput {
  task_type: string;
  execution_result: TaskResult;
  quality_standards: QualityStandard[];
}
```

### 输出
```typescript
interface VerificationOutput {
  status: "passed" | "failed" | "needs_improvement";
  issues: Issue[];               // 发现的问题
  suggestions: Suggestion[];     // 改进建议
  should_retry: boolean;         // 是否应该重试
}
```

### 验证规则

```yaml
coding:
  - 代码可运行
  - 测试通过
  - 无安全漏洞
  - 符合代码风格

video-creation:
  - 生成了完整的 Remotion 项目
  - 包含渲染命令
  - 提供了素材生成指令

data-analysis:
  - SQL 查询语法正确
  - 结果符合预期
  - 性能优化（使用 CTE）

ui-design:
  - 符合设计规范
  - 响应式设计
  - 无障碍性
```

### Context 需求
- **核心**: `rules/core/work-mode.md` (~5KB)
- **领域**: 根据任务类型加载验证规则 (~5KB)

---

## 🔄 Agent 协作流程

### 标准流程

```
用户请求: "做一个30秒的产品介绍视频"
  ↓
[Context Manager]
  识别: video-creation
  加载: remotion-guide (12KB) + processing-skill (8KB)
  ↓
[Task Router]
  选择: Video Creation Agent
  参数: { duration: 30, type: "product-demo" }
  ↓
[Video Creation Agent]
  1. 分析需求
  2. 匹配风格: Glassmorphism + Tech Innovation
  3. 生成场景: 4个场景
  4. 生成代码: 完整 Remotion 项目
  5. 生成素材指令: Nano Banana Pro prompts
  ↓
[Verification Agent]
  ✓ 检查项目结构
  ✓ 检查代码完整性
  ✓ 检查渲染命令
  ✓ 检查素材指令
  → PASSED
  ↓
返回用户: 完整的视频项目
```

### 多任务场景

```
用户请求: "做一个产品视频，包含数据可视化图表"
  ↓
[Context Manager]
  识别: video-creation + data-analysis
  加载: remotion-guide + data-analysis-guide
  ↓
[Task Router]
  选择: Parallel Execution
    - Video Creation Agent
    - Data Analysis Agent
  ↓
[并行执行]
  Video Creation Agent → 生成视频框架
  Data Analysis Agent → 生成图表数据
  ↓
[集成]
  将图表集成到视频中
  ↓
[Verification Agent]
  验证集成结果
  ↓
返回用户
```

---

## 📊 Context 使用对比

### 传统方式（无 Subagent）
```
加载所有文档: 120KB
  ↓
处理任务
  ↓
context 使用: 60%
free context: 40%
```

### Subagent 架构
```
Context Manager (10KB)
  ↓
Task Router (8KB)
  ↓
Execution Agent (15-30KB)
  ↓
Verification Agent (5KB)
  ↓
总计: 38-53KB (19-27%)
free context: 73-81%
```

**提升**: 2x free context

---

## 🎯 设计原则

### 1. 单一职责
每个 agent 只做一件事，并做好。

### 2. 最小 Context
只加载完成任务必需的文档。

### 3. 独立性
Agent 之间通过标准接口通信，不共享状态。

### 4. 可测试性
每个 agent 都可以独立测试。

### 5. 可组合性
Agent 可以串联或并联组合。

---

## 🚀 扩展性

### 添加新 Agent

1. **定义 Agent**
   ```yaml
   name: New Agent
   capabilities: [...]
   required_context: [...]
   ```

2. **更新 Task Router**
   ```typescript
   // 添加新任务类型映射
   "new-task-type": "New Agent"
   ```

3. **更新 Context Manager**
   ```yaml
   new-task-type:
     keywords: [...]
     load: [...]
   ```

4. **测试**
   ```
   用户请求 → 识别 → 路由 → 执行 → 验证
   ```

---

## 📚 相关文档

- `CONTEXT_MANAGER.md` - Context 加载规则
- `index/task-router.md` - 任务路由决策树
- `rules/core/work-mode.md` - 工作模式
- `capabilities/` - 各个能力的详细文档

---

**版本**: v1.0
**更新**: 2026-02-05
**状态**: Active
