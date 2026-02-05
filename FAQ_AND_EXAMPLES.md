# Context Engineering v5.0 - 常见问题和示例

> **用途**: 快速解答常见问题，提供实用示例

---

## ❓ 常见问题（FAQ）

### 基础问题

#### Q1: 我需要手动指定加载哪些文档吗？

**A**: **不需要！** 系统会自动识别任务类型并加载相关文档。

```
你说: "帮我写个 Playwright 脚本"
系统: 自动识别为 browser-automation
     自动加载相关文档
     开始工作
```

#### Q2: 如何知道系统加载了哪些文档？

**A**: 系统会在内部处理，你不需要关心。但如果想了解，可以：

```bash
# 查看任务类型映射
cat ~/.claude/CONTEXT_MANAGER.md
```

#### Q3: 识别错误怎么办？

**A**: 可以手动指定：

```
@load capabilities/browser-automation/decision-tree.md
```

#### Q4: 旧版本的文档还能用吗？

**A**: 能用！所有现有文档都保持不变，只是加载方式改为按需加载。

#### Q5: v5.0 比 v4.2 有什么优势？

**A**:
- ✅ Context 使用从 60% → 21%（节省 ~75KB）
- ✅ Free context 从 40% → 79%（2x 提升）
- ✅ 智能按需加载（自动识别任务）
- ✅ 30秒快速查找（4个索引文件）
- ✅ 清晰的 Subagent 架构

---

### 技术问题

#### Q6: 系统如何识别任务类型？

**A**: 基于关键词匹配：

```typescript
// 示例
const keywords_map = {
  "browser-automation": ["浏览器", "playwright", "自动化", "爬虫"],
  "video-creation": ["视频", "remotion", "动画", "特效"],
  // ...
};

// 匹配用户输入中的关键词
for (const keyword of keywords) {
  if (user_request.includes(keyword)) {
    return task_type;
  }
}
```

#### Q7: 如果我的任务包含多个类型怎么办？

**A**: 系统会加载所有相关文档的并集：

```
输入: "做一个产品视频，包含数据图表"
识别: video-creation + data-analysis
加载: 两个任务的文档并集
```

#### Q8: Context 预算是如何分配的？

**A**:
```
总预算: 200KB

Layer 0 (总是加载): ~15KB
  - CLAUDE.md (7.7KB)
  - core rules (10KB)

Layer 1 (任务识别): ~3KB
  - task-router.md

Layer 2 (按需加载): ~20-30KB
  - 相关能力文档

留给工作: ~152-162KB (76-81%)
```

#### Q9: 如何验证加载策略是否有效？

**A**: 查看测试文档：

```bash
cat ~/.claude/TESTING_AND_MONITORING.md
```

---

### 使用问题

#### Q10: 我应该先看哪个文档？

**A**: 新手3分钟路线：

```
1. CLAUDE.md (1分钟) - 核心原则
2. index/task-router.md (1分钟) - 快速查找工具
3. 开始工作 (1分钟) - 直接描述任务
```

#### Q11: 找不到某个工具怎么办？

**A**: 使用索引系统：

```bash
# 30秒找到任何工具
cat ~/.claude/index/task-router.md

# 查看所有能力
cat ~/.claude/index/capabilities-index.md

# 查看所有工具
cat ~/.claude/index/tools-index.md
```

#### Q12: 遇到错误怎么快速诊断？

**A**: 使用错误索引：

```bash
# 查看 Top 5 高频错误
cat ~/.claude/errors/top-5-errors.md

# 完整错误目录
cat ~/.claude/errors/ERROR_CATALOG.md

# 错误模式索引
cat ~/.claude/index/error-patterns-index.md
```

---

## 💡 使用示例

### 示例 1: 浏览器自动化

**场景**: 批量抓取产品信息

**你的输入**:
```
我需要写一个脚本，自动打开 Amazon，搜索"机械键盘"，
然后抓取前20个产品的名称、价格和评分
```

**系统处理**:
```
1. 识别: browser-automation
2. 加载:
   - CLAUDE.md
   - work-mode.md
   - coding.md
   - browser-automation/decision-tree.md
3. 判断: 批量操作 → 推荐 agent-browser CLI
4. 生成代码
```

**输出**:
```bash
# agent-browser 脚本
agent-browser "打开 Amazon，搜索机械键盘，抓取前20个产品信息"
```

---

### 示例 2: 视频创作（快速模板）

**场景**: 制作公司介绍视频

**你的输入**:
```
做一个15秒的公司介绍视频，要有：
1. 公司 Logo 入场动画
2. 3个核心优势展示
3. 联系方式
```

**系统处理**:
```
1. 识别: video-creation
2. 加载:
   - CLAUDE.md
   - remotion-auto-production.md
   - REMOTION_TEMPLATES_LIBRARY.md
3. 匹配模板:
   - animated-text (Logo)
   - animated-list (3个优势)
   - bounce-text (联系方式)
4. 生成代码
```

**输出**:
```typescript
// 完整的 Remotion 项目
// 包含3个模板的组合使用
```

---

### 示例 3: 数据分析

**场景**: 分析用户增长趋势

**你的输入**:
```
查询最近30天的用户注册数据，按天分组，
计算每日新增用户和累计用户数，生成折线图
```

**系统处理**:
```
1. 识别: data-analysis
2. 加载:
   - CLAUDE.md
   - data-analysis-guide.md
   - sql-patterns.md
3. 生成 SQL:
   - 使用 CTE 优化
   - 窗口函数计算累计
4. 生成图表
```

**输出**:
```sql
WITH daily_registrations AS (
  SELECT
    DATE(created_at) as date,
    COUNT(*) as new_users
  FROM users
  WHERE created_at >= NOW() - INTERVAL 30 DAY
  GROUP BY DATE(created_at)
)
SELECT
  date,
  new_users,
  SUM(new_users) OVER (ORDER BY date) as cumulative_users
FROM daily_registrations
ORDER BY date;
```

---

### 示例 4: UI 设计

**场景**: 设计现代简约风格的登录页

**你的输入**:
```
设计一个登录页面，要求：
- 现代简约风格
- 居中布局
- 包含邮箱/密码输入框和登录按钮
- 浅色背景
```

**系统处理**:
```
1. 识别: ui-design
2. 加载:
   - CLAUDE.md
   - DESIGN_MASTER_PERSONA.md
   - UI_DESIGN_STYLES_REFERENCE.md
3. 选择风格: Minimalist
4. 生成设计
```

**输出**:
```jsx
// 完整的 React 组件
// 包含 Tailwind CSS 样式
```

---

### 示例 5: 营销内容

**场景**: 写 SEO 博客文章

**你的输入**:
```
写一篇关于"AI 写作工具如何提升效率"的博客文章，
要求 SEO 优化，目标关键词是"AI 写作工具"
```

**系统处理**:
```
1. 识别: marketing
2. 加载:
   - CLAUDE.md
   - VIBE_MARKETING_GUIDE.md
   - MARKETING_SKILLS_GUIDE.md
3. 使用 Skills:
   - seo-content-writer
   - seo-meta-optimizer
4. 生成文章
```

**输出**:
```markdown
# AI 写作工具如何提升效率：完整指南

## 目录
1. 什么是 AI 写作工具
2. 5个关键效率提升点
3. 实战案例分析
...

Meta Title: AI 写作工具如何提升效率 | 2024完整指南
Meta Description: 了解 AI 写作工具如何帮助你...
```

---

### 示例 6: 代码开发（TDD）

**场景**: 实现用户认证

**你的输入**:
```
用 TDD 方式实现用户认证功能，包括：
- 用户注册
- 邮箱验证
- 密码加密
- JWT Token 生成
```

**系统处理**:
```
1. 识别: coding
2. 加载:
   - CLAUDE.md
   - work-mode.md
   - coding.md
   - testing.md
   - security.md
3. 工作流程:
   - 先写测试（RED）
   - 实现功能（GREEN）
   - 重构（REFACTOR）
4. 安全检查:
   - 密码加密（bcrypt）
   - JWT 安全配置
   - 输入验证
```

**输出**:
```typescript
// 1. 测试文件
describe('UserAuth', () => {
  it('should register user with hashed password', async () => {
    // ...
  });
});

// 2. 实现文件
class UserAuth {
  async register(email, password) {
    // ...
  }
}

// 3. 安全配置
// - bcrypt rounds: 12
// - JWT secret: 环境变量
// - 输入验证: Zod
```

---

### 示例 7: 错误调试

**场景**: 异步性能问题

**你的输入**:
```
我的代码很慢，需要处理 100 个 API 请求，
每个请求大约 2 秒，现在总共需要 200 秒
```

**系统处理**:
```
1. 识别: debugging
2. 加载:
   - CLAUDE.md
   - top-5-errors.md
3. 匹配错误: E001 异步未并行
4. 提供修复方案
```

**输出**:
```javascript
// ❌ 你的代码（顺序执行，200秒）
for (const item of items) {
  const result = await api.call(item);
  results.push(result);
}

// ✅ 修复后（并行执行，2秒）
const promises = items.map(item => api.call(item));
const results = await Promise.all(promises);

// 如果担心并发过高，可以分批：
const batchSize = 10;
for (let i = 0; i < items.length; i += batchSize) {
  const batch = items.slice(i, i + batchSize);
  const batchResults = await Promise.all(
    batch.map(item => api.call(item))
  );
  results.push(...batchResults);
}
```

---

### 示例 8: 安全审计

**场景**: API 安全审查

**你的输入**:
```
审查这个 API 端点的安全性：

POST /api/users/:id/update
Body: { name, email, role }

目前没有任何验证
```

**系统处理**:
```
1. 识别: security
2. 加载:
   - CLAUDE.md
   - security.md
3. 检查 OWASP Top 10
4. 提供修复建议
```

**输出**:
```typescript
// 🔴 发现的安全问题：

1. ❌ 无身份验证
2. ❌ 无授权检查（任何人可以修改任何用户）
3. ❌ 无输入验证
4. ❌ 可能的权限提升（role 字段）
5. ❌ 无速率限制

// ✅ 修复方案：

// 1. 添加身份验证
router.post('/api/users/:id/update',
  authenticateToken,  // JWT 验证
  async (req, res) => {
    // ...
  }
);

// 2. 添加授权检查
if (req.user.id !== req.params.id && !req.user.isAdmin) {
  return res.status(403).json({ error: 'Forbidden' });
}

// 3. 输入验证
const schema = z.object({
  name: z.string().min(1).max(100),
  email: z.string().email(),
  role: z.enum(['user', 'admin']).optional()  // 仅管理员可修改
});

const data = schema.parse(req.body);

// 4. 权限检查（role 修改）
if (data.role && !req.user.isAdmin) {
  delete data.role;  // 非管理员不能修改 role
}

// 5. 速率限制
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000,  // 15分钟
  max: 100  // 最多 100 个请求
});
router.use('/api/', limiter);
```

---

## 🎓 进阶技巧

### 技巧 1: 组合多个能力

**场景**: 制作数据可视化视频

```
输入: "做一个视频，展示我们的季度业绩数据"

系统处理:
1. 识别: video-creation + data-analysis
2. 加载两个领域的文档
3. 组合使用:
   - 用 SQL 查询数据
   - 用 Chart 生成图表
   - 用 Remotion 制作动画视频
```

### 技巧 2: 使用快速索引

**场景**: 不确定用什么工具

```bash
# 30秒找到答案
cat ~/.claude/index/task-router.md

# 查找特定能力
grep -i "视频" ~/.claude/index/task-router.md
```

### 技巧 3: 编码前检查清单

**场景**: 避免常见错误

```bash
# 查看 Top 5 错误
cat ~/.claude/errors/top-5-errors.md

# 快速过一遍检查清单
# [ ] 异步并行？
# [ ] 轮询超时？
# [ ] 错误抛出？
# [ ] SQL CTE？
# [ ] 资源清理？
```

### 技巧 4: GPT 专家咨询

**场景**: 复杂架构决策

```
输入: "我应该用 Redis 还是 Memcached 做缓存？"

触发: GPT Architect（架构专家）
提供: 详细对比和建议
```

---

## 🔗 快速链接

### 核心文档
- `CLAUDE.md` - 主索引
- `CONTEXT_MANAGER.md` - 智能加载规则
- `index/task-router.md` - 30秒找工具

### 索引文件
- `index/capabilities-index.md` - 100+ 能力
- `index/tools-index.md` - 150+ 工具
- `index/error-patterns-index.md` - 15个错误

### 测试和监控
- `TESTING_AND_MONITORING.md` - 测试计划
- `FAQ_AND_EXAMPLES.md` (本文档) - FAQ 和示例

---

## 💬 还有问题？

1. **查看完整文档**
   ```bash
   ls ~/.claude/
   ```

2. **搜索关键词**
   ```bash
   grep -r "关键词" ~/.claude/
   ```

3. **直接问我**
   ```
   "我想做 [具体任务]，应该用什么工具？"
   ```

---

**版本**: v1.0
**创建**: 2026-02-05
**示例数量**: 8个详细示例
**FAQ 数量**: 12个常见问题
