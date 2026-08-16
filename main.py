"""
OCR 截图转文字工具 — 主入口
双击启动原生窗口（macOS WKWebView），不依赖浏览器
"""
import os
import sys

os.environ.setdefault("TK_SILENCE_DEPRECATION", "1")

if __name__ == "__main__":
    try:
        from app_native import main
        main()
    except ImportError as e:
        print(f"依赖缺失: {e}")
        print("请先安装: pip3 install pywebview")
        print()
        print("安装完成后重新运行: python3 main.py")
        print()
        # 回退到浏览器版本
        print("注意: 正在回退到浏览器版本...")
        from app import main as browser_main
        browser_main()
