import pytesseract
from PIL import Image
from pathlib import Path

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg"]

def extract_text_from_image(file_path: str) -> str:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if path.suffix.lower() not in SUPPORTED_FORMATS:
        raise ValueError(f"Unsupported image format: {path.suffix}. Supported: {SUPPORTED_FORMATS}")

    print(f"Opening image: {file_path}")

    image = Image.open(file_path)

    print(f"Image size: {image.size}, Mode: {image.mode}")
    print(f"Running OCR...")

    text = pytesseract.image_to_string(image)

    if not text.strip():
        raise ValueError("OCR could not extract any text from the image — try anorher image")

    print(f"Extracted {len(text)} characters from the image")
    return text