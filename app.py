"""
OCR 截图转文字工具 — Web 版本
Mac 桌面小工具：粘贴截图 → 识别文字 → 一键复制
启动后自动打开浏览器，Cmd+V 直接粘贴截图
"""
import os
import io
import base64
import webbrowser
import threading
from flask import Flask, render_template, request, jsonify
from PIL import Image

from ocr_engine import OCREngine

app = Flask(__name__)
ocr_engine = OCREngine(langs=["zh", "en"])

# 端口配置：避开 macOS AirPlay Receiver 默认占用的 5000 端口
PORT = 5050


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/ocr", methods=["POST"])
def ocr_endpoint():
    """接受 base64 图片，返回识别文字"""
    data = request.get_json(silent=True)
    if not data or "image" not in data:
        return jsonify({"error": "需要提供 image 字段（base64 编码）"}), 400

    try:
        # 解码 base64 → PIL Image
        raw = data["image"]
        # 去掉 data:image/png;base64, 前缀
        if "," in raw:
            raw = raw.split(",", 1)[1]

        image_bytes = base64.b64decode(raw)
        image = Image.open(io.BytesIO(image_bytes))

        # OCR 识别
        text = ocr_engine.recognize(image)

        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": f"OCR 识别失败: {str(e)}"}), 500


def open_browser():
    """延迟打开浏览器"""
    webbrowser.open(f"http://127.0.0.1:{PORT}")


def main():
    print("=" * 50)
    print("  OCR 截图转文字工具")
    print(f"  浏览器打开 http://127.0.0.1:{PORT}")
    print("  Cmd+V 粘贴截图即可识别")
    print("=" * 50)

    # 延迟 0.8 秒等服务器启动后打开浏览器
    threading.Timer(0.8, open_browser).start()

    app.run(host="127.0.0.1", port=PORT, debug=False)


if __name__ == "__main__":
    main()
