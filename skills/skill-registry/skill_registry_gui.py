import csv
import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk


USER_HOME = Path.home()
BASE_DIR = USER_HOME / ".claude" / "skills"
REGISTRY_PATH = BASE_DIR / "SKILLS_REGISTRY.csv"
README_PATH = BASE_DIR / "SKILLS_REGISTRY_README.md"
USAGE_GUIDE_PATH = BASE_DIR / "SKILLS_USAGE_GUIDE.md"
TRASH_DIR = BASE_DIR / ".trash"
AGENTS_SKILLS_DIR = USER_HOME / ".agents" / "skills"
NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0)

CSV_FIELDS = [
    "ID",
    "Skill",
    "Status",
    "Agent",
    "Source",
    "LocalPath",
    "Installed",
    "LastUpdated",
    "Purpose",
    "Notes",
]

EXCLUDED_NAMES = {
    ".trash",
    "SKILLS_REGISTRY.csv",
    "SKILLS_REGISTRY_README.md",
}

KNOWN_PURPOSE_MAP = {
    "humanizer": "把文字改写得更自然更像人写的",
    "find-skills": "搜索并安装更多 agent skills",
    "skill-creator": "创建改进和评估自定义 skill",
    "skill-registry": "维护技能注册表并提供可视化管理界面",
    "cek-agent-evaluation": "评估和改进 commands、skills、agents 的效果",
    "cek-analyze-issue": "分析 GitHub issue 并整理技术规格说明",
    "cek-anthropic-skill-best-practices": "按 Anthropic 最佳实践完善 skill 结构和写法",
    "cek-attach-review-to-pr": "把评审意见按行挂到 Pull Request 上",
    "cek-brainstorm": "把模糊想法逐步澄清成可执行设计",
    "cek-build-mcp": "指导构建高质量 MCP 服务",
    "cek-commit": "生成结构化提交信息并完成 git commit",
    "cek-compare-worktrees": "比较不同 git worktree 或分支之间的差异",
    "cek-context-engineering": "理解和优化 commands、skills、sub-agents 的上下文工程",
    "cek-create-command": "指导创建新的 command 并补齐结构规范",
    "cek-create-hook": "指导创建和配置 hook",
    "cek-create-pr": "通过 GitHub CLI 创建规范的 Pull Request",
    "cek-create-rule": "把重复问题沉淀成长期可复用的规则",
    "cek-create-skill": "指导创建新的 skill 并验证可用性",
    "cek-create-worktree": "创建并初始化 git worktree 用于并行开发",
    "cek-critique": "用多视角评审方式审查当前方案或结果",
    "cek-do-competitively": "让多个子代理竞争生成方案再综合优胜结果",
    "cek-do-in-parallel": "并行启动多个子代理处理独立任务",
    "cek-do-in-steps": "把复杂任务拆成顺序步骤交给子代理执行",
    "cek-five-whys": "使用五个为什么方法追查问题根因",
    "cek-fix-tests": "系统化修复当前失败的测试",
    "cek-fpf-query": "查询 FPF 知识库中的假设和结论",
    "cek-fpf-status": "查看当前 FPF 知识库状态",
    "cek-implement": "按计划实施任务并配合校验",
    "cek-judge-with-debate": "通过多轮辩论式评审比较多个方案",
    "cek-kaizen": "以持续改进思路优化代码设计流程和实现",
    "cek-launch-sub-agent": "按任务复杂度智能启动合适的子代理",
    "cek-load-issues": "加载 GitHub 开放 issue 并保存为本地文档",
    "cek-merge-worktree": "把 worktree 中的改动安全合并回当前分支",
    "cek-multi-agent-patterns": "设计适合复杂任务的多代理协作模式",
    "cek-notes": "给 git 提交补充 notes 元数据而不改历史",
    "cek-plan": "把草稿任务整理成可实施计划",
    "cek-prompt-engineering": "改进 prompts、commands 和技能说明的质量",
    "cek-propose-hypotheses": "围绕问题提出假设并推进完整验证循环",
    "cek-reflect": "对上一步输出做反思并迭代优化",
    "cek-review-local-changes": "评审当前未提交代码并给出改进建议",
    "cek-review-pr": "使用多代理方式评审 Pull Request",
    "cek-root-cause-tracing": "沿调用链回溯问题根因并定位原始触发点",
    "cek-setup-context7-mcp": "配置 Context7 MCP 文档服务",
    "cek-setup-serena-mcp": "配置 Serena MCP 语义检索服务",
    "cek-test-driven-development": "按测试驱动开发方式实现功能或修复问题",
    "cek-test-prompt": "测试 prompt、commands、skills 的触发和输出质量",
    "cek-test-skill": "测试 skill 在真实场景下是否可靠",
    "cek-thought-based-reasoning": "处理复杂推理任务时提供系统化思考方法",
    "cek-tree-of-thoughts": "通过树状探索方式系统比较多条解题路径",
    "cek-typescript-best-practices": "把 TypeScript 最佳实践写入项目规则",
    "cek-update-docs": "根据本地代码变更同步更新文档",
    "cek-worktrees": "使用 git worktree 管理并行开发目录",
    "cek-write-concisely": "把文档写得更清晰简洁专业",
    "cek-write-tests": "为本地代码改动补齐测试覆盖",
}

KNOWN_DISPLAY_NAME_MAP = {
    "humanizer": "文案自然化",
    "find-skills": "技能搜索",
    "skill-creator": "技能创建器",
    "skill-registry": "技能注册表",
    "cek-agent-evaluation": "技能效果评估",
    "cek-analyze-issue": "Issue 技术分析",
    "cek-anthropic-skill-best-practices": "Anthropic 技能最佳实践",
    "cek-attach-review-to-pr": "PR 行级评审挂载",
    "cek-brainstorm": "方案脑暴",
    "cek-build-mcp": "MCP 构建",
    "cek-commit": "规范提交",
    "cek-compare-worktrees": "Worktree 差异比较",
    "cek-context-engineering": "上下文工程",
    "cek-create-command": "创建命令",
    "cek-create-hook": "创建 Hook",
    "cek-create-pr": "创建 Pull Request",
    "cek-create-rule": "创建规则",
    "cek-create-skill": "创建技能",
    "cek-create-worktree": "创建 Worktree",
    "cek-critique": "多视角评审",
    "cek-do-competitively": "竞争式执行",
    "cek-do-in-parallel": "并行执行",
    "cek-do-in-steps": "分步执行",
    "cek-five-whys": "五个为什么",
    "cek-fix-tests": "修复测试",
    "cek-fpf-query": "FPF 查询",
    "cek-fpf-status": "FPF 状态",
    "cek-implement": "按计划实施",
    "cek-judge-with-debate": "辩论式评审",
    "cek-kaizen": "持续改进",
    "cek-launch-sub-agent": "启动子代理",
    "cek-load-issues": "加载 Issues",
    "cek-merge-worktree": "合并 Worktree",
    "cek-multi-agent-patterns": "多代理模式",
    "cek-notes": "Git Notes",
    "cek-plan": "实施计划",
    "cek-prompt-engineering": "Prompt 工程",
    "cek-propose-hypotheses": "提出假设",
    "cek-reflect": "反思优化",
    "cek-review-local-changes": "本地改动评审",
    "cek-review-pr": "PR 评审",
    "cek-root-cause-tracing": "根因回溯",
    "cek-setup-context7-mcp": "配置 Context7 MCP",
    "cek-setup-serena-mcp": "配置 Serena MCP",
    "cek-test-driven-development": "测试驱动开发",
    "cek-test-prompt": "测试 Prompt",
    "cek-test-skill": "测试技能",
    "cek-thought-based-reasoning": "系统化推理",
    "cek-tree-of-thoughts": "思维树探索",
    "cek-typescript-best-practices": "TypeScript 最佳实践",
    "cek-update-docs": "更新文档",
    "cek-worktrees": "Worktree 工作流",
    "cek-write-concisely": "简洁写作",
    "cek-write-tests": "补充测试",
}

SKILL_CATEGORY_MAP = {
    "humanizer": ("通用能力", "文案与表达"),
    "find-skills": ("通用能力", "技能发现"),
    "skill-creator": ("技能开发", "设计与优化"),
    "skill-registry": ("技能管理", "注册表与界面"),
    "cek-agent-evaluation": ("技能开发", "设计与优化"),
    "cek-analyze-issue": ("Git 协作", "Issue 与 PR"),
    "cek-anthropic-skill-best-practices": ("技能开发", "设计与优化"),
    "cek-attach-review-to-pr": ("Git 协作", "Issue 与 PR"),
    "cek-brainstorm": ("规划实施", "需求与方案"),
    "cek-build-mcp": ("MCP 与技术栈", "MCP 构建"),
    "cek-commit": ("Git 协作", "提交与分支"),
    "cek-compare-worktrees": ("Git 协作", "Worktree 管理"),
    "cek-context-engineering": ("技能开发", "设计与优化"),
    "cek-create-command": ("技能开发", "设计与优化"),
    "cek-create-hook": ("技能开发", "规则与 Hook"),
    "cek-create-pr": ("Git 协作", "Issue 与 PR"),
    "cek-create-rule": ("技能开发", "规则与 Hook"),
    "cek-create-skill": ("技能开发", "设计与优化"),
    "cek-create-worktree": ("Git 协作", "Worktree 管理"),
    "cek-critique": ("评审与反思", "方案评审"),
    "cek-do-competitively": ("多代理协作", "执行模式"),
    "cek-do-in-parallel": ("多代理协作", "执行模式"),
    "cek-do-in-steps": ("多代理协作", "执行模式"),
    "cek-five-whys": ("分析与根因", "根因分析"),
    "cek-fix-tests": ("测试与质量", "测试修复"),
    "cek-fpf-query": ("分析与根因", "假设管理"),
    "cek-fpf-status": ("分析与根因", "假设管理"),
    "cek-implement": ("规划实施", "需求与方案"),
    "cek-judge-with-debate": ("多代理协作", "评审模式"),
    "cek-kaizen": ("分析与根因", "持续改进"),
    "cek-launch-sub-agent": ("多代理协作", "执行模式"),
    "cek-load-issues": ("Git 协作", "Issue 与 PR"),
    "cek-merge-worktree": ("Git 协作", "Worktree 管理"),
    "cek-multi-agent-patterns": ("多代理协作", "评审模式"),
    "cek-notes": ("Git 协作", "提交与分支"),
    "cek-plan": ("规划实施", "需求与方案"),
    "cek-prompt-engineering": ("技能开发", "设计与优化"),
    "cek-propose-hypotheses": ("分析与根因", "假设管理"),
    "cek-reflect": ("评审与反思", "方案评审"),
    "cek-review-local-changes": ("评审与反思", "代码评审"),
    "cek-review-pr": ("评审与反思", "代码评审"),
    "cek-root-cause-tracing": ("分析与根因", "根因分析"),
    "cek-setup-context7-mcp": ("MCP 与技术栈", "MCP 配置"),
    "cek-setup-serena-mcp": ("MCP 与技术栈", "MCP 配置"),
    "cek-test-driven-development": ("测试与质量", "测试驱动"),
    "cek-test-prompt": ("技能开发", "设计与优化"),
    "cek-test-skill": ("技能开发", "设计与优化"),
    "cek-thought-based-reasoning": ("分析与根因", "推理方法"),
    "cek-tree-of-thoughts": ("分析与根因", "推理方法"),
    "cek-typescript-best-practices": ("MCP 与技术栈", "技术规范"),
    "cek-update-docs": ("文档与表达", "文档维护"),
    "cek-worktrees": ("Git 协作", "Worktree 管理"),
    "cek-write-concisely": ("文档与表达", "文案与表达"),
    "cek-write-tests": ("测试与质量", "测试驱动"),
}

CATEGORY_ICON_MAP = {
    "通用能力": "◎",
    "技能开发": "◆",
    "技能管理": "▣",
    "Git 协作": "⑂",
    "多代理协作": "◉",
    "评审与反思": "✦",
    "规划实施": "▦",
    "分析与根因": "✧",
    "测试与质量": "✓",
    "文档与表达": "✎",
    "MCP 与技术栈": "⌘",
    "工程工作流": "▤",
    "安全与测试": "🛡",
    "DevOps 与部署": "⚙",
    "未分类": "•",
}

SUBCATEGORY_ICON_MAP = {
    "文案与表达": "✎",
    "技能发现": "⌕",
    "设计与优化": "✦",
    "注册表与界面": "▣",
    "Issue 与 PR": "⑂",
    "需求与方案": "▦",
    "MCP 构建": "⌘",
    "提交与分支": "⑃",
    "Worktree 管理": "⑄",
    "规则与 Hook": "⚓",
    "方案评审": "✧",
    "执行模式": "▶",
    "根因分析": "◎",
    "测试修复": "✓",
    "假设管理": "◌",
    "评审模式": "◉",
    "推理方法": "∞",
    "MCP 配置": "⌘",
    "技术规范": "⚖",
    "文档维护": "✎",
    "Trail of Bits 测试": "🧪",
    "Trail of Bits 安全": "🛡",
    "Superpowers": "✦",
    "AgentSys": "▤",
    "AgentSys 性能": "⚡",
    "模板生成": "⚙",
    "配置校验": "✓",
    "专项工具": "🧰",
    "其他": "•",
}


@dataclass
class SkillRow:
    data: dict

    @property
    def skill(self) -> str:
        return self.data["Skill"]

    @property
    def local_path(self) -> Path:
        return Path(self.data["LocalPath"])


def today_str() -> str:
    return datetime.now().strftime("%Y-%m-%d")


def build_registry_readme_text() -> str:
    base = str(BASE_DIR)
    registry = str(REGISTRY_PATH)
    readme = str(README_PATH)
    usage_guide = str(USAGE_GUIDE_PATH)
    skill_md = str(BASE_DIR / "skill-registry" / "SKILL.md")
    gui_py = str(BASE_DIR / "skill-registry" / "skill_registry_gui.py")
    gui_bat = str(BASE_DIR / "skill-registry" / "launch_skill_registry_gui.bat")
    trash = str(TRASH_DIR)
    return f"""# OpenCode Skills 清单说明

这个目录下的 skills 使用一张总表统一维护：

- `{registry}`

你可以把它理解成 skills 的主数据库，设计思路类似 awesome-opencode 资源总表。

## 这张表是干什么的

- 记录当前安装了哪些 OpenCode skills
- 记录每个 skill 的来源、路径、安装时间和最近更新时间
- 方便后续新增、更新、删除 skill 时统一管理
- 便于以后继续做自动生成说明页、搜索、筛选、导出

## 主表位置

- `{registry}`

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
- `Purpose` 尽量从该 skill 的 `SKILL.md` 描述中提炼，并统一写成中文

## 配套 skill

用于维护这张表的 skill 在这里：

- `{skill_md}`

## 可视化界面

如果你想更方便地查看、打开目录、刷新、删除 skill，可以直接启动图形界面：

- 脚本：`{gui_py}`
- 启动器：`{gui_bat}`

界面支持：

- 查看当前 skill 列表
- 查看每个 skill 的详细信息
- 新增 skill（支持 GitHub 克隆或本地目录导入）
- 通过远程搜索查找 skill，并一键安装到本地 OpenCode skills
- 编辑 skill 的来源、用途、备注
- 打开 skill 目录
- 打开注册表 CSV
- 同步目录与注册表
- 删除 skill（删除时会移动到 `{trash}`）

## 常见问题

- 如果点击远程搜索时报“找不到命令”，通常是系统里没有正确找到 `npx` 或 `git`
- 现在界面会优先自动解析命令路径，并在 Windows 下尝试通过 `cmd /c` 调用
- 如果某些命令输出带有 GBK/UTF-8 混合字符，界面会按 UTF-8 忽略非法字节解码，避免搜索时崩溃
- 如果你刚更新过脚本，请关闭旧界面后重新启动一次再试

当你以后安装、复制、更新、删除 skill 时，应该同步更新这张 CSV 表。

## 日常怎么看

平时直接看下面这个文件就可以：

- `{registry}`

如果想看说明，再看这个文件：

- `{readme}`

如果想看“什么情况下用哪个 skill、怎么使用”，看这个文件：

- `{usage_guide}`
"""


def ensure_registry_exists() -> None:
    BASE_DIR.mkdir(parents=True, exist_ok=True)
    if not REGISTRY_PATH.exists():
        with REGISTRY_PATH.open("w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
            writer.writeheader()


def ensure_readme_exists() -> None:
    if not README_PATH.exists():
        README_PATH.write_text(build_registry_readme_text(), encoding="utf-8")


def load_registry() -> list[dict]:
    ensure_registry_exists()
    ensure_readme_exists()
    with REGISTRY_PATH.open("r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        rows = []
        for row in reader:
            clean_row = {
                field: (row.get(field, "") or "").strip() for field in CSV_FIELDS
            }
            if any(clean_row.values()):
                rows.append(clean_row)
        return rows


def save_registry(rows: list[dict]) -> None:
    with REGISTRY_PATH.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def infer_skill_name(source: str) -> str:
    cleaned = source.replace("\\", "/").rstrip("/")
    name = cleaned.split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return name or "new-skill"


def to_chinese_purpose(skill_name: str, raw_purpose: str) -> str:
    if skill_name in KNOWN_PURPOSE_MAP:
        return KNOWN_PURPOSE_MAP[skill_name]

    text = (raw_purpose or "").strip()
    if not text:
        return f"用于 {skill_name} 相关任务"

    if any("\u4e00" <= ch <= "\u9fff" for ch in text):
        return text

    lowered = text.lower()
    rules = [
        (
            (
                "security",
                "audit",
                "vulnerability",
                "codeql",
                "semgrep",
                "sarif",
                "supply-chain",
            ),
            "用于安全审计、漏洞分析和风险检测",
        ),
        (
            (
                "test",
                "testing",
                "tdd",
                "fuzz",
                "coverage",
                "sanitizer",
                "libfuzzer",
                "ossfuzz",
            ),
            "用于测试设计、测试增强和测试验证",
        ),
        (
            ("review", "pull request", "pr", "diff", "code review"),
            "用于代码评审、差异检查和问题发现",
        ),
        (
            ("git", "commit", "branch", "worktree", "issue", "github", "notes"),
            "用于 Git 流程、分支协作和 Issue/PR 管理",
        ),
        (
            ("prompt", "skill", "agent", "hook", "command", "workflow"),
            "用于技能设计、提示优化和代理工作流改进",
        ),
        (
            (
                "plan",
                "brainstorm",
                "implement",
                "execute",
                "orchestrat",
                "parallel",
                "subagent",
            ),
            "用于任务规划、拆解执行和多代理协作",
        ),
        (
            ("debug", "root cause", "trace", "why", "kaizen", "hypothes"),
            "用于问题定位、根因分析和持续改进",
        ),
        (
            ("docs", "documentation", "write", "blog", "report", "concise"),
            "用于文档写作、说明整理和表达优化",
        ),
        (
            (
                "devops",
                "docker",
                "kubernetes",
                "terraform",
                "iac",
                "deployment",
                "pipeline",
            ),
            "用于部署、基础设施和 DevOps 流程",
        ),
        (
            ("session", "history", "context", "memory", "search"),
            "用于会话恢复、上下文管理和历史检索",
        ),
        (("mcp", "context7", "serena"), "用于 MCP 服务构建与接入配置"),
        (("postgres", "sql", "database", "query"), "用于数据库查询和数据读取分析"),
    ]
    for keywords, chinese in rules:
        if any(keyword in lowered for keyword in keywords):
            return chinese

    normalized = skill_name.replace("_", "-").strip("-")
    normalized = normalized.replace("-", " ")
    return f"用于 {normalized} 相关任务"


def get_skill_category(skill_name: str) -> tuple[str, str]:
    if skill_name in SKILL_CATEGORY_MAP:
        return SKILL_CATEGORY_MAP[skill_name]
    if skill_name.startswith("tob-"):
        if any(
            key in skill_name
            for key in [
                "fuzz",
                "testing",
                "coverage",
                "sanitizer",
                "libfuzzer",
                "ossfuzz",
            ]
        ):
            return ("安全与测试", "Trail of Bits 测试")
        return ("安全与测试", "Trail of Bits 安全")
    if skill_name.startswith("sp-"):
        return ("工程工作流", "Superpowers")
    if skill_name.startswith("ags-"):
        if "perf-" in skill_name:
            return ("工程工作流", "AgentSys 性能")
        return ("工程工作流", "AgentSys")
    if skill_name.startswith("devops-"):
        if skill_name.endswith("-generator"):
            return ("DevOps 与部署", "模板生成")
        if skill_name.endswith("-validator"):
            return ("DevOps 与部署", "配置校验")
        return ("DevOps 与部署", "专项工具")
    return ("未分类", "其他")


def get_skill_display_name(skill_name: str) -> str:
    alias = KNOWN_DISPLAY_NAME_MAP.get(skill_name)
    if alias:
        return f"{alias}（{skill_name}）"
    if any(
        skill_name.startswith(prefix) for prefix in ["tob-", "sp-", "ags-", "devops-"]
    ):
        readable = skill_name.split("-", 1)[1].replace("-", " ")
        return f"{readable}（{skill_name}）"
    return skill_name


def decorate_category_name(category: str) -> str:
    icon = CATEGORY_ICON_MAP.get(category, "•")
    return f"{icon} {category}"


def decorate_subcategory_name(subcategory: str) -> str:
    icon = SUBCATEGORY_ICON_MAP.get(subcategory, "•")
    return f"{icon} {subcategory}"


def to_chinese_status(status: str) -> str:
    return {
        "active": "启用",
        "removed": "已移除",
    }.get((status or "").strip(), status)


def to_chinese_agent(agent: str) -> str:
    return {
        "OpenCode": "本地 OpenCode",
    }.get((agent or "").strip(), agent)


def parse_find_skills_output(output: str) -> list[dict]:
    if not output:
        return []
    results = []
    pattern = re.compile(r"([A-Za-z0-9_.\-/]+)@([A-Za-z0-9_.\-]+)\s+(\d+) installs")
    for line in output.splitlines():
        clean = re.sub(r"\x1b\[[0-9;]*m", "", line).strip()
        match = pattern.search(clean)
        if not match:
            continue
        repo, skill, installs = match.groups()
        results.append(
            {
                "repo": repo,
                "skill": skill,
                "installs": installs,
                "source": f"https://github.com/{repo.split('@')[0]}",
                "label": f"{repo}@{skill} ({installs} installs)",
            }
        )
    return results


def run_cli_command(args: list[str]) -> subprocess.CompletedProcess:
    if not args:
        raise RuntimeError("未提供可执行命令")

    executable = args[0]
    resolved = shutil.which(executable)

    if resolved:
        result = subprocess.run(
            [resolved, *args[1:]],
            check=True,
            capture_output=True,
            text=False,
            shell=False,
            creationflags=NO_WINDOW,
        )
        stdout = (result.stdout or b"").decode("utf-8", errors="ignore")
        stderr = (result.stderr or b"").decode("utf-8", errors="ignore")
        return subprocess.CompletedProcess(
            result.args, result.returncode, stdout, stderr
        )

    if os.name == "nt":
        cmdline = subprocess.list2cmdline(args)
        comspec = os.environ.get("COMSPEC", r"C:\Windows\System32\cmd.exe")
        result = subprocess.run(
            [comspec, "/c", cmdline],
            check=True,
            capture_output=True,
            text=False,
            shell=False,
            creationflags=NO_WINDOW,
        )
        stdout = (result.stdout or b"").decode("utf-8", errors="ignore")
        stderr = (result.stderr or b"").decode("utf-8", errors="ignore")
        return subprocess.CompletedProcess(
            result.args, result.returncode, stdout, stderr
        )

    raise FileNotFoundError(f"找不到命令：{executable}")


def next_skill_id(rows: list[dict]) -> str:
    numbers = []
    for row in rows:
        value = row.get("ID", "")
        if value.startswith("skill-"):
            try:
                numbers.append(int(value.split("-", 1)[1]))
            except ValueError:
                pass
    next_number = max(numbers, default=0) + 1
    return f"skill-{next_number:03d}"


def read_skill_purpose(skill_dir: Path) -> str:
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return "请补充中文用途说明"

    try:
        lines = skill_md.read_text(encoding="utf-8").splitlines()
    except UnicodeDecodeError:
        lines = skill_md.read_text(encoding="utf-8", errors="ignore").splitlines()

    in_description = False
    desc_lines = []
    for line in lines:
        stripped = line.rstrip()
        if stripped == "---" and not in_description and desc_lines:
            break
        if stripped.startswith("description:"):
            if stripped.endswith("|"):
                in_description = True
                continue
            value = stripped.split(":", 1)[1].strip()
            return value or "请补充中文用途说明"
        if in_description:
            if stripped.startswith(
                ("name:", "metadata:", "license:", "version:", "compatibility:")
            ):
                continue
            if stripped.startswith("---"):
                break
            if stripped.startswith("  "):
                desc_lines.append(stripped.strip())
            elif stripped:
                break
    if desc_lines:
        return " ".join(desc_lines)
    return "请补充中文用途说明"


def iter_skill_dirs() -> list[Path]:
    results = []
    for item in BASE_DIR.iterdir():
        if item.name in EXCLUDED_NAMES:
            continue
        if item.is_dir() and (item / "SKILL.md").exists():
            results.append(item)
    return sorted(results, key=lambda p: p.name.lower())


def sync_registry() -> list[dict]:
    rows = load_registry()
    rows_by_skill = {row["Skill"]: row for row in rows}
    today = today_str()

    for skill_dir in iter_skill_dirs():
        skill_name = skill_dir.name
        purpose = to_chinese_purpose(skill_name, read_skill_purpose(skill_dir))
        if skill_name not in rows_by_skill:
            new_row = {
                "ID": next_skill_id(rows),
                "Skill": skill_name,
                "Status": "active",
                "Agent": "OpenCode",
                "Source": "manual",
                "LocalPath": str(skill_dir),
                "Installed": today,
                "LastUpdated": today,
                "Purpose": purpose,
                "Notes": "由技能管理界面自动补录",
            }
            rows.append(new_row)
            rows_by_skill[skill_name] = new_row
            continue

        row = rows_by_skill[skill_name]
        row["Status"] = "active"
        row["LocalPath"] = str(skill_dir)
        row["Purpose"] = purpose
        if not row.get("Installed"):
            row["Installed"] = today

    existing_skills = {skill_dir.name for skill_dir in iter_skill_dirs()}
    for row in rows:
        if row["Skill"] not in existing_skills and row.get("Status") == "active":
            row["Status"] = "removed"
            row["LastUpdated"] = today

    rows.sort(key=lambda item: item["Skill"].lower())
    save_registry(rows)
    return rows


class SkillRegistryApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("SkillForest 技能管理器")
        self.root.geometry("1420x860")
        self.root.minsize(1220, 760)
        self.rows: list[dict] = []
        self.search_query_var = tk.StringVar(value="")
        self.search_results: list[dict] = []

        self.status_var = tk.StringVar(value="准备就绪")
        self.detail_vars = {field: tk.StringVar(value="") for field in CSV_FIELDS}
        self.detail_text: tk.Text | None = None
        self.empty_tip_var = tk.StringVar(
            value="请从左侧技能树选择一个 skill，查看详情与用途。"
        )
        self.metric_total_var = tk.StringVar(value="0")
        self.metric_active_var = tk.StringVar(value="0")
        self.metric_group_var = tk.StringVar(value="0")
        self.metric_recent_var = tk.StringVar(value="-")

        self.bg_color = "#f4f7fb"
        self.surface_color = "#ffffff"
        self.header_color = "#16324f"
        self.header_accent = "#2f80ed"
        self.text_color = "#1f2937"
        self.muted_color = "#6b7280"
        self.border_color = "#dbe5f0"
        self.soft_blue = "#eaf2ff"

        self._build_ui()
        self.refresh_data(sync_first=True)

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.root.configure(bg=self.bg_color)

        style.configure("App.TFrame", background=self.bg_color)
        style.configure("Surface.TFrame", background=self.surface_color)
        style.configure("Toolbar.TFrame", background=self.surface_color)
        style.configure(
            "Card.TLabelframe",
            background=self.surface_color,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Card.TLabelframe.Label",
            background=self.surface_color,
            foreground=self.text_color,
            font=("Microsoft YaHei UI", 11, "bold"),
        )
        style.configure(
            "HeaderTitle.TLabel",
            background=self.header_color,
            foreground="#ffffff",
            font=("Microsoft YaHei UI", 22, "bold"),
        )
        style.configure(
            "HeaderSub.TLabel",
            background=self.header_color,
            foreground="#d7e6ff",
            font=("Microsoft YaHei UI", 10),
        )
        style.configure(
            "SectionTitle.TLabel",
            background=self.surface_color,
            foreground=self.text_color,
            font=("Microsoft YaHei UI", 11, "bold"),
        )
        style.configure(
            "SmallTitle.TLabel",
            background=self.surface_color,
            foreground=self.muted_color,
            font=("Microsoft YaHei UI", 9, "bold"),
        )
        style.configure(
            "MetricTitle.TLabel",
            background=self.surface_color,
            foreground=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        )
        style.configure(
            "MetricValue.TLabel",
            background=self.surface_color,
            foreground=self.text_color,
            font=("Segoe UI Semibold", 18, "bold"),
        )
        style.configure(
            "HeroValue.TLabel",
            background=self.surface_color,
            foreground=self.header_color,
            font=("Segoe UI Semibold", 16, "bold"),
        )
        style.configure(
            "Muted.TLabel",
            background=self.surface_color,
            foreground=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        )
        style.configure(
            "Toolbar.TButton", padding=(10, 7), font=("Microsoft YaHei UI", 9)
        )
        style.map("Toolbar.TButton", background=[("active", self.soft_blue)])
        style.configure(
            "Accent.TButton",
            padding=(12, 8),
            font=("Microsoft YaHei UI", 9, "bold"),
            foreground="#ffffff",
            background=self.header_accent,
            borderwidth=0,
        )
        style.map("Accent.TButton", background=[("active", "#1f6fd1")])
        style.configure(
            "Status.TLabel",
            background=self.surface_color,
            foreground=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        )
        style.configure(
            "Treeview",
            rowheight=28,
            font=("Microsoft YaHei UI", 9),
            fieldbackground=self.surface_color,
            background=self.surface_color,
            foreground=self.text_color,
            bordercolor=self.border_color,
        )
        style.configure(
            "Treeview.Heading",
            font=("Microsoft YaHei UI", 9, "bold"),
            background="#edf3fa",
            foreground=self.text_color,
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", "#d7e8ff")],
            foreground=[("selected", self.text_color)],
        )
        style.configure("TEntry", padding=6)
        style.configure(
            "SearchCard.TLabelframe",
            background=self.surface_color,
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "SearchCard.TLabelframe.Label",
            background=self.surface_color,
            foreground=self.text_color,
            font=("Microsoft YaHei UI", 10, "bold"),
        )

    def _build_ui(self) -> None:
        self._configure_styles()

        header = tk.Frame(self.root, bg=self.header_color, padx=22, pady=18)
        header.pack(fill=tk.X)

        ttk.Label(header, text="SkillForest", style="HeaderTitle.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header,
            text="把本地 OpenCode skills 整理成可搜索、可登记、可分类、可分享的技能森林。",
            style="HeaderSub.TLabel",
        ).pack(anchor=tk.W, pady=(6, 0))

        dashboard = ttk.Frame(self.root, style="App.TFrame", padding=(16, 14, 16, 6))
        dashboard.pack(fill=tk.X)

        metrics = ttk.Frame(dashboard, style="App.TFrame")
        metrics.pack(fill=tk.X)
        self._build_metric_card(metrics, "当前技能总数", self.metric_total_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8)
        )
        self._build_metric_card(metrics, "启用技能数", self.metric_active_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=8
        )
        self._build_metric_card(metrics, "技能分组数", self.metric_group_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=8
        )
        self._build_metric_card(metrics, "最近更新时间", self.metric_recent_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0)
        )

        toolbar_wrap = ttk.Frame(self.root, style="App.TFrame", padding=(16, 6, 16, 8))
        toolbar_wrap.pack(fill=tk.X)
        toolbar = ttk.Frame(toolbar_wrap, style="Toolbar.TFrame", padding=12)
        toolbar.pack(fill=tk.X)

        ttk.Button(
            toolbar, text="刷新列表", command=self.refresh_data, style="Toolbar.TButton"
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            toolbar,
            text="新增 skill",
            command=self.add_skill_dialog,
            style="Accent.TButton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Label(toolbar, text="搜索 skill：", style="SectionTitle.TLabel").pack(
            side=tk.LEFT, padx=(18, 4)
        )
        ttk.Entry(toolbar, textvariable=self.search_query_var, width=28).pack(
            side=tk.LEFT, padx=4
        )
        ttk.Button(
            toolbar,
            text="远程搜索",
            command=self.search_remote_skills,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            toolbar,
            text="编辑说明",
            command=self.edit_selected_skill,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            toolbar,
            text="同步注册表",
            command=self.sync_and_refresh,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            toolbar,
            text="打开技能目录",
            command=self.open_skill_dir,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            toolbar,
            text="打开注册表",
            command=self.open_registry_file,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            toolbar, text="打开说明", command=self.open_readme, style="Toolbar.TButton"
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            toolbar,
            text="用途说明",
            command=self.open_usage_guide,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=4)
        ttk.Button(
            toolbar,
            text="删除技能",
            command=self.delete_selected_skill,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=12)

        main_wrap = ttk.Frame(self.root, style="App.TFrame", padding=(16, 0, 16, 12))
        main_wrap.pack(fill=tk.BOTH, expand=True)
        main = ttk.PanedWindow(main_wrap, orient=tk.HORIZONTAL)
        main.pack(fill=tk.BOTH, expand=True)

        left = ttk.Frame(main, style="Surface.TFrame", padding=10)
        right = ttk.Frame(main, style="Surface.TFrame", padding=10)
        main.add(left, weight=3)
        main.add(right, weight=2)

        ttk.Label(left, text="技能树浏览", style="SectionTitle.TLabel").pack(
            anchor=tk.W, pady=(0, 8)
        )

        columns = ("Status", "Installed", "LastUpdated", "Purpose")
        self.tree = ttk.Treeview(left, columns=columns, show="tree headings", height=24)
        self.tree.heading("#0", text="技能树")
        self.tree.heading("Status", text="状态")
        self.tree.heading("Installed", text="首次安装")
        self.tree.heading("LastUpdated", text="最近更新")
        self.tree.heading("Purpose", text="用途")
        self.tree.column("#0", width=260, anchor=tk.W)
        self.tree.column("Status", width=80, anchor=tk.CENTER)
        self.tree.column("Installed", width=100, anchor=tk.CENTER)
        self.tree.column("LastUpdated", width=100, anchor=tk.CENTER)
        self.tree.column("Purpose", width=480, anchor=tk.W)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        tree_scroll = ttk.Scrollbar(left, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scroll.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        info_frame = ttk.LabelFrame(
            right, text="技能详情", style="Card.TLabelframe", padding=12
        )
        info_frame.pack(fill=tk.BOTH, expand=True)

        hero = ttk.Frame(info_frame, style="Surface.TFrame")
        hero.pack(fill=tk.X)
        ttk.Label(hero, text="当前选中技能", style="SmallTitle.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            hero,
            textvariable=self.detail_vars["Skill"],
            style="HeroValue.TLabel",
            wraplength=430,
            justify=tk.LEFT,
        ).pack(anchor=tk.W, pady=(4, 8))
        ttk.Label(
            hero,
            textvariable=self.empty_tip_var,
            style="Muted.TLabel",
            wraplength=430,
            justify=tk.LEFT,
        ).pack(anchor=tk.W)

        basic_card = ttk.LabelFrame(
            info_frame, text="基础信息", style="Card.TLabelframe", padding=10
        )
        basic_card.pack(fill=tk.X, pady=(12, 8))
        path_card = ttk.LabelFrame(
            info_frame, text="路径与来源", style="Card.TLabelframe", padding=10
        )
        path_card.pack(fill=tk.X, pady=8)
        desc_card = ttk.LabelFrame(
            info_frame, text="用途与备注", style="Card.TLabelframe", padding=10
        )
        desc_card.pack(fill=tk.BOTH, expand=True, pady=(8, 0))

        field_label_map = {
            "ID": "编号",
            "Skill": "技能名",
            "Status": "状态",
            "Agent": "归属",
            "Source": "来源",
            "LocalPath": "本地路径",
            "Installed": "首次安装",
            "LastUpdated": "最近更新",
            "Purpose": "用途",
        }

        for row_index, field in enumerate(
            ["ID", "Status", "Agent", "Installed", "LastUpdated"]
        ):
            ttk.Label(
                basic_card, text=field_label_map[field], style="SmallTitle.TLabel"
            ).grid(row=row_index, column=0, sticky=tk.NW, pady=4)
            ttk.Label(
                basic_card,
                textvariable=self.detail_vars[field],
                wraplength=320,
                justify=tk.LEFT,
            ).grid(row=row_index, column=1, sticky=tk.NW, pady=4, padx=(10, 0))

        for row_index, field in enumerate(["Source", "LocalPath"]):
            ttk.Label(
                path_card, text=field_label_map[field], style="SmallTitle.TLabel"
            ).grid(row=row_index, column=0, sticky=tk.NW, pady=4)
            ttk.Label(
                path_card,
                textvariable=self.detail_vars[field],
                wraplength=340,
                justify=tk.LEFT,
            ).grid(row=row_index, column=1, sticky=tk.NW, pady=4, padx=(10, 0))

        ttk.Label(desc_card, text="用途", style="SmallTitle.TLabel").grid(
            row=0, column=0, sticky=tk.NW, pady=4
        )
        ttk.Label(
            desc_card,
            textvariable=self.detail_vars["Purpose"],
            wraplength=340,
            justify=tk.LEFT,
        ).grid(row=0, column=1, sticky=tk.NW, pady=4, padx=(10, 0))
        ttk.Label(desc_card, text="备注", style="SmallTitle.TLabel").grid(
            row=1, column=0, sticky=tk.NW, pady=(10, 4)
        )
        self.detail_text = tk.Text(
            desc_card,
            height=9,
            width=44,
            wrap=tk.WORD,
            relief=tk.FLAT,
            bg="#f8fbff",
            fg=self.text_color,
            font=("Microsoft YaHei UI", 9),
            padx=10,
            pady=8,
        )
        self.detail_text.grid(
            row=1, column=1, sticky=tk.NSEW, pady=(10, 4), padx=(10, 0)
        )
        self.detail_text.configure(state=tk.DISABLED)

        basic_card.columnconfigure(1, weight=1)
        path_card.columnconfigure(1, weight=1)
        desc_card.columnconfigure(1, weight=1)
        desc_card.rowconfigure(1, weight=1)

        status_wrap = ttk.Frame(self.root, style="App.TFrame", padding=(16, 0, 16, 14))
        status_wrap.pack(fill=tk.X)
        status_bar = ttk.Label(
            status_wrap,
            textvariable=self.status_var,
            anchor=tk.W,
            style="Status.TLabel",
        )
        status_bar.pack(fill=tk.X)

    def _build_metric_card(
        self, parent: ttk.Frame, title: str, variable: tk.StringVar
    ) -> ttk.Frame:
        frame = ttk.Frame(parent, style="Surface.TFrame", padding=(14, 12))
        ttk.Label(frame, text=title, style="MetricTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(frame, textvariable=variable, style="MetricValue.TLabel").pack(
            anchor=tk.W, pady=(6, 0)
        )
        return frame

    def refresh_data(self, sync_first: bool = False) -> None:
        if sync_first:
            self.rows = sync_registry()
        else:
            self.rows = load_registry()

        self._refresh_metrics()

        for item in self.tree.get_children():
            self.tree.delete(item)

        top_nodes: dict[str, str] = {}
        sub_nodes: dict[tuple[str, str], str] = {}

        for row in self.rows:
            top_category, sub_category = get_skill_category(row["Skill"])

            if top_category not in top_nodes:
                top_id = f"cat::{top_category}"
                self.tree.insert(
                    "",
                    tk.END,
                    iid=top_id,
                    text=decorate_category_name(top_category),
                    open=True,
                    values=("", "", "", ""),
                )
                top_nodes[top_category] = top_id

            sub_key = (top_category, sub_category)
            if sub_key not in sub_nodes:
                sub_id = f"sub::{top_category}::{sub_category}"
                self.tree.insert(
                    top_nodes[top_category],
                    tk.END,
                    iid=sub_id,
                    text=decorate_subcategory_name(sub_category),
                    open=True,
                    values=("", "", "", ""),
                )
                sub_nodes[sub_key] = sub_id

            self.tree.insert(
                sub_nodes[sub_key],
                tk.END,
                iid=row["ID"],
                text=get_skill_display_name(row["Skill"]),
                values=(
                    to_chinese_status(row["Status"]),
                    row["Installed"],
                    row["LastUpdated"],
                    row["Purpose"],
                ),
            )

        self.clear_details()
        self.status_var.set(f"已加载 {len(self.rows)} 个 skill")

    def _refresh_metrics(self) -> None:
        total = len(self.rows)
        active = sum(1 for row in self.rows if row.get("Status") == "active")
        groups = len({get_skill_category(row["Skill"])[0] for row in self.rows})
        latest = "-"
        dates = [
            row.get("LastUpdated", "") for row in self.rows if row.get("LastUpdated")
        ]
        if dates:
            latest = max(dates)

        self.metric_total_var.set(str(total))
        self.metric_active_var.set(str(active))
        self.metric_group_var.set(str(groups))
        self.metric_recent_var.set(latest)

    def sync_and_refresh(self) -> None:
        self.refresh_data(sync_first=True)
        self.status_var.set("已同步技能目录和注册表")

    def clear_details(self) -> None:
        for var in self.detail_vars.values():
            var.set("")
        self.empty_tip_var.set("请从左侧技能树选择一个 skill，查看详情与用途。")
        if self.detail_text is None:
            return
        self.detail_text.configure(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.configure(state=tk.DISABLED)

    def selected_row(self) -> dict | None:
        selected = self.tree.selection()
        if not selected:
            return None
        selected_id = selected[0]
        if not selected_id.startswith("skill-"):
            return None
        for row in self.rows:
            if row["ID"] == selected_id:
                return row
        return None

    def on_select(self, _event=None) -> None:
        row = self.selected_row()
        if not row:
            self.clear_details()
            return

        for field in CSV_FIELDS:
            if field == "Notes":
                continue
            value = row.get(field, "")
            if field == "Skill":
                value = get_skill_display_name(value)
            elif field == "Status":
                value = to_chinese_status(value)
            elif field == "Agent":
                value = to_chinese_agent(value)
            self.detail_vars[field].set(value)
        self.empty_tip_var.set("你可以继续编辑来源、用途、备注，或直接打开技能目录。")

        if self.detail_text is None:
            return
        self.detail_text.configure(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.insert("1.0", row.get("Notes", ""))
        self.detail_text.configure(state=tk.DISABLED)

    def open_path(self, path: Path) -> None:
        if not path.exists():
            messagebox.showwarning("路径不存在", f"找不到路径：\n{path}")
            return
        os.startfile(str(path))

    def open_skill_dir(self) -> None:
        row = self.selected_row()
        if not row:
            messagebox.showinfo("请选择 skill", "请先在左侧选择一个 skill。")
            return
        self.open_path(Path(row["LocalPath"]))

    def open_registry_file(self) -> None:
        self.open_path(REGISTRY_PATH)

    def open_readme(self) -> None:
        self.open_path(README_PATH)

    def open_usage_guide(self) -> None:
        self.open_path(USAGE_GUIDE_PATH)

    def add_registry_row(
        self, skill_name: str, local_path: Path, source: str, notes: str
    ) -> None:
        rows = load_registry()
        existing = None
        for row in rows:
            if row["Skill"] == skill_name:
                existing = row
                break

        purpose = to_chinese_purpose(skill_name, read_skill_purpose(local_path))
        today = today_str()
        if existing is None:
            rows.append(
                {
                    "ID": next_skill_id(rows),
                    "Skill": skill_name,
                    "Status": "active",
                    "Agent": "OpenCode",
                    "Source": source,
                    "LocalPath": str(local_path),
                    "Installed": today,
                    "LastUpdated": today,
                    "Purpose": purpose,
                    "Notes": notes,
                }
            )
        else:
            existing["Status"] = "active"
            existing["Source"] = source
            existing["LocalPath"] = str(local_path)
            existing["LastUpdated"] = today
            existing["Purpose"] = purpose
            if not existing.get("Installed"):
                existing["Installed"] = today
            existing["Notes"] = notes

        rows.sort(key=lambda item: item["Skill"].lower())
        save_registry(rows)

    def add_skill_dialog(self) -> None:
        answer = messagebox.askyesnocancel(
            "新增 skill",
            "请选择新增方式：\n\n是：从 GitHub 地址克隆\n否：从本地目录复制\n取消：退出",
        )
        if answer is None:
            return

        if answer:
            source = simpledialog.askstring(
                "GitHub 地址",
                "请输入 skill 仓库地址：",
                parent=self.root,
            )
            if not source:
                return
            default_name = infer_skill_name(source)
            skill_name = simpledialog.askstring(
                "Skill 名称",
                "请输入安装后的目录名：",
                initialvalue=default_name,
                parent=self.root,
            )
            if not skill_name:
                return
            target = BASE_DIR / skill_name.strip()
            if target.exists():
                messagebox.showerror("目录已存在", f"目标目录已存在：\n{target}")
                return
            try:
                run_cli_command(["git", "clone", source, str(target)])
            except FileNotFoundError as exc:
                messagebox.showerror("克隆失败", f"找不到命令：{exc}")
                return
            except subprocess.CalledProcessError as exc:
                messagebox.showerror("克隆失败", exc.stderr or exc.stdout or str(exc))
                return
            notes = "通过可视化界面从 GitHub 克隆安装"
        else:
            selected_dir = filedialog.askdirectory(title="选择本地 skill 目录")
            if not selected_dir:
                return
            source_path = Path(selected_dir)
            if not (source_path / "SKILL.md").exists():
                messagebox.showerror(
                    "目录无效", "所选目录中没有 SKILL.md，不能作为 skill 导入。"
                )
                return
            default_name = source_path.name
            skill_name = simpledialog.askstring(
                "Skill 名称",
                "请输入复制后的目录名：",
                initialvalue=default_name,
                parent=self.root,
            )
            if not skill_name:
                return
            target = BASE_DIR / skill_name.strip()
            if target.exists():
                messagebox.showerror("目录已存在", f"目标目录已存在：\n{target}")
                return
            shutil.copytree(source_path, target)
            source = str(source_path)
            notes = "通过可视化界面从本地目录复制导入"

        self.add_registry_row(skill_name.strip(), target, source, notes)
        self.refresh_data(sync_first=False)
        self.status_var.set(f"已新增 skill：{skill_name.strip()}")
        messagebox.showinfo("完成", f"已新增 skill：{skill_name.strip()}")

    def search_remote_skills(self) -> None:
        query = self.search_query_var.get().strip()
        if not query:
            messagebox.showinfo("请输入关键词", "请先输入要搜索的 skill 关键词。")
            return

        self.status_var.set(f"正在搜索：{query}")
        self.root.update_idletasks()
        try:
            result = run_cli_command(["npx", "skills", "find", query])
        except FileNotFoundError as exc:
            messagebox.showerror("搜索失败", f"找不到命令：{exc}")
            self.status_var.set("远程搜索失败")
            return
        except subprocess.CalledProcessError as exc:
            messagebox.showerror("搜索失败", exc.stderr or exc.stdout or str(exc))
            self.status_var.set("远程搜索失败")
            return

        results = parse_find_skills_output(result.stdout)
        if not results:
            messagebox.showinfo("没有结果", f"没有找到与“{query}”相关的 skill。")
            self.status_var.set("未找到匹配 skill")
            return

        self.search_results = results
        self.show_search_results_window(query)
        self.status_var.set(f"搜索到 {len(results)} 个 skill")

    def show_search_results_window(self, query: str) -> None:
        window = tk.Toplevel(self.root)
        window.title(f"搜索结果 - {query}")
        window.geometry("980x620")
        window.configure(bg=self.bg_color)

        header = tk.Frame(window, bg=self.header_color, padx=18, pady=14)
        header.pack(fill=tk.X)
        ttk.Label(header, text=f"Skill 搜索：{query}", style="HeaderTitle.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            header,
            text="从远程结果中选择一个 skill，一键安装到本地 OpenCode 技能库。",
            style="HeaderSub.TLabel",
        ).pack(anchor=tk.W, pady=(6, 0))

        body = ttk.Frame(window, style="App.TFrame", padding=(14, 14, 14, 10))
        body.pack(fill=tk.BOTH, expand=True)

        card = ttk.LabelFrame(
            body, text="搜索结果", style="SearchCard.TLabelframe", padding=12
        )
        card.pack(fill=tk.BOTH, expand=True)

        columns = ("repo", "skill", "installs")
        tree = ttk.Treeview(card, columns=columns, show="headings", height=18)
        tree.heading("repo", text="仓库")
        tree.heading("skill", text="技能")
        tree.heading("installs", text="安装量")
        tree.column("repo", width=420, anchor=tk.W)
        tree.column("skill", width=220, anchor=tk.W)
        tree.column("installs", width=100, anchor=tk.CENTER)

        scroll = ttk.Scrollbar(card, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 0), pady=(0, 10))
        scroll.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0), pady=(0, 10))

        for idx, item in enumerate(self.search_results):
            tree.insert(
                "",
                tk.END,
                iid=str(idx),
                values=(item["repo"], item["skill"], item["installs"]),
            )

        actions = ttk.Frame(body, style="App.TFrame", padding=(0, 8, 0, 0))
        actions.pack(fill=tk.X)

        def install_selected() -> None:
            selected = tree.selection()
            if not selected:
                messagebox.showinfo("请选择", "请先选择一个 skill。", parent=window)
                return
            item = self.search_results[int(selected[0])]
            try:
                self.install_remote_skill(item)
            except RuntimeError as exc:
                messagebox.showerror("安装失败", str(exc), parent=window)
                return
            messagebox.showinfo(
                "安装完成", f"已安装 skill：{item['skill']}", parent=window
            )
            window.destroy()

        ttk.Button(
            actions, text="安装到本地", command=install_selected, style="Accent.TButton"
        ).pack(side=tk.LEFT)
        ttk.Button(
            actions, text="关闭", command=window.destroy, style="Toolbar.TButton"
        ).pack(side=tk.LEFT, padx=8)

    def install_remote_skill(self, item: dict) -> None:
        repo_name = item["repo"].split("@", 1)[0]
        repo_url = f"https://github.com/{repo_name}"
        skill_name = item["skill"]

        self.status_var.set(f"正在安装：{skill_name}")
        self.root.update_idletasks()

        try:
            run_cli_command(
                [
                    "npx",
                    "skills",
                    "add",
                    repo_url,
                    "--skill",
                    skill_name,
                    "--agent",
                    "opencode",
                    "--global",
                    "--yes",
                ]
            )
        except FileNotFoundError as exc:
            raise RuntimeError(f"找不到命令：{exc}") from exc
        except subprocess.CalledProcessError as exc:
            raise RuntimeError(exc.stderr or exc.stdout or str(exc)) from exc

        source_dir = AGENTS_SKILLS_DIR / skill_name
        target_dir = BASE_DIR / skill_name
        if not source_dir.exists():
            raise RuntimeError(f"安装后未找到通用 skills 目录：{source_dir}")

        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source_dir, target_dir)

        self.add_registry_row(
            skill_name,
            target_dir,
            repo_url,
            "通过远程搜索结果一键安装，并同步复制到 OpenCode 本地目录",
        )
        self.refresh_data(sync_first=False)
        self.status_var.set(f"已安装 skill：{skill_name}")

    def edit_selected_skill(self) -> None:
        row = self.selected_row()
        if not row:
            messagebox.showinfo("请选择 skill", "请先在左侧选择一个 skill。")
            return

        source = simpledialog.askstring(
            "编辑来源",
            "请输入新的 Source：",
            initialvalue=row.get("Source", ""),
            parent=self.root,
        )
        if source is None:
            return

        purpose = simpledialog.askstring(
            "编辑用途",
            "请输入新的 Purpose（必须用中文）：",
            initialvalue=row.get("Purpose", ""),
            parent=self.root,
        )
        if purpose is None:
            return
        purpose = purpose.strip()
        if not purpose:
            messagebox.showerror("用途不能为空", "Purpose 不能为空，而且必须使用中文。")
            return
        if not any("\u4e00" <= ch <= "\u9fff" for ch in purpose):
            messagebox.showerror("用途必须为中文", "Purpose 必须使用中文填写。")
            return

        notes = simpledialog.askstring(
            "编辑备注",
            "请输入新的 Notes：",
            initialvalue=row.get("Notes", ""),
            parent=self.root,
        )
        if notes is None:
            return

        for item in self.rows:
            if item["ID"] == row["ID"]:
                item["Source"] = source.strip()
                item["Purpose"] = purpose
                item["Notes"] = notes.strip()
                item["LastUpdated"] = today_str()
                break

        save_registry(self.rows)
        self.refresh_data(sync_first=False)
        self.status_var.set(f"已更新 skill：{row['Skill']}")

    def delete_selected_skill(self) -> None:
        row = self.selected_row()
        if not row:
            messagebox.showinfo("请选择 skill", "请先在左侧选择一个 skill。")
            return

        skill_name = row["Skill"]
        skill_path = Path(row["LocalPath"])
        if not skill_path.exists():
            messagebox.showwarning(
                "目录不存在", f"技能目录不存在：\n{skill_path}\n将只更新注册表状态。"
            )
        else:
            confirmed = messagebox.askyesno(
                "确认删除",
                f"确定要删除 skill `{skill_name}` 吗？\n\n"
                f"目录会被移动到：\n{TRASH_DIR}\n\n"
                "注册表状态会改成 removed。",
            )
            if not confirmed:
                return

            TRASH_DIR.mkdir(parents=True, exist_ok=True)
            target = (
                TRASH_DIR / f"{skill_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            )
            shutil.move(str(skill_path), str(target))

        for item in self.rows:
            if item["ID"] == row["ID"]:
                item["Status"] = "removed"
                item["LastUpdated"] = today_str()
                item["Notes"] = f"已通过可视化界面移到 {TRASH_DIR}"
                break

        save_registry(self.rows)
        self.refresh_data(sync_first=False)
        self.status_var.set(f"已删除 skill：{skill_name}")


def main() -> None:
    ensure_registry_exists()
    root = tk.Tk()
    app = SkillRegistryApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
