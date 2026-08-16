"""
OCR 引擎封装 — 基于 Surya
提供简洁接口：输入 PIL Image → 输出文字字符串
"""
from typing import List, Optional
from PIL import Image

from surya.ocr import run_ocr
from surya.model.detection.model import load_model as load_det_model, load_processor as load_det_processor
from surya.model.recognition.model import load_model as load_rec_model
from surya.model.recognition.processor import load_processor as load_rec_processor


class OCREngine:
    """Surya OCR 引擎封装，支持模型缓存和单张/批量识别"""

    def __init__(self, langs: Optional[List[str]] = None):
        """
        初始化 OCR 引擎并加载模型。

        Args:
            langs: 识别语言列表，默认 ['zh', 'en']。
                   首次初始化会从 HuggingFace 下载模型（约 1-2GB）。
        """
        self._langs = langs or ["zh", "en"]
        self._det_model = None
        self._det_processor = None
        self._rec_model = None
        self._rec_processor = None
        self._loaded = False

    def _ensure_loaded(self):
        """惰性加载模型（首次调用时加载）"""
        if self._loaded:
            return
        self._det_model = load_det_model()
        self._det_processor = load_det_processor()
        self._rec_model = load_rec_model()
        self._rec_processor = load_rec_processor()
        self._loaded = True

    def recognize(self, image: Image.Image) -> str:
        """
        识别单张图片中的文字。

        Args:
            image: PIL Image 对象

        Returns:
            识别出的文字，多行用换行符分隔。若无文字则返回空字符串。
        """
        self._ensure_loaded()

        results = run_ocr(
            images=[image],
            langs=[self._langs],
            det_model=self._det_model,
            det_processor=self._det_processor,
            rec_model=self._rec_model,
            rec_processor=self._rec_processor,
        )

        if not results:
            return ""

        lines = []
        for result in results:
            for text_line in result.text_lines:
                text = text_line.text.strip()
                if text:
                    lines.append(text)

        return "\n".join(lines)

    @property
    def is_loaded(self) -> bool:
        """模型是否已加载"""
        return self._loaded

    @property
    def langs(self) -> List[str]:
        """当前识别语言"""
        return self._langs.copy()
