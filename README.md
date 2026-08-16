# OCR 截图转文字

一个轻量级的 macOS 桌面工具：**截图 → 粘贴 → 自动识别文字 → 一键复制**。

基于 **Flask + Surya OCR + pywebview**，支持中文 / 英文识别，完全本地运行，无需联网调用任何云端 API。

## 功能特性

- 🖼️ 三种图片输入方式：**Cmd+V 粘贴**、**拖拽文件**、**上传按钮**
- ⚡ 粘贴 / 拖入后**自动识别**，无需额外点击
- 🌐 中英文混合识别（基于 Surya OCR，本地模型推理）
- 📋 识别结果一键复制到系统剪贴板
- ✏️ 结果可手动编辑修正后复制
- 🖥️ 原生窗口（pywebview / WKWebView），不依赖浏览器；也可用浏览器版本
- 🔒 完全本地运行，图片和文字不出本机

## 环境要求

- macOS 10.13+
- Python 3.9+
- 首次运行需联网下载 Surya OCR 模型（约 1-2GB，下载后缓存本地）

## 安装

```bash
git clone https://github.com/quaresun/article-to-knowledge-cards.git
cd article-to-knowledge-cards

# 创建虚拟环境（推荐）
python3 -m venv .venv
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

> 注意：`surya-ocr` 会拉取 `torch` 等较重的依赖，首次安装耗时较长属正常现象。

## 使用

### 方式一：浏览器版本（最简）

```bash
python3 app.py
```

启动后自动打开浏览器 `http://127.0.0.1:5050`，即可 `Cmd+V` 粘贴截图识别。

### 方式二：原生桌面窗口（推荐）

```bash
python3 main.py
```

基于 pywebview 打开原生窗口（需先 `pip install pywebview`）。

### 方式三：构建 .app

```bash
python3 build_app.py
```

生成 `OCR 截图转文字.app`，可双击启动。

## 工作原理

```
图片（粘贴/拖拽/上传）
        │
        ▼
Flask 后端接收 base64 图片
        │
        ▼
Surya OCR 引擎（本地模型，中英文）
        │
        ▼
识别文字 → 前端展示 → 一键复制
```

## 项目结构

```
.
├── app.py            # Flask Web 版本后端
├── app_native.py     # pywebview 原生窗口版本
├── main.py           # 程序主入口（优先原生窗口，回退浏览器）
├── ocr_engine.py     # Surya OCR 引擎封装
├── build_app.py      # 构建 macOS .app 包脚本
├── templates/
│   └── index.html    # 前端界面
├── tests/            # pytest 测试
├── requirements.txt  # Python 依赖
└── PRD.md            # 产品需求文档
```

## 测试

```bash
# 运行全部测试（单元测试为主，模型集成测试默认跳过）
pytest

# 运行包含模型下载的慢速集成测试
pytest -m slow
```

## 技术栈

| 模块 | 选型 |
|---|---|
| 语言 | Python 3.9+ |
| 界面 | Flask + 原生 HTML/CSS/JS；pywebview (WKWebView) |
| OCR 引擎 | [Surya OCR](https://github.com/VikParuchuri/surya) 0.5.0 |
| 图片处理 | Pillow |

## 开源协议

[MIT](./LICENSE)

## 贡献

欢迎提交 Issue 和 Pull Request。如有功能建议，请先开 Issue 讨论。

## 致谢

- [Surya OCR](https://github.com/VikParuchuri/surya) — 强大的开源 OCR 引擎
- Flask / pywebview / Pillow 开源社区
