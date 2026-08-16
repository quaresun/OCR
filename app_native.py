"""
OCR 截图转文字工具 — 原生 Mac 桌面版本
基于 pywebview + WKWebView，不依赖浏览器
Flask 作为 OCR 后端，pywebview 提供原生窗口
"""
import os
import sys
import threading
import time
import webview

from app import app, PORT as FLASK_PORT


def start_flask():
    """在后台线程启动 Flask 服务器"""
    app.run(host="127.0.0.1", port=FLASK_PORT, debug=False, use_reloader=False)


def main():
    # 启动 Flask 后端
    flask_thread = threading.Thread(target=start_flask, daemon=True)
    flask_thread.start()

    # 等待 Flask 就绪
    url = f"http://127.0.0.1:{FLASK_PORT}"
    print(f"Flask 后端启动中... {url}")
    time.sleep(1.0)

    # 创建原生窗口
    window = webview.create_window(
        title="OCR 截图转文字",
        url=url,
        width=900,
        height=680,
        min_size=(600, 450),
        resizable=True,
        text_select=True,
        confirm_close=False,
    )

    # 启动 webview 事件循环（阻塞直到窗口关闭）
    webview.start()

    print("窗口已关闭")


if __name__ == "__main__":
    main()
