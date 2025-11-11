"""
개선된 OCR 서비스
- Tesseract와 EasyOCR 모두 지원
- PIL Image 객체 직접 처리
"""
from easyocr import Reader
from PIL import Image
import pytesseract
import numpy as np
from io import BytesIO

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV가 설치되지 않아 이미지 전처리를 사용할 수 없습니다.")

# EasyOCR reader 초기화 (한글 + 영어 지원)
reader = Reader(['ko', 'en'], gpu=False)


class OCRService:
    """OCR 텍스트 추출 서비스"""

    def __init__(self):
        possible_paths = [
            r'D:\AI\tesseract\tesseract.exe',  # 사용자 지정 경로
        ]

        import os
        tesseract_found = False

        for path in possible_paths:
            if os.path.exists(path):
                pytesseract.pytesseract.tesseract_cmd = path
                tesseract_found = True
                print(f"✅ Tesseract 경로 설정 완료: {path}")

                # tessdata 경로 확인 및 설정
                # D:\AI\tesseract 폴더 내의 tessdata 또는 D:\AI\tessdata 확인
                tessdata_paths = [
                    r'D:\AI\tesseract\tessdata',
                    r'D:\AI\tessdata',
                ]
                for tessdata_dir in tessdata_paths:
                    if os.path.exists(tessdata_dir):
                        os.environ['TESSDATA_PREFIX'] = tessdata_dir
                        print(f"✅ TESSDATA 경로 설정: {tessdata_dir}")
                        break
                break

        if not tesseract_found:
            print("⚠️ Tesseract를 찾을 수 없습니다.")

    def extract_text_tesseract(self, image, preprocess=True):
        """
        Tesseract OCR로 텍스트 추출

        Args:
            image: PIL Image 객체 또는 bytes
            preprocess: 이미지 전처리 여부

        Returns:
            str: 추출된 텍스트
        """
        try:
            # Tesseract 설치 확인
            if pytesseract.pytesseract.tesseract_cmd is None:
                raise Exception(
                    "Tesseract OCR이 설치되지 않았습니다.\n"
                    "다운로드: https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "추천 설치 경로: D:\\Tesseract-OCR\n"
                    "설치 후 백엔드를 재시작하세요."
                )
            
            # bytes인 경우 PIL Image로 변환
            if isinstance(image, bytes):
                image = Image.open(BytesIO(image)).convert("RGB")

            # 전처리 옵션 (영수증 등에 유용)
            if preprocess:
                image = self._preprocess_image(image)

            # Tesseract OCR 실행 (한글 + 영어)
            text = pytesseract.image_to_string(image, lang='kor+eng')

            return text.strip()

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Tesseract OCR 오류: {error_msg}")
            
            # 설치 관련 오류인 경우 자세한 안내 제공
            if "not installed" in error_msg or "PATH" in error_msg:
                raise Exception(
                    "Tesseract OCR이 설치되지 않았거나 PATH에 등록되지 않았습니다.\n\n"
                    "해결 방법:\n"
                    "1. Tesseract 다운로드: https://github.com/UB-Mannheim/tesseract/wiki\n"
                    "2. D:\\Tesseract-OCR 또는 C:\\Program Files\\Tesseract-OCR에 설치\n"
                    "3. 설치 시 Korean 언어 팩 체크\n"
                    "4. 백엔드 서버 재시작"
                )
            raise Exception(f"Tesseract OCR 실패: {error_msg}")

    def extract_text_easyocr(self, image, preprocess=True):
        """
        EasyOCR로 텍스트 추출 (손글씨 인식 가능)

        Args:
            image: PIL Image 객체 또는 bytes
            preprocess: 이미지 전처리 여부

        Returns:
            str: 추출된 텍스트
        """
        try:
            # bytes인 경우 PIL Image로 변환
            if isinstance(image, bytes):
                image = Image.open(BytesIO(image)).convert("RGB")

            # 전처리 옵션 (영수증 등에 유용)
            if preprocess:
                image = self._preprocess_image(image)

            # NumPy 배열로 변환
            img_array = np.array(image)

            # EasyOCR 실행
            result = reader.readtext(img_array, detail=0)

            if not result:
                return "[이미지에서 텍스트를 추출하지 못했습니다.]"

            return "\n".join(result)

        except Exception as e:
            print(f"❌ EasyOCR 오류: {str(e)}")
            raise Exception(f"EasyOCR 실패: {str(e)}")

    def _preprocess_image(self, image):
        """
        영수증 이미지 전처리
        - 그레이스케일 변환
        - 노이즈 제거
        - 대비 향상
        Args:
            image: PIL Image 객체
        Returns:
            PIL Image: 전처리된 이미지
        """
        try:
            if not CV2_AVAILABLE:
                print("⚠️ OpenCV 미설치, 전처리 생략")
                return image

            # NumPy 배열로 변환
            img_array = np.array(image)

            # 그레이스케일 변환
            if len(img_array.shape) == 3:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
            else:
                gray = img_array

            # 노이즈 제거 (Bilateral Filter)
            denoised = cv2.bilateralFilter(gray, 9, 75, 75)

            # 적응형 임계값 적용
            adaptive_thresh = cv2.adaptiveThreshold(
                denoised, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11, 2
            )

            # PIL 이미지로 다시 변환
            processed_image = Image.fromarray(adaptive_thresh)

            return processed_image

        except Exception as e:
            print(f"⚠️ 이미지 전처리 실패, 원본 사용: {str(e)}")
            return image

    def extract_text_from_image(self, file_bytes: bytes, use_easy_ocr=False):
        """
        기존 함수 호환성 유지 (레거시)
        Args:
            file_bytes: 이미지 바이트 데이터
            use_easy_ocr: EasyOCR 사용 여부
        Returns:
            str: 추출된 텍스트
        """
        if use_easy_ocr:
            return self.extract_text_easyocr(file_bytes)
        else:
            return self.extract_text_tesseract(file_bytes)


# 기존 함수 호환성 유지
def extract_text_from_image(file_bytes: bytes,
                            use_easy_ocr: bool = False
                            ) -> str:
    """
    기존 코드 호환용 래퍼 함수
    Args:
        file_bytes: 이미지 바이트 데이터
        use_easy_ocr: True면 EasyOCR, False면 Tesseract
    Returns:
        str: 추출된 텍스트
    """
    service = OCRService()
    if use_easy_ocr:
        return service.extract_text_easyocr(file_bytes)
    else:
        return service.extract_text_tesseract(file_bytes)
