"""
构建 macOS .app 应用包
运行后生成 OCR.app，可双击启动
"""
import os
import sys
import stat
import shutil
from pathlib import Path

APP_NAME = "OCR 截图转文字"
PROJECT_DIR = Path(__file__).parent.resolve()
APP_DIR = PROJECT_DIR / f"{APP_NAME}.app"
CONTENTS = APP_DIR / "Contents"
MACOS = CONTENTS / "MacOS"
RESOURCES = CONTENTS / "Resources"

PYTHON_PATH = sys.executable

INFO_PLIST = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
 "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleName</key>
    <string>{name}</string>
    <key>CFBundleDisplayName</key>
    <string>{name}</string>
    <key>CFBundleIdentifier</key>
    <string>com.ocr.screentotext</string>
    <key>CFBundleVersion</key>
    <string>1.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleExecutable</key>
    <string>ocr</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.13</string>
    <key>LSUIElement</key>
    <false/>
    <key>NSHighResolutionCapable</key>
    <true/>
</dict>
</plist>
"""

LAUNCHER_TEMPLATE = """#!/bin/bash
# OCR 截图转文字 — 原生 Mac 应用启动脚本
# 使用 pywebview（WKWebView），不依赖浏览器

PROJECT_DIR="{project_dir}"
PYTHON="{python}"

cd "$PROJECT_DIR"

# 后台启动，不阻塞应用启动过程
"$PYTHON" main.py &
"""

PROJECT_DIR_STR = str(PROJECT_DIR)


def build():
    print(f"构建 {APP_NAME}.app 到 {APP_DIR}")

    # 清理旧版本
    if APP_DIR.exists():
        shutil.rmtree(APP_DIR)
        print("  已清理旧版本")

    # 创建目录结构
    MACOS.mkdir(parents=True, exist_ok=True)
    RESOURCES.mkdir(parents=True, exist_ok=True)
    print("  创建目录结构")

    # Info.plist
    plist_path = CONTENTS / "Info.plist"
    plist_path.write_text(INFO_PLIST.format(name=APP_NAME))
    print("  写入 Info.plist")

    # 启动器（直接启动，不弹终端窗口）
    launcher_path = MACOS / "ocr"
    launcher_path.write_text(LAUNCHER_TEMPLATE.format(
        project_dir=PROJECT_DIR_STR,
        python=PYTHON_PATH,
    ))
    launcher_path.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    print(f"  写入启动脚本 ({PYTHON_PATH})")

    # 创建 .command 备用启动器
    command_file = PROJECT_DIR / "启动OCR.command"
    command_content = f"""#!/bin/bash
cd "{PROJECT_DIR_STR}"
{PYTHON_PATH} main.py
"""
    command_file.write_text(command_content)
    command_file.chmod(stat.S_IRWXU | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    print(f"  创建备用启动器: 启动OCR.command")

    print(f"\n构建完成！")
    print(f"  应用: {APP_DIR}")
    print(f"  双击启动或运行: open '{APP_DIR}'")


if __name__ == "__main__":
    build()
