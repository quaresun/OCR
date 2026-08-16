"""Flask 与 OCR 引擎之间的集成测试。"""

import base64
import io

from PIL import Image

import app as web_app


def _image_data_url() -> str:
    image = Image.new("RGB", (8, 8), "white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def test_ocr_endpoint_returns_recognized_text(monkeypatch):
    monkeypatch.setattr(web_app.ocr_engine, "recognize", lambda image: "你好\nHello")

    response = web_app.app.test_client().post(
        "/ocr", json={"image": _image_data_url()}
    )

    assert response.status_code == 200
    assert response.get_json() == {"text": "你好\nHello"}


def test_ocr_endpoint_rejects_missing_image():
    response = web_app.app.test_client().post("/ocr", json={})

    assert response.status_code == 400
    assert "error" in response.get_json()


def test_ocr_endpoint_reports_invalid_image():
    response = web_app.app.test_client().post(
        "/ocr", json={"image": "data:image/png;base64,not-an-image"}
    )

    assert response.status_code == 500
    assert "OCR 识别失败" in response.get_json()["error"]
