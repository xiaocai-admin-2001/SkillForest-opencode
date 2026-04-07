# skill-

这是一个用于管理和维护本地 OpenCode skills 的仓库，核心提供了一个 `skill-registry` 功能包，用来：

- 维护 skills 注册表 CSV
- 提供可视化界面管理本地 skills
- 支持远程搜索、导入、删除和登记 skills
- 提供技能索引和使用说明文档

## 主要内容

- `skill-registry/`
  - 图形界面
  - skill 注册表维护逻辑
  - 启动脚本
- `docs/SKILLS_REGISTRY_README.md`
  - 技能注册表说明
- `docs/SKILLS_USAGE_GUIDE.md`
  - 常用 skill 的适用场景与使用方式
- `docs/CEK_SKILLS_INDEX.md`
  - CEK 技能分类索引

## 建议安装位置

把 `skill-registry` 目录放到：

- `%USERPROFILE%\.claude\skills\skill-registry`

## 启动方式

```bash
python "%USERPROFILE%\.claude\skills\skill-registry\skill_registry_gui.py"
```

或者直接双击：

- `launch_skill_registry_gui.bat`

## 说明

这个仓库里的 GUI 与说明文档已经按当前用户目录工作，不依赖固定用户名路径。
