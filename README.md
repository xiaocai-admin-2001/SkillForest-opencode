# SkillForest

SkillForest 是一套面向 OpenCode 的本地技能库管理方案。它把分散的 skills、注册表、说明文档和可视化管理界面整理到一个仓库里，方便你长期维护、迁移和复用。

## 它解决什么问题

如果你的本地 skills 越装越多，很快就会遇到这些问题：

- 不知道现在到底装了哪些 skill
- 看不懂 skill 名称，前缀太多，说明太弱
- 想搜索、分类、筛选、整理，但没有统一入口
- 技能库可以用，却很难维护、迁移、分享

SkillForest 的目标很简单：让本地 skills 变成一套可管理、可观察、可持续优化的技能森林。

## 当前包含的核心能力

- 本地 skills 注册表
- 可视化技能管理界面
- 技能分类、用途说明和来源记录
- 远程搜索并导入新 skill
- 技能使用频率、评分和运营面板
- 当前本地技能库的同步快照

## 你可以直接做什么

- 查看当前安装了哪些 skill
- 按分类浏览和筛选技能
- 搜索远程 skill 并导入本地
- 删除、登记、同步、整理本地 skill 库
- 查看每个 skill 的用途、来源和最近使用情况
- 根据使用频率和评分识别高频 skill、沉睡 skill 和待清理 skill

## 快速导航

| 路径 | 作用 |
| --- | --- |
| `skill-registry/` | 核心目录，包含 GUI、启动器、注册表维护逻辑 |
| `skills/` | 当前本地 OpenCode skills 的同步快照 |
| `docs/INSTALL.md` | 安装说明 |
| `docs/SKILLS_REGISTRY_README.md` | 注册表结构、字段和维护规则 |
| `docs/SKILLS_USAGE_GUIDE.md` | 常用 skill 的适用场景和用法 |
| `docs/CEK_SKILLS_INDEX.md` | CEK 系列技能索引 |
| `docs/SKILLS_REGISTRY.template.csv` | 注册表模板 |
| `docs/RELEASE.md` | 打包和发布说明 |
| `tools/package_skillforest_release.py` | 一键生成发布目录和 zip 包 |
| `tools/sync_to_claude_skills.py` | 把仓库内 `skills/` 同步到本机运行目录 |
| `tools/sync_to_claude_skills.bat` | Windows 下一键同步本机 skill 目录 |

## 建议阅读顺序

第一次看这个仓库，建议按这个顺序：

1. `docs/INSTALL.md`
2. `skill-registry/README.md`
3. `docs/SKILLS_REGISTRY_README.md`
4. `docs/SKILLS_USAGE_GUIDE.md`
5. `docs/CEK_SKILLS_INDEX.md`

## 仓库结构

### `skill-registry/`

这是整个项目的核心。这里放的是技能注册表维护和图形界面相关文件。

- `SKILL.md`：skill 说明文件
- `skill_registry_gui.py`：图形界面主程序
- `launch_skill_registry_gui.bat`：Windows 启动器
- `launch_skill_registry_gui.command`：macOS 启动器
- `README.md`：这个模块自己的说明文档

### `skills/`

这是当前本地 `.claude/skills` 的同步快照，适合：

- 做备份
- 做迁移
- 分享给别人直接复用
- 统一整理多来源的 skills

## 推荐维护方式

建议只维护这一处：

- 仓库内的 `skills/`

不要把 `~/.claude/skills` 当成手工编辑目录。更推荐的工作流是：

1. 只修改仓库里的 `skills/<skill-name>/`
2. 提交并推送仓库
3. 用同步脚本把仓库内容发布到本机运行目录

这样可以避免“本地运行目录”和 Git 仓库各改一份导致内容分叉。

## 同步到本机运行目录

仓库已经提供同步脚本，路径都以仓库根目录为基准，不依赖某个人的绝对路径。

在仓库根目录下：

Windows：

```bat
tools\sync_to_claude_skills.bat
```

只预览、不真正写入：

```bat
tools\sync_to_claude_skills.bat --dry-run
```

Python 方式：

```bash
python tools/sync_to_claude_skills.py --prune
```

脚本行为：

- 源目录：仓库内 `skills/`
- 目标目录：当前用户主目录下的 `.claude/skills`
- 默认保留 `skill-registry/` 等运行支撑目录
- `--prune` 会删除本机运行目录中仓库里不存在的 skill

这样不同人的机器只要仓库位置正确，脚本都会自动同步到各自用户目录下的 `.claude/skills`。

### `docs/`

这里放的是使用说明、结构说明和发布说明，不是程序本体。

## GUI 现在能做什么

当前界面已经支持：

- 左侧分类导航
- 中间技能卡片浏览
- 右侧详情面板
- 远程搜索和一键安装
- 鼠标滚轮浏览卡片
- 按添加时间、评分、使用次数排序
- 自动读取 OpenCode 真实 skill 调用记录
- 统计每个 skill 的使用次数、最近使用时间和评分
- 展示技能运营面板，包括高频技能、近 7 天活跃、沉睡技能和总调用次数

## 安装方式

至少复制下面这个目录到目标机器：

- `skill-registry/` -> 当前用户主目录下的 `.claude/skills/skill-registry`

如果你还想把当前技能库一起同步过去，再复制：

- `skills/` -> 当前用户主目录下的 `.claude/skills`

详细步骤见 `docs/INSTALL.md`。

## 启动 GUI

Windows：

- `skill-registry/launch_skill_registry_gui.bat`

macOS：

- `skill-registry/launch_skill_registry_gui.command`

也可以手动运行：

```bash
python "%USERPROFILE%\.claude\skills\skill-registry\skill_registry_gui.py"
```

macOS 下：

```bash
python3 "$HOME/.claude/skills/skill-registry/skill_registry_gui.py"
```

## 适合谁用

- 想维护自己本地 OpenCode skills 的人
- 想把 skill 库发给别人复用的人
- 想做技能分类、用途说明和注册表管理的人
- 想把多个 skill 仓库整理成统一本地库的人

## 推荐先关注的技能

如果你刚开始使用这套技能库，建议先关注这些高频核心 skill：

| Skill | 作用 |
| --- | --- |
| `humanizer` | 把文案、说明、周报改得更自然 |
| `find-skills` | 按需求搜索适合的新 skill |
| `skill-creator` | 创建、重构和优化 skill |
| `skill-registry` | 管理本地 skills、维护注册表、打开 GUI |
| `cek-context-engineering` | 优化 prompt、command、skill 的上下文设计 |
| `cek-review-local-changes` | 评审当前本地未提交代码 |
| `cek-root-cause-tracing` | 沿调用链倒推 bug 根因 |
| `cek-do-in-parallel` | 把任务拆成并行子任务执行 |
| `sp-systematic-debugging` | 用系统化方法定位复杂问题 |
| `tob-codeql` | 做静态安全分析和漏洞审计 |

如果你更偏工程交付，也建议优先看：

- `cek-plan`
- `cek-implement`
- `cek-create-pr`
- `devops-dockerfile-generator`
- `devops-k8s-yaml-validator`

## 当前状态

这不是一个展示型仓库，而是一套正在持续打磨的本地技能管理工作台。重点不在“列出所有 skill”，而在于：

- 让 skill 看得懂
- 让 skill 找得到
- 让 skill 用得起来
- 让 skill 的价值能被观察和整理
