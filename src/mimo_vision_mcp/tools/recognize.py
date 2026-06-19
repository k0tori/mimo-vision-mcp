"""Image recognition tool implementation."""

import json

from mimo_vision_mcp.api.client import call_vision_api, load_config
from mimo_vision_mcp.utils.image import resolve_image
from mimo_vision_mcp.utils.prompts import get_system_prompt, build_user_message, VALID_MODES


async def recognize_image(
    image: str,
    mode: str,
    prompt: str = "",
    format: str = "auto",
) -> str:
    """Recognize and analyze an image using mimo-v2.5.

    Args:
        image: Local file path or image URL.
        mode: Recognition mode ("describe", "ocr", "extract").
        prompt: Optional supplementary prompt.
        format: Output format for extract mode ("auto", "json", "table").

    Returns:
        Recognition result as text. Errors returned as text (never raises).
    """
    # Validate mode
    if mode not in VALID_MODES:
        return f"错误：未知的识别模式 '{mode}'，支持: {', '.join(sorted(VALID_MODES))}"

    # Resolve image to URL or data URI
    try:
        image_url = resolve_image(image)
    except ValueError as e:
        return str(e)

    # Get prompts
    try:
        system_prompt = get_system_prompt(mode)
    except ValueError as e:
        return str(e)

    user_message = build_user_message(mode, prompt)

    # Add format hint for extract mode
    if mode == "extract" and format == "json":
        user_message += "\n\n请确保输出为 JSON 对象格式。"
    elif mode == "extract" and format == "table":
        user_message += "\n\n请确保输出为 Markdown 表格格式。"

    # Load config and call API
    try:
        base_url, api_key = load_config()
    except ValueError as e:
        return str(e)

    try:
        result = await call_vision_api(
            base_url=base_url,
            api_key=api_key,
            system_prompt=system_prompt,
            image_url=image_url,
            user_message=user_message,
        )
    except Exception as e:
        return str(e)

    # Handle empty result
    if not result or not result.strip():
        return "错误：模型返回空内容，请检查图片是否有效"

    # Validate JSON for extract mode
    if mode == "extract":
        try:
            json.loads(result)
        except json.JSONDecodeError:
            return f"警告：模型返回的非标准 JSON，原始输出如下：\n{result}"

    return result
