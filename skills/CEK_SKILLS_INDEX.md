# Context Engineering Kit 技能索引

这份索引整理了从 `https://github.com/NeoLabHQ/context-engineering-kit` 引入到本地 OpenCode skill 库中的核心 skill，方便按类别快速查找。

## 核心优先推荐

- `cek-context-engineering`：理解和优化 commands、skills、sub-agents 的上下文工程
- `cek-create-skill`：指导创建新的 skill 并验证可用性
- `cek-test-skill`：测试 skill 在真实场景下是否可靠
- `cek-review-local-changes`：评审当前未提交代码并给出改进建议
- `cek-review-pr`：使用多代理方式评审 Pull Request
- `cek-do-in-parallel`：并行启动多个子代理处理独立任务
- `cek-root-cause-tracing`：沿调用链回溯问题根因并定位原始触发点
- `cek-thought-based-reasoning`：处理复杂推理任务时提供系统化思考方法

## Skill / Prompt / Agent 开发类

- `cek-agent-evaluation`：评估和改进 commands、skills、agents 的效果
- `cek-anthropic-skill-best-practices`：按 Anthropic 最佳实践完善 skill 结构和写法
- `cek-context-engineering`：理解和优化 commands、skills、sub-agents 的上下文工程
- `cek-create-command`：指导创建新的 command 并补齐结构规范
- `cek-create-hook`：指导创建和配置 hook
- `cek-create-rule`：把重复问题沉淀成长期可复用的规则
- `cek-create-skill`：指导创建新的 skill 并验证可用性
- `cek-prompt-engineering`：改进 prompts、commands 和技能说明的质量
- `cek-test-prompt`：测试 prompt、commands、skills 的触发和输出质量
- `cek-test-skill`：测试 skill 在真实场景下是否可靠

## 规划 / 实施 / 多代理协作类

- `cek-brainstorm`：把模糊想法逐步澄清成可执行设计
- `cek-do-competitively`：让多个子代理竞争生成方案再综合优胜结果
- `cek-do-in-parallel`：并行启动多个子代理处理独立任务
- `cek-do-in-steps`：把复杂任务拆成顺序步骤交给子代理执行
- `cek-implement`：按计划实施任务并配合校验
- `cek-judge-with-debate`：通过多轮辩论式评审比较多个方案
- `cek-launch-sub-agent`：按任务复杂度智能启动合适的子代理
- `cek-multi-agent-patterns`：设计适合复杂任务的多代理协作模式
- `cek-plan`：把草稿任务整理成可实施计划
- `cek-tree-of-thoughts`：通过树状探索方式系统比较多条解题路径

## 评审 / 反思 / 质量改进类

- `cek-critique`：用多视角评审方式审查当前方案或结果
- `cek-reflect`：对上一步输出做反思并迭代优化
- `cek-review-local-changes`：评审当前未提交代码并给出改进建议
- `cek-review-pr`：使用多代理方式评审 Pull Request

## Git / Issue / Worktree 类

- `cek-analyze-issue`：分析 GitHub issue 并整理技术规格说明
- `cek-attach-review-to-pr`：把评审意见按行挂到 Pull Request 上
- `cek-commit`：生成结构化提交信息并完成 git commit
- `cek-compare-worktrees`：比较不同 git worktree 或分支之间的差异
- `cek-create-pr`：通过 GitHub CLI 创建规范的 Pull Request
- `cek-create-worktree`：创建并初始化 git worktree 用于并行开发
- `cek-load-issues`：加载 GitHub 开放 issue 并保存为本地文档
- `cek-merge-worktree`：把 worktree 中的改动安全合并回当前分支
- `cek-notes`：给 git 提交补充 notes 元数据而不改历史
- `cek-worktrees`：使用 git worktree 管理并行开发目录

## 测试 / TDD 类

- `cek-fix-tests`：系统化修复当前失败的测试
- `cek-test-driven-development`：按测试驱动开发方式实现功能或修复问题
- `cek-write-tests`：为本地代码改动补齐测试覆盖

## 文档类

- `cek-update-docs`：根据本地代码变更同步更新文档
- `cek-write-concisely`：把文档写得更清晰简洁专业

## 分析 / 根因 / 持续改进类

- `cek-five-whys`：使用五个为什么方法追查问题根因
- `cek-kaizen`：以持续改进思路优化代码设计流程和实现
- `cek-propose-hypotheses`：围绕问题提出假设并推进完整验证循环
- `cek-root-cause-tracing`：沿调用链回溯问题根因并定位原始触发点

## FPF / 假设管理类

- `cek-fpf-query`：查询 FPF 知识库中的假设和结论
- `cek-fpf-status`：查看当前 FPF 知识库状态

## MCP / 技术栈类

- `cek-build-mcp`：指导构建高质量 MCP 服务
- `cek-setup-context7-mcp`：配置 Context7 MCP 文档服务
- `cek-setup-serena-mcp`：配置 Serena MCP 语义检索服务
- `cek-typescript-best-practices`：把 TypeScript 最佳实践写入项目规则

## 本地路径

这些 skill 当前都位于：

- `C:\Users\Administrator\.claude\skills`

完整注册信息见：

- `C:\Users\Administrator\.claude\skills\SKILLS_REGISTRY.csv`
