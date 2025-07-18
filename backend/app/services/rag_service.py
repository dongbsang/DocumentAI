from typing import Dict
from app.services.ocr_service import extract_text_from_image
from app.services.pdf_service import extract_text_from_pdf
from app.services.text_splitter_service import split_text
from app.services.vector_store_service import create_vectorstore_from_chunks

def deduplicate_lines(text: str) -> str:
    seen = set()
    result = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped and stripped not in seen:
            seen.add(stripped)
            result.append(stripped)
    return "\n".join(result)

def process_uploaded_file(file_bytes: bytes, file_format: str) -> Dict:
    """
    업로드된 파일의 형식에 따라 텍스트를 추출하고, 분할하고, 벡터 저장소를 생성합니다.

    Args:
        file_bytes (bytes): 업로드된 파일의 바이트 데이터
        file_format (str): 'image' 또는 'pdf'

    Returns:
        dict: {
            "text": 전체 텍스트,
            "chunks": 분할된 청크 리스트,
            "retriever": 벡터 검색용 retriever 객체 (추후 RAG에 사용 가능)
        }
    """

    # 1. 텍스트 추출 (OCR 또는 PDF)
    if file_format == "image":
        text = extract_text_from_image(file_bytes)
    elif file_format == "pdf":
        text = extract_text_from_pdf(file_bytes)
        text = deduplicate_lines(text)  # ✅ 중복 줄 제거 추가
    else:
        raise ValueError(f"❌ '{file_format}' 형식은 아직 지원되지 않습니다.")

    if not text.strip():
        text = "[텍스트를 추출하지 못했습니다.]"
        print(text)    
        
    # 2. 텍스트 분할 (chunking)
    chunks = split_text(text)
    print(f"분할된 청크 수: {len(chunks)}")
    
    # 3. 벡터 저장소 생성 (메모리 내)
    vectorstore = create_vectorstore_from_chunks(chunks)

    return {
        "text": text,
        "chunks": chunks,
        "retriever": vectorstore.as_retriever()
    }