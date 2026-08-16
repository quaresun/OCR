"""Web 窗口骨架测试：确保首页不再依赖有兼容问题的 Tk。"""

from app import app


def test_home_page_renders_ocr_interface():
    response = app.test_client().get("/")

    assert response.status_code == 200
    html = response.get_data(as_text=True)
    assert "OCR 截图转文字" in html
    assert "按 Cmd+V 粘贴截图" in html
    assert 'id="imageZone"' in html
    assert 'id="resultText"' in html
    assert 'id="copyBtn"' in html


def test_health_endpoint_reports_ready():
    response = app.test_client().get("/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
