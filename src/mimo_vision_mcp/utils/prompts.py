"""System prompts for different recognition modes."""

SYSTEM_PROMPTS: dict[str, str] = {
    "describe": (
        "你是一个图像分析专家。请仔细观察这张图片，用连贯的中文句子描述图片中的内容，"
        "包括主要的对象、人物、场景环境、它们之间的位置关系、重要的细节和文字信息，"
        "以及图片整体传达的氛围或用途。描述要准确、有条理、详略得当。"
    ),
    "ocr": (
        "你是一个专业的文字识别引擎。请提取图片中的所有文字内容，"
        "按照文字在图片中的位置和阅读顺序输出，保留原始的换行和段落结构。"
        "如果有表格，用 Markdown 表格格式输出。"
        "只输出识别到的文字，不要添加额外描述。"
        "如果图片中没有可识别的文字，只输出空字符串。"
    ),
    "extract": (
        "你是一个结构化信息提取专家。请从图片中提取关键信息并以 JSON 格式输出。"
        "根据图片内容自动识别类型（发票、名片、表格、证件等），"
        "提取所有有意义的字段，输出合法的 JSON，不要包含 markdown 标记。"
        "如果无法识别图片类别或无法提取有效信息，输出空 JSON {}。"
    ),
}

VALID_MODES = set(SYSTEM_PROMPTS.keys())


def get_system_prompt(mode: str) -> str:
    """Get system prompt for the specified recognition mode.

    Args:
        mode: Recognition mode ("describe", "ocr", or "extract").

    Returns:
        System prompt string.

    Raises:
        ValueError: If mode is not recognized.
    """
    if mode not in VALID_MODES:
        raise ValueError(f"错误：未知的识别模式 '{mode}'，支持: {', '.join(sorted(VALID_MODES))}")
    return SYSTEM_PROMPTS[mode]


def build_user_message(mode: str, prompt: str) -> str:
    """Build the user message text based on mode and optional prompt.

    Args:
        mode: Recognition mode.
        prompt: Optional user prompt.

    Returns:
        User message text.
    """
    if not prompt:
        if mode == "extract":
            return "请提取这张图片中的结构化信息。"
        return "请分析这张图片。"

    if mode == "extract":
        return f"{prompt}\n\n请根据以上要求分析这张图片。"

    return prompt
