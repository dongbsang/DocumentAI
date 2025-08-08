import json
import mimetypes

import fitz

def detect_file_format(file_bytes: bytes, filename: str) -> str:
    """
    파일 바이트와 파일명을 입력받아 JSON 문자열로 반환합니다.
    반환 예시: '{"format": "searchable_pdf", "pages": 3}'

    format 종류:
      - searchable_pdf: 텍스트가 포함된 PDF
      - scanned_pdf: 이미지 형태만 있는 스캔 PDF
      - image: 일반 이미지 파일 (PNG, JPEG 등)
      - unknown_pdf: PDF이지만 분석 실패
      - unknown: 위 분류에 속하지 않는 파일
   
    Args:
        file_bytes (bytes): 업로드된 파일의 바이트 스트림
        filename (str): 원본 파일명 (확장자 검사용)

    Returns:
        str: JSON으로 직렬화된 형식 정보
    """
    # MIME 타입과 확장자
    mime_type, _ = mimetypes.guess_type(filename)
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    format_type = "unknown"
    pages = None

    # PDF 파일 처리
    if mime_type == "application/pdf" or ext == "pdf":
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            # 각 페이지에 텍스트가 있는지 검사
            has_text = any(page.get_text(strip=True) for page in doc)
            format_type = "searchable_pdf" if has_text else "scanned_pdf"
            pages = doc.page_count
        except Exception:
            format_type = "unknown_pdf"

    # 이미지 파일 처리
    elif (mime_type and mime_type.startswith("image/")) or ext in [
        "jpg",
        "jpeg",
        "png",
        "bmp",
        "tiff",
        "gif",
    ]:
        format_type = "image"

    # 결과 JSON 생성
    result = {"format": format_type}
    if pages is not None:
        result["pages"] = pages

    return json.dumps(result)
