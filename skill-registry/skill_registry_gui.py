import csv
import json
import os
import re
import shutil
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk
from typing import Any


USER_HOME = Path.home()
BASE_DIR = USER_HOME / ".claude" / "skills"
REGISTRY_PATH = BASE_DIR / "SKILLS_REGISTRY.csv"
README_PATH = BASE_DIR / "SKILLS_REGISTRY_README.md"
USAGE_GUIDE_PATH = BASE_DIR / "SKILLS_USAGE_GUIDE.md"
OPENCODE_DB_PATH = USER_HOME / ".local" / "share" / "opencode" / "opencode.db"
TRASH_DIR = BASE_DIR / ".trash"
AGENTS_SKILLS_DIR = USER_HOME / ".agents" / "skills"
QUALITY_REVIEWS_PATH = BASE_DIR / "skill-registry" / "skill_quality_reviews.json"
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

CARD_BATCH_SIZE = 48
SEARCH_DEBOUNCE_MS = 220
USAGE_REFRESH_MS = 5000
MAX_DASHBOARD_ITEMS = 3
SORT_MODE_OPTIONS = {
    "installed": "添加时间排序",
    "score": "按评分排序",
    "usage": "按使用次数排序",
}

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
    "opencode-skill-best-practices": "把通用 skill 编写原则翻译成适用于本地 OpenCode 环境的落地规范",
    "opencode-skill-quality-reviewer": "自动审查本地 skill 质量并生成评分结果",
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
    "opencode-skill-best-practices": "OpenCode 技能最佳实践",
    "opencode-skill-quality-reviewer": "技能质量审查器",
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
    "sp-brainstorming": "Superpowers 脑暴设计",
    "sp-dispatching-parallel-agents": "Superpowers 并行分派",
    "sp-executing-plans": "Superpowers 按计划执行",
    "sp-finishing-a-development-branch": "Superpowers 分支收尾",
    "sp-receiving-code-review": "Superpowers 接收评审",
    "sp-requesting-code-review": "Superpowers 发起评审",
    "sp-subagent-driven-development": "Superpowers 子代理开发",
    "sp-systematic-debugging": "Superpowers 系统调试",
    "sp-test-driven-development": "Superpowers 测试驱动",
    "sp-using-git-worktrees": "Superpowers Worktree",
    "sp-using-superpowers": "Superpowers 总控入口",
    "sp-verification-before-completion": "Superpowers 完成前验证",
    "sp-writing-plans": "Superpowers 写实施计划",
    "sp-writing-skills": "Superpowers 写技能",
}

RUNTIME_SKILL_NAME_MAP = {
    "systematic-debugging": "sp-systematic-debugging",
    "verification-before-completion": "sp-verification-before-completion",
    "test-driven-development": "sp-test-driven-development",
    "brainstorming": "sp-brainstorming",
    "dispatching-parallel-agents": "sp-dispatching-parallel-agents",
    "writing-plans": "sp-writing-plans",
    "kaizen:why": "cek-five-whys",
    "git:commit": "cek-commit",
}

SKILL_CATEGORY_MAP = {
    "humanizer": ("通用能力", "文案与表达"),
    "find-skills": ("通用能力", "技能发现"),
    "skill-creator": ("技能开发", "设计与优化"),
    "skill-registry": ("技能管理", "注册表与界面"),
    "cek-agent-evaluation": ("技能开发", "设计与优化"),
    "cek-analyze-issue": ("Git 协作", "Issue 与 PR"),
    "cek-anthropic-skill-best-practices": ("技能开发", "设计与优化"),
    "opencode-skill-best-practices": ("技能开发", "设计与优化"),
    "opencode-skill-quality-reviewer": ("技能开发", "设计与优化"),
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

CATEGORY_TAG_MAP = {
    "通用能力": "cat_general",
    "技能开发": "cat_skilldev",
    "技能管理": "cat_registry",
    "Git 协作": "cat_git",
    "多代理协作": "cat_multi",
    "评审与反思": "cat_review",
    "规划实施": "cat_plan",
    "分析与根因": "cat_analysis",
    "测试与质量": "cat_quality",
    "文档与表达": "cat_docs",
    "MCP 与技术栈": "cat_mcp",
    "工程工作流": "cat_flow",
    "安全与测试": "cat_security",
    "DevOps 与部署": "cat_devops",
    "未分类": "cat_other",
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
    prefix_map = {
        "tob-": "Trail of Bits",
        "sp-": "Superpowers",
        "ags-": "AgentSys",
        "devops-": "DevOps",
    }
    for prefix, family in prefix_map.items():
        if skill_name.startswith(prefix):
            readable = skill_name.split("-", 1)[1].replace("-", " ")
            return f"{family} · {readable}（{skill_name}）"
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


def _date_rank(value: str) -> int:
    digits = (value or "").replace("-", "")
    if digits.isdigit():
        return int(digits)
    return 0


def mousewheel_units(delta: int) -> int:
    if delta == 0:
        return 0
    step = max(1, abs(delta) // 120) if abs(delta) >= 120 else 1
    return -step if delta > 0 else step


def score_from_usage_count(usage_count: int) -> int:
    if usage_count <= 0:
        return 0
    return min(100, 20 + usage_count * 5)


def compose_skill_score(usage_score: int, quality_score: int) -> int:
    usage_score = max(0, min(100, int(usage_score or 0)))
    quality_score = max(0, min(100, int(quality_score or 0)))
    if quality_score and usage_score:
        return round(quality_score * 0.65 + usage_score * 0.35)
    if quality_score:
        return round(quality_score * 0.8)
    return usage_score


def load_skill_quality_reviews(
    path: Path = QUALITY_REVIEWS_PATH,
) -> dict[str, dict[str, Any]]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}
    skills = payload.get("skills") if isinstance(payload, dict) else None
    if not isinstance(skills, dict):
        return {}
    result: dict[str, dict[str, Any]] = {}
    for skill_name, item in skills.items():
        if not isinstance(skill_name, str) or not isinstance(item, dict):
            continue
        result[skill_name] = item
    return result


def merge_skill_metrics(
    rows: list[dict],
    usage_summary: dict[str, dict],
    quality_reviews: dict[str, dict[str, Any]] | None = None,
) -> dict[str, dict[str, Any]]:
    quality_reviews = quality_reviews or {}
    merged: dict[str, dict[str, Any]] = {}
    skill_names = {row.get("Skill", "") for row in rows if row.get("Skill")}
    skill_names.update(usage_summary.keys())
    skill_names.update(quality_reviews.keys())

    for skill_name in skill_names:
        usage = usage_summary.get(skill_name, {})
        review = quality_reviews.get(skill_name, {})
        usage_count = int(usage.get("usage_count", 0))
        usage_score = int(usage.get("usage_score", usage.get("score", 0)))
        quality_score = int(review.get("quality_score", 0))
        merged[skill_name] = {
            "usage_count": usage_count,
            "usage_score": usage_score,
            "quality_score": quality_score,
            "score": compose_skill_score(usage_score, quality_score),
            "last_used_ts": int(usage.get("last_used_ts", 0)),
            "last_used": usage.get("last_used", "未使用"),
            "quality_summary": str(review.get("summary", "")).strip(),
            "quality_reviewed_at": str(review.get("reviewed_at", "")).strip(),
            "quality_recommendations": list(review.get("recommendations", []))
            if isinstance(review.get("recommendations", []), list)
            else [],
        }
    return merged


def get_skill_recommendations(skill_name: str) -> list[str]:
    explicit_map = {
        "opencode-skill-best-practices": [
            "cek-create-skill",
            "cek-prompt-engineering",
            "cek-test-skill",
            "opencode-skill-quality-reviewer",
        ],
        "opencode-skill-quality-reviewer": [
            "opencode-skill-best-practices",
            "cek-test-skill",
            "skill-registry",
        ],
        "cek-create-skill": [
            "opencode-skill-best-practices",
            "cek-prompt-engineering",
            "cek-test-skill",
        ],
        "cek-prompt-engineering": [
            "opencode-skill-best-practices",
            "cek-context-engineering",
            "cek-test-prompt",
        ],
        "cek-context-engineering": [
            "opencode-skill-best-practices",
            "cek-prompt-engineering",
            "cek-create-skill",
        ],
        "cek-test-skill": [
            "opencode-skill-quality-reviewer",
            "opencode-skill-best-practices",
            "cek-create-skill",
        ],
    }
    recommendations = list(explicit_map.get(skill_name, []))
    if skill_name.startswith(("cek-", "sp-", "ags-")) and skill_name not in {
        "opencode-skill-best-practices",
        "opencode-skill-quality-reviewer",
        "skill-registry",
    }:
        recommendations.append("opencode-skill-best-practices")
    deduped = []
    seen = set()
    for item in recommendations:
        if item == skill_name or item in seen:
            continue
        seen.add(item)
        deduped.append(item)
    return deduped[:4]


def canonical_skill_name(skill_name: str) -> str:
    return RUNTIME_SKILL_NAME_MAP.get(skill_name.strip(), skill_name.strip())


def format_usage_timestamp(timestamp_ms: int) -> str:
    if timestamp_ms <= 0:
        return "未使用"
    return datetime.fromtimestamp(timestamp_ms / 1000).strftime("%Y-%m-%d %H:%M")


def extract_skill_usage_event(part_data: dict, time_created: int) -> dict | None:
    if part_data.get("type") != "tool":
        return None
    if part_data.get("tool") != "skill":
        return None
    state = part_data.get("state") or {}
    payload = state.get("input") or {}
    skill_name = payload.get("name")
    if not isinstance(skill_name, str) or not skill_name.strip():
        return None
    return {
        "skill": canonical_skill_name(skill_name),
        "time_created": int(time_created or 0),
    }


def summarize_skill_usage(events: list[dict]) -> dict[str, dict]:
    summary: dict[str, dict] = {}
    for event in events:
        skill_name = canonical_skill_name(event["skill"])
        timestamp_ms = int(event.get("time_created", 0))
        item = summary.setdefault(
            skill_name,
            {
                "usage_count": 0,
                "usage_score": 0,
                "quality_score": 0,
                "score": 0,
                "last_used_ts": 0,
                "last_used": "未使用",
            },
        )
        item["usage_count"] += 1
        if timestamp_ms > item["last_used_ts"]:
            item["last_used_ts"] = timestamp_ms
            item["last_used"] = format_usage_timestamp(timestamp_ms)
        item["usage_score"] = score_from_usage_count(item["usage_count"])
        item["score"] = item["usage_score"]
    return summary


def build_usage_overview(events: list[dict], limit: int = 5) -> dict:
    ordered = sorted(events, key=lambda item: -int(item.get("time_created", 0)))
    recent = []
    for event in ordered[:limit]:
        recent.append(
            {
                "skill": event["skill"],
                "time_created": int(event.get("time_created", 0)),
                "time_text": format_usage_timestamp(int(event.get("time_created", 0))),
            }
        )
    return {
        "total_invocations": len(events),
        "recent_events": recent,
    }


def load_skill_usage_summary(db_path: Path = OPENCODE_DB_PATH) -> dict[str, dict]:
    if not db_path.exists():
        return {}
    con = sqlite3.connect(str(db_path))
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT time_created, data FROM part WHERE data LIKE ? ORDER BY time_created DESC",
            ('%"tool":"skill"%',),
        )
        events = []
        for time_created, data in cur.fetchall():
            try:
                part_data = json.loads(data)
            except Exception:
                continue
            event = extract_skill_usage_event(part_data, int(time_created or 0))
            if event is not None:
                events.append(event)
        return summarize_skill_usage(events)
    finally:
        con.close()


def load_skill_usage_events(db_path: Path = OPENCODE_DB_PATH) -> list[dict]:
    if not db_path.exists():
        return []
    con = sqlite3.connect(str(db_path))
    try:
        cur = con.cursor()
        cur.execute(
            "SELECT time_created, data FROM part WHERE data LIKE ? ORDER BY time_created DESC",
            ('%"tool":"skill"%',),
        )
        events = []
        for time_created, data in cur.fetchall():
            try:
                part_data = json.loads(data)
            except Exception:
                continue
            event = extract_skill_usage_event(part_data, int(time_created or 0))
            if event is not None:
                events.append(event)
        return events
    finally:
        con.close()


def usage_summary_changed(previous: dict[str, dict], current: dict[str, dict]) -> bool:
    return json.dumps(previous, sort_keys=True, ensure_ascii=False) != json.dumps(
        current, sort_keys=True, ensure_ascii=False
    )


def build_operations_dashboard(
    rows: list[dict], usage_summary: dict[str, dict], now_ts: int | None = None
) -> dict:
    now_ts = int(now_ts or datetime.now().timestamp() * 1000)
    active_rows = [row for row in rows if row.get("Status") == "active"]

    def usage_for(row: dict) -> dict:
        return usage_summary.get(
            row.get("Skill", ""),
            {
                "usage_count": 0,
                "usage_score": 0,
                "quality_score": 0,
                "score": 0,
                "last_used_ts": 0,
                "last_used": "未使用",
            },
        )

    high_usage = []
    recent_active = []
    sleeping = []
    top_used = []
    average_scores = []
    seven_days_ms = 7 * 24 * 60 * 60 * 1000
    thirty_days_ms = 30 * 24 * 60 * 60 * 1000

    for row in active_rows:
        usage = usage_for(row)
        usage_count = int(usage.get("usage_count", 0))
        score = int(usage.get("score", 0))
        last_used_ts = int(usage.get("last_used_ts", 0))
        decorated = {**row, **usage}
        average_scores.append(score)
        top_used.append(decorated)
        if usage_count >= 5:
            high_usage.append(decorated)
        if last_used_ts and now_ts - last_used_ts <= seven_days_ms:
            recent_active.append(decorated)
        if usage_count == 0 or (
            last_used_ts and now_ts - last_used_ts > thirty_days_ms
        ):
            sleeping.append(decorated)
        if usage_count == 0 and not last_used_ts:
            sleeping.append(decorated)

    def dedupe(items: list[dict]) -> list[dict]:
        seen = set()
        result = []
        for item in items:
            skill = item["Skill"]
            if skill in seen:
                continue
            seen.add(skill)
            result.append(item)
        return result

    sleeping = dedupe(sleeping)
    top_used.sort(
        key=lambda item: (
            -int(item.get("usage_count", 0)),
            -int(item.get("score", 0)),
            -_date_rank(item.get("Installed", "")),
        )
    )
    recent_active.sort(key=lambda item: -int(item.get("last_used_ts", 0)))
    sleeping.sort(
        key=lambda item: (
            int(item.get("usage_count", 0)),
            int(item.get("score", 0)),
            -_date_rank(item.get("Installed", "")),
        )
    )

    average_score = (
        round(sum(average_scores) / len(average_scores)) if average_scores else 0
    )
    if sleeping:
        insight_text = f"有 {len(sleeping)} 个技能处于沉睡状态，建议优先清理 0 分技能。"
    elif top_used:
        insight_text = f"当前主力技能是 {get_skill_display_name(top_used[0]['Skill'])}，可考虑加入常用入口。"
    else:
        insight_text = "还没有足够的调用数据，先多使用几次 skill 再看运营面板。"

    return {
        "summary": {
            "high_usage_count": len(high_usage),
            "active_7d_count": len(recent_active),
            "sleeping_count": len(sleeping),
            "average_score": average_score,
        },
        "top_used": top_used[:5],
        "recent_active": recent_active[:5],
        "cleanup_candidates": sleeping[:5],
        "insight_text": insight_text,
    }


def dashboard_preview_items(
    items: list[dict], limit: int = MAX_DASHBOARD_ITEMS
) -> list[dict]:
    return items[:limit]


def operations_panel_toggle_label(collapsed: bool) -> str:
    return "展开运营面板" if collapsed else "收起运营面板"


def _skill_id_rank(value: str) -> int:
    if value.startswith("skill-"):
        suffix = value.split("-", 1)[1]
        if suffix.isdigit():
            return int(suffix)
    return 0


def _row_sort_key(row: dict) -> tuple:
    return (
        0 if row.get("Status") == "active" else 1,
        -_date_rank(row.get("Installed", "")),
        -_skill_id_rank(row.get("ID", "")),
        -_date_rank(row.get("LastUpdated", "")),
        get_skill_display_name(row.get("Skill", "")).lower(),
    )


def _indexed_sort_key(item: dict, sort_mode: str) -> tuple:
    row = item["row"]
    base = _row_sort_key(row)
    if sort_mode == "score":
        return (
            0 if row.get("Status") == "active" else 1,
            -int(item.get("score", 0)),
            -int(item.get("usage_count", 0)),
            -_date_rank(row.get("Installed", "")),
            -_skill_id_rank(row.get("ID", "")),
            get_skill_display_name(row.get("Skill", "")).lower(),
        )
    if sort_mode == "usage":
        return (
            0 if row.get("Status") == "active" else 1,
            -int(item.get("usage_count", 0)),
            -int(item.get("score", 0)),
            -_date_rank(row.get("Installed", "")),
            -_skill_id_rank(row.get("ID", "")),
            get_skill_display_name(row.get("Skill", "")).lower(),
        )
    return base


def index_registry_rows(
    rows: list[dict],
    usage_summary: dict[str, dict] | None = None,
    sort_mode: str = "installed",
) -> list[dict]:
    usage_summary = usage_summary or {}
    indexed = []
    for row in rows:
        display_name = get_skill_display_name(row.get("Skill", ""))
        top_category, sub_category = get_skill_category(row["Skill"])
        status_label = to_chinese_status(row.get("Status", ""))
        usage = usage_summary.get(row.get("Skill", ""), {})
        usage_count = int(usage.get("usage_count", 0))
        usage_score = int(usage.get("usage_score", score_from_usage_count(usage_count)))
        quality_score = int(usage.get("quality_score", 0))
        score = int(usage.get("score", 0))
        last_used = usage.get("last_used", "未使用")
        search_blob = " ".join(
            [
                row.get("Skill", ""),
                display_name,
                row.get("Purpose", ""),
                row.get("Notes", ""),
                top_category,
                sub_category,
                status_label,
                str(usage_count),
                str(usage_score),
                str(quality_score),
                str(score),
            ]
        ).lower()
        indexed.append(
            {
                "row": row,
                "display_name": display_name,
                "top_category": top_category,
                "sub_category": sub_category,
                "status_label": status_label,
                "usage_count": usage_count,
                "usage_score": usage_score,
                "quality_score": quality_score,
                "score": score,
                "last_used": last_used,
                "search_blob": search_blob,
                "sort_key": _row_sort_key(row),
            }
        )
    return sorted(indexed, key=lambda item: _indexed_sort_key(item, sort_mode))


def filter_indexed_rows(
    indexed_rows: list[dict], selected_filter: str, query: str
) -> list[dict]:
    tokens = [token.lower() for token in query.strip().split() if token.strip()]
    filtered = []
    for item in indexed_rows:
        row = item["row"]
        if selected_filter == "active" and row.get("Status") != "active":
            continue
        if selected_filter == "removed" and row.get("Status") != "removed":
            continue
        if selected_filter.startswith("category:"):
            expected = selected_filter.split(":", 1)[1]
            if item["top_category"] != expected:
                continue
        if tokens and not all(token in item["search_blob"] for token in tokens):
            continue
        filtered.append(item)
    return filtered


def limit_visible_rows(
    indexed_rows: list[dict], limit: int = CARD_BATCH_SIZE
) -> tuple[list[dict], int]:
    visible = indexed_rows[:limit]
    remaining = max(0, len(indexed_rows) - len(visible))
    return visible, remaining


def summarize_registry_rows(rows: list[dict]) -> dict:
    latest = "-"
    dates = [row.get("LastUpdated", "") for row in rows if row.get("LastUpdated")]
    if dates:
        latest = max(dates)
    return {
        "total": len(rows),
        "active": sum(1 for row in rows if row.get("Status") == "active"),
        "removed": sum(1 for row in rows if row.get("Status") == "removed"),
        "categories": len({get_skill_category(row["Skill"])[0] for row in rows}),
        "latest": latest,
    }


def build_filter_options(rows: list[dict]) -> list[dict]:
    options = [
        {"key": "all", "label": "全部技能", "count": len(rows)},
        {
            "key": "active",
            "label": "已启用",
            "count": sum(1 for row in rows if row.get("Status") == "active"),
        },
        {
            "key": "removed",
            "label": "已停用",
            "count": sum(1 for row in rows if row.get("Status") == "removed"),
        },
    ]

    category_counts: dict[str, int] = {}
    for row in rows:
        top_category, _ = get_skill_category(row["Skill"])
        category_counts[top_category] = category_counts.get(top_category, 0) + 1

    for category in sorted(category_counts):
        options.append(
            {
                "key": f"category:{category}",
                "label": category,
                "count": category_counts[category],
            }
        )
    return options


def filter_skill_rows(rows: list[dict], selected_filter: str, query: str) -> list[dict]:
    return [
        item["row"]
        for item in filter_indexed_rows(
            index_registry_rows(rows), selected_filter, query
        )
    ]


class SkillRegistryApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("技能管理器")
        self.root.geometry("1500x920")
        self.root.minsize(1260, 780)
        self.rows: list[dict] = []
        self.indexed_rows: list[dict] = []
        self.usage_summary: dict[str, dict] = {}
        self.quality_reviews: dict[str, dict[str, Any]] = {}
        self.usage_events: list[dict] = []
        self.usage_overview: dict[str, Any] = {}
        self.operations_dashboard: dict[str, Any] = {}
        self.search_query_var = tk.StringVar(value="")
        self.search_results: list[dict] = []
        self.selected_filter = "all"
        self.sort_mode_var = tk.StringVar(value="installed")
        self.selected_skill_id = ""
        self.visible_limit = CARD_BATCH_SIZE
        self.filtered_indexed_rows: list[dict] = []
        self.pending_search_job: str | None = None
        self.pending_usage_refresh_job: str | None = None
        self.filter_buttons: dict[str, tk.Button] = {}
        self.card_widgets: dict[str, dict[str, Any]] = {}
        self.cards_window = None
        self.card_columns = 0

        self.status_var = tk.StringVar(value="准备就绪")
        self.detail_vars = {field: tk.StringVar(value="") for field in CSV_FIELDS}
        self.detail_text: tk.Text | None = None
        self.empty_tip_var = tk.StringVar(
            value="从中间卡片中选择一个技能，右侧会显示详情。"
        )
        self.metric_total_var = tk.StringVar(value="0")
        self.metric_active_var = tk.StringVar(value="0")
        self.metric_removed_var = tk.StringVar(value="0")
        self.metric_recent_var = tk.StringVar(value="-")
        self.results_var = tk.StringVar(value="0 个技能")
        self.load_more_var = tk.StringVar(value="")
        self.detail_usage_var = tk.StringVar(value="0 次")
        self.detail_usage_score_var = tk.StringVar(value="0")
        self.detail_quality_score_var = tk.StringVar(value="0")
        self.detail_score_var = tk.StringVar(value="0")
        self.detail_last_used_var = tk.StringVar(value="未使用")
        self.detail_recommend_var = tk.StringVar(value="-")
        self.high_usage_var = tk.StringVar(value="0")
        self.active_7d_var = tk.StringVar(value="0")
        self.sleeping_var = tk.StringVar(value="0")
        self.average_score_var = tk.StringVar(value="0")
        self.insight_var = tk.StringVar(value="")
        self.total_invocations_var = tk.StringVar(value="0")
        self.ops_collapsed = False
        self.dashboard_lists: dict[str, tk.Frame] = {}
        self.recent_usage_list: tk.Frame | None = None
        self.ops_toggle_button: ttk.Button | None = None
        self.main_vertical = None
        self.ops_shell = None

        self.bg_color = "#F5F7FA"
        self.surface_color = "#FFFFFF"
        self.panel_color = "#EEF2F6"
        self.header_color = "#EEF2F6"
        self.header_accent = "#2F80ED"
        self.header_alt = "#EAF3FF"
        self.text_color = "#1F2A37"
        self.muted_color = "#5B6875"
        self.border_color = "#D9E1EA"
        self.soft_blue = "#EAF3FF"
        self.soft_peach = "#FFF4E8"
        self.soft_green = "#EAF8F0"
        self.shadow_color = "#E7EDF5"
        self.danger_soft = "#FDECEC"
        self.button_text_on_accent = "#FFFFFF"

        self.search_query_var.trace_add("write", self._on_filter_text_changed)

        self._build_ui()
        self.refresh_data(sync_first=True)
        self._schedule_usage_refresh()

    def _configure_styles(self) -> None:
        style = ttk.Style(self.root)
        if "clam" in style.theme_names():
            style.theme_use("clam")

        self.root.configure(bg=self.bg_color)

        style.configure("App.TFrame", background=self.bg_color)
        style.configure("Surface.TFrame", background=self.surface_color)
        style.configure("Toolbar.TFrame", background=self.panel_color)
        style.configure("TopShell.TFrame", background=self.surface_color)
        style.configure(
            "Panel.TFrame",
            background=self.surface_color,
            relief="solid",
            borderwidth=1,
        )
        style.configure(
            "SoftPanel.TFrame",
            background=self.soft_blue,
            relief="solid",
            borderwidth=1,
        )
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
            background=self.surface_color,
            foreground=self.text_color,
            font=("Microsoft YaHei UI", 20, "bold"),
        )
        style.configure(
            "HeaderSub.TLabel",
            background=self.surface_color,
            foreground=self.muted_color,
            font=("Microsoft YaHei UI", 10),
        )
        style.configure(
            "HeaderBadge.TLabel",
            background=self.soft_blue,
            foreground="#2A5D9F",
            font=("Microsoft YaHei UI", 9, "bold"),
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
            foreground=self.text_color,
            font=("Segoe UI Semibold", 16, "bold"),
        )
        style.configure(
            "Muted.TLabel",
            background=self.surface_color,
            foreground=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        )
        style.configure(
            "PanelMuted.TLabel",
            background=self.soft_blue,
            foreground=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        )
        style.configure(
            "Toolbar.TButton", padding=(10, 7), font=("Microsoft YaHei UI", 9)
        )
        style.map(
            "Toolbar.TButton",
            background=[("active", self.soft_blue)],
            relief=[("pressed", "flat"), ("active", "flat")],
        )
        style.configure(
            "Accent.TButton",
            padding=(12, 8),
            font=("Microsoft YaHei UI", 9, "bold"),
            foreground=self.button_text_on_accent,
            background=self.header_accent,
            borderwidth=0,
        )
        style.map("Accent.TButton", background=[("active", "#1F6FD1")])
        style.configure(
            "Ghost.TButton",
            padding=(11, 8),
            font=("Microsoft YaHei UI", 9),
            foreground=self.text_color,
            background="#F8FAFC",
            borderwidth=0,
        )
        style.map("Ghost.TButton", background=[("active", self.soft_blue)])
        style.configure(
            "Status.TLabel",
            background=self.bg_color,
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
            background=self.panel_color,
            foreground=self.text_color,
            relief="flat",
        )
        style.map(
            "Treeview",
            background=[("selected", self.soft_blue)],
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
        style.configure(
            "Divider.TFrame",
            background=self.border_color,
        )

    def _build_ui(self) -> None:
        self._configure_styles()

        top = tk.Frame(self.root, bg=self.bg_color, padx=16, pady=16)
        top.pack(fill=tk.X)

        header = tk.Frame(
            top,
            bg=self.surface_color,
            padx=18,
            pady=16,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        header.pack(fill=tk.X)

        title_row = tk.Frame(header, bg=self.surface_color)
        title_row.pack(fill=tk.X)

        title_wrap = tk.Frame(title_row, bg=self.surface_color)
        title_wrap.pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Label(title_wrap, text="技能管理器", style="HeaderTitle.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            title_wrap,
            text="简单、清晰地查看本地 skills，快速搜索、分类、启停和进入详情。",
            style="HeaderSub.TLabel",
        ).pack(anchor=tk.W, pady=(4, 0))

        action_wrap = tk.Frame(title_row, bg=self.surface_color)
        action_wrap.pack(side=tk.RIGHT, anchor=tk.NE)
        self.global_ops_toggle_button = ttk.Button(
            action_wrap,
            text=operations_panel_toggle_label(self.ops_collapsed),
            command=self.toggle_operations_panel,
            style="Toolbar.TButton",
        )
        self.global_ops_toggle_button.pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            action_wrap, text="刷新", command=self.refresh_data, style="Toolbar.TButton"
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            action_wrap,
            text="新增技能",
            command=self.add_skill_dialog,
            style="Accent.TButton",
        ).pack(side=tk.LEFT)

        toolbar = tk.Frame(header, bg=self.panel_color, padx=12, pady=12)
        toolbar.pack(fill=tk.X, pady=(14, 0))

        search_wrap = tk.Frame(toolbar, bg=self.panel_color)
        search_wrap.pack(side=tk.LEFT, fill=tk.X, expand=True)
        search_entry = ttk.Entry(
            search_wrap, textvariable=self.search_query_var, width=40
        )
        search_entry.pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            search_wrap,
            text="远程搜索",
            command=self.search_remote_skills,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(
            search_wrap,
            text="同步注册表",
            command=self.sync_and_refresh,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT)

        quick_wrap = tk.Frame(toolbar, bg=self.panel_color)
        quick_wrap.pack(side=tk.RIGHT)
        for text, command in [
            ("打开注册表", self.open_registry_file),
            ("说明文档", self.open_readme),
            ("用途说明", self.open_usage_guide),
        ]:
            ttk.Button(
                quick_wrap, text=text, command=command, style="Toolbar.TButton"
            ).pack(side=tk.LEFT, padx=(8, 0))

        metrics = ttk.Frame(top, style="App.TFrame")
        metrics.pack(fill=tk.X, pady=(14, 0))
        self._build_metric_card(metrics, "技能总数", self.metric_total_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8)
        )
        self._build_metric_card(metrics, "已启用", self.metric_active_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=8
        )
        self._build_metric_card(metrics, "已停用", self.metric_removed_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=8
        )
        self._build_metric_card(metrics, "最近更新", self.metric_recent_var).pack(
            side=tk.LEFT, fill=tk.X, expand=True, padx=(8, 0)
        )

        main_vertical_wrap = ttk.Frame(
            self.root, style="App.TFrame", padding=(16, 0, 16, 12)
        )
        main_vertical_wrap.pack(fill=tk.BOTH, expand=True)
        self.main_vertical = ttk.PanedWindow(main_vertical_wrap, orient=tk.VERTICAL)
        self.main_vertical.pack(fill=tk.BOTH, expand=True)

        ops_shell = tk.Frame(
            self.main_vertical,
            bg=self.surface_color,
            padx=16,
            pady=14,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        self.ops_shell = ops_shell
        ops_top = tk.Frame(ops_shell, bg=self.surface_color)
        ops_top.pack(fill=tk.X)
        ttk.Label(ops_top, text="技能运营面板", style="SectionTitle.TLabel").pack(
            side=tk.LEFT
        )
        self.ops_toggle_button = ttk.Button(
            ops_top,
            text=operations_panel_toggle_label(self.ops_collapsed),
            command=self.toggle_operations_panel,
            style="Toolbar.TButton",
        )
        self.ops_toggle_button.pack(side=tk.LEFT, padx=(10, 0))
        tk.Label(
            ops_top,
            textvariable=self.insight_var,
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        ).pack(side=tk.RIGHT)

        ops_summary = ttk.Frame(ops_shell, style="App.TFrame")
        ops_summary.pack(fill=tk.X, pady=(12, 10))
        for title, var in [
            ("高频技能", self.high_usage_var),
            ("近7天活跃", self.active_7d_var),
            ("沉睡技能", self.sleeping_var),
            ("平均评分", self.average_score_var),
        ]:
            self._build_metric_card(ops_summary, title, var).pack(
                side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8)
            )

        usage_summary_strip = ttk.Frame(ops_shell, style="App.TFrame")
        usage_summary_strip.pack(fill=tk.X, pady=(0, 10))
        self._build_metric_card(
            usage_summary_strip, "总调用次数", self.total_invocations_var
        ).pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        ops_lists = tk.Frame(ops_shell, bg=self.surface_color)
        ops_lists.pack(fill=tk.X)
        for idx, (key, title) in enumerate(
            [
                ("top_used", "Top 常用"),
                ("recent_active", "最近活跃"),
                ("cleanup_candidates", "待清理"),
            ]
        ):
            panel = tk.Frame(
                ops_lists,
                bg="#F8FAFC",
                padx=12,
                pady=10,
                highlightbackground=self.border_color,
                highlightthickness=1,
            )
            panel.pack(
                side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0 if idx == 0 else 8, 0)
            )
            tk.Label(
                panel,
                text=title,
                bg="#F8FAFC",
                fg=self.text_color,
                font=("Microsoft YaHei UI", 9, "bold"),
            ).pack(anchor=tk.W)
            body = tk.Frame(panel, bg="#F8FAFC")
            body.pack(fill=tk.X, pady=(8, 0))
            self.dashboard_lists[key] = body

        recent_usage_panel = tk.Frame(
            ops_shell,
            bg="#F8FAFC",
            padx=12,
            pady=10,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        recent_usage_panel.pack(fill=tk.X, pady=(10, 0))
        tk.Label(
            recent_usage_panel,
            text="最近真实 skill 调用",
            bg="#F8FAFC",
            fg=self.text_color,
            font=("Microsoft YaHei UI", 9, "bold"),
        ).pack(anchor=tk.W)
        self.recent_usage_list = tk.Frame(recent_usage_panel, bg="#F8FAFC")
        self.recent_usage_list.pack(fill=tk.X, pady=(8, 0))

        body = ttk.Frame(self.main_vertical, style="App.TFrame")
        layout = ttk.PanedWindow(body, orient=tk.HORIZONTAL)
        layout.pack(fill=tk.BOTH, expand=True)

        sidebar = tk.Frame(
            layout,
            bg=self.surface_color,
            padx=14,
            pady=14,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        center = tk.Frame(
            layout,
            bg=self.surface_color,
            padx=14,
            pady=14,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        detail = tk.Frame(
            layout,
            bg=self.surface_color,
            padx=14,
            pady=14,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        layout.add(sidebar, weight=1)
        layout.add(center, weight=3)
        layout.add(detail, weight=2)
        self.main_vertical.add(ops_shell, weight=1)
        self.main_vertical.add(body, weight=4)

        ttk.Label(sidebar, text="分类导航", style="SectionTitle.TLabel").pack(
            anchor=tk.W
        )
        tk.Label(
            sidebar,
            text="按状态或分类筛选，尽量减少找技能的时间。",
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9),
            justify=tk.LEFT,
            wraplength=210,
        ).pack(anchor=tk.W, pady=(6, 12))

        self.filter_nav = tk.Frame(sidebar, bg=self.surface_color)
        self.filter_nav.pack(fill=tk.BOTH, expand=True)

        center_top = tk.Frame(center, bg=self.surface_color)
        center_top.pack(fill=tk.X)
        ttk.Label(center_top, text="技能卡片", style="SectionTitle.TLabel").pack(
            side=tk.LEFT
        )
        sort_wrap = tk.Frame(center_top, bg=self.surface_color)
        sort_wrap.pack(side=tk.RIGHT)
        tk.Label(
            sort_wrap,
            text="排序",
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        ).pack(side=tk.LEFT, padx=(0, 6))
        self.sort_menu = ttk.Combobox(
            sort_wrap,
            state="readonly",
            width=14,
            values=[SORT_MODE_OPTIONS[key] for key in ("installed", "score", "usage")],
        )
        self.sort_menu.current(0)
        self.sort_menu.bind("<<ComboboxSelected>>", self._on_sort_mode_changed)
        self.sort_menu.pack(side=tk.LEFT, padx=(0, 10))
        tk.Label(
            center_top,
            textvariable=self.results_var,
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        ).pack(side=tk.RIGHT)

        center_hint = tk.Label(
            center,
            text="卡片里只保留最关键的信息：名称、用途、状态、更新时间和快捷操作。",
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        )
        center_hint.pack(anchor=tk.W, pady=(6, 12))

        cards_shell = tk.Frame(center, bg=self.bg_color)
        cards_shell.pack(fill=tk.BOTH, expand=True)

        self.cards_canvas = tk.Canvas(
            cards_shell,
            bg=self.bg_color,
            highlightthickness=0,
            bd=0,
        )
        cards_scroll = ttk.Scrollbar(
            cards_shell, orient=tk.VERTICAL, command=self.cards_canvas.yview
        )
        self.cards_canvas.configure(yscrollcommand=cards_scroll.set)
        self.cards_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        cards_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        self.cards_frame = tk.Frame(self.cards_canvas, bg=self.bg_color)
        self.cards_window = self.cards_canvas.create_window(
            (0, 0), window=self.cards_frame, anchor="nw"
        )
        self.cards_frame.bind("<Configure>", self._on_cards_frame_configured)
        self.cards_canvas.bind("<Configure>", self._on_cards_canvas_configured)
        self._bind_mousewheel(self.cards_canvas)
        self._bind_mousewheel(cards_shell)
        self._bind_mousewheel(self.cards_frame)

        load_more_wrap = tk.Frame(center, bg=self.surface_color)
        load_more_wrap.pack(fill=tk.X, pady=(12, 0))
        self.load_more_label = tk.Label(
            load_more_wrap,
            textvariable=self.load_more_var,
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9),
        )
        self.load_more_label.pack(side=tk.LEFT)
        self.load_more_button = ttk.Button(
            load_more_wrap,
            text="加载更多",
            command=self.load_more_cards,
            style="Toolbar.TButton",
        )
        self.load_more_button.pack(side=tk.RIGHT)

        ttk.Label(detail, text="技能详情", style="SectionTitle.TLabel").pack(
            anchor=tk.W
        )
        ttk.Label(
            detail, textvariable=self.detail_vars["Skill"], style="HeroValue.TLabel"
        ).pack(anchor=tk.W, pady=(8, 4))
        tk.Label(
            detail,
            textvariable=self.empty_tip_var,
            bg=self.surface_color,
            fg=self.muted_color,
            justify=tk.LEFT,
            wraplength=320,
            font=("Microsoft YaHei UI", 9),
        ).pack(anchor=tk.W)

        detail_actions = tk.Frame(detail, bg=self.surface_color)
        detail_actions.pack(fill=tk.X, pady=(14, 12))
        ttk.Button(
            detail_actions,
            text="打开技能目录",
            command=self.open_skill_dir,
            style="Accent.TButton",
        ).pack(side=tk.LEFT)
        ttk.Button(
            detail_actions,
            text="编辑说明",
            command=self.edit_selected_skill,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=(8, 0))
        ttk.Button(
            detail_actions,
            text="删除技能",
            command=self.delete_selected_skill,
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=(8, 0))

        detail_grid = tk.Frame(detail, bg=self.surface_color)
        detail_grid.pack(fill=tk.X, pady=(0, 12))

        detail_fields = [
            ("状态", "Status"),
            ("归属", "Agent"),
            ("首次安装", "Installed"),
            ("最近更新", "LastUpdated"),
            ("使用次数", "__usage_count__"),
            ("热度分", "__usage_score__"),
            ("质量分", "__quality_score__"),
            ("综合评分", "__score__"),
            ("最近使用", "__last_used__"),
            ("推荐搭配", "__recommend__"),
            ("来源", "Source"),
            ("本地路径", "LocalPath"),
            ("用途", "Purpose"),
        ]
        for row_index, (label_text, key) in enumerate(detail_fields):
            tk.Label(
                detail_grid,
                text=label_text,
                bg=self.surface_color,
                fg=self.muted_color,
                font=("Microsoft YaHei UI", 9, "bold"),
                anchor="w",
            ).grid(row=row_index, column=0, sticky="nw", pady=4)
            if key == "__usage_count__":
                value_source = self.detail_usage_var
            elif key == "__usage_score__":
                value_source = self.detail_usage_score_var
            elif key == "__quality_score__":
                value_source = self.detail_quality_score_var
            elif key == "__score__":
                value_source = self.detail_score_var
            elif key == "__last_used__":
                value_source = self.detail_last_used_var
            elif key == "__recommend__":
                value_source = self.detail_recommend_var
            else:
                value_source = self.detail_vars[key]
            tk.Label(
                detail_grid,
                textvariable=value_source,
                bg=self.surface_color,
                fg=self.text_color,
                font=("Microsoft YaHei UI", 9),
                anchor="w",
                justify=tk.LEFT,
                wraplength=250,
            ).grid(row=row_index, column=1, sticky="nw", padx=(10, 0), pady=4)

        detail_grid.columnconfigure(1, weight=1)

        tk.Label(
            detail,
            text="备注",
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9, "bold"),
        ).pack(anchor=tk.W)
        self.detail_text = tk.Text(
            detail,
            height=9,
            wrap=tk.WORD,
            relief=tk.FLAT,
            bg="#F8FAFC",
            fg=self.text_color,
            font=("Microsoft YaHei UI", 9),
            padx=10,
            pady=10,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )
        self.detail_text.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
        self.detail_text.configure(state=tk.DISABLED)

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
        frame.configure(style="Surface.TFrame")
        frame["padding"] = (14, 12)
        ttk.Label(frame, text=title, style="MetricTitle.TLabel").pack(anchor=tk.W)
        ttk.Label(frame, textvariable=variable, style="MetricValue.TLabel").pack(
            anchor=tk.W, pady=(6, 0)
        )
        return frame

    def _build_filter_button(self, parent: tk.Frame, text: str, key: str) -> None:
        button = tk.Button(
            parent,
            text=text,
            anchor="w",
            relief=tk.FLAT,
            bd=0,
            padx=12,
            pady=8,
            font=("Microsoft YaHei UI", 9),
            command=lambda value=key: self.set_filter(value),
            cursor="hand2",
        )
        button.pack(fill=tk.X, pady=3)
        self.filter_buttons[key] = button
        self._style_filter_button(button, key == self.selected_filter)

    def _style_filter_button(self, button: tk.Button, selected: bool) -> None:
        if selected:
            button.configure(
                bg=self.soft_blue,
                fg=self.header_accent,
                activebackground=self.soft_blue,
                activeforeground=self.header_accent,
            )
        else:
            button.configure(
                bg=self.surface_color,
                fg=self.text_color,
                activebackground="#F1F5F9",
                activeforeground=self.text_color,
            )

    def _render_filters(self) -> None:
        for child in self.filter_nav.winfo_children():
            child.destroy()
        self.filter_buttons.clear()

        filters = build_filter_options(self.rows)
        primary = tk.Frame(self.filter_nav, bg=self.surface_color)
        primary.pack(fill=tk.X, pady=(0, 14))
        tk.Label(
            primary,
            text="常用视图",
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9, "bold"),
        ).pack(anchor=tk.W, pady=(0, 8))

        for item in filters[:3]:
            self._build_filter_button(
                primary, f"{item['label']}  ({item['count']})", item["key"]
            )

        category_frame = tk.Frame(self.filter_nav, bg=self.surface_color)
        category_frame.pack(fill=tk.X)
        tk.Label(
            category_frame,
            text="按分类查看",
            bg=self.surface_color,
            fg=self.muted_color,
            font=("Microsoft YaHei UI", 9, "bold"),
        ).pack(anchor=tk.W, pady=(0, 8))
        for item in filters[3:]:
            self._build_filter_button(
                category_frame, f"{item['label']}  ({item['count']})", item["key"]
            )

    def _on_cards_frame_configured(self, _event=None) -> None:
        self.cards_canvas.configure(scrollregion=self.cards_canvas.bbox("all"))

    def _on_cards_canvas_configured(self, event) -> None:
        if self.cards_window is not None:
            self.cards_canvas.itemconfigure(self.cards_window, width=event.width)
        columns = self._card_column_count(event.width)
        if columns != self.card_columns:
            self.card_columns = columns
            self._render_cards()

    def _bind_mousewheel(self, widget: tk.Misc) -> None:
        widget.bind("<MouseWheel>", self._on_cards_mousewheel, add="+")
        widget.bind("<Button-4>", self._on_cards_mousewheel_linux, add="+")
        widget.bind("<Button-5>", self._on_cards_mousewheel_linux, add="+")

    def _bind_mousewheel_tree(self, widget: tk.Misc) -> None:
        self._bind_mousewheel(widget)
        for child in widget.winfo_children():
            self._bind_mousewheel_tree(child)

    def _on_cards_mousewheel(self, event) -> str | None:
        units = mousewheel_units(getattr(event, "delta", 0))
        if units:
            self.cards_canvas.yview_scroll(units, "units")
            return "break"
        return None

    def _on_cards_mousewheel_linux(self, event) -> str:
        units = -1 if getattr(event, "num", None) == 4 else 1
        self.cards_canvas.yview_scroll(units, "units")
        return "break"

    def _card_column_count(self, width: int) -> int:
        if width >= 1180:
            return 3
        if width >= 760:
            return 2
        return 1

    def _filtered_rows(self) -> list[dict]:
        return [item["row"] for item in self.filtered_indexed_rows]

    def _reindex_rows(self) -> None:
        self.indexed_rows = index_registry_rows(
            self.rows,
            self.usage_summary,
            sort_mode=self.sort_mode_var.get(),
        )

    def _schedule_usage_refresh(self) -> None:
        if self.pending_usage_refresh_job is not None:
            self.root.after_cancel(self.pending_usage_refresh_job)
        self.pending_usage_refresh_job = self.root.after(
            USAGE_REFRESH_MS, self._poll_usage_summary
        )

    def _poll_usage_summary(self) -> None:
        self.pending_usage_refresh_job = None
        try:
            latest_events = load_skill_usage_events()
            latest_usage = merge_skill_metrics(
                self.rows,
                load_skill_usage_summary(),
                self.quality_reviews,
            )
            if (
                usage_summary_changed(self.usage_summary, latest_usage)
                or self.usage_events != latest_events
            ):
                self.usage_events = latest_events
                self.usage_summary = latest_usage
                self._refresh_operations_dashboard()
                self._reindex_rows()
                self._refresh_visible_rows(reset_limit=False)
                self.status_var.set("已自动刷新 skill 使用统计")
        finally:
            if self.root.winfo_exists():
                self._schedule_usage_refresh()

    def _on_filter_text_changed(self, *_args) -> None:
        if self.pending_search_job is not None:
            self.root.after_cancel(self.pending_search_job)
        self.pending_search_job = self.root.after(
            SEARCH_DEBOUNCE_MS, self._apply_debounced_search
        )

    def _apply_debounced_search(self) -> None:
        self.pending_search_job = None
        self._refresh_visible_rows(reset_limit=True)

    def _on_sort_mode_changed(self, _event=None) -> None:
        labels = {value: key for key, value in SORT_MODE_OPTIONS.items()}
        self.sort_mode_var.set(labels.get(self.sort_menu.get(), "installed"))
        self._reindex_rows()
        self._refresh_visible_rows(reset_limit=True)

    def set_filter(self, key: str) -> None:
        self.selected_filter = key
        for button_key, button in self.filter_buttons.items():
            self._style_filter_button(button, button_key == key)
        self._refresh_visible_rows(reset_limit=True)

    def _refresh_visible_rows(self, reset_limit: bool = False) -> None:
        if reset_limit:
            self.visible_limit = CARD_BATCH_SIZE
        self.filtered_indexed_rows = filter_indexed_rows(
            self.indexed_rows, self.selected_filter, self.search_query_var.get()
        )
        filtered = self.filtered_indexed_rows
        self.results_var.set(f"{len(filtered)} 个技能")

        if filtered:
            if not any(
                item["row"]["ID"] == self.selected_skill_id for item in filtered
            ):
                self.selected_skill_id = filtered[0]["row"]["ID"]
        else:
            self.selected_skill_id = ""
        self._render_cards(filtered)
        self._sync_detail_panel()

    def refresh_data(self, sync_first: bool = False) -> None:
        if sync_first:
            self.rows = sync_registry()
        else:
            self.rows = load_registry()
        self.usage_events = load_skill_usage_events()
        self.quality_reviews = load_skill_quality_reviews()
        self.usage_summary = merge_skill_metrics(
            self.rows,
            load_skill_usage_summary(),
            self.quality_reviews,
        )
        self._refresh_operations_dashboard()
        self._reindex_rows()

        self._refresh_metrics()
        self._render_filters()
        if self.selected_filter not in self.filter_buttons:
            self.selected_filter = "all"
        for button_key, button in self.filter_buttons.items():
            self._style_filter_button(button, button_key == self.selected_filter)
        if not any(row["ID"] == self.selected_skill_id for row in self.rows):
            self.selected_skill_id = ""
        self._refresh_visible_rows(reset_limit=True)
        self.status_var.set(f"已加载 {len(self.rows)} 个 skill")

    def _refresh_metrics(self) -> None:
        summary = summarize_registry_rows(self.rows)
        self.metric_total_var.set(str(summary["total"]))
        self.metric_active_var.set(str(summary["active"]))
        self.metric_removed_var.set(str(summary["removed"]))
        self.metric_recent_var.set(summary["latest"])

    def _render_dashboard_list(self, key: str, items: list[dict]) -> None:
        container = self.dashboard_lists.get(key)
        if container is None:
            return
        for child in container.winfo_children():
            child.destroy()
        if not items:
            tk.Label(
                container,
                text="暂无数据",
                bg="#F8FAFC",
                fg=self.muted_color,
                font=("Microsoft YaHei UI", 9),
            ).pack(anchor=tk.W)
            return
        for item in dashboard_preview_items(items):
            skill_name = item["Skill"]
            btn = tk.Button(
                container,
                text=f"{get_skill_display_name(skill_name)}  ·  {item.get('usage_count', 0)}次 / {item.get('score', 0)}分",
                anchor="w",
                relief=tk.FLAT,
                bd=0,
                bg="#F8FAFC",
                fg=self.text_color,
                activebackground=self.soft_blue,
                activeforeground=self.text_color,
                font=("Microsoft YaHei UI", 9),
                cursor="hand2",
                command=lambda row_id=item["ID"]: self.select_skill(row_id),
            )
            btn.pack(fill=tk.X, pady=2)

    def _render_recent_usage_events(self) -> None:
        if self.recent_usage_list is None:
            return
        for child in self.recent_usage_list.winfo_children():
            child.destroy()
        recent_events = self.usage_overview.get("recent_events", [])
        if not recent_events:
            tk.Label(
                self.recent_usage_list,
                text="还没有捕获到真实 skill 调用记录",
                bg="#F8FAFC",
                fg=self.muted_color,
                font=("Microsoft YaHei UI", 9),
            ).pack(anchor=tk.W)
            return
        for event in recent_events:
            tk.Label(
                self.recent_usage_list,
                text=f"{event['time_text']}  ·  {event['skill']}",
                bg="#F8FAFC",
                fg=self.text_color,
                font=("Microsoft YaHei UI", 9),
                anchor="w",
                justify=tk.LEFT,
            ).pack(anchor=tk.W, pady=2)

    def toggle_operations_panel(self) -> None:
        if self.main_vertical is None or self.ops_shell is None:
            return
        self.ops_collapsed = not self.ops_collapsed
        label = operations_panel_toggle_label(self.ops_collapsed)
        if self.ops_collapsed:
            self.main_vertical.forget(self.ops_shell)
            self.status_var.set("已收起技能运营面板")
        else:
            self.main_vertical.insert(0, self.ops_shell, weight=1)
            self.status_var.set("已展开技能运营面板")
        if self.ops_toggle_button is not None:
            self.ops_toggle_button.configure(text=label)
        if getattr(self, "global_ops_toggle_button", None) is not None:
            self.global_ops_toggle_button.configure(text=label)

    def _refresh_operations_dashboard(self) -> None:
        self.operations_dashboard = build_operations_dashboard(
            self.rows, self.usage_summary
        )
        self.usage_overview = build_usage_overview(self.usage_events)
        summary = self.operations_dashboard["summary"]
        self.high_usage_var.set(str(summary["high_usage_count"]))
        self.active_7d_var.set(str(summary["active_7d_count"]))
        self.sleeping_var.set(str(summary["sleeping_count"]))
        self.average_score_var.set(str(summary["average_score"]))
        self.total_invocations_var.set(
            str(self.usage_overview.get("total_invocations", 0))
        )
        self.insight_var.set(self.operations_dashboard["insight_text"])
        self._render_dashboard_list("top_used", self.operations_dashboard["top_used"])
        self._render_dashboard_list(
            "recent_active", self.operations_dashboard["recent_active"]
        )
        self._render_dashboard_list(
            "cleanup_candidates", self.operations_dashboard["cleanup_candidates"]
        )
        self._render_recent_usage_events()

    def sync_and_refresh(self) -> None:
        self.refresh_data(sync_first=True)
        self.status_var.set("已同步技能目录和注册表")

    def clear_details(self) -> None:
        for var in self.detail_vars.values():
            var.set("-")
        self.detail_vars["Skill"].set("未选择技能")
        self.empty_tip_var.set("从中间卡片中选择一个技能，右侧会显示详情。")
        self.detail_usage_var.set("0 次")
        self.detail_usage_score_var.set("0")
        self.detail_quality_score_var.set("0")
        self.detail_score_var.set("0")
        self.detail_last_used_var.set("未使用")
        self.detail_recommend_var.set("-")
        if self.detail_text is None:
            return
        self.detail_text.configure(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        self.detail_text.configure(state=tk.DISABLED)

    def selected_row(self) -> dict | None:
        for row in self.rows:
            if row["ID"] == self.selected_skill_id:
                return row
        return None

    def _sync_detail_panel(self) -> None:
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
        self.detail_vars["Skill"].set(get_skill_display_name(row["Skill"]))
        top_category, sub_category = get_skill_category(row["Skill"])
        usage = self.usage_summary.get(row["Skill"], {})
        self.detail_usage_var.set(f"{int(usage.get('usage_count', 0))} 次")
        self.detail_usage_score_var.set(str(int(usage.get("usage_score", 0))))
        self.detail_quality_score_var.set(str(int(usage.get("quality_score", 0))))
        self.detail_score_var.set(str(int(usage.get("score", 0))))
        self.detail_last_used_var.set(str(usage.get("last_used", "未使用")))
        recommendations = [
            get_skill_display_name(item)
            for item in get_skill_recommendations(row["Skill"])
        ]
        self.detail_recommend_var.set(
            " / ".join(recommendations) if recommendations else "-"
        )
        self.empty_tip_var.set(
            f"{top_category} / {sub_category} · 可直接打开目录或编辑说明。"
        )

        if self.detail_text is None:
            return
        self.detail_text.configure(state=tk.NORMAL)
        self.detail_text.delete("1.0", tk.END)
        notes = row.get("Notes", "")
        quality_summary = str(usage.get("quality_summary", "")).strip()
        quality_reviewed_at = str(usage.get("quality_reviewed_at", "")).strip()
        recommendation_notes = usage.get("quality_recommendations", []) or []
        note_parts = []
        if quality_summary:
            note_parts.append(f"质量审查：{quality_summary}")
        if recommendation_notes:
            note_parts.append(
                "改进建议：" + "；".join(str(item) for item in recommendation_notes[:3])
            )
        if quality_reviewed_at:
            note_parts.append(f"审查时间：{quality_reviewed_at}")
        if notes:
            note_parts.append(f"备注：{notes}")
        self.detail_text.insert("1.0", "\n\n".join(note_parts) if note_parts else notes)
        self.detail_text.configure(state=tk.DISABLED)

    def _render_cards(self, filtered_rows: list[dict] | None = None) -> None:
        if filtered_rows is None:
            filtered_rows = self.filtered_indexed_rows

        for child in self.cards_frame.winfo_children():
            child.destroy()
        self.card_widgets.clear()

        if not filtered_rows:
            empty = tk.Frame(
                self.cards_frame,
                bg=self.surface_color,
                padx=28,
                pady=28,
                highlightbackground=self.border_color,
                highlightthickness=1,
            )
            empty.grid(row=0, column=0, sticky="ew", padx=4, pady=4)
            tk.Label(
                empty,
                text="没有找到匹配的技能",
                bg=self.surface_color,
                fg=self.text_color,
                font=("Microsoft YaHei UI", 13, "bold"),
            ).pack(anchor=tk.W)
            tk.Label(
                empty,
                text="可以换一个搜索词，或从左侧切回“全部技能”。",
                bg=self.surface_color,
                fg=self.muted_color,
                font=("Microsoft YaHei UI", 9),
            ).pack(anchor=tk.W, pady=(8, 0))
            self.cards_frame.columnconfigure(0, weight=1)
            self.load_more_var.set("")
            self.load_more_button.pack_forget()
            return

        visible_rows, remaining = limit_visible_rows(filtered_rows, self.visible_limit)

        columns = self.card_columns or self._card_column_count(
            self.cards_canvas.winfo_width()
        )
        for col in range(columns):
            self.cards_frame.columnconfigure(col, weight=1)

        for index, item in enumerate(visible_rows):
            card = self._create_skill_card(self.cards_frame, item)
            card.grid(
                row=index // columns,
                column=index % columns,
                sticky="nsew",
                padx=6,
                pady=6,
            )
        if remaining > 0:
            self.load_more_var.set(f"还有 {remaining} 个技能未显示")
            if not self.load_more_button.winfo_manager():
                self.load_more_button.pack(side=tk.RIGHT)
        else:
            self.load_more_var.set("已显示全部技能")
            self.load_more_button.pack_forget()

    def _create_skill_card(self, parent: tk.Frame, item: dict) -> tk.Frame:
        row = item["row"]
        selected = row["ID"] == self.selected_skill_id
        card = tk.Frame(
            parent,
            bg=self.surface_color,
            padx=14,
            pady=14,
            highlightbackground=self.border_color,
            highlightthickness=1,
        )

        header = tk.Frame(card, bg=self.surface_color)
        header.pack(fill=tk.X)
        icon = tk.Label(
            header,
            text=CATEGORY_ICON_MAP.get(item["top_category"], "•"),
            bg=self.panel_color,
            fg=self.header_accent,
            width=3,
            pady=6,
            font=("Segoe UI Symbol", 11, "bold"),
        )
        icon.pack(side=tk.LEFT)

        title_wrap = tk.Frame(header, bg=self.surface_color)
        title_wrap.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 8))
        tk.Label(
            title_wrap,
            text=item["display_name"],
            bg=self.surface_color,
            fg=self.text_color,
            anchor="w",
            justify=tk.LEFT,
            wraplength=280,
            font=("Microsoft YaHei UI", 10, "bold"),
        ).pack(anchor=tk.W)
        tk.Label(
            title_wrap,
            text=f"{item['top_category']} / {item['sub_category']}",
            bg=self.surface_color,
            fg=self.muted_color,
            anchor="w",
            font=("Microsoft YaHei UI", 8),
        ).pack(anchor=tk.W, pady=(4, 0))

        status_bg, status_fg = self._status_colors(row.get("Status", ""))
        status_chip = tk.Label(
            header,
            text=item["status_label"],
            bg=status_bg,
            fg=status_fg,
            padx=10,
            pady=4,
            font=("Microsoft YaHei UI", 8, "bold"),
        )
        status_chip.pack(side=tk.RIGHT)

        tk.Label(
            card,
            text=row.get("Purpose", "未填写用途说明"),
            bg=self.surface_color,
            fg=self.text_color,
            justify=tk.LEFT,
            wraplength=320,
            font=("Microsoft YaHei UI", 9),
        ).pack(anchor=tk.W, pady=(12, 10))

        meta = tk.Frame(card, bg=self.surface_color)
        meta.pack(fill=tk.X)
        for text in [
            f"更新 {row.get('LastUpdated') or '-'}",
            f"来源 {row.get('Source') or '-'}",
        ]:
            tk.Label(
                meta,
                text=text,
                bg=self.panel_color,
                fg=self.muted_color,
                padx=8,
                pady=4,
                font=("Microsoft YaHei UI", 8),
            ).pack(side=tk.LEFT, padx=(0, 8))

        usage_row = tk.Frame(card, bg=self.surface_color)
        usage_row.pack(fill=tk.X, pady=(10, 0))
        for text, bg, fg in [
            (f"已用 {item['usage_count']} 次", self.panel_color, self.muted_color),
            (f"质量 {item.get('quality_score', 0)}", self.soft_peach, "#B76E00"),
            (f"综合 {item['score']}", self.soft_blue, self.header_accent),
            (f"最近使用 {item['last_used']}", self.soft_green, "#1F7A48"),
        ]:
            tk.Label(
                usage_row,
                text=text,
                bg=bg,
                fg=fg,
                padx=8,
                pady=4,
                font=("Microsoft YaHei UI", 8),
            ).pack(side=tk.LEFT, padx=(0, 8))

        actions = tk.Frame(card, bg=self.surface_color)
        actions.pack(fill=tk.X, pady=(12, 0))
        detail_button = ttk.Button(
            actions,
            text="详情",
            command=lambda row_id=row["ID"]: self.select_skill(row_id),
            style="Ghost.TButton",
        )
        detail_button.pack(side=tk.LEFT)
        ttk.Button(
            actions,
            text="打开",
            command=lambda row_id=row["ID"]: self.open_skill_dir_for(row_id),
            style="Toolbar.TButton",
        ).pack(side=tk.LEFT, padx=(8, 0))

        for widget in (card, header, title_wrap, icon, meta):
            self._bind_select_click(widget, row["ID"])
        self._bind_mousewheel_tree(card)
        self.card_widgets[row["ID"]] = {
            "frame": card,
            "icon": icon,
            "detail_button": detail_button,
            "selected": selected,
        }
        self._apply_card_selection_state(row["ID"], selected)
        return card

    def _bind_select_click(self, widget: tk.Widget, row_id: str) -> None:
        widget.bind("<Button-1>", lambda _event, value=row_id: self.select_skill(value))

    def _status_colors(self, status: str) -> tuple[str, str]:
        if status == "active":
            return (self.soft_green, "#1F7A48")
        if status == "removed":
            return (self.danger_soft, "#B54747")
        return (self.panel_color, self.muted_color)

    def _apply_card_selection_state(self, row_id: str, selected: bool) -> None:
        controls = self.card_widgets.get(row_id)
        if not controls:
            return
        frame = controls["frame"]
        icon = controls["icon"]
        detail_button = controls["detail_button"]
        frame.configure(
            highlightbackground=self.header_accent if selected else self.border_color,
            highlightthickness=2 if selected else 1,
        )
        icon.configure(bg=self.soft_blue if selected else self.panel_color)
        detail_button.configure(style="Accent.TButton" if selected else "Ghost.TButton")
        controls["selected"] = selected

    def select_skill(self, row_id: str) -> None:
        previous = self.selected_skill_id
        if previous == row_id:
            self._sync_detail_panel()
            return
        self.selected_skill_id = row_id
        if previous:
            self._apply_card_selection_state(previous, False)
        if row_id in self.card_widgets:
            self._apply_card_selection_state(row_id, True)
        else:
            self._render_cards()
        self._sync_detail_panel()

    def load_more_cards(self) -> None:
        self.visible_limit += CARD_BATCH_SIZE
        self._render_cards(self.filtered_indexed_rows)

    def open_skill_dir_for(self, row_id: str) -> None:
        self.selected_skill_id = row_id
        self._sync_detail_panel()
        self.open_skill_dir()

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

        header = tk.Frame(window, bg=self.surface_color, padx=18, pady=14)
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
