import pytest
import os
import tempfile
from mimo_vision_mcp.utils.image import detect_media_type, read_and_encode_image, encode_image_data_uri


class TestDetectMediaType:
    """Test magic bytes based media type detection."""

    def test_png_detection(self):
        png_header = b'\x89PNG\r\n\x1a\n' + b'\x00' * 8
        assert detect_media_type(png_header) == "image/png"

    def test_jpeg_detection(self):
        jpeg_header = b'\xFF\xD8\xFF\xE0' + b'\x00' * 8
        assert detect_media_type(jpeg_header) == "image/jpeg"

    def test_webp_detection(self):
        webp_header = b'RIFF\x00\x00\x00\x00WEBP' + b'\x00' * 8
        assert detect_media_type(webp_header) == "image/webp"

    def test_gif87a_detection(self):
        gif_header = b'GIF87a' + b'\x00' * 8
        assert detect_media_type(gif_header) == "image/gif"

    def test_gif89a_detection(self):
        gif_header = b'GIF89a' + b'\x00' * 8
        assert detect_media_type(gif_header) == "image/gif"

    def test_unsupported_format_raises(self):
        with pytest.raises(ValueError, match="不支持的图片格式"):
            detect_media_type(b'\x00\x00\x00\x00')

    def test_empty_data_raises(self):
        with pytest.raises(ValueError, match="不支持的图片格式"):
            detect_media_type(b'')


class TestReadAndEncodeImage:
    """Test file reading and base64 encoding."""

    def test_read_png_file(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        data_uri = read_and_encode_image(str(file_path))
        assert data_uri.startswith("data:image/png;base64,")

    def test_read_jpeg_file(self, tmp_path):
        jpeg_data = b'\xFF\xD8\xFF\xE0' + b'\x00' * 100
        file_path = tmp_path / "test.jpg"
        file_path.write_bytes(jpeg_data)

        data_uri = read_and_encode_image(str(file_path))
        assert data_uri.startswith("data:image/jpeg;base64,")

    def test_nonexistent_file_raises(self):
        with pytest.raises(ValueError, match="文件不存在"):
            read_and_encode_image("/nonexistent/path/image.png")

    def test_directory_raises(self, tmp_path):
        with pytest.raises(ValueError, match="文件不存在"):
            read_and_encode_image(str(tmp_path))

    def test_file_too_large_raises(self, tmp_path):
        large_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * (21 * 1024 * 1024)
        file_path = tmp_path / "large.png"
        file_path.write_bytes(large_data)

        with pytest.raises(ValueError, match="文件过大"):
            read_and_encode_image(str(file_path))


class TestEncodeImageDataUri:
    """Test base64 data URI encoding."""

    def test_encode_png(self):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 10
        result = encode_image_data_uri(png_data)
        assert result.startswith("data:image/png;base64,")
        assert len(result) > len("data:image/png;base64,")

    def test_encode_jpeg(self):
        jpeg_data = b'\xFF\xD8\xFF\xE0' + b'\x00' * 10
        result = encode_image_data_uri(jpeg_data)
        assert result.startswith("data:image/jpeg;base64,")


from mimo_vision_mcp.utils.image import is_url, resolve_image


class TestIsUrl:
    """Test URL detection."""

    def test_http_url(self):
        assert is_url("http://example.com/image.png") is True

    def test_https_url(self):
        assert is_url("https://example.com/image.png") is True

    def test_local_path(self):
        assert is_url("/home/user/image.png") is False

    def test_windows_path(self):
        assert is_url(r"C:\Users\image.png") is False

    def test_relative_path(self):
        assert is_url("./image.png") is False


class TestResolveImage:
    """Test image resolution (URL passthrough, file encoding)."""

    def test_url_passthrough(self):
        url = "https://example.com/image.png"
        result = resolve_image(url)
        assert result == url

    def test_local_file_encoding(self, tmp_path):
        png_data = b'\x89PNG\r\n\x1a\n' + b'\x00' * 100
        file_path = tmp_path / "test.png"
        file_path.write_bytes(png_data)

        result = resolve_image(str(file_path))
        assert result.startswith("data:image/png;base64,")
