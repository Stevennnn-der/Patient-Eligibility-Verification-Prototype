from typing import Tuple


def extract_text_from_image(file_bytes: bytes) -> str:
    """
    Simulated OCR service.
    In production this would call AWS Textract, Google Vision, or Tesseract.
    """

    mock_text = """
    DRIVER LICENSE
    Michael Motorist
    DOB: 1978-03-08
    Address: 345 Anywhere Street, Your City, NY 12345
    """

    return mock_text