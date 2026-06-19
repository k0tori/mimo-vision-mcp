"""OpenAI-compatible API client for mimo-v2.5."""

import os
from typing import Tuple

from openai import AsyncOpenAI

TIMEOUT = 60.0  # seconds


def load_config() -> Tuple[str, str]:
    """Load API configuration from environment variables.

    Returns:
        Tuple of (base_url, api_key).

    Raises:
        ValueError: If required variables are missing.
    """
    base_url = os.environ.get("MIMO_API_BASE_URL")
    api_key = os.environ.get("MIMO_API_KEY")

    if not base_url:
        raise ValueError("错误：环境变量 MIMO_API_BASE_URL 未设置")
    if not api_key:
        raise ValueError("错误：环境变量 MIMO_API_KEY 未设置")

    return base_url, api_key


async def call_vision_api(
    base_url: str,
    api_key: str,
    system_prompt: str,
    image_url: str,
    user_message: str,
) -> str:
    """Call the vision API with OpenAI-compatible format.

    Args:
        base_url: API base URL (e.g., "https://api.xiaomimimo.com/v1").
        api_key: API authentication key.
        system_prompt: System prompt for the mode.
        image_url: Image URL or data URI.
        user_message: User message text.

    Returns:
        Model response text.

    Raises:
        Exception: On API errors or network failures.
    """
    client = AsyncOpenAI(
        api_key=api_key,
        base_url=base_url,
        timeout=TIMEOUT,
    )

    try:
        completion = await client.chat.completions.create(
            model="mimo-v2.5",
            max_completion_tokens=4096,
            messages=[
                {"role": "system", "content": system_prompt},
                {
                    "role": "user",
                    "content": [
                        {"type": "image_url", "image_url": {"url": image_url}},
                        {"type": "text", "text": user_message},
                    ],
                },
            ],
        )
    except Exception as e:
        raise Exception(f"错误：模型调用失败 - {e}")

    content = completion.choices[0].message.content
    if content is None:
        raise Exception("错误：模型返回空内容")
    return content
