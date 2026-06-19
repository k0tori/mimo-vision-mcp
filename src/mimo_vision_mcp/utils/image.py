"""Image processing utilities."""

import base64
import os

MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB


def detect_media_type(data: bytes) -> str:
    """Detect image media type from magic bytes.

    Args:
        data: First bytes of image file (at least 12 bytes recommended).

    Returns:
        MIME type string (e.g., "image/png").

    Raises:
        ValueError: If format cannot be detected.
    """
    if len(data) < 4:
        raise ValueError("错误：不支持的图片格式，支持 PNG/JPEG/WebP/GIF")

    # Check PNG (8 bytes)
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return "image/png"

    # Check JPEG (3 bytes)
    if data[:3] == b'\xFF\xD8\xFF':
        return "image/jpeg"

    # Check WebP (RIFF + WEBP at offset 8)
    if data[:4] == b'RIFF' and len(data) >= 12 and data[8:12] == b'WEBP':
        return "image/webp"

    # Check GIF (6 bytes)
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return "image/gif"

    raise ValueError("错误：不支持的图片格式，支持 PNG/JPEG/WebP/GIF")


def encode_image_data_uri(data: bytes) -> str:
    """Encode raw image bytes as a base64 data URI.

    Args:
        data: Raw image file bytes.

    Returns:
        Data URI string (e.g., "data:image/png;base64,...").
    """
    media_type = detect_media_type(data[:12])
    b64 = base64.b64encode(data).decode("ascii")
    return f"data:{media_type};base64,{b64}"


def read_and_encode_image(file_path: str) -> str:
    """Read a local image file and return as base64 data URI.

    Args:
        file_path: Absolute path to the image file.

    Returns:
        Data URI string.

    Raises:
        ValueError: If file doesn't exist, is too large, or unsupported format.
    """
    if not os.path.isfile(file_path):
        raise ValueError(f"错误：文件不存在 - {file_path}")

    file_size = os.path.getsize(file_path)
    if file_size > MAX_FILE_SIZE:
        size_mb = file_size / (1024 * 1024)
        raise ValueError(f"错误：文件过大（{size_mb:.1f}MB），限制 20MB")

    with open(file_path, "rb") as f:
        data = f.read()

    return encode_image_data_uri(data)


def is_url(image: str) -> bool:
    """Check if the input is a URL (http/https).

    Args:
        image: Input string to check.

    Returns:
        True if input starts with http:// or https://.
    """
    return image.startswith("http://") or image.startswith("https://")


def resolve_image(image: str) -> str:
    """Resolve image input to API-ready format.

    If input is a URL, returns it directly.
    If input is a file path, reads and encodes as base64 data URI.

    Args:
        image: File path or URL.

    Returns:
        URL string or data URI string.
    """
    if is_url(image):
        return image
    return read_and_encode_image(image)
