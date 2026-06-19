import pytest
from mimo_vision_mcp.utils.prompts import get_system_prompt, build_user_message


class TestGetSystemPrompt:
    """Test system prompt retrieval by mode."""

    def test_describe_mode(self):
        prompt = get_system_prompt("describe")
        assert "图像分析专家" in prompt
        assert "连贯的中文句子" in prompt

    def test_ocr_mode(self):
        prompt = get_system_prompt("ocr")
        assert "文字识别引擎" in prompt
        assert "空字符串" in prompt

    def test_extract_mode(self):
        prompt = get_system_prompt("extract")
        assert "结构化信息提取" in prompt
        assert "JSON" in prompt
        assert "{}" in prompt

    def test_invalid_mode_raises(self):
        with pytest.raises(ValueError, match="未知的识别模式"):
            get_system_prompt("invalid")


class TestBuildUserMessage:
    """Test user message construction."""

    def test_describe_no_prompt(self):
        msg = build_user_message("describe", "")
        assert msg == "请分析这张图片。"

    def test_describe_with_prompt(self):
        msg = build_user_message("describe", "描述颜色")
        assert msg == "描述颜色"

    def test_ocr_no_prompt(self):
        msg = build_user_message("ocr", "")
        assert msg == "请分析这张图片。"

    def test_ocr_with_prompt(self):
        msg = build_user_message("ocr", "只提取标题")
        assert msg == "只提取标题"

    def test_extract_no_prompt(self):
        msg = build_user_message("extract", "")
        assert msg == "请提取这张图片中的结构化信息。"

    def test_extract_with_prompt(self):
        msg = build_user_message("extract", "提取金额")
        assert "提取金额" in msg
        assert "请根据以上要求分析这张图片。" in msg
