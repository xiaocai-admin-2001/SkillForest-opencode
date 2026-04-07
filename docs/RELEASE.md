# SkillForest 发布说明

这份文档说明如何把 SkillForest 打包成一个可以直接发给别人的发布包。

## 推荐发布内容

一个完整的 SkillForest 发布包建议包含：

- `skill-registry/`
  - 技能管理 GUI
  - Windows 启动器
  - macOS 启动器
- `skills/`
  - 当前本地 skills 快照
- `docs/`
  - 安装说明
  - 注册表说明
  - 使用指南
  - 分类索引
  - 注册表模板

## 两种发布模式

### 1. 轻量版

适合只发管理功能：

- `skill-registry/`
- `docs/INSTALL.md`
- `docs/SKILLS_REGISTRY_README.md`

### 2. 完整版

适合把你当前整套技能库一起发给别人：

- `skill-registry/`
- `skills/`
- `docs/`

## 自动打包脚本

仓库里提供了一个发布打包脚本：

- `tools/package_skillforest_release.py`

运行方式：

```bash
python tools/package_skillforest_release.py
```

默认会在当前用户目录生成：

- `C:\Users\Administrator\SkillForest-release`
- `C:\Users\Administrator\SkillForest-release.zip`

在其他机器上运行时，会自动按当前用户目录生成对应输出，不依赖固定用户名。

## 发布前建议检查

- GUI 是否能正常启动
- `docs/INSTALL.md` 是否还是最新
- `skills/SKILLS_REGISTRY.csv` 是否已同步
- 新增 skill 的 `Purpose` 是否已经是中文

## 推荐对外说明

发给别人时建议附带一句话：

> 先看 `docs/INSTALL.md`，再把 `skill-registry/` 复制到 `%USERPROFILE%\.claude\skills\skill-registry`，需要整套技能库的话再复制 `skills/`。
