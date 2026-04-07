# OpenCode Skills 使用指南

这份文档用来说明你本地 skill 库里每个 skill 的：

- 适用场景
- 怎么使用

## 怎么理解“怎么使用”

大多数 skill 不需要你手动输入固定命令，它们更像“遇到对应场景时应该调用的专用能力”。

你平时可以这样理解：

- **直接描述任务场景**：例如“帮我把这段文案改得更自然一点”
- **明确说出意图**：例如“帮我评审一下本地改动”
- **需要时点名 skill 方向**：例如“用多代理并行做这个任务”

如果你想更稳定地触发某个 skill，建议在提需求时把“场景 + 目标”说清楚。

例如：

- “帮我把这段文案改得更自然，别那么像 AI 写的” -> 更容易用到 `humanizer`
- “帮我检查本地未提交改动有没有问题” -> 更容易用到 `cek-review-local-changes`
- “这个 bug 很绕，帮我沿调用链倒推根因” -> 更容易用到 `cek-root-cause-tracing`

## 技能树怎么看

在可视化界面里，skills 已经按技能树分成了大类和子类，不再是简单平铺：

- 第一层：大类，例如 `技能开发`、`多代理协作`、`Git 协作`
- 第二层：子类，例如 `设计与优化`、`执行模式`、`Issue 与 PR`
- 第三层：具体 skill

你可以先按大类找方向，再点开具体 skill 看详情和用途。

## 核心通用 Skills

### `humanizer`
- 适用场景：你要把文字改得更自然、更像人写的，适合周报、邮件、文档、说明文案
- 怎么使用：直接说“把这段话改得自然一点”“帮我去 AI 味”“帮我润色成更像真人表达”

### `find-skills`
- 适用场景：你不知道该装什么 skill，想按需求搜索现成 skill
- 怎么使用：直接说“帮我找一个写周报的 skill”“帮我找一个适合 DevOps 的 skill”

### `skill-creator`
- 适用场景：你要新建 skill、优化已有 skill、做 skill 评估
- 怎么使用：直接说“帮我做一个新 skill”“帮我优化这个 skill 的触发描述”“帮我评估这个 skill 好不好用”

### `skill-registry`
- 适用场景：安装、复制、更新、删除、盘点 skills 时维护技能总表
- 怎么使用：直接说“把这个 skill 装进本地并更新注册表”“帮我刷新 skill 清单”

## CEK 核心优先推荐

### `cek-context-engineering`
- 适用场景：你在写 commands、skills、agents、system prompt，想提升上下文设计质量
- 怎么使用：直接说“帮我优化这个 skill 的上下文设计”“帮我看这段 prompt 的上下文工程问题”

### `cek-create-skill`
- 适用场景：你要创建一个新 skill，或者重做一个已有 skill
- 怎么使用：直接说“帮我设计一个新的 skill”“按规范帮我做一个 skill”

### `cek-test-skill`
- 适用场景：skill 做完后想验证是否真的能稳定工作
- 怎么使用：直接说“帮我测试一下这个 skill 是否可靠”“帮我验证这个 skill 的触发和执行效果”

### `cek-review-local-changes`
- 适用场景：你改完代码后，想审查本地未提交改动
- 怎么使用：直接说“帮我 review 一下本地改动”“检查我当前没提交的代码有没有问题”

### `cek-review-pr`
- 适用场景：你要评审一个 Pull Request
- 怎么使用：直接说“帮我 review 这个 PR”“帮我看看这个合并请求的风险点”

### `cek-do-in-parallel`
- 适用场景：任务可以拆成多个互不依赖的小任务，想并行完成
- 怎么使用：直接说“这个任务拆成几部分并行处理”“并行帮我检查这几个模块”

### `cek-root-cause-tracing`
- 适用场景：问题链路复杂，想从报错一路倒查根因
- 怎么使用：直接说“帮我沿调用链倒推根因”“这个 bug 很深，帮我找最早触发点”

### `cek-thought-based-reasoning`
- 适用场景：问题复杂，普通直觉式回答不够，需要系统推理
- 怎么使用：直接说“这个问题请一步一步推理”“帮我系统分析不同方案的利弊”

## Skill / Prompt / Agent 开发类

### `cek-agent-evaluation`
- 适用场景：要评估 command、skill、agent 的实际效果
- 怎么使用：说“帮我评估这个 agent 的效果”“看看这个 skill 是否值得保留”

### `cek-anthropic-skill-best-practices`
- 适用场景：想按 Anthropic 风格完善 skill 结构和说明
- 怎么使用：说“按 Anthropic 最佳实践帮我改这个 skill”

### `cek-create-command`
- 适用场景：要做新的 command / slash command
- 怎么使用：说“帮我创建一个 command”“帮我设计这个命令的结构”

### `cek-create-hook`
- 适用场景：要创建 hook 或自动化校验逻辑
- 怎么使用：说“帮我做一个 hook”“帮我设计提交前自动检查”

### `cek-create-rule`
- 适用场景：某类错误总重复出现，想沉淀成规则
- 怎么使用：说“把这个问题沉淀成规则”“以后避免再犯这个错误”

### `cek-prompt-engineering`
- 适用场景：优化 prompt、命令描述、skill 描述
- 怎么使用：说“帮我优化这段 prompt”“让这个技能描述更容易触发”

### `cek-test-prompt`
- 适用场景：想验证 prompt 是否稳定、是否容易误解
- 怎么使用：说“帮我测一下这个 prompt”“看看这个描述会不会触发偏掉”

## 规划 / 实施 / 多代理协作类

### `cek-brainstorm`
- 适用场景：需求还模糊，先发散再收敛
- 怎么使用：说“先帮我脑暴一下这个方案”“把这个想法扩展开再收敛”

### `cek-do-competitively`
- 适用场景：希望多个方案竞争，再选最优
- 怎么使用：说“让多个方案竞争一下”“并行生成多个实现，再选最好一个”

### `cek-do-in-steps`
- 适用场景：复杂任务不适合一次做完，要分步推进
- 怎么使用：说“分步骤帮我完成”“按阶段推进这个任务”

### `cek-implement`
- 适用场景：已经有计划，进入实施阶段
- 怎么使用：说“按这个计划开始实现”“根据方案落代码”

### `cek-judge-with-debate`
- 适用场景：需要多轮辩论式评审，而不是一次性拍板
- 怎么使用：说“让不同立场辩论一下这个方案”“多轮评估后再给结论”

### `cek-launch-sub-agent`
- 适用场景：单个任务适合交给专门子代理处理
- 怎么使用：说“给这个任务起一个合适的子代理去做”“用子代理处理这个专项问题”

### `cek-multi-agent-patterns`
- 适用场景：你想知道一个复杂任务适合怎样拆成多代理协作
- 怎么使用：说“帮我设计这个任务的多代理协作模式”

### `cek-plan`
- 适用场景：把草稿需求整理成可落地计划
- 怎么使用：说“帮我做实施计划”“把这个需求整理成执行步骤”

### `cek-tree-of-thoughts`
- 适用场景：有多条思路，想系统探索再比较
- 怎么使用：说“把不同解法都展开比较”“树状探索一下这个问题”

## 评审 / 反思 / 质量改进类

### `cek-critique`
- 适用场景：你已经有一个方案或输出，想多角度挑毛病
- 怎么使用：说“帮我批判性审查这个方案”“从多个角度挑问题”

### `cek-reflect`
- 适用场景：前一步结果不够好，想反思后再优化
- 怎么使用：说“对刚才的结果做反思并优化”“重新审视刚才的回答”

## Git / Issue / Worktree 类

### `cek-analyze-issue`
- 适用场景：GitHub issue 还比较模糊，想先转成技术实现说明
- 怎么使用：说“分析一下这个 issue，整理成规格说明”

### `cek-attach-review-to-pr`
- 适用场景：把评审意见精确挂到 PR 具体代码行上
- 怎么使用：说“把 review 意见直接挂到 PR 行评论里”

### `cek-commit`
- 适用场景：要生成规范 commit message 并提交
- 怎么使用：说“帮我整理提交信息并 commit”

### `cek-compare-worktrees`
- 适用场景：要比较不同 worktree / 分支差异
- 怎么使用：说“比较这两个 worktree 的差别”

### `cek-create-pr`
- 适用场景：要创建 Pull Request
- 怎么使用：说“帮我创建 PR”“整理好标题和描述后发起 PR”

### `cek-create-worktree`
- 适用场景：想开一个新的 worktree 做并行开发
- 怎么使用：说“帮我创建一个新的 worktree 来做这个任务”

### `cek-load-issues`
- 适用场景：想把仓库里 open issues 拉下来做本地整理
- 怎么使用：说“加载当前仓库的 issues 到本地文档”

### `cek-merge-worktree`
- 适用场景：worktree 开发完成，准备合并回主工作区
- 怎么使用：说“把这个 worktree 的改动合并回来”

### `cek-notes`
- 适用场景：想给 commit 补充元信息，但不改 commit 历史
- 怎么使用：说“给这个 commit 加备注信息”“用 git notes 记录这次评审结果”

### `cek-worktrees`
- 适用场景：整体管理 worktree 工作流
- 怎么使用：说“帮我设计 worktree 工作流”“用 worktree 处理并行需求”

## 测试 / TDD 类

### `cek-fix-tests`
- 适用场景：测试已经挂了，需要系统修复
- 怎么使用：说“帮我系统修失败测试”“把当前 failing tests 修好”

### `cek-test-driven-development`
- 适用场景：想按 TDD 实现功能或修 bug
- 怎么使用：说“按 TDD 帮我做这个功能”“先写失败测试再实现”

### `cek-write-tests`
- 适用场景：已有改动但测试覆盖不足
- 怎么使用：说“帮我给这次改动补测试”

## 文档类

### `cek-update-docs`
- 适用场景：代码变了，文档也要同步
- 怎么使用：说“根据这次改动更新文档”“同步 README / docs”

### `cek-write-concisely`
- 适用场景：文档太啰嗦，想改得更清晰简洁
- 怎么使用：说“把这段文档写得更简洁专业”

## 分析 / 根因 / 持续改进类

### `cek-five-whys`
- 适用场景：要用“五个为什么”追根溯源
- 怎么使用：说“用五个为什么分析这个问题”

### `cek-kaizen`
- 适用场景：想做持续改进，而不是一次性大改
- 怎么使用：说“按持续改进思路优化这块设计”

### `cek-propose-hypotheses`
- 适用场景：问题还不明确，需要提出假设再验证
- 怎么使用：说“围绕这个问题提出几个假设并验证”

## FPF / 假设管理类

### `cek-fpf-query`
- 适用场景：要查看已有假设、结论、证据
- 怎么使用：说“查询一下 FPF 里的结论”“看看之前记录过什么假设”

### `cek-fpf-status`
- 适用场景：想看当前 FPF 知识库整体状态
- 怎么使用：说“查看当前 FPF 状态”

## MCP / 技术栈类

### `cek-build-mcp`
- 适用场景：想构建新的 MCP 服务
- 怎么使用：说“帮我设计并实现一个 MCP server”

### `cek-setup-context7-mcp`
- 适用场景：要配置 Context7 文档服务
- 怎么使用：说“帮我接入 Context7 MCP”

### `cek-setup-serena-mcp`
- 适用场景：要配置 Serena 语义检索能力
- 怎么使用：说“帮我配置 Serena MCP”

### `cek-typescript-best-practices`
- 适用场景：TypeScript 项目想补最佳实践规则
- 怎么使用：说“给这个 TS 项目补最佳实践规范”
