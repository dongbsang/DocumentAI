from easyocr import Reader
from PIL import Image
import numpy as np
from io import BytesIO

# EasyOCR reader 초기화 (한글 + 영어 지원)
reader = Reader(['ko', 'en'], gpu=True)

def extract_text_from_image(file_bytes: bytes) -> str:
    image = Image.open(BytesIO(file_bytes)).convert("RGB")
    result = reader.readtext(np.array(image), detail=0)
    return "\n".join(result)