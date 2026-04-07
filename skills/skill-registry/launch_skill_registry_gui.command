#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
  PYTHON_BIN="python3"
elif command -v python >/dev/null 2>&1; then
  PYTHON_BIN="python"
else
  osascript -e 'display alert "SkillForest" message "未找到 Python 解释器，请先安装 Python 3。" as critical'
  exit 1
fi

"$PYTHON_BIN" "$SCRIPT_DIR/skill_registry_gui.py"
