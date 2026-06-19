# Mimo Vision MCP

> 基于 [mimo-v2.5](https://github.com/XiaoMi/mimo) 的图像识别 MCP 服务器，为 AI 助手提供"看图"能力。

[![Python 3.10+](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 功能特性

单一工具 `recognize_image`，通过 `mode` 参数切换三种识别能力：

| 模式 | 用途 | 输出格式 | 典型场景 |
|:-----|:-----|:---------|:---------|
| `describe` | 通用图像描述 | 纯文本 | 场景理解、内容审核、图片摘要 |
| `ocr` | 文字识别 | 纯文本 | 截图提取、文档数字化、车牌/招牌识别 |
| `extract` | 结构化信息提取 | JSON | 发票解析、名片录入、表格数据化 |

### extract 模式输出格式

通过 `format` 参数控制输出结构：

| 值 | 行为 |
|:---|:-----|
| `auto`（默认） | 由模型自动判断最合适的结构 |
| `json` | 强制输出 JSON 对象 |
| `table` | 强制输出 Markdown 表格 |

---

## 快速开始

### 1. 安装

```bash
# 克隆仓库
git clone https://github.com/k0tori/mimo-vision-mcp.git
cd mimo-vision-mcp

# 安装（开发模式）
pip install -e .
```

### 2. 配置 API

```bash
cp .env.example .env
```

编辑 `.env`，填入你的 API 凭据：

```env
MIMO_API_BASE_URL=https://your-api-endpoint/v1
MIMO_API_KEY=your-api-key
```

### 3. 注册 MCP 服务器

在你的 MCP 客户端配置中添加：

```json
{
  "mcpServers": {
    "mimo-vision": {
      "command": "python",
      "args": ["-m", "mimo_vision_mcp"],
      "env": {
        "MIMO_API_BASE_URL": "https://your-api-endpoint/v1",
        "MIMO_API_KEY": "your-api-key"
      }
    }
  }
}
```

> **提示：** `env` 字段可选。如果省略，服务器会从项目目录下的 `.env` 文件读取配置。

---

## 使用示例

### describe — 描述图片内容

```json
{
  "image": "/path/to/photo.jpg",
  "mode": "describe"
}
```

> 也支持 URL 输入：
> ```json
> { "image": "https://example.com/photo.jpg", "mode": "describe" }
> ```

### ocr — 提取文字

```json
{
  "image": "/path/to/screenshot.png",
  "mode": "ocr"
}
```

### extract — 结构化提取

```json
{
  "image": "/path/to/invoice.jpg",
  "mode": "extract",
  "prompt": "提取发票号码、开票日期和总金额"
}
```

强制 JSON 输出：

```json
{
  "image": "/path/to/business-card.png",
  "mode": "extract",
  "format": "json"
}
```

---

## 工具接口

### `recognize_image`

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|:-----|:-----|:-----|:-------|:-----|
| `image` | string | ✅ | — | 本地文件路径或图片 URL |
| `mode` | string | ✅ | — | `describe` / `ocr` / `extract` |
| `prompt` | string | — | `""` | 补充提示词，引导模型关注特定内容 |
| `format` | string | — | `"auto"` | 仅 extract 模式：`auto` / `json` / `table` |

---

## 支持的图片格式

| 格式 | 扩展名 | 最大大小 |
|:-----|:-------|:---------|
| PNG | `.png` | 20 MB |
| JPEG | `.jpg` / `.jpeg` | 20 MB |
| WebP | `.webp` | 20 MB |
| GIF | `.gif`（静态） | 20 MB |

格式通过文件头（magic bytes）自动检测，不依赖扩展名。

---

## 错误处理

所有错误以纯文本返回，不会抛出异常。常见错误类型：

| 错误 | 示例 |
|:-----|:-----|
| 文件不存在 | `错误：文件不存在 - /path/to/missing.png` |
| 格式不支持 | `错误：不支持的图片格式，支持 PNG/JPEG/WebP/GIF` |
| 文件过大 | `错误：文件过大（25.3MB），限制 20MB` |
| API 认证失败 | `错误：API 认证失败，请检查 API Key` |
| 模型返回异常 | `错误：模型调用失败 - ...` |

---

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 运行测试（详细输出）
pytest -v
```

### 项目结构

```
src/mimo_vision_mcp/
├── __init__.py          # 包初始化
├── __main__.py          # python -m 入口
├── server.py            # MCP 服务，注册工具
├── api/
│   └── client.py        # OpenAI 兼容 API 客户端
├── tools/
│   └── recognize.py     # recognize_image 实现
└── utils/
    ├── image.py         # 图片处理（magic bytes、base64）
    └── prompts.py       # System prompt 定义
```

---

## License

[MIT](LICENSE)
