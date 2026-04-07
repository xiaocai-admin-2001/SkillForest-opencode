---
name: skill-registry
description: |
  当安装、更新、删除、复制或盘点 OpenCode skills 时使用。这个 skill
  会维护一份类似 awesome-opencode 资源表的技能清单文件：
  `C:\Users\Administrator\.claude\skills\SKILLS_REGISTRY.csv`。
---

# Skill Registry

这个 skill 用来维护 OpenCode 的技能总表。

主表文件：

- `C:\Users\Administrator\.claude\skills\SKILLS_REGISTRY.csv`

你可以把它理解成一个小型的 skills 数据库。每个 skill 占一行，后续新增、更新、删除都在这个 CSV 里维护，方式类似 `E:\awesome-opencode-main` 里的资源总表。

## 什么时候使用

出现以下场景时必须使用这个 skill：

- 安装一个新的 skill
- 把 skill 复制到 `C:\Users\Administrator\.claude\skills`
- 更新已有 skill
- 删除 skill
- 盘点当前已安装的 skill
- 用户要求查看或刷新 OpenCode skills 清单

## 固定工作流

1. 先扫描 `C:\Users\Administrator\.claude\skills`。
2. 读取 `C:\Users\Administrator\.claude\skills\SKILLS_REGISTRY.csv`。
3. 根据本次变更，新增或更新对应的 CSV 行。
4. 如果 skill 被删除，不要删历史记录，只把 `Status` 改成 `removed`。
5. 保持 CSV 是结构化表，不要改成自然语言列表。

## CSV 字段

字段顺序必须保持如下：

`ID,Skill,Status,Agent,Source,LocalPath,Installed,LastUpdated,Purpose,Notes`

## 字段含义

- `ID`：稳定编号，例如 `skill-001`
- `Skill`：skill 名称，通常等于目录名
- `Status`：通常写 `active` 或 `removed`
- `Agent`：当前这张表默认写 `OpenCode`
- `Source`：原始来源，例如 GitHub 仓库地址或安装来源
- `LocalPath`：本地绝对路径，使用 Windows 路径
- `Installed`：首次安装日期，格式 `YYYY-MM-DD`
- `LastUpdated`：最近一次更新日期，格式 `YYYY-MM-DD`
- `Purpose`：一句话说明这个 skill 的用途，必须使用中文
- `Notes`：补充说明，例如安装方式、是否做过本地改动

## 更新规则

- 修改已有 skill 时，保留原来的 `Installed`
- 每次变更都要更新 `LastUpdated`
- 新增 skill 时，分配下一个可用的 `skill-XXX`
- `Purpose` 优先从该 skill 的 `SKILL.md` 描述中提炼，并统一改成中文
- 如果来源不清楚，`Source` 写 `manual`，并在 `Notes` 里补充说明

## 输出要求

更新完表之后，简短说明：

- 哪个 skill 发生了变化
- 这是新增、更新还是删除
- 更新的是哪个 CSV 文件

只要用户要求安装或调整 skill，就不能跳过这张表的更新。

## 可视化管理

这个 skill 自带一个图形界面，路径如下：

- `C:\Users\Administrator\.claude\skills\skill-registry\skill_registry_gui.py`
- `C:\Users\Administrator\.claude\skills\skill-registry\launch_skill_registry_gui.bat`

图形界面可以用于：

- 查看当前 skill 列表
- 查看详细信息
- 新增 skill（支持 GitHub 克隆和本地目录导入）
- 利用远程搜索查找 skill，并选择后安装到本地 OpenCode 目录
- 编辑已有 skill 的来源、用途、备注
- 打开 skill 目录
- 打开注册表 CSV
- 同步技能目录与注册表
- 删除 skill（移动到 `.trash` 目录）
