"""Passes the Canadian flag image to the Anthropic API for analysis."""

import anthropic
import base64
from pathlib import Path


_MAGIC_BYTES: list[tuple[bytes, str]] = [
    (b"\x89PNG\r\n\x1a\n", "image/png"),
    (b"\xff\xd8\xff", "image/jpeg"),
    (b"GIF87a", "image/gif"),
    (b"GIF89a", "image/gif"),
    (b"RIFF????WEBP", "image/webp"),  # handled separately below
]


def detect_media_type(path: str) -> str:
    """Detect the image media type by inspecting the file's magic bytes."""
    with open(path, "rb") as f:
        header = f.read(12)

    if header[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if header[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if header[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if header[:4] == b"RIFF" and header[8:12] == b"WEBP":
        return "image/webp"
    raise ValueError(
        f"Unrecognised image format for '{path}'. "
        "Anthropic vision supports: PNG, JPEG, GIF, WebP."
    )


def analyze_flag(image_path: str) -> str:
    """Send the flag image to Claude and return its description."""
    media_type = detect_media_type(image_path)

    image_data = base64.standard_b64encode(Path(image_path).read_bytes()).decode()

    client = anthropic.Anthropic()
    message = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=256,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": "What flag is shown in this image? Describe it briefly.",
                    },
                ],
            }
        ],
    )
    return message.content[0].text


if __name__ == "__main__":
    flag_path = "images/canadian-flag.png"
    print(f"Detected media type: {detect_media_type(flag_path)}")
    print(analyze_flag(flag_path))
