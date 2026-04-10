from __future__ import annotations

import argparse
import csv
import json
import re
from datetime import datetime
from pathlib import Path


CLAUDE_SKILLS_DIR = Path.home() / ".claude" / "skills"
AGENTS_SKILLS_DIR = Path.home() / ".agents" / "skills"
SKILL_BASE_DIRS = (CLAUDE_SKILLS_DIR, AGENTS_SKILLS_DIR)
REGISTRY_PATH = CLAUDE_SKILLS_DIR / "SKILLS_REGISTRY.csv"
OUTPUT_PATH = CLAUDE_SKILLS_DIR / "skill-registry" / "skill_quality_reviews.json"
GENERIC_PURPOSE_FRAGMENTS = (
    "相关任务",
    "仓库导入",
    "工作流场景整理展示",
    "安全审计、漏洞分析和风险检测",
    "代码评审、差异检查和问题发现",
    "任务规划、拆解执行和多代理协作",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Review local skill quality")
    parser.add_argument("--skill", help="Review one skill by directory name")
    parser.add_argument("--all", action="store_true", help="Review all local skills")
    parser.add_argument("--output", default=str(OUTPUT_PATH), help="Output json path")
    return parser.parse_args()


def iter_skill_dirs() -> list[Path]:
    results_by_name: dict[str, Path] = {}
    for base_dir in SKILL_BASE_DIRS:
        if not base_dir.exists():
            continue
        for item in base_dir.iterdir():
            if item.is_dir() and (item / "SKILL.md").exists():
                results_by_name[item.name] = item
    return sorted(results_by_name.values(), key=lambda p: p.name.lower())


def load_registry() -> dict[str, dict[str, str]]:
    if not REGISTRY_PATH.exists():
        return {}
    with REGISTRY_PATH.open("r", encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.DictReader(handle))
    return {row.get("Skill", ""): row for row in rows if row.get("Skill")}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    data: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def extract_markdown_refs(text: str) -> list[str]:
    return re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)


def score_metadata(frontmatter: dict[str, str]) -> tuple[int, list[str], list[str]]:
    score = 0
    strengths: list[str] = []
    issues: list[str] = []
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if name:
        score += 35
        strengths.append("frontmatter 包含稳定的 name")
    else:
        issues.append("缺少 frontmatter name")
    if description:
        score += 30
        strengths.append("frontmatter 包含 description")
        if "use when" in description.lower():
            score += 15
            strengths.append("description 说明了触发时机")
        else:
            issues.append("description 没有显式说明何时使用")
        if 40 <= len(description) <= 220:
            score += 10
        else:
            issues.append("description 长度不理想，可能过短或过长")
        if not re.search(r"\b(i|you|we)\b", description.lower()):
            score += 10
        else:
            issues.append("description 视角不够稳定，建议改成第三人称/中性表述")
    else:
        issues.append("缺少 frontmatter description")
    return min(100, score), strengths, issues


def score_structure(text: str) -> tuple[int, list[str], list[str]]:
    lower = text.lower()
    score = 0
    strengths: list[str] = []
    issues: list[str] = []
    if re.search(r"^#\s+", text, re.MULTILINE):
        score += 15
    else:
        issues.append("缺少主标题")
    for marker, points, label in (
        ("## core rule", 20, "包含 Core Rule"),
        ("## when to use", 20, "包含 When To Use"),
        ("## workflow", 25, "包含 Workflow"),
        ("## anti-pattern", 10, "包含 Anti-Patterns"),
        ("## related", 10, "包含 Related References/Notes"),
    ):
        if marker in lower:
            score += points
            strengths.append(label)
    if score < 55:
        issues.append("结构不够清晰，建议补齐 Core Rule / When To Use / Workflow")
    return min(100, score), strengths, issues


def score_local_alignment(
    text: str, frontmatter: dict[str, str]
) -> tuple[int, list[str], list[str]]:
    lower = text.lower()
    score = 0
    strengths: list[str] = []
    issues: list[str] = []
    if any(
        tool in text
        for tool in (
            "`Read`",
            "`Glob`",
            "`Grep`",
            "`Bash`",
            "`apply_patch`",
            "`TodoWrite`",
            "`Task`",
        )
    ):
        score += 35
        strengths.append("内容与本地 OpenCode 工具对齐")
    elif "tool" not in lower:
        score += 20
    else:
        issues.append("提到了工具但未明显对齐本地 OpenCode 工具")
    if "\\" not in text:
        score += 15
    else:
        issues.append("出现反斜杠路径，建议统一成 / 风格")
    if set(frontmatter).issubset(
        {"name", "description", "argument-hint", "model", "allowed-tools"}
    ):
        score += 20
    else:
        issues.append("frontmatter 含未知字段，建议检查是否真的适用于本地环境")
    if "opencode" in lower or "local" in lower or "registry" in lower:
        score += 20
        strengths.append("明确考虑了本地 OpenCode/registry 场景")
    else:
        issues.append("缺少本地 OpenCode 场景说明")
    return min(100, score), strengths, issues


def score_maintainability(
    skill_dir: Path, text: str
) -> tuple[int, list[str], list[str]]:
    score = 0
    strengths: list[str] = []
    issues: list[str] = []
    line_count = len(text.splitlines())
    if line_count <= 220:
        score += 35
        strengths.append("主文件长度适中")
    elif line_count <= 500:
        score += 25
    else:
        issues.append("主文件过长，建议拆成引用文件")
    if "todo" not in text.lower() and "tbd" not in text.lower():
        score += 20
    else:
        issues.append("文件中仍有 TODO/TBD 占位")
    refs = extract_markdown_refs(text)
    nested_refs = [ref for ref in refs if ref.count("/") > 2]
    if not nested_refs:
        score += 20
        strengths.append("引用层级较浅")
    else:
        issues.append("引用层级较深，可能影响按需加载")
    extra_files = [
        p for p in skill_dir.rglob("*") if p.is_file() and p.name != "SKILL.md"
    ]
    if extra_files:
        score += 10
        strengths.append("包含可扩展的辅助文件")
    else:
        score += 5
    if skill_dir.name.islower():
        score += 10
    return min(100, score), strengths, issues


def score_registry_alignment(
    skill_name: str, registry_row: dict[str, str] | None
) -> tuple[int, list[str], list[str]]:
    score = 0
    strengths: list[str] = []
    issues: list[str] = []
    if registry_row:
        score += 35
        strengths.append("注册表中存在对应条目")
        purpose = registry_row.get("Purpose", "")
        notes = registry_row.get("Notes", "")
        if purpose and not any(
            fragment in purpose for fragment in GENERIC_PURPOSE_FRAGMENTS
        ):
            score += 35
            strengths.append("注册表用途说明较具体")
        else:
            issues.append("注册表用途说明仍偏泛化")
        if notes and len(notes.strip()) >= 8:
            score += 20
        else:
            issues.append("注册表备注信息偏少")
        if registry_row.get("Status") == "active":
            score += 10
    else:
        issues.append("注册表中缺少该 skill 条目")
    return min(100, score), strengths, issues


def review_skill(skill_dir: Path, registry: dict[str, dict[str, str]]) -> dict:
    text = read_text(skill_dir / "SKILL.md")
    frontmatter = parse_frontmatter(text)
    sections = [
        score_metadata(frontmatter),
        score_structure(text),
        score_local_alignment(text, frontmatter),
        score_maintainability(skill_dir, text),
        score_registry_alignment(skill_dir.name, registry.get(skill_dir.name)),
    ]
    dimension_names = [
        "metadata",
        "structure",
        "local_alignment",
        "maintainability",
        "registry_alignment",
    ]
    breakdown = {}
    strengths: list[str] = []
    issues: list[str] = []
    for name, (score, good, bad) in zip(dimension_names, sections, strict=True):
        breakdown[name] = score
        strengths.extend(good)
        issues.extend(bad)
    quality_score = round(sum(breakdown.values()) / len(breakdown))
    top_issues = []
    for issue in issues:
        if issue not in top_issues:
            top_issues.append(issue)
    summary = (
        "结构和元数据质量较好。"
        if quality_score >= 80
        else "存在可执行性或可维护性改进空间。"
    )
    return {
        "quality_score": quality_score,
        "reviewed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "summary": summary,
        "breakdown": breakdown,
        "strengths": strengths[:5],
        "issues": top_issues[:5],
        "recommendations": top_issues[:3],
    }


def main() -> int:
    args = parse_args()
    if not args.all and not args.skill:
        raise SystemExit("Use --all or --skill <name>")
    registry = load_registry()
    skill_dirs = iter_skill_dirs()
    if args.skill:
        skill_dirs = [item for item in skill_dirs if item.name == args.skill]
        if not skill_dirs:
            raise SystemExit(f"Skill not found: {args.skill}")
    results = {
        skill_dir.name: review_skill(skill_dir, registry) for skill_dir in skill_dirs
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "skills": results,
    }
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"Wrote {len(results)} skill reviews to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
