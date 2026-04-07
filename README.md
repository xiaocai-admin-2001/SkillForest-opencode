# SkillForest

SkillForest 是一个面向 OpenCode 的本地技能库管理仓库，提供：

- 本地 skills 注册表
- 可视化技能管理界面
- 技能树分类与说明文档
- 当前本地 skills 快照同步

## 你可以用它做什么

- 查看当前装了哪些 skill
- 按技能树分类浏览 skills
- 远程搜索 skill 并一键导入本地
- 删除、登记、同步、整理本地 skill 库
- 查看每个 skill 的适用场景和使用方式

## 快速导航

| 入口 | 作用 |
| --- | --- |
| `skill-registry/` | 核心功能目录，包含 GUI、启动器、注册表维护逻辑 |
| `skills/` | 当前本地 OpenCode skills 的同步快照 |
| `docs/INSTALL.md` | 安装说明，告诉别人如何落地这套能力 |
| `docs/SKILLS_REGISTRY_README.md` | 注册表结构、字段、维护规则说明 |
| `docs/SKILLS_USAGE_GUIDE.md` | 每个主要 skill 的适用场景与使用方法 |
| `docs/CEK_SKILLS_INDEX.md` | CEK 系列 skills 的分类索引 |
| `docs/SKILLS_REGISTRY.template.csv` | 注册表模板 |

## 推荐阅读顺序

如果你是第一次看这个仓库，建议按这个顺序：

1. `docs/INSTALL.md`
2. `skill-registry/README.md`
3. `docs/SKILLS_REGISTRY_README.md`
4. `docs/SKILLS_USAGE_GUIDE.md`
5. `docs/CEK_SKILLS_INDEX.md`

## 核心目录说明

### `skill-registry/`

这是整个仓库的核心工具目录，主要包含：

- `SKILL.md`：skill 说明文件
- `skill_registry_gui.py`：图形界面主程序
- `launch_skill_registry_gui.bat`：Windows 启动器
- `README.md`：这个功能包自己的说明文档

### `skills/`

这是当前本地 `.claude/skills` 的同步快照，方便：

- 做备份
- 做迁移
- 发给别人直接复用
- 后续统一整理和筛选

### `docs/`

这里放的是“怎么看”和“怎么用”的说明文档，而不是程序本体。

## 安装方式

把下面目录复制到目标机器：

- `skill-registry/` -> `%USERPROFILE%\.claude\skills\skill-registry`

如果你还想把当前技能库一并同步过去，也可以复制：

- `skills/` -> `%USERPROFILE%\.claude\skills`

详细步骤看：

- `docs/INSTALL.md`

## 启动 GUI

Windows 下可以直接双击：

- `skill-registry/launch_skill_registry_gui.bat`

或者运行：

```bash
python "%USERPROFILE%\.claude\skills\skill-registry\skill_registry_gui.py"
```

## 当前仓库特点

- 中文说明优先
- 支持技能树展示
- 支持注册表维护
- 支持远程搜索与本地导入
- 支持和你当前本地 skill 库保持同步

## 适合谁用

- 想维护自己本地 OpenCode skills 的人
- 想把 skill 库发给别人复用的人
- 想做技能树分类、用途说明、注册表管理的人
- 想把多个 skill 仓库整理成统一本地库的人

## 核心推荐技能

如果你第一次使用这套技能库，建议优先关注这些高频核心 skill：

| Skill | 作用 |
| --- | --- |
| `humanizer` | 把文案、说明、周报改得更自然、更像人写的 |
| `find-skills` | 按需求搜索适合的新 skill |
| `skill-creator` | 创建、重构、优化 skill |
| `skill-registry` | 管理本地 skills、维护注册表、打开 GUI |
| `cek-context-engineering` | 优化 prompt、command、skill 的上下文设计 |
| `cek-review-local-changes` | 评审当前本地未提交代码 |
| `cek-root-cause-tracing` | 沿调用链倒推 bug 根因 |
| `cek-do-in-parallel` | 把任务拆成并行子任务执行 |
| `sp-systematic-debugging` | 用系统化方法定位复杂问题 |
| `tob-codeql` | 做静态安全分析和漏洞审计 |

如果你偏工程交付，也建议优先看：

- `cek-plan`
- `cek-implement`
- `cek-create-pr`
- `devops-dockerfile-generator`
- `devops-k8s-yaml-validator`

## 后续可以继续做的方向

- 增加“核心推荐技能”精简清单
- 增加更完整的图标和界面美化
- 增加导入/导出配置能力
- 增加技能搜索结果预览和批量安装
