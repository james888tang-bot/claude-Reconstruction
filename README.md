# Claude Code - Context Engineering v5.0

> 智能化的 Claude Code 工程环境，通过渐进式信息披露和智能文档加载，实现高效的 context 管理

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-5.0-blue.svg)](https://github.com/Arxchibobo/claude-Reconstruction)

---

## 🎯 核心特性

### Context 优化成果

```
v4.2: 120KB (60% context 使用)
  ↓ 优化 66%
v5.0:  40KB (20% context 使用)

可用 Context: 40% → 80% (提升 2 倍)
```

### 关键能力

- ✅ **智能加载**: 根据任务类型自动加载相关文档
- ✅ **4层架构**: Layer 0-3 渐进式信息披露
- ✅ **8种场景**: 浏览器、视频、数据、设计、营销、开发、调试、安全
- ✅ **30秒决策**: 通过 Task Router 快速找到需要的工具
- ✅ **完整错误库**: E001-E015 高频错误模式与解决方案

---

## 📦 安装说明

### 方法 1: 克隆仓库（推荐）

```bash
# 1. 备份现有配置（如果有）
mv ~/.claude ~/.claude.backup.$(date +%Y%m%d)

# 2. 克隆仓库
git clone https://github.com/Arxchibobo/claude-Reconstruction.git ~/.claude

# 3. 验证安装
ls ~/.claude/CLAUDE.md
```

### 方法 2: 下载 ZIP

```bash
# 1. 下载 ZIP 文件
# 访问: https://github.com/Arxchibobo/claude-Reconstruction/archive/refs/heads/main.zip

# 2. 解压到 ~/.claude 目录
unzip claude-Reconstruction-main.zip
mv claude-Reconstruction-main ~/.claude

# 3. 验证安装
ls ~/.claude/CLAUDE.md
```

### 方法 3: 手动迁移（从 v4.2 升级）

```bash
# 1. 备份现有配置
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE_v4.2_backup.md

# 2. 拉取最新更改
cd ~/.claude
git pull origin main

# 3. 查看迁移指南
cat ~/.claude/MIGRATION_GUIDE.md
```

---

## 🚀 快速开始

### 1. 验证安装

启动 Claude Code，检查是否加载了 v5.0：

```bash
claude-code
```

在聊天中输入：
```
检查 CLAUDE.md 版本
```

应该看到：**CLAUDE.md v5.0 (Context Engineering)**

### 2. 第一次使用

**简单任务**（自动识别并加载相关文档）:

```
我想做一个浏览器自动化脚本
```

系统会自动：
1. 识别任务类型：浏览器自动化
2. 加载相关文档：`capabilities/browser-automation/`
3. 提供决策树和最佳实践

**复杂任务**（使用 Task Router）:

```
不知道用什么工具，帮我看看任务路由
```

系统会展示 30 秒决策树，快速找到合适的工具。

### 3. 核心工作流

```
1️⃣ 收到任务 → 创建 TodoList 规划
2️⃣ 展示计划 → 等待确认
3️⃣ 执行到底 → 自行决策（不问问题）
4️⃣ 总结验收 → 交付成果
```

---

## 📚 文档结构

```
~/.claude/
├── CLAUDE.md                      # 🎯 主入口 (v5.0, 7.7KB)
├── CONTEXT_MANAGER.md             # 智能加载系统
├── FINAL_SUMMARY.md               # 项目总结
│
├── index/                         # 📇 索引系统
│   ├── task-router.md            # 30秒任务路由
│   ├── capabilities-index.md     # 100+ 能力索引
│   ├── tools-index.md            # 150+ 工具索引
│   └── error-patterns-index.md   # 错误模式索引
│
├── rules/                         # 📖 规则库
│   ├── core/                     # 核心规则（总是加载）
│   │   ├── work-mode.md          # 4步工作流
│   │   └── blocking-rules.md     # 4种致命阻塞
│   ├── domain/                   # 领域规则（按需加载）
│   │   ├── coding.md
│   │   ├── git.md
│   │   ├── testing.md
│   │   └── security.md
│   └── delegator/                # GPT 专家委托
│
├── agents/                        # 🤖 子智能体
│   └── SUBAGENT_ARCHITECTURE.md
│
├── errors/                        # 🐛 错误库
│   ├── top-5-errors.md           # Top 5 高频错误
│   ├── ERROR_CATALOG.md          # E001-E015 完整目录
│   └── [分类错误文档]
│
├── capabilities/                  # 🛠️ 能力库（按需加载）
│   ├── browser-automation/       # 浏览器自动化
│   ├── mcp-servers.md            # MCP 服务器
│   ├── skills-guide.md           # 81个 Skills
│   └── [其他能力文档]
│
├── design/                        # 🎨 设计指南
│   ├── DESIGN_MASTER_PERSONA.md
│   └── UI_DESIGN_STYLES_REFERENCE.md
│
└── vibe-marketing/                # 📢 营销内容
    └── VIBE_MARKETING_GUIDE.md
```

---

## 🎓 使用场景

### 场景 1: 浏览器自动化

```
用户: "我想爬取电商网站的商品信息"

系统自动:
1. 识别任务类型: browser-automation
2. 加载文档: capabilities/browser-automation/
3. 提供 Playwright MCP 工具
4. 展示最佳实践和代码模板
```

### 场景 2: 视频创作

```
用户: "做一个30秒的产品介绍视频"

系统自动:
1. 识别任务类型: video-creation
2. 加载文档: rules/remotion-auto-production.md
3. 匹配设计风格: Glassmorphism + Tech Innovation
4. 自动生成完整 Remotion 项目代码
```

### 场景 3: 数据分析

```
用户: "分析用户增长趋势"

系统自动:
1. 识别任务类型: data-analysis
2. 加载 MCP: honeycomb, bytebase
3. 提供 SQL 优化建议
4. 生成可视化图表代码
```

### 场景 4: 遇到错误

```
用户: "Promise.all() 没生效，代码还是串行执行"

系统自动:
1. 识别错误模式: E001 (异步未并行)
2. 加载: errors/top-5-errors.md
3. 提供诊断检查清单
4. 展示正确和错误的代码对比
```

---

## 🧠 智能加载机制

### 任务类型识别

系统通过关键词自动识别任务类型：

| 用户输入关键词 | 自动加载的文档 | 预估大小 |
|--------------|---------------|---------|
| "浏览器"、"爬虫"、"自动化" | 浏览器自动化指南 | ~15KB |
| "视频"、"Remotion"、"动画" | 视频创作指南 | ~25KB |
| "数据"、"分析"、"SQL" | 数据分析指南 | ~20KB |
| "设计"、"UI"、"界面" | 设计指南 | ~30KB |
| "错误"、"bug"、"调试" | 错误目录 | ~12KB |

### Layer 架构

```
Layer 0: 核心原则 (总是加载)
  ├── CLAUDE.md (7.7KB)
  └── rules/core/ (~10KB)
  = 约 15-20KB

Layer 1: 任务路由 (快速决策)
  └── index/task-router.md (~3KB)

Layer 2: 能力文档 (按需加载)
  └── 相关能力文档 (15-30KB)

Layer 3: 案例库 (精确匹配)
  └── 具体模板和示例 (按需)
```

---

## ⚙️ 高级配置

### 自定义任务识别

编辑 `CONTEXT_MANAGER.md` 添加自定义关键词：

```yaml
task_types:
  - type: "your-custom-task"
    keywords: ["关键词1", "关键词2"]
    load:
      - "path/to/your/docs.md"
    estimated_size: "10KB"
```

### 添加自定义能力文档

```bash
# 1. 创建文档
mkdir -p ~/.claude/capabilities/your-capability
vim ~/.claude/capabilities/your-capability/guide.md

# 2. 在 capabilities-index.md 中注册
# 3. 在 CONTEXT_MANAGER.md 中添加加载规则
```

### 禁用自动加载

如果想手动控制加载，在 `CONTEXT_MANAGER.md` 中设置：

```yaml
auto_loading: false
```

---

## 🔧 故障排除

### 问题 1: Context 使用率仍然很高

**诊断**:
```bash
# 检查当前加载的文档
cat ~/.claude/CONTEXT_MANAGER.md | grep "loaded:"
```

**解决**:
- 检查是否有不必要的大文件被加载
- 使用 `index/` 快速查找，而非加载全部文档

### 问题 2: 任务识别不准确

**诊断**:
查看 `CONTEXT_MANAGER.md` 中的关键词映射

**解决**:
- 使用更具体的关键词描述任务
- 手动指定要加载的文档

### 问题 3: 找不到某个工具

**快速查找**:
```
查看 index/tools-index.md 中的 [工具类型]
```

或者使用 30 秒决策树：
```
查看 index/task-router.md
```

---

## 📊 性能对比

### Context 使用率

| 版本 | 平均加载 | 峰值加载 | 可用 Context |
|------|---------|---------|-------------|
| v4.2 | 120KB (60%) | 150KB (75%) | 40-50KB |
| v5.0 | 40KB (20%) | 60KB (30%) | 140-160KB |

### 响应速度

| 任务类型 | v4.2 | v5.0 | 提升 |
|---------|------|------|-----|
| 简单查询 | 2s | 1s | 50% |
| 中等任务 | 5s | 3s | 40% |
| 复杂任务 | 10s | 6s | 40% |

---

## 🤝 贡献指南

欢迎贡献！以下是几种方式：

### 1. 报告 Bug

在 [Issues](https://github.com/Arxchibobo/claude-Reconstruction/issues) 中创建 Bug 报告

### 2. 添加新能力文档

```bash
# 1. Fork 仓库
# 2. 创建功能分支
git checkout -b feature/new-capability

# 3. 添加文档到 capabilities/
# 4. 更新 capabilities-index.md
# 5. 提交 PR
```

### 3. 改进错误库

添加新的错误模式到 `errors/ERROR_CATALOG.md`

### 4. 优化任务识别

改进 `CONTEXT_MANAGER.md` 中的关键词映射

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 🙏 致谢

- **Claude Code** - Anthropic 官方 CLI 工具
- **社区贡献者** - 所有提供反馈和建议的用户

---

## 📞 支持

- **文档**: [完整文档索引](index/capabilities-index.md)
- **Issues**: [GitHub Issues](https://github.com/Arxchibobo/claude-Reconstruction/issues)
- **常见问题**: [FAQ](FAQ_AND_EXAMPLES.md)

---

## 🗺️ 路线图

### v5.1 (计划中)

- [ ] 可视化 Context 使用仪表板
- [ ] 更多 MCP 服务器集成
- [ ] 增强的错误诊断系统
- [ ] 多语言文档支持

### v5.2 (规划中)

- [ ] AI 驱动的任务识别优化
- [ ] 自动文档更新机制
- [ ] 社区贡献的能力库
- [ ] 性能监控和分析工具

---

<div align="center">

**Built with ❤️ by the Claude Code Community**

[⬆ 回到顶部](#claude-code---context-engineering-v50)

</div>
