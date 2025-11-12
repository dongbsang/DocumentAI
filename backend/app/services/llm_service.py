"""
개선된 LLM 서비스
- OllamaLLM 래퍼 클래스 제공
- 재사용 가능한 API
- OCR 신뢰도 정보를 LLM에 전달
- 상세 로깅 추가
"""
try:
    from langchain_ollama import OllamaLLM as BaseLLM
    print("✅ langchain_ollama에서 OllamaLLM import 성공")
except ImportError:
    print("⚠️ langchain_ollama import 실패, 대안 방법 시도 중...")
    try:
        from langchain_community.llms import Ollama as BaseLLM
        print("✅ langchain_community에서 OllamaLLM import 성공")
    except ImportError:
        print("❌ langchain_community에서도 import 실패")
        raise ImportError(
            "Ollama LLM을 import할 수 없습니다. 다음을 확인하세요:\n"
            "1. 가상환경이 활성화되어 있는지\n"
            "2. pip install langchain-ollama 또는 pip install langchain-community 실행\n"
            "3. pip list로 설치 확인"
        )

from app.services.pdf_service import (
    extract_text_from_pdf,
    extract_images_from_pdf,
)
from app.services.ocr_service import extract_text_from_image_detailed
from app.services.word_service import extract_text_from_docx, extract_text_from_doc
from app.services.text_service import extract_text_from_txt
from app.services.hwp_service import extract_text_from_hwp
from app.services.prompt_service import get_prompt_template
from app.services.upload_service import FileFormat
import logging

# 로거 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LLMService:
    """LLM 서비스 래퍼 클래스"""

    def __init__(self, model="llama3.2:3b",  # "mistral:7b-instruct-q4_0",
                 temperature=0.3,
                 top_p=0.95
                 ):
        """model: ""llama3.2:3b"""
        self.llm = BaseLLM(
            model=model,
            temperature=temperature,
            top_p=top_p,
            num_gpu=0  # CPU 사용 강제 (GPU 메모리 부족 방지)
        )

    def generate(self, prompt: str) -> str:
        """
        LLM으로 텍스트 생성
        Args:
            prompt: 프롬프트 문자열
        Returns:
            str: LLM 응답
        """
        try:
            response = self.llm.invoke(prompt)
            return response
        except Exception as e:
            raise Exception(f"LLM 생성 실패: {str(e)}")


# 전역 LLM 인스턴스
llm = BaseLLM(
    model="llama3.2:3b",
    temperature=0.3,
    top_p=0.95,
    num_gpu=0  # CPU 사용 강제 (GPU 메모리 부족 방지)
)


def analyze_document(
    file_bytes: bytes,
    file_format: str,
    category: str,
    use_handwriting: bool = False
) -> str:
    """
    문서 분석 및 LLM 요약
    Args:
        file_bytes: 파일 바이너리 데이터
        file_format: 파일 포맷 (pdf, image, word_docx, word_doc, hwp, txt 등)
        category: 문서 카테고리 (이력서, 영수증 등)
        use_handwriting: 손글씨 인식 여부

    Returns:
        str: LLM 분석 결과 또는 에러 메시지
    """
    try:
        text = ""
        ocr_context = ""  # OCR 신뢰도 정보
        logger.info(f"📋 파일 포맷: {file_format}, 카테고리: {category}, 손글씨: {use_handwriting}")

        # ✅ 1. 포맷별 텍스트 추출
        if file_format == FileFormat.SEARCHABLE_PDF.value:
            logger.info("📄 검색 가능한 PDF 문서 감지 → 텍스트 추출 중...")
            text = extract_text_from_pdf(file_bytes)

        elif file_format == FileFormat.SCANNED_PDF.value:
            logger.info("📄 스캔된 PDF 문서 감지 → 이미지 추출 후 OCR 중...")
            images = extract_images_from_pdf(file_bytes)

            # 각 이미지에 대해 OCR 수행 (상세 정보 포함)
            texts = []
            for idx, img in enumerate(images):
                logger.info(f"🖼️ 페이지 {idx+1}/{len(images)} OCR 처리 중...")
                result = extract_text_from_image_detailed(img, use_easy_ocr=use_handwriting)
                texts.append(result['text'])

                # OCR 컨텍스트 정보 수집
                if result.get('llm_context'):
                    ocr_context += f"\n[페이지 {idx+1}] {result['llm_context']}"

            text = "\n\n--- 페이지 구분 ---\n\n".join(texts)

        elif file_format == FileFormat.IMAGE.value:
            logger.info("🖼️ 이미지 파일 감지 → OCR 중...")
            result = extract_text_from_image_detailed(file_bytes, use_easy_ocr=use_handwriting)
            text = result['text']
            
            logger.info(f"📝 OCR 추출 텍스트 길이: {len(text)} 자")
            logger.info(f"📝 OCR 추출 텍스트 샘플 (처음 500자):\n{text[:500]}")
            
            # OCR 컨텍스트 정보 추가
            if result.get('llm_context'):
                ocr_context = result['llm_context']

        elif file_format == FileFormat.WORD_DOCX.value:
            logger.info("📄 Word .docx 문서 감지 → python-docx로 직접 텍스트 추출 중...")
            text = extract_text_from_docx(file_bytes)

        elif file_format == FileFormat.WORD_DOC.value:
            logger.info("📄 Word .doc 문서 감지 → olefile로 텍스트 추출 중...")
            text = extract_text_from_doc(file_bytes)

        elif file_format == FileFormat.TXT.value:
            logger.info("📄 텍스트 파일 감지 → 인코딩 자동 감지 후 읽기...")
            text = extract_text_from_txt(file_bytes)

        elif file_format == FileFormat.HWP.value:
            logger.info("📄 HWP 문서 감지 → pyhwp로 텍스트 추출 중...")
            text = extract_text_from_hwp(file_bytes)

        else:
            error_msg = f"지원하지 않는 형식: {file_format}"
            logger.error(f"❌ {error_msg}")
            return f"[오류] {error_msg}"

        # ✅ 2. 텍스트 후처리 (OCR 텍스트만)
        logger.info(f"📝 후처리 전 텍스트 길이: {len(text)} 자")
        text = deduplicate_lines(text)
        logger.info(f"📝 후처리 후 텍스트 길이: {len(text)} 자")
        
        if not text.strip():
            logger.warning("⚠️ 텍스트를 추출하지 못했습니다.")
            return "[오류] 텍스트를 추출하지 못했습니다."

        logger.info(f"📝 최종 추출 텍스트 길이: {len(text)} 자")

        # ✅ 3. OCR 컨텍스트 정보를 텍스트에 추가
        if ocr_context:
            logger.info(f"⚠️ OCR 컨텍스트 추가: {ocr_context}")
            # LLM에게 OCR 신뢰도 정보 전달
            text = f"{ocr_context}\n\n=== 추출된 텍스트 ===\n\n{text}"

        # ✅ 4. 프롬프트 생성 및 LLM 호출
        prompt = get_prompt_template(
            context=text,
            category=category,
            use_handwriting=use_handwriting
        )

        logger.info("🤖 LLM 분석 시작...")
        response = llm.invoke(prompt)
        
        # ✅ 상세 로깅
        logger.info("=" * 80)
        logger.info(f"✅ LLM 응답 완료")
        logger.info(f"📊 응답 타입: {type(response)}")
        logger.info(f"📏 응답 길이: {len(response)} 자")
        logger.info("📄 응답 내용 (처음 500자):")
        logger.info(response[:500])
        logger.info("=" * 80)
        logger.info("📄 전체 응답:")
        logger.info(response)
        logger.info("=" * 80)
        
        # ✅ 빈 응답 체크
        if not response or not response.strip():
            logger.error("❌ LLM이 빈 응답을 반환했습니다!")
            return "[오류] LLM이 빈 응답을 반환했습니다."
        
        return response

    except Exception as e:
        error_msg = f"문서 분석 중 오류 발생: {str(e)}"
        logger.error(f"❌ {error_msg}")
        import traceback
        logger.error(traceback.format_exc())
        return f"[오류] {error_msg}"


def deduplicate_lines(text: str) -> str:
    """
    중복된 줄 제거 (OCR 텍스트용)
    
    Args:
        text: 원본 텍스트
    Returns:
        str: 중복 제거된 텍스트
    """
    if not text:
        return text
    
    seen = set()
    result = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and stripped not in seen:
            seen.add(stripped)
            result.append(stripped)
    
    return "\n".join(result)
