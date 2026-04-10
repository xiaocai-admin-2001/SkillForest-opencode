from __future__ import annotations

import argparse
import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = REPO_ROOT / "skills"
TARGET_DIR = Path.home() / ".claude" / "skills"
REGISTRY_FILE = "SKILLS_REGISTRY.csv"
PRESERVE_DIRS = {"skill-registry"}
PRESERVE_FILES = {REGISTRY_FILE}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sync skill-repo skills into ~/.claude/skills"
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="Remove target skill directories that do not exist in the repo source",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show planned changes without writing files",
    )
    return parser.parse_args()


def copy_tree(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"COPY {source} -> {target}")
        return
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(source, target)


def copy_file(source: Path, target: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"COPY {source} -> {target}")
        return
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def remove_path(path: Path, dry_run: bool) -> None:
    if dry_run:
        print(f"REMOVE {path}")
        return
    if path.is_dir():
        shutil.rmtree(path)
    elif path.exists():
        path.unlink()


def main() -> int:
    args = parse_args()
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    source_skill_dirs = sorted(
        p for p in SOURCE_DIR.iterdir() if p.is_dir() and (p / "SKILL.md").exists()
    )

    for skill_dir in source_skill_dirs:
        copy_tree(skill_dir, TARGET_DIR / skill_dir.name, args.dry_run)

    source_registry = SOURCE_DIR / REGISTRY_FILE
    if source_registry.exists():
        copy_file(source_registry, TARGET_DIR / REGISTRY_FILE, args.dry_run)

    if args.prune:
        source_names = {p.name for p in source_skill_dirs}
        for target_child in TARGET_DIR.iterdir():
            if (
                target_child.name in PRESERVE_DIRS
                or target_child.name in PRESERVE_FILES
            ):
                continue
            if (
                target_child.is_dir()
                and (target_child / "SKILL.md").exists()
                and target_child.name not in source_names
            ):
                remove_path(target_child, args.dry_run)

    print("Sync complete")
    print(f"Source: {SOURCE_DIR}")
    print(f"Target: {TARGET_DIR}")
    print(f"Prune: {args.prune}")
    print(f"Dry run: {args.dry_run}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
