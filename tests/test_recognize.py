import pytest
from unittest.mock import AsyncMock, patch
from mimo_vision_mcp.tools.recognize import recognize_image


class TestRecognizeImage:
    """Test the main recognize_image function."""

    @pytest.mark.asyncio
    async def test_describe_mode(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        with (
            patch("mimo_vision_mcp.tools.recognize.call_vision_api", new_callable=AsyncMock) as mock_api,
            patch("mimo_vision_mcp.tools.recognize.load_config", return_value=("https://api.example.com", "test-key")),
        ):
            mock_api.return_value = "A beautiful sunset over the ocean."
            result = await recognize_image(str(file_path), "describe")

        assert result == "A beautiful sunset over the ocean."
        mock_api.assert_called_once()

    @pytest.mark.asyncio
    async def test_ocr_mode(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        with (
            patch("mimo_vision_mcp.tools.recognize.call_vision_api", new_callable=AsyncMock) as mock_api,
            patch("mimo_vision_mcp.tools.recognize.load_config", return_value=("https://api.example.com", "test-key")),
        ):
            mock_api.return_value = "Hello World"
            result = await recognize_image(str(file_path), "ocr")

        assert result == "Hello World"

    @pytest.mark.asyncio
    async def test_extract_mode_returns_json(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        with (
            patch("mimo_vision_mcp.tools.recognize.call_vision_api", new_callable=AsyncMock) as mock_api,
            patch("mimo_vision_mcp.tools.recognize.load_config", return_value=("https://api.example.com", "test-key")),
        ):
            mock_api.return_value = '{"name": "John", "age": 30}'
            result = await recognize_image(str(file_path), "extract")

        assert result == '{"name": "John", "age": 30}'

    @pytest.mark.asyncio
    async def test_extract_mode_handles_invalid_json(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        with (
            patch("mimo_vision_mcp.tools.recognize.call_vision_api", new_callable=AsyncMock) as mock_api,
            patch("mimo_vision_mcp.tools.recognize.load_config", return_value=("https://api.example.com", "test-key")),
        ):
            mock_api.return_value = "This is not JSON"
            result = await recognize_image(str(file_path), "extract")

        assert "警告" in result
        assert "This is not JSON" in result

    @pytest.mark.asyncio
    async def test_url_input(self):
        with (
            patch("mimo_vision_mcp.tools.recognize.call_vision_api", new_callable=AsyncMock) as mock_api,
            patch("mimo_vision_mcp.tools.recognize.load_config", return_value=("https://api.example.com", "test-key")),
        ):
            mock_api.return_value = "A cat."
            result = await recognize_image("https://example.com/cat.png", "describe")

        assert result == "A cat."

    @pytest.mark.asyncio
    async def test_invalid_mode_raises(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        result = await recognize_image(str(file_path), "invalid")
        assert "错误" in result
        assert "未知的识别模式" in result

    @pytest.mark.asyncio
    async def test_file_not_found_returns_error(self):
        result = await recognize_image("/nonexistent/image.png", "describe")
        assert "错误" in result
        assert "文件不存在" in result

    @pytest.mark.asyncio
    async def test_api_error_returns_error(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        with (
            patch("mimo_vision_mcp.tools.recognize.call_vision_api", new_callable=AsyncMock) as mock_api,
            patch("mimo_vision_mcp.tools.recognize.load_config", return_value=("https://api.example.com", "test-key")),
        ):
            mock_api.side_effect = Exception("错误：API 认证失败，请检查 API Key")
            result = await recognize_image(str(file_path), "describe")

        assert "错误" in result
        assert "API 认证失败" in result

    @pytest.mark.asyncio
    async def test_with_custom_prompt(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        with (
            patch("mimo_vision_mcp.tools.recognize.call_vision_api", new_callable=AsyncMock) as mock_api,
            patch("mimo_vision_mcp.tools.recognize.load_config", return_value=("https://api.example.com", "test-key")),
        ):
            mock_api.return_value = "Red car."
            result = await recognize_image(str(file_path), "describe", prompt="描述车辆颜色")

        assert result == "Red car."
        call_args = mock_api.call_args
        assert "描述车辆颜色" in call_args.kwargs["user_message"]
