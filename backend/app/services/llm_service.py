"""
개선된 LLM 서비스
- OllamaLLM 래퍼 클래스 제공
- 재사용 가능한 API
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
from app.services.ocr_service import extract_text_from_image
from app.services.word_service import convert_docx_to_pdf_bytes
from app.services.prompt_service import get_prompt_template
from app.services.upload_service import FileFormat


class LLMService:
    """LLM 서비스 래퍼 클래스"""

    def __init__(self, model="llama3.2:1b",  # "mistral:7b-instruct-q4_0",
                 temperature=0.3,
                 top_p=0.95
                 ):
        """model: "llama3.2:1b"""
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
    model="llama3.2:1b",
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
        file_format: 파일 포맷 (pdf, image, word, hwp 등)
        category: 문서 카테고리 (이력서, 영수증 등)
        use_handwriting: 손글씨 인식 여부

    Returns:
        str: LLM 분석 결과 또는 에러 메시지
    """
    try:
        text = ""
        print(f"📋 파일 포맷: {file_format}, 카테고리: {category}, 손글씨: {use_handwriting}")

        # ✅ 1. 포맷별 텍스트 추출
        if file_format == FileFormat.SEARCHABLE_PDF.value:
            print("📄 검색 가능한 PDF 문서 감지 → 텍스트 추출 중...")
            text = extract_text_from_pdf(file_bytes)

        elif file_format == FileFormat.SCANNED_PDF.value:
            print("📄 스캔된 PDF 문서 감지 → 이미지 추출 후 OCR 중...")
            images = extract_images_from_pdf(file_bytes)
            text = "\n".join(extract_text_from_image(img, use_easy_ocr=use_handwriting) for img in images)

        elif file_format == FileFormat.IMAGE.value:
            print("🖼️ 이미지 파일 감지 → OCR 중...")
            text = extract_text_from_image(file_bytes, use_easy_ocr=use_handwriting)

        elif file_format == FileFormat.WORD.value:
            print("📄 Word 문서 감지 → PDF 변환 중...")
            try:
                pdf_bytes = convert_docx_to_pdf_bytes(file_bytes)
                print("📄 Word → PDF 변환 완료 → 텍스트 추출 중...")
                text = extract_text_from_pdf(pdf_bytes)
            except Exception as e:
                error_msg = f"Word → PDF 변환 실패: {str(e)}"
                print(f"❌ {error_msg}")
                return f"[오류] {error_msg}"

        elif file_format == FileFormat.HWP.value:
            error_msg = "HWP 파일 형식은 아직 지원되지 않습니다."
            print(f"⚠️ {error_msg}")
            return f"[오류] {error_msg}"

        else:
            error_msg = f"지원하지 않는 형식: {file_format}"
            print(f"❌ {error_msg}")
            return f"[오류] {error_msg}"

        # ✅ 2. 텍스트 후처리
        text = deduplicate_lines(text)
        if not text.strip():
            return "[오류] 텍스트를 추출하지 못했습니다."

        print(f"📝 추출된 텍스트 길이: {len(text)} 자")

        # ✅ 3. 프롬프트 생성 및 LLM 호출
        prompt = get_prompt_template(
            context=text,
            category=category,
            use_handwriting=use_handwriting
        )

        print("🤖 LLM 분석 시작...")
        response = llm.invoke(prompt)
        print(f"✅ LLM 응답 완료 (길이: {len(response)} 자)")

        return response

    except Exception as e:
        error_msg = f"문서 분석 중 오류 발생: {str(e)}"
        print(f"❌ {error_msg}")
        return f"[오류] {error_msg}"


def deduplicate_lines(text: str) -> str:
    """
    중복된 줄 제거
    Args:
        text: 원본 텍스트
    Returns:
        str: 중복 제거된 텍스트
    """
    seen = set()
    result = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and stripped not in seen:
            seen.add(stripped)
            result.append(stripped)
    return "\n".join(result)
