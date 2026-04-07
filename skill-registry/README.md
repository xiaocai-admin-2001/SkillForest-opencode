# SkillForest Registry 打包说明

这是 SkillForest 里的核心技能管理工具，主要给 OpenCode 使用，作用是：

- 维护 skills 注册表 CSV
- 提供可视化界面查看和管理 skills
- 支持远程搜索并一键安装 skill

## 它在 SkillForest 里的位置

你可以把这个目录理解成 SkillForest 的“管理器内核”，负责：

- 维护本地 skill 总表
- 提供图形界面
- 管理技能树视图
- 打开技能用途说明和分类索引

## 建议安装位置

把整个 `skill-registry` 文件夹放到：

- `%USERPROFILE%\.claude\skills\skill-registry`

## 启动方式

- Windows：双击 `launch_skill_registry_gui.bat`
- macOS：双击 `launch_skill_registry_gui.command`
- 或手动运行：

```bash
python "%USERPROFILE%\.claude\skills\skill-registry\skill_registry_gui.py"
```

macOS 也可以运行：

```bash
python3 "$HOME/.claude/skills/skill-registry/skill_registry_gui.py"
```

## 首次运行会自动创建

- `%USERPROFILE%\.claude\skills\SKILLS_REGISTRY.csv`
- `%USERPROFILE%\.claude\skills\SKILLS_REGISTRY_README.md`

## 依赖

- Python 3
- 如果要远程搜索或一键安装 skill，还需要：
  - `git`
  - `npx`

## macOS 兼容说明

- 已提供 `launch_skill_registry_gui.command` 作为 macOS 启动器
- 首次运行如果提示没有执行权限，可在终端执行：

```bash
chmod +x "$HOME/.claude/skills/skill-registry/launch_skill_registry_gui.command"
```

## 说明

这个打包版本已经去掉了对固定用户名路径的依赖，会自动按当前用户目录运行。
