# OpenCode Skills 清单说明

这个目录下的 skills 使用一张总表统一维护：

- `C:\Users\Administrator\.claude\skills\SKILLS_REGISTRY.csv`

你可以把它理解成 skills 的主数据库，设计思路类似 `E:\awesome-opencode-main` 里的资源总表。

## 这张表是干什么的

- 记录当前安装了哪些 OpenCode skills
- 记录每个 skill 的来源、路径、安装时间和最近更新时间
- 方便后续新增、更新、删除 skill 时统一管理
- 便于以后继续做自动生成说明页、搜索、筛选、导出

## 主表位置

- `C:\Users\Administrator\.claude\skills\SKILLS_REGISTRY.csv`

## 字段说明

- `ID`：唯一编号，例如 `skill-001`
- `Skill`：skill 名称，通常与目录名一致
- `Status`：当前状态，通常是 `active` 或 `removed`
- `Agent`：所属 agent，目前这张表默认记录 `OpenCode`
- `Source`：skill 的来源地址或安装来源
- `LocalPath`：本地目录的绝对路径
- `Installed`：首次安装日期
- `LastUpdated`：最近一次变更日期
- `Purpose`：一句话描述 skill 的用途，必须使用中文
- `Notes`：补充说明，比如安装方式、是否做过本地修改

## 维护规则

- 新装一个 skill，就新增一行
- 更新一个 skill，就更新这一行的 `LastUpdated`
- 删除 skill 时，不删历史行，只把 `Status` 改成 `removed`
- `Installed` 保留第一次安装时间，不要覆盖
- `Purpose` 尽量从该 skill 的 `SKILL.md` 描述中提炼，并统一改成中文

## 配套 skill

用于维护这张表的 skill 在这里：

- `C:\Users\Administrator\.claude\skills\skill-registry\SKILL.md`

## 可视化界面

如果你想更方便地查看、打开目录、刷新、删除 skill，可以直接启动图形界面：

- 脚本：`C:\Users\Administrator\.claude\skills\skill-registry\skill_registry_gui.py`
- 启动器：`C:\Users\Administrator\.claude\skills\skill-registry\launch_skill_registry_gui.bat`
- macOS 启动器：`$HOME/.claude/skills/skill-registry/launch_skill_registry_gui.command`
- 启动器现在会使用 `pythonw` 启动图形界面，正常情况下不会再弹出黑色控制台窗口

界面支持：

- 按技能树查看当前 skill 列表
- 使用中文别名显示 skill（同时保留原始 skill 名）
- 把状态和归属按中文显示
- 查看每个 skill 的详细信息
- 新增 skill（支持 GitHub 克隆或本地目录导入）
- 通过远程搜索查找 skill，并一键安装到本地 OpenCode skills
- 编辑 skill 的来源、用途、备注
- 打开 skill 目录
- 打开注册表 CSV
- 同步目录与注册表
- 打开 Skills 使用说明
- 删除 skill（删除时会移动到 `C:\Users\Administrator\.claude\skills\.trash`）

## 常见问题

- 如果点击远程搜索时报“找不到命令”，通常是系统里没有正确找到 `npx` 或 `git`
- 现在界面会优先自动解析命令路径，并在 Windows 下尝试通过 `cmd /c` 调用
- 如果某些命令输出带有 GBK/UTF-8 混合字符，界面会按 UTF-8 忽略非法字节解码，避免搜索时崩溃
- 如果你刚更新过脚本，请关闭旧界面后重新启动一次再试

当你以后安装、复制、更新、删除 skill 时，应该同步更新这张 CSV 表。

## CEK 技能索引

如果你想查看从 `context-engineering-kit` 精选整理出的技能分类说明，可以看：

- `C:\Users\Administrator\.claude\skills\CEK_SKILLS_INDEX.md`

## Skills 使用说明

如果你想知道“什么情况下可以使用哪个 skill、应该怎么提需求更容易触发”，可以看：

- `C:\Users\Administrator\.claude\skills\SKILLS_USAGE_GUIDE.md`

## 日常怎么看

平时直接看下面这个文件就可以：

- `C:\Users\Administrator\.claude\skills\SKILLS_REGISTRY.csv`

如果想看说明，再看这个文件：

- `C:\Users\Administrator\.claude\skills\SKILLS_REGISTRY_README.md`
