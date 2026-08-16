"""Web GUI 合约测试。"""

from app import app


def test_home_page_contains_paste_and_drag_handlers():
    html = app.test_client().get("/").get_data(as_text=True)

    assert 'addEventListener("paste"' in html
    assert 'addEventListener("drop"' in html
    assert 'accept = "image/*"' in html


def test_home_page_contains_copy_and_clear_actions():
    html = app.test_client().get("/").get_data(as_text=True)

    assert "copyResult()" in html
    assert "clearAll()" in html
    assert "navigator.clipboard.writeText" in html
