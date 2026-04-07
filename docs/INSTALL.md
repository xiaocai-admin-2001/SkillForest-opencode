# 安装说明

这份仓库同步了当前本地 OpenCode skills 的一整套功能，包括：

- `skill-registry` 可视化管理界面
- 当前本地 skills 快照
- 注册表说明、用途说明、分类索引

## 一、安装 `skill-registry`

把仓库里的目录复制到你的用户目录：

- `skill-registry/` -> `%USERPROFILE%\.claude\skills\skill-registry`

如果你想直接带上当前全部 skills，也可以把下面整个目录一起复制：

- `skills/` -> `%USERPROFILE%\.claude\skills`

注意：如果目标目录已有文件，请先备份再覆盖。

## 二、启动图形界面

安装完成后，可以直接双击：

- `%USERPROFILE%\.claude\skills\skill-registry\launch_skill_registry_gui.bat`

或者运行：

```bash
python "%USERPROFILE%\.claude\skills\skill-registry\skill_registry_gui.py"
```

## 三、首次运行会生成 / 使用这些文件

- `%USERPROFILE%\.claude\skills\SKILLS_REGISTRY.csv`
- `%USERPROFILE%\.claude\skills\SKILLS_REGISTRY_README.md`
- `%USERPROFILE%\.claude\skills\SKILLS_USAGE_GUIDE.md`
- `%USERPROFILE%\.claude\skills\CEK_SKILLS_INDEX.md`

## 四、依赖要求

- Python 3
- 如果要远程搜索或一键安装 skill，还需要：
  - `git`
  - `npx`

## 五、仓库目录说明

- `skill-registry/`
  - 图形界面和核心 skill 说明
- `skills/`
  - 当前本地 skills 的同步快照
- `docs/SKILLS_REGISTRY_README.md`
  - 技能注册表说明
- `docs/SKILLS_USAGE_GUIDE.md`
  - 技能适用场景与使用方式
- `docs/CEK_SKILLS_INDEX.md`
  - CEK 技能分类索引
- `docs/SKILLS_REGISTRY.template.csv`
  - 注册表模板

## 六、推荐同步方式

如果你要发给别人使用，推荐两种方式：

1. 只发 `skill-registry/`
   - 适合只分享管理功能
2. 发 `skill-registry/ + skills/ + docs/`
   - 适合完整同步你当前这套本地 skills 体系
