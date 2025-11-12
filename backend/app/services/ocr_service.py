"""
개선된 OCR 서비스
- Tesseract와 EasyOCR 모두 지원
- 이미지 전처리로 인식률 향상
- 영수증/문서 최적화
- OCR 언어 설정 최적화 (PSM 모드 조정)
- 추출된 텍스트 후처리
- 에러 로깅 강화
- 성능 최적화 (메모리 관리, 이미지 크기 제한)
- LLM 프롬프트 개선
"""
from easyocr import Reader
from PIL import Image, ImageEnhance
import pytesseract
import numpy as np
from io import BytesIO
import re
import logging

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("⚠️ OpenCV가 설치되지 않아 고급 이미지 전처리를 사용할 수 없습니다.")

# 로거 설정 (DEBUG 레벨로 변경하여 상세 로그 확인)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# EasyOCR reader 초기화 (한글 + 영어 지원)
reader = Reader(['ko', 'en'], gpu=False)


class OCRService:
    """OCR 텍스트 추출 서비스"""

    # 최대 이미지 크기 제한 (메모리 최적화)
    MAX_IMAGE_DIMENSION = 4000

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
                logger.info(f"✅ Tesseract 경로 설정 완료: {path}")

                # tessdata 경로 확인 및 설정
                tessdata_paths = [
                    r'D:\AI\tesseract\tessdata',
                    r'D:\AI\tessdata',
                ]
                for tessdata_dir in tessdata_paths:
                    if os.path.exists(tessdata_dir):
                        os.environ['TESSDATA_PREFIX'] = tessdata_dir
                        logger.info(f"✅ TESSDATA 경로 설정: {tessdata_dir}")
                        break
                break

        if not tesseract_found:
            logger.warning("⚠️ Tesseract를 찾을 수 없습니다.")

    def extract_text_tesseract(self, image, preprocess=True):
        """
        Tesseract OCR로 텍스트 추출

        Args:
            image: PIL Image 객체 또는 bytes
            preprocess: 이미지 전처리 여부

        Returns:
            dict: {
                'text': 추출된 텍스트,
                'confidence': 신뢰도 점수 (0-100),
                'warning': 경고 메시지 (있을 경우)
            }
        """
        confidence_score = None
        warning_message = None

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

            logger.info(f"📐 원본 이미지 크기: {image.size}")

            # 이미지 크기 제한 (성능 최적화)
            image = self._limit_image_size(image)

            # 전처리 적용
            if preprocess:
                logger.info("🔧 OCR 전처리 시작...")
                image = self._preprocess_image_advanced(image)
                logger.info(f"✅ 전처리 완료, 최종 크기: {image.size}")

            # Tesseract 설정 개선 (영수증에 최적화된 PSM 6)
            custom_config = r'--oem 3 --psm 6 -c preserve_interword_spaces=1'
            # --oem 3: LSTM OCR 엔진 (최신, 가장 정확)
            # --psm 6: 단일 균일한 텍스트 블록 가정 (영수증 형태에 적합)
            # preserve_interword_spaces: 단어 간 공백 유지

            # Tesseract OCR 실행 (한글 + 영어)
            text = pytesseract.image_to_string(
                image,
                lang='kor+eng',
                config=custom_config
            )

            # OCR 신뢰도 측정
            try:
                data = pytesseract.image_to_data(image, lang='kor+eng',
                                                 config=custom_config,
                                                 output_type=pytesseract.Output.DICT
                                                 )
                confidences = [int(conf) for conf in data['conf'] if conf != '-1']
                if confidences:
                    confidence_score = sum(confidences) / len(confidences)
                    logger.info(f"📊 OCR 신뢰도: {confidence_score:.2f}%")

                    # 낮은 신뢰도 경고
                    if confidence_score < 60:
                        warning_message = f"⚠️ OCR 신뢰도가 낮습니다({confidence_score:.1f}%). 결과가 정확하지 않을 수 있습니다."
                        logger.warning(warning_message)
            except Exception as e:
                logger.warning(f"⚠️ 신뢰도 측정 실패: {str(e)}")

            # 원본 텍스트 길이 확인
            logger.info(f"📝 후처리 전 텍스트 길이: {len(text)} 자")
            if len(text) > 0:
                logger.info(f"📝 후처리 전 텍스트 샘플 (처음 200자): {text[:200]}")
            else:
                logger.warning("⚠️ 후처리 전 텍스트가 비어있습니다!")

            # 텍스트 후처리
            text = self._postprocess_text(text)

            logger.info(f"📝 후처리 후 텍스트 길이: {len(text)} 자")

            if not text.strip():
                logger.warning("⚠️ Tesseract가 텍스트를 추출하지 못했습니다.")
                return {
                    'text': "[텍스트를 추출하지 못했습니다. EasyOCR(손글씨 인식)을 시도해보세요.]",
                    'confidence': 0,
                    'warning': "텍스트 추출 실패"
                }

            logger.info(f"✅ Tesseract 추출 완료: {len(text)} 자")

            # 메모리 해제
            del image

            return {
                'text': text.strip(),
                'confidence': confidence_score if confidence_score else None,
                'warning': warning_message
            }

        except Exception as e:
            error_msg = str(e)
            logger.error(f"❌ Tesseract OCR 오류: {error_msg}")

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
            dict: {
                'text': 추출된 텍스트,
                'confidence': 평균 신뢰도 점수 (0-1),
                'warning': 경고 메시지 (있을 경우)
            }
        """
        confidence_score = None
        warning_message = None

        try:
            # bytes인 경우 PIL Image로 변환
            if isinstance(image, bytes):
                image = Image.open(BytesIO(image)).convert("RGB")

            logger.info(f"📐 원본 이미지 크기: {image.size}")

            # 이미지 크기 제한 (성능 최적화)
            image = self._limit_image_size(image)

            # EasyOCR용 전처리
            if preprocess:
                logger.info("🔧 EasyOCR 전처리 시작...")
                image = self._preprocess_image_for_easyocr(image)
                logger.info(f"✅ 전처리 완료, 최종 크기: {image.size}")

            # NumPy 배열로 변환
            img_array = np.array(image)

            # EasyOCR 실행 (detail=1로 신뢰도 포함)
            logger.info("🤖 EasyOCR 텍스트 인식 중...")
            result = reader.readtext(img_array, detail=1)

            if not result:
                logger.warning("⚠️ EasyOCR이 텍스트를 추출하지 못했습니다.")
                return {
                    'text': "[이미지에서 텍스트를 추출하지 못했습니다.]",
                    'confidence': 0,
                    'warning': "텍스트 추출 실패"
                }

            # 텍스트와 신뢰도 추출
            texts = [item[1] for item in result]
            confidences = [item[2] for item in result]

            # 평균 신뢰도 계산
            if confidences:
                confidence_score = sum(confidences) / len(confidences)
                logger.info(f"📊 EasyOCR 신뢰도: {confidence_score:.2%}")

                # 낮은 신뢰도 경고
                if confidence_score < 0.6:
                    warning_message = f"⚠️ OCR 신뢰도가 낮습니다 ({confidence_score:.1%}). 결과가 정확하지 않을 수 있습니다."
                    logger.warning(warning_message)

            text = "\n".join(texts)

            # 원본 텍스트 길이 확인
            logger.info(f"📝 후처리 전 텍스트 길이: {len(text)} 자")
            if len(text) > 0:
                logger.info(f"📝 후처리 전 텍스트 샘플 (처음 200자): {text[:200]}")
            else:
                logger.warning("⚠️ 후처리 전 텍스트가 비어있습니다!")

            # 텍스트 후처리
            text = self._postprocess_text(text)

            logger.info(f"📝 후처리 후 텍스트 길이: {len(text)} 자")
            logger.info(f"✅ EasyOCR 추출 완료: {len(text)} 자")

            # 메모리 해제
            del image
            del img_array

            return {
                'text': text,
                'confidence': confidence_score if confidence_score else None,
                'warning': warning_message
            }

        except Exception as e:
            logger.error(f"❌ EasyOCR 오류: {str(e)}")
            raise Exception(f"EasyOCR 실패: {str(e)}")

    def _limit_image_size(self, image):
        """
        이미지 크기를 제한하여 메모리 사용량 최적화

        Args:
            image: PIL Image 객체
        Returns:
            PIL Image: 크기 제한된 이미지
        """
        width, height = image.size
        max_dim = self.MAX_IMAGE_DIMENSION

        if width > max_dim or height > max_dim:
            ratio = min(max_dim / width, max_dim / height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            logger.info(f"📏 이미지 크기 제한: {width}x{height} → {new_width}x{new_height}")

        return image

    def _postprocess_text(self, text):
        """
        추출된 텍스트 후처리
        - 의미 없는 특수문자 제거 (보수적으로)
        - 연속된 공백 제거
        - 날짜/금액 패턴 정규화
        Args:
            text: 원본 텍스트
        Returns:
            str: 후처리된 텍스트
        """
        if not text:
            return text

        # 원본 텍스트 보존 (후처리 최소화)
        # 1. 제어 문자만 제거 (일반적인 특수문자는 유지)
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x9f]', '', text)

        # 2. 연속된 공백을 하나로
        text = re.sub(r' +', ' ', text)

        # 3. 연속된 줄바꿈을 최대 2개로 제한
        text = re.sub(r'\n{3,}', '\n\n', text)

        # 4. 각 줄의 앞뒤 공백 제거 (빈 줄 제거)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        text = '\n'.join(lines)

        return text.strip()

    def _preprocess_image_advanced(self, image):
        """
        Tesseract를 위한 고급 이미지 전처리
        - 해상도 향상 (적응형)
        - 그레이스케일 변환
        - 노이즈 제거
        - 적응형 이진화
        - 대비 향상

        Args:
            image: PIL Image 객체
        Returns:
            PIL Image: 전처리된 이미지
        """
        try:
            width, height = image.size

            # 1. 해상도 확대 (너무 작은 경우만)
            if width < 1000 or height < 1000:  # 기준 완화
                scale_factor = 2
                new_width = width * scale_factor
                new_height = height * scale_factor
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logger.info(f"  📏 해상도 확대: {width}x{height} → {new_width}x{new_height}")
            else:
                logger.info("   📏 해상도 적절, 확대 스킵")

            # 2. 대비 향상 (적응형)
            enhancer = ImageEnhance.Contrast(image)
            # 이미지 밝기에 따라 대비 조정
            stat = image.convert('L').getextrema()
            if stat[1] - stat[0] < 100:  # 대비가 낮은 경우
                image = enhancer.enhance(1.8)
                logger.info("  ✨ 대비 향상 완료 (강함)")
            else:
                image = enhancer.enhance(1.3)
                logger.info("  ✨ 대비 향상 완료 (보통)")

            # OpenCV 사용 가능한 경우 추가 전처리
            if CV2_AVAILABLE:
                img_array = np.array(image)

                # 3. 그레이스케일 변환
                if len(img_array.shape) == 3:
                    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                else:
                    gray = img_array
                logger.info("  🎨 그레이스케일 변환 완료")

                # 4. 노이즈 제거 (적응형)
                # 이미지 품질 체크
                noise_level = cv2.Laplacian(gray, cv2.CV_64F).var()
                if noise_level < 100:  # 노이즈가 많은 경우
                    denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
                    logger.info("  🧹 노이즈 제거 완료 (강함)")
                else:
                    denoised = cv2.GaussianBlur(gray, (3, 3), 0)
                    logger.info("  🧹 노이즈 제거 완료 (가벼움)")

                # 5. Otsu의 이진화 (적응형 임계값)
                # 먼저 적응형 이진화 시도
                binary = cv2.adaptiveThreshold(
                    denoised,
                    255,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY,
                    11,
                    2
                )
                logger.info("  ⚫⚪ 적응형 이진화 완료")

                # PIL Image로 변환
                image = Image.fromarray(binary)

                # 중간 배열 메모리 해제
                del img_array, gray, denoised, binary
            else:
                # OpenCV 없으면 간단한 전처리
                image = image.convert('L')
                logger.info("  🎨 그레이스케일 변환 완료 (기본)")

            return image

        except Exception as e:
            logger.warning(f"⚠️ 전처리 실패, 원본 사용: {str(e)}")
            return image

    def _preprocess_image_for_easyocr(self, image):
        """
        EasyOCR을 위한 전처리 (Tesseract보다 가볍게)

        Args:
            image: PIL Image 객체
        Returns:
            PIL Image: 전처리된 이미지
        """
        try:
            # 1. 해상도 확인 (너무 크면 축소)
            width, height = image.size
            max_dimension = 2000

            if width > max_dimension or height > max_dimension:
                ratio = min(max_dimension / width, max_dimension / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
                logger.info(f"  📏 이미지 크기 조정: {width}x{height} → {new_width}x{new_height}")

            # 2. 대비 향상
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(1.3)
            logger.info("  ✨ 대비 향상 완료")

            # 3. 선명도 향상
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(1.5)
            logger.info("  🔍 선명도 향상 완료")

            return image

        except Exception as e:
            logger.warning(f"⚠️ EasyOCR 전처리 실패, 원본 사용: {str(e)}")
            return image

    def _preprocess_image(self, image):
        """
        기본 이미지 전처리 (레거시, 호환성 유지)
        """
        return self._preprocess_image_advanced(image)


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
        result = service.extract_text_easyocr(file_bytes, preprocess=True)
    else:
        result = service.extract_text_tesseract(file_bytes, preprocess=True)

    # 이전 버전 호환성을 위해 텍스트만 반환
    # (신규 코드에서는 result 딕셔너리 전체를 사용 권장)
    return result['text']


def extract_text_from_image_detailed(file_bytes: bytes,
                                     use_easy_ocr: bool = False
                                     ) -> dict:
    """
    상세 정보 포함 텍스트 추출 함수

    Args:
        file_bytes: 이미지 바이트 데이터
        use_easy_ocr: True면 EasyOCR, False면 Tesseract

    Returns:
        dict: {
            'text': 추출된 텍스트,
            'confidence': 신뢰도 점수,
            'warning': 경고 메시지,
            'llm_context': LLM에 전달할 컨텍스트 정보
        }
    """
    service = OCRService()
    if use_easy_ocr:
        result = service.extract_text_easyocr(file_bytes, preprocess=True)
    else:
        result = service.extract_text_tesseract(file_bytes, preprocess=True)

    # LLM 프롬프트에 추가할 컨텍스트 정보
    llm_context = ""
    if result.get('confidence'):
        conf = result['confidence']
        if isinstance(conf, float) and conf < 1:  # EasyOCR (0-1 범위)
            conf *= 100

        if conf < 60:
            llm_context = f"[주의: OCR 신뢰도가 낮음 ({conf:.1f}%). 텍스트에 오류가 있을 수 있음]"
        elif conf < 80:
            llm_context = f"[참고: OCR 신뢰도 보통 ({conf:.1f}%). 일부 텍스트가 부정확할 수 있음]"

    result['llm_context'] = llm_context
    return result
