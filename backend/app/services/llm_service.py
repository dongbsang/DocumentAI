from langchain_ollama import OllamaLLM
from app.services.pdf_service import (
    extract_text_from_pdf,
    extract_images_from_pdf,
)
from app.services.ocr_service import extract_text_from_image
from app.services.doc_service import convert_docx_to_pdf_bytes
from app.services.prompt_service import get_prompt_template
from app.services.text_splitter_service import split_text
from app.services.vector_store_service import create_vectorstore_from_chunks
from app.services.upload_service import FileFormat


# ✅ Ollama는 model_path 필요 없음
llm = OllamaLLM(
    model="mistral",   # 설치된 Ollama 모델 이름
    temperature=0.3,
    top_p=0.95
)


def analyze_document(
    file_bytes: bytes,
    file_format: str,
    category: str,
    use_handwriting: bool = False
) -> str:
    """
    문서 분석
    """
    try:
        text = ""

        # ✅ 1. 포맷 분기 처리
        if file_format == FileFormat.SEARCHABLE_PDF.value:
            text = extract_text_from_pdf(file_bytes)

        elif file_format == FileFormat.SCANNED_PDF.value:
            images = extract_images_from_pdf(file_bytes)
            text = "\n".join(extract_text_from_image(img) for img in images)
            return {"error": f"[지원하지 않는 형식] {file_format}"}

        elif file_format == FileFormat.IMAGE.value:
            text = extract_text_from_image(file_bytes)

        elif file_format == FileFormat.WORD.value:
            print("📄 Word 문서 감지 → PDF 변환 중...")
            try:
                pdf_bytes = convert_docx_to_pdf_bytes(file_bytes)
                text = extract_text_from_pdf(pdf_bytes)
            except Exception as e:
                return {"error": f"Word → PDF 변환 실패: {str(e)}"}
        elif file_format == FileFormat.HWP.value:
            # ⚠️ 향후 구현 필요: hwp → pdf 변환 후 다시 분석
            text = "[해당 문서 유형은 아직 지원되지 않습니다.]"
            return {"error": text}

        else:
            return {"error": f"[지원하지 않는 형식] {file_format}"}

        # ✅ 2. 후처리: deduplication
        text = deduplicate_lines(text)

        if not text.strip():
            text = "[텍스트를 추출하지 못했습니다.]"

        # ✅ 3. 텍스트 → chunk → vectorstore
        chunks = split_text(text)
        retriever = create_vectorstore_from_chunks(chunks).as_retriever()

        prompt = get_prompt_template(
            context=text,
            category=category,
            use_handwriting=use_handwriting
        )

        print("start---------------------------------------")
        response = llm.invoke(prompt)
        print("end---------------------------------------")

        return {
            "text": text,
            "chunks": chunks,
            "llm_output": response.strip() if isinstance(response, str) else str(response)
        }

    except Exception as e:
        return f"❌ 분석 중 오류 발생: {e}"


def deduplicate_lines(text: str) -> str:
    """_summary_

    Args:
        text (str): _description_

    Returns:
        str: _description_
    """
    seen = set()
    result = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and stripped not in seen:
            seen.add(stripped)
            result.append(stripped)
    return "\n".join(result)