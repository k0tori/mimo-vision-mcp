# Mimo Vision MCP

基于 mimo-v2.5 模型的图像识别 MCP 服务器。

## 功能

| 模式 | 用途 | 输出格式 |
|------|------|----------|
| `describe` | 通用图像描述 | 纯文本 |
| `ocr` | 文字识别 | 纯文本 |
| `extract` | 结构化信息提取 | JSON |

## 安装

```bash
pip install -e .
```

## 配置

复制 `.env.example` 为 `.env` 并填入配置：

```bash
cp .env.example .env
```

```env
MIMO_API_BASE_URL=http://localhost:8080
MIMO_API_KEY=sk-xxx
```

## MCP 配置

在 Claude Desktop 或其他 MCP 客户端的配置文件中添加：

```json
{
  "mcpServers": {
    "mimo-vision": {
      "command": "python",
      "args": ["-m", "mimo_vision_mcp"]
    }
  }
}
```

## 使用示例

### 描述图片

```json
{
  "image": "/path/to/image.png",
  "mode": "describe"
}
```

### OCR 文字识别

```json
{
  "image": "https://example.com/screenshot.png",
  "mode": "ocr"
}
```

### 结构化提取

```json
{
  "image": "/path/to/invoice.jpg",
  "mode": "extract",
  "prompt": "提取发票号码、金额和日期"
}
```

## 开发

```bash
pip install -e ".[dev]"
pytest
```
