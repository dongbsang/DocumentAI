import pytesseract
from PIL import Image

def extract_text(image_stream):
    """
    이미지 스트림에서 텍스트를 추출하는 함수
    """
     # PIL 이미지로 로드
    image = Image.open(image_stream)
    # 전처리: 그레이스케일 변환, 스케일링 등
    # image = image.convert("L")

    # pytesseract로 OCR 실행
    text = pytesseract.image_to_string(image, lang="kor+eng")
    
    # 후처리: 불필요한 공백 제거 등
    text = text.strip() 
    
    return text