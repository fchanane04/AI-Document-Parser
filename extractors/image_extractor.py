import pytesseract
from PIL import Image
from pathlib import Path

SUPPORTED_FORMATS = [".png", ".jpg", ".jpeg"]

def check_image_quality(text: str, total_chars: int) -> dict:
    if total_chars == 0:
        return {"quality": "bad", "score": 0}
    
    #count how many characters look like garbage
    garbage_chars = sum(1 for c in text if not c.isalnum() and c not in " @.,\n-_/:")
    garbage_ratio = garbage_chars / total_chars

    #score quality based on calculated ratio
    if garbage_ratio > 0.3:
        return {"quality": "poor", "score": round((1 - garbage_ratio) * 100)}
    elif garbage_ratio > 0.15:
        return {"quality": "fair", "score": round((1 - garbage_ratio) * 100)}
    else:
        return {"quality": "good", "score": round((1 - garbage_ratio) * 100)}

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

    #check quality
    quality = check_image_quality(text, len(text))

    if quality["quality"] == "poor":
        print(f"\n WARNING: Image quality is poor (score: {quality['score']}/100)")
        print(f"Some data may be missing or replaced with null")
        print(f"For better results use a clearer, higher resolution image\n")
    elif quality["quality"] == "fair":
        print(f"\nWARNING: Image quality is fair (score: {quality['score']}/100)")
        print(f"Some data may be inaccurate, please verify the results\n")
    else:
        print(f"Image quality looks good (score: {quality['score']}/100)")

    print(f"Extracted {len(text)} characters from the image")
    return text