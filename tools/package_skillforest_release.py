from pathlib import Path
import shutil
import zipfile


REPO_ROOT = Path(__file__).resolve().parents[1]
HOME = Path.home()
STAGE_DIR = HOME / "SkillForest-release"
ZIP_PATH = HOME / "SkillForest-release.zip"

INCLUDE_PATHS = [
    "skill-registry",
    "skills",
    "docs",
    "README.md",
]


def clean_output() -> None:
    if STAGE_DIR.exists():
        shutil.rmtree(STAGE_DIR)
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()


def copy_payload() -> None:
    STAGE_DIR.mkdir(parents=True, exist_ok=True)
    for rel in INCLUDE_PATHS:
        src = REPO_ROOT / rel
        dst = STAGE_DIR / rel
        if not src.exists():
            continue
        if src.is_dir():
            shutil.copytree(
                src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git")
            )
        else:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)


def write_release_note() -> None:
    note = STAGE_DIR / "README-RELEASE.txt"
    note.write_text(
        "SkillForest 发布包\n\n"
        "1. 先阅读 docs/INSTALL.md\n"
        "2. 把 skill-registry/ 复制到 %USERPROFILE%\\.claude\\skills\\skill-registry\n"
        "3. 如果需要完整技能库，再把 skills/ 复制到 %USERPROFILE%\\.claude\\skills\n",
        encoding="utf-8",
    )


def build_zip() -> None:
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in STAGE_DIR.rglob("*"):
            zf.write(path, path.relative_to(STAGE_DIR.parent))


def main() -> None:
    clean_output()
    copy_payload()
    write_release_note()
    build_zip()
    print(f"stage: {STAGE_DIR}")
    print(f"zip:   {ZIP_PATH}")


if __name__ == "__main__":
    main()
