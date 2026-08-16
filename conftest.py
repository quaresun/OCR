"""pytest 配置"""
import pytest


def pytest_configure(config):
    config.addinivalue_line("markers", "slow: OCR 集成测试（需下载模型，耗时长）")
