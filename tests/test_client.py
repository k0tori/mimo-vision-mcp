import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from mimo_vision_mcp.api.client import call_vision_api, load_config


class TestLoadConfig:
    """Test configuration loading."""

    def test_loads_from_env(self):
        with patch.dict("os.environ", {
            "MIMO_API_BASE_URL": "https://api.xiaomimimo.com/v1",
            "MIMO_API_KEY": "test-key"
        }):
            url, key = load_config()
            assert url == "https://api.xiaomimimo.com/v1"
            assert key == "test-key"

    def test_missing_url_raises(self):
        with patch.dict("os.environ", {"MIMO_API_KEY": "test-key"}, clear=True):
            with pytest.raises(ValueError, match="MIMO_API_BASE_URL"):
                load_config()

    def test_missing_key_raises(self):
        with patch.dict("os.environ", {"MIMO_API_BASE_URL": "https://api.xiaomimimo.com/v1"}, clear=True):
            with pytest.raises(ValueError, match="MIMO_API_KEY"):
                load_config()


class TestCallVisionApi:
    """Test API call construction and response handling."""

    @pytest.mark.asyncio
    async def test_successful_call(self):
        mock_choice = MagicMock()
        mock_choice.message.content = "A cat sitting on a table."
        mock_completion = MagicMock()
        mock_completion.choices = [mock_choice]

        with patch("mimo_vision_mcp.api.client.AsyncOpenAI") as MockClient:
            instance = MockClient.return_value
            instance.chat.completions.create = AsyncMock(return_value=mock_completion)

            result = await call_vision_api(
                base_url="https://api.xiaomimimo.com/v1",
                api_key="test-key",
                system_prompt="You are an image analyst.",
                image_url="data:image/png;base64,abc123",
                user_message="Describe this image."
            )

        assert result == "A cat sitting on a table."

    @pytest.mark.asyncio
    async def test_api_error_raises(self):
        with patch("mimo_vision_mcp.api.client.AsyncOpenAI") as MockClient:
            instance = MockClient.return_value
            instance.chat.completions.create = AsyncMock(
                side_effect=Exception("Authentication failed")
            )

            with pytest.raises(Exception, match="模型调用失败"):
                await call_vision_api(
                    base_url="https://api.xiaomimimo.com/v1",
                    api_key="bad-key",
                    system_prompt="test",
                    image_url="data:image/png;base64,abc",
                    user_message="test"
                )
