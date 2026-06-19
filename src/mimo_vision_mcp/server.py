"""MCP server entry point."""

import asyncio
from pathlib import Path

from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from mimo_vision_mcp.tools.recognize import recognize_image

# Load .env: try CWD first, then project root (for development)
env_path = Path.cwd() / ".env"
if not env_path.exists():
    env_path = Path(__file__).parent.parent.parent / ".env"
load_dotenv(env_path)

# Tool definition
RECOGNIZE_TOOL = Tool(
    name="recognize_image",
    description=(
        "识别和分析图片内容。支持三种模式：\n"
        "- describe: 通用图像描述（场景、物体、人物、关系）\n"
        "- ocr: 提取图片中的所有文字\n"
        "- extract: 提取结构化信息（表格、发票、名片等）为 JSON 格式"
    ),
    inputSchema={
        "type": "object",
        "properties": {
            "image": {
                "type": "string",
                "description": "本地图片文件路径或图片 URL",
            },
            "mode": {
                "type": "string",
                "enum": ["describe", "ocr", "extract"],
                "description": "识别模式：describe（描述）、ocr（文字识别）、extract（结构化提取）",
            },
            "prompt": {
                "type": "string",
                "description": "可选的补充提示词，用于指定识别需求",
                "default": "",
            },
            "format": {
                "type": "string",
                "enum": ["auto", "json", "table"],
                "description": "仅 extract 模式生效：auto（自动）、json（JSON 对象）、table（Markdown 表格）",
                "default": "auto",
            },
        },
        "required": ["image", "mode"],
    },
)


def create_server() -> Server:
    """Create and configure the MCP server."""
    server = Server("mimo-vision")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [RECOGNIZE_TOOL]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[TextContent]:
        if name != "recognize_image":
            return [TextContent(type="text", text=f"错误：未知工具 '{name}'")]

        result = await recognize_image(
            image=arguments["image"],
            mode=arguments["mode"],
            prompt=arguments.get("prompt", ""),
            format=arguments.get("format", "auto"),
        )

        return [TextContent(type="text", text=result)]

    return server


async def main():
    """Run the MCP server via stdio."""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())


if __name__ == "__main__":
    asyncio.run(main())
