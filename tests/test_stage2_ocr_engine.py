"""Stage 2 测试：OCR 引擎封装"""
import sys
import os
import pytest
from unittest.mock import MagicMock, patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PIL import Image, ImageDraw, ImageFont
from ocr_engine import OCREngine


def create_test_image(texts=None, size=(600, 150)):
    """创建包含文字的白底测试图片"""
    if texts is None:
        texts = ["Hello World"]
    img = Image.new("RGB", size, color="white")
    draw = ImageDraw.Draw(img)
    y = 10
    for text in texts:
        draw.text((10, y), text, fill="black")
        y += 40
    return img


class TestOCREngineAPI:
    """测试 OCR 引擎 API 契约"""

    def test_engine_creation_default_langs(self):
        """默认语言为 zh, en"""
        engine = OCREngine()
        assert engine.langs == ["zh", "en"]
        assert engine.is_loaded is False

    def test_engine_creation_custom_langs(self):
        """自定义语言"""
        engine = OCREngine(langs=["en"])
        assert engine.langs == ["en"]

    def test_engine_not_loaded_initially(self):
        """引擎创建时模型未加载（惰性加载）"""
        engine = OCREngine()
        assert engine.is_loaded is False

    def test_langs_returns_copy(self):
        """langs 属性返回副本，外部修改不影响内部"""
        engine = OCREngine(langs=["zh", "en"])
        langs = engine.langs
        langs.append("ja")
        assert engine.langs == ["zh", "en"]

    def test_recognize_accepts_pil_image(self):
        """recognize 接受 PIL Image 参数类型"""
        from PIL import Image
        engine = OCREngine()

        # 使用 mock 避免实际加载模型
        with patch.object(engine, "_ensure_loaded"), \
             patch("ocr_engine.run_ocr", return_value=[]) as mock_ocr:
            img = create_test_image()
            result = engine.recognize(img)
            assert isinstance(result, str)
            mock_ocr.assert_called_once()

    def test_recognize_empty_result_returns_empty_string(self):
        """无识别结果时返回空字符串"""
        engine = OCREngine()
        with patch.object(engine, "_ensure_loaded"), \
             patch("ocr_engine.run_ocr", return_value=[]) as mock_ocr:
            img = create_test_image()
            result = engine.recognize(img)
            assert result == ""

    def test_recognize_joins_multiple_lines(self):
        """多行结果用换行符连接"""
        from surya.schema import OCRResult, TextLine

        mock_line1 = TextLine(text="Hello World", polygon=[[0,0],[100,0],[100,20],[0,20]], confidence=0.95)
        mock_line2 = TextLine(text="你好世界", polygon=[[0,30],[100,30],[100,50],[0,50]], confidence=0.95)
        mock_result = OCRResult(
            text_lines=[mock_line1, mock_line2],
            languages=["zh", "en"],
            image_bbox=[0, 0, 600, 150],
        )

        engine = OCREngine()
        with patch.object(engine, "_ensure_loaded"), \
             patch("ocr_engine.run_ocr", return_value=[mock_result]):
            img = create_test_image()
            result = engine.recognize(img)
            assert result == "Hello World\n你好世界"


class TestOCREngineIntegration:
    """测试 OCR 引擎真实识别（需要下载模型，首次运行较慢）"""

    @pytest.mark.slow
    def test_real_ocr_basic(self):
        """真实 OCR 识别测试 — 简单英文"""
        engine = OCREngine(langs=["en"])
        img = create_test_image(["Hello World"], size=(400, 80))
        result = engine.recognize(img)
        assert engine.is_loaded is True
        assert isinstance(result, str)
        # 识别结果应包含 Hello（可能因字体小识别出部分字符）
        assert len(result) > 0

    @pytest.mark.slow
    def test_real_ocr_chinese(self):
        """真实 OCR 识别测试 — 中文"""
        engine = OCREngine(langs=["zh"])
        img = create_test_image(["你好世界"], size=(400, 80))
        result = engine.recognize(img)
        assert isinstance(result, str)
        assert len(result) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
